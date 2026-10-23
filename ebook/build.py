"""Build the ebook PDF.

    python3 build.py            # charts + full book
    AUTHOR="Jane Doe" python3 build.py

Pipeline: render the body (two passes, so the index can print real page numbers),
then render the front matter with a contents page built from the body's anchors,
then the cover, and merge all three into one PDF.
"""
import html
import os
import re
import subprocess
import sys
from pathlib import Path

import weasyprint

import diagrams

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "out"
BUILD = ROOT / "build"
OUT.mkdir(exist_ok=True)
BUILD.mkdir(exist_ok=True)

TITLE = "The AI Business Blueprint"
SUBTITLE = "Eight Models for Building a Company in the Age of AI Agents"
AUTHOR = os.environ.get("AUTHOR", "").strip()
PDF_NAME = "The-AI-Business-Blueprint.pdf"

FONTS = weasyprint.text.fonts.FontConfiguration()
CSS = weasyprint.CSS(filename=str(ROOT / "style.css"), font_config=FONTS)


def expand(src: str) -> str:
    src = re.sub(r"<!--@svg:(\w+)-->", lambda m: diagrams.REGISTRY[m.group(1)](), src)
    src = re.sub(r"<!--@map:(\d)-->", lambda m: diagrams.model_map(int(m.group(1)), size=88), src)
    src = re.sub(r"<!--@partart:([\d,]+)-->",
                 lambda m: diagrams.part_art([int(x) for x in m.group(1).split(",")]), src)
    src = re.sub(r"<!--@chart:(\w+)-->", r'<img src="build/charts/\1.svg" alt="">', src)
    src = src.replace("{{HOLDER}}", html.escape(AUTHOR) if AUTHOR else "the Author")
    src = src.replace("{{AUTHOR}}", html.escape(AUTHOR))
    # drop caps: wrap the first letter so it floats reliably
    src = re.sub(r'(<p class="lead dropcap">)(&[a-z]+;|[^<&\s])', r'\1<span class="dc">\2</span>', src)
    # captions become labels above the table, so they can be kept with it
    src = re.sub(r"(<table[^>]*>)\s*<caption>(.*?)</caption>", r'<div class="tcap">\2</div>\1', src, flags=re.S)

    # keep short tables on one page, together with their label and a heading right before them
    def keep(m):
        t = m.group(0)
        if t.count("<tr") > 10:
            return t
        return f'<div style="break-inside:avoid">{t}</div>'
    src = re.sub(r'(?:<h[23][^>]*>(?:(?!</h[23]>).)*</h[23]>\s*(?:<p>[^<]{0,400}</p>\s*)?)?(?:<div class="tcap">[^<]*</div>\s*)?<table[^>]*>.*?</table>',
                 keep, src, flags=re.S)
    return src


def doc(body: str, title: str = TITLE) -> str:
    author_meta = f'<meta name="author" content="{html.escape(AUTHOR)}">' if AUTHOR else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{author_meta}'
            f'<meta name="description" content="{SUBTITLE}. A plain-English study guide.">'
            '<meta name="keywords" content="AI business models, AI agents, entrepreneurship, study guide, startups">'
            f'</head><body>{body}</body></html>')


def render(body: str):
    return weasyprint.HTML(string=doc(body), base_url=str(ROOT)).render(stylesheets=[CSS], font_config=FONTS)


def anchor_pages(document):
    pages = {}
    for i, page in enumerate(document.pages, start=1):
        for name in page.anchors:
            pages.setdefault(name, i)
    return pages


# ---------------------------------------------------------------- body + index
def body_source():
    files = sorted(p for p in CONTENT.glob("*.html") if not p.name.startswith("00-"))
    src = '<div class="booktitle-marker"></div>' + "\n".join(expand(p.read_text()) for p in files)

    # number figures and give them anchors for the list of figures
    figs = []

    def fig_id(m):
        figs.append(None)
        return f'<figure id="fig-{len(figs)}"' + m.group(1)
    src = re.sub(r"<figure(?![^>]*\bid=)([\s>])", fig_id, src)

    # index terms: <dfn data-ix="Term">text</dfn>
    terms = {}

    def ix(m):
        term = html.unescape(m.group(1))
        n = sum(len(v) for v in terms.values()) + 1
        terms.setdefault(term, []).append(f"ix-{n}")
        return f'<dfn id="ix-{n}" data-ix="{m.group(1)}"'
    src = re.sub(r'<dfn data-ix="([^"]+)"', ix, src)
    return src, terms


def index_html(terms, pages):
    rows = {}
    for term, ids in terms.items():
        nums = sorted({pages[i] for i in ids if i in pages})
        rows[term] = nums
    out = ['<section class="backmatter m0" id="index"><h1>Index</h1><div class="index">']
    letter = None
    for term in sorted(rows, key=lambda t: re.sub(r"[^a-z0-9]", "", t.lower())):
        first = "#" if term[:1].isdigit() else (re.sub(r"[^A-Za-z]", "", term)[:1].upper() or "#")
        if first != letter:
            letter = first
            out.append(f'<div class="ix-letter">{letter}</div>')
        nums = ", ".join(str(n) for n in rows[term])
        out.append(f'<div class="ix">{html.escape(term)}, {nums}</div>')
    out.append("</div></section>")
    return "".join(out)


# ---------------------------------------------------------------- front matter
def toc_html(body_src, pages):
    entries = []
    for m in re.finditer(r'<(section|div) class="(part|chapter[^"]*|backmatter[^"]*)"[^>]*id="([^"]+)"', body_src):
        kind, ident = m.group(2).split()[0], m.group(3)
        seg = body_src[m.end(): m.end() + 4000]
        if kind == "part":
            num = re.search(r'class="part-num">([^<]+)<', seg).group(1)
            title = re.search(r"<h1[^>]*>(.*?)</h1>", seg, re.S).group(1)
            entries.append(("part", num, title, ident))
        elif kind == "chapter":
            num = re.search(r'class="ch-num">([^<]+)<', seg)
            title = re.search(r"<h1[^>]*>(.*?)</h1>", seg, re.S).group(1)
            entries.append(("chapter", num.group(1) if num else "", title, ident))
        else:
            title = re.search(r"<h1[^>]*>(.*?)</h1>", seg, re.S).group(1)
            entries.append(("back", "", title, ident))
    out = ['<section class="front front-chapter m0"><h1 id="contents">Contents</h1><div class="toc">']
    first_back = True
    for kind, num, title, ident in entries:
        title = re.sub(r"<br\s*/?>", " ", title)
        page = pages.get(ident, "")
        if kind == "part":
            out.append(f'<div class="toc-part">{num} &#8212; {title}</div>')
        else:
            if kind == "back" and first_back:
                out.append('<div class="toc-part">Study Tools &amp; Reference</div>')
                first_back = False
            out.append(f'<a class="toc-row" href="#{ident}"><span class="t-num">{num}</span><span class="t-title">{title}</span>'
                       f'<span class="t-dots"></span><span class="t-page">{page}</span></a>')
    out.append("</div></section>")
    return "".join(out)


def lof_html(body_src, pages):
    out = ['<section class="front front-chapter m0"><h1 id="figures">Figures &amp; Charts</h1><div class="toc">']
    for m in re.finditer(r'<figure id="(fig-\d+)".*?<figcaption><b>([^<]+)</b>(.*?)</figcaption>', body_src, re.S):
        ident, num, cap = m.groups()
        cap = re.sub(r"<[^>]+>", "", cap).strip()
        cap = cap.split(". ")[0].rstrip(".")
        out.append(f'<a class="toc-sub" href="#{ident}" style="margin-left:0"><span class="t-title"><b style="font-weight:700;color:#1d2433">{num}</b>&#8194;{cap}</span>'
                   f'<span class="t-dots"></span><span class="t-page">{pages.get(ident, "")}</span></a>')
    out.append("</div></section>")
    return "".join(out)


def cover_html():
    author = f'<div class="cv-author">{html.escape(AUTHOR)}</div>' if AUTHOR else ""
    return (f'<div class="cover">{diagrams.cover_art()}'
            '<div class="cv-kicker">A Plain-English Study Guide</div>'
            '<div class="cv-title">The AI Business<br><i>Blueprint</i></div>'
            f'<div class="cv-sub">{SUBTITLE}</div>{author}'
            '<div class="cv-bar"><span>Worksheets · Review Questions · 90-Day Plans</span><span>Answer Key Included</span></div></div>')


def main():
    if "--no-charts" not in sys.argv:
        subprocess.run([sys.executable, str(ROOT / "charts.py")], check=True)

    body_src, terms = body_source()
    print("pass 1: body")
    first = render(body_src + index_html(terms, {}))
    body_full = body_src + index_html(terms, anchor_pages(first))
    print("pass 2: body with index")
    body = render(body_full)
    pages = anchor_pages(body)
    (BUILD / "body.html").write_text(doc(body_full))

    front_src = expand((CONTENT / "00-front.html").read_text())
    front_src = front_src.replace("<!--@toc-->", toc_html(body_full, pages)).replace("<!--@lof-->", lof_html(body_full, pages))
    front = render(front_src)
    cover = render(cover_html())

    merged = cover.copy(cover.pages + front.pages + body.pages)
    target = OUT / PDF_NAME
    merged.write_pdf(target)
    print(f"wrote {target} ({len(merged.pages)} pages: cover 1, front {len(front.pages)}, body {len(body.pages)})")

    # Cover image for store listings
    cover.write_pdf(BUILD / "cover.pdf")
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(BUILD / "cover.pdf"), str(OUT / "cover")], check=True)


if __name__ == "__main__":
    main()
