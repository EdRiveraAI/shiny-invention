"""Original SVG diagrams for the book. Every function returns an inline <svg> string."""

INK = "#1d2433"
SOFT = "#4a5263"
MUTED = "#8a8f9c"
NAVY = "#16213a"
GOLD = "#c9973b"
M = {1: "#c8553d", 2: "#3a66a8", 3: "#1f8178", 4: "#74589a", 5: "#b98424", 6: "#b5426f", 7: "#4d7a37", 8: "#4a5a70"}

# Positions on "the map" (x: 0 = a person watching a screen, 1 = an agent in a loop;
# y: 1 = sells expertise and outcomes, 0 = builds compounding assets).
POS = {1: (0.17, 0.77), 2: (0.45, 0.65), 3: (0.80, 0.24), 4: (0.61, 0.71),
       5: (0.18, 0.30), 6: (0.13, 0.55), 7: (0.61, 0.38), 8: (0.52, 0.16)}
SHORT = {1: "Services", 2: "Harnesses", 3: "Headless", 4: "Agent-native", 5: "Taste-led", 6: "Ambient agents",
         7: "Data products", 8: "Open-source core"}

FONT = 'font-family="Inter"'


def _svg(w, h, body, width=None):
    width_attr = f' width="{width}"' if width else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{width_attr} '
            f'style="max-width:100%" {FONT}>'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{SOFT}"/></marker>'
            '<marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{GOLD}"/></marker></defs>'
            f'{body}</svg>')


def _box(x, y, w, h, fill, stroke, text, size=12, color=INK, weight=600, r=14, sub=None, sub_size=9.5):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
    cy = y + h / 2 + (size * 0.35 if not sub else -2)
    out += f'<text x="{x + w/2}" y="{cy}" text-anchor="middle" font-size="{size}" font-weight="{weight}" fill="{color}">{text}</text>'
    if sub:
        out += f'<text x="{x + w/2}" y="{cy + sub_size + 6}" text-anchor="middle" font-size="{sub_size}" fill="{color}" fill-opacity=".85">{sub}</text>'
    return out


def _arrow(x1, y1, x2, y2, color=SOFT, label=None, lx=None, ly=None, dash=False, marker="ah", width=1.4):
    d = ' stroke-dasharray="4 4"' if dash else ""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d} marker-end="url(#{marker})"/>'
    if label:
        out += f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="9.5" fill="{SOFT}">{label}</text>'
    return out


# ---------------------------------------------------------------------------- the map
def model_map(highlight=None, size=120, labels=False, axes=False):
    """The 2x2 positioning map. highlight = model number to color; others are gray."""
    pad = 14 if not axes else 70
    S = 400
    W = S + pad * 2 + (150 if labels else 0)
    H = S + pad * 2 + (40 if axes else 0)
    o = pad
    b = f'<rect x="{o}" y="{o}" width="{S}" height="{S}" rx="16" fill="#fff" stroke="#cfc9bd" stroke-width="2"/>'
    b += f'<line x1="{o + S/2}" y1="{o}" x2="{o + S/2}" y2="{o + S}" stroke="#d9d4ca" stroke-width="2"/>'
    b += f'<line x1="{o}" y1="{o + S/2}" x2="{o + S}" y2="{o + S/2}" stroke="#d9d4ca" stroke-width="2"/>'
    for k, (x, y) in POS.items():
        cx, cy = o + x * S, o + (1 - y) * S
        if highlight is None and labels:
            b += f'<circle cx="{cx}" cy="{cy}" r="17" fill="{M[k]}"/>'
            b += f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">{k}</text>'
            b += f'<text x="{cx + 24}" y="{cy + 6}" font-size="15" font-weight="600" fill="{INK}">{SHORT[k]}</text>'
        elif highlight == "all":
            b += f'<circle cx="{cx}" cy="{cy}" r="13" fill="{M[k]}" stroke="#fff" stroke-width="2"/>'
        elif k == highlight:
            b += f'<circle cx="{cx}" cy="{cy}" r="26" fill="{M[k]}" opacity=".18"/>'
            b += f'<circle cx="{cx}" cy="{cy}" r="15" fill="{M[k]}" stroke="#fff" stroke-width="3"/>'
        else:
            b += f'<circle cx="{cx}" cy="{cy}" r="8" fill="#b4b0a8"/>'
    if axes:
        b += f'<text x="{o}" y="{o + S + 34}" font-size="15" fill="{SOFT}" font-weight="600">&#8592; A person watching a screen</text>'
        b += f'<text x="{o + S}" y="{o + S + 34}" text-anchor="end" font-size="15" fill="{SOFT}" font-weight="600">An agent in a loop &#8594;</text>'
        b += (f'<text transform="translate({o - 22},{o + S}) rotate(-90)" font-size="15" fill="{SOFT}" font-weight="600">'
              'Builds compounding assets &#8594;</text>')
        b += (f'<text transform="translate({o - 22},{o}) rotate(-90)" text-anchor="end" font-size="15" fill="{SOFT}" font-weight="600">'
              '&#8592; Sells expertise and outcomes</text>')
    return _svg(W, H, b, width=f"{size}pt")


# ---------------------------------------------------------------------------- heroes
def _people(x, y, n, cols, color, r=4.2, gap=12):
    out = ""
    for i in range(n):
        cx = x + (i % cols) * gap
        cy = y + (i // cols) * gap
        out += f'<circle cx="{cx}" cy="{cy - 3}" r="{r*0.62}" fill="{color}"/><path d="M{cx - r},{cy + r} a{r},{r} 0 0 1 {2*r},0 z" fill="{color}"/>'
    return out


def hero1():
    b = _box(40, 22, 190, 70, "#e3e3e0", "#a9a9a4", "Before", 13, sub="A 20-person firm", sub_size=11)
    b += _box(290, 22, 190, 70, "#e3daf5", "#7c5cc4", "After", 13, sub="2 people + AI systems", sub_size=11)
    b += _people(78, 112, 20, 10, "#9b9b96")
    b += _people(370, 112, 2, 2, "#7c5cc4", r=5, gap=16)
    b += f'<g transform="translate(414,104)"><path d="M6,0 L8,5 L13,6 L8,8 L6,13 L4,8 L-1,6 L4,5 z" fill="{GOLD}"/></g>'
    b += _arrow(135, 140, 225, 182)
    b += _arrow(385, 140, 295, 182)
    b += _box(170, 184, 180, 48, "#5fbf6a", "#3f8f48", "Same client outcome", 12.5, color="#fff")
    b += f'<text x="260" y="254" text-anchor="middle" font-size="10" fill="{MUTED}" font-style="italic">The client sees the result, not the headcount.</text>'
    return _svg(520, 262, b)


def hero2():
    cx, cy = 260, 132
    nodes = [("Tools", 260, 36, "what it can do"), ("Knowledge", 420, 92, "what it knows"),
             ("Workflows", 380, 222, "how the job flows"), ("Memory", 140, 222, "what it remembers"),
             ("Rules", 100, 92, "what it must obey")]
    b = ""
    for _, x, y, _ in nodes:
        b += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#55606f" stroke-width="1.4"/>'
    for name, x, y, sub in nodes:
        b += _box(x - 62, y - 23, 124, 46, "#cfe0f6", M[2], name, 12, sub=sub, sub_size=8.5)
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="64" ry="36" fill="{INK}" stroke="#9aa3b5" stroke-width="2"/>'
    b += f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">AI model</text>'
    b += f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="9" fill="#c9cfdc">the engine</text>'
    b += f'<text x="{cx}" y="268" text-anchor="middle" font-size="10.5" font-weight="700" fill="{INK}">The harness: built around the model for one niche</text>'
    return _svg(520, 278, b)


def hero3():
    b = _box(20, 30, 130, 56, "#6c4fd6", "#4c33a8", "Agent", 13.5, color="#fff")
    b += _arrow(152, 58, 190, 58)
    b += _box(192, 30, 150, 56, "#5b9be6", "#2f6fbd", "CLI · API · MCP", 12.5, color="#fff")
    b += _arrow(344, 58, 382, 58)
    b += _box(384, 30, 120, 56, "#63bf6f", "#3f8f48", "Result", 13.5, color="#fff")
    b += _box(70, 132, 150, 64, "#ededea", "#c9c9c4", "Screen / UI", 12, color="#9a9a96", weight=500)
    b += f'<line x1="74" y1="136" x2="216" y2="192" stroke="#d6614e" stroke-width="4" stroke-linecap="round"/>'
    b += f'<line x1="216" y1="136" x2="74" y2="192" stroke="#d6614e" stroke-width="4" stroke-linecap="round"/>'
    b += _box(282, 128, 186, 72, "#f4c35a", "#c99a2e", "The docs and output", 12, sub="are the interface", sub_size=12)
    b += f'<text x="260" y="232" text-anchor="middle" font-size="10" fill="{MUTED}" font-style="italic">No screen to design. The agent reads your documentation and parses your output.</text>'
    return _svg(520, 244, b)


def hero4():
    b = _box(120, 14, 280, 52, "#ddd2f3", M[4], "Plugin: skills · commands · sub-agents", 12)
    b += _arrow(260, 68, 260, 112, label="your method", lx=310, ly=94)
    b += _box(20, 116, 110, 54, "#e3e3e0", "#a9a9a4", "Customer", 12.5)
    b += _arrow(132, 143, 196, 143, label="asks", lx=164, ly=136)
    b += _box(198, 114, 124, 58, "#6c4fd6", "#4c33a8", "Their agent", 12.5, color="#fff")
    b += _arrow(324, 143, 388, 143, label="works", lx=356, ly=136)
    b += _box(390, 116, 112, 54, "#5b9be6", "#2f6fbd", "Dashboard", 12.5, color="#fff")
    b += f'<path d="M446,172 L446,206 L75,206 L75,178" fill="none" stroke="{SOFT}" stroke-width="1.4" marker-end="url(#ah)"/>'
    b += f'<rect x="196" y="197" width="128" height="18" fill="#fff"/><text x="260" y="210" text-anchor="middle" font-size="9.5" fill="{SOFT}">watch and approve</text>'
    b += f'<text x="260" y="238" text-anchor="middle" font-size="10" fill="{MUTED}" font-style="italic">The customer supervises; the agent does the work your way.</text>'
    return _svg(520, 248, b)


def hero5():
    b = f'<ellipse cx="260" cy="130" rx="236" ry="112" fill="#efefec" stroke="#b9b9b4" stroke-width="1.4"/>'
    b += f'<ellipse cx="260" cy="146" rx="160" ry="80" fill="#cfe2f6" stroke="#5b9be6" stroke-width="1.4"/>'
    b += f'<ellipse cx="260" cy="164" rx="88" ry="40" fill="#4d8fe0" stroke="#2f6fbd" stroke-width="1.6"/>'
    b += f'<text x="260" y="40" text-anchor="middle" font-size="12.5" font-weight="700" fill="{INK}">Everyone</text>'
    b += f'<text x="260" y="94" text-anchor="middle" font-size="12" font-weight="700" fill="{INK}">Your community</text>'
    b += f'<text x="260" y="169" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">1,000 true fans</text>'
    b += f'<text x="260" y="262" text-anchor="middle" font-size="10" fill="{MUTED}" font-style="italic">Build for the center. Let it spread outward.</text>'
    return _svg(520, 270, b)


def _bubble(x, y, w, name, lines, fill, stroke, namecol=INK):
    h = 30 + 15 * len(lines)
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
    out += f'<text x="{x + 14}" y="{y + 19}" font-size="10" font-weight="700" fill="{namecol}">{name}</text>'
    for i, ln in enumerate(lines):
        out += f'<text x="{x + 14}" y="{y + 36 + i*15}" font-size="11" fill="{INK}">{ln}</text>'
    return out, h


def hero6():
    b = f'<rect x="60" y="6" width="400" height="252" rx="18" fill="#fbfbfa" stroke="#d6d3cc" stroke-width="1.3"/>'
    b += f'<text x="84" y="32" font-size="11" font-weight="700" fill="{INK}">Family group chat</text>'
    b += f'<text x="436" y="32" text-anchor="end" font-size="9" fill="{MUTED}">4 members + assistant</text>'
    s, h = _bubble(84, 46, 230, "Mom", ["Who's free for something on Saturday?"], "#fff", "#d6d3cc")
    b += s
    s, h2 = _bubble(84, 46 + h + 10, 196, "Sam", ["Me! Somewhere outdoorsy?"], "#fff", "#d6d3cc")
    b += s
    y3 = 46 + h + 10 + h2 + 12
    s, _ = _bubble(196, y3, 244, "Assistant", ["Booked climbing for 4 at 10 a.m. Saturday", "and added it to everyone's calendar."],
                   "#dccff6", "#a58be0", namecol="#5b3fb5")
    b += s
    return _svg(520, 264, b)


def hero7(big=False):
    cx, cy, rx, ry = 200, 128, 118, 92
    pts = {"top": (cx, cy - ry), "right": (cx + rx, cy), "bottom": (cx, cy + ry), "left": (cx - rx, cy)}
    b = ""
    arcs = [("top", "right"), ("right", "bottom"), ("bottom", "left"), ("left", "top")]
    for a, c in arcs:
        x1, y1 = pts[a]
        x2, y2 = pts[c]
        if a == "top":
            x1 += 64; x2 -= 0; y2 -= 26
        elif a == "right":
            y1 += 26; x2 += 66
        elif a == "bottom":
            x1 -= 64; y2 += 22
        else:
            y1 -= 22; x2 -= 66
        sweep = 1
        b += f'<path d="M{x1},{y1} A{rx},{ry} 0 0 {sweep} {x2},{y2}" fill="none" stroke="{SOFT}" stroke-width="1.5" marker-end="url(#ah)"/>'
    b += _box(pts["top"][0] - 66, pts["top"][1] - 22, 132, 44, "#cdeccc", "#5fae5f", "People use the app", 11)
    b += _box(pts["left"][0] - 66, pts["left"][1] - 22, 132, 44, "#cdeccc", "#5fae5f", "More people join", 11)
    b += _box(pts["bottom"][0] - 66, pts["bottom"][1] - 22, 132, 44, "#cdeccc", "#5fae5f", "Better product", 11)
    b += _box(pts["right"][0] - 66, pts["right"][1] - 24, 132, 48, "#4d8fe0", "#2f6fbd", "Unique data", 12.5, color="#fff")
    b += _arrow(cx + rx + 68, cy, 392, cy, color="#e08a3c")
    b += _box(394, cy - 34, 118, 68, "#f0a656", "#c97a2a", "Buyers &amp; agents", 11.5, color="#fff", sub="pay to query it", sub_size=10.5)
    return _svg(520, 252, b)


def hero8():
    b = f'<path d="M20,100 L500,100" stroke="#5b9be6" stroke-width="2.4"/>'
    b += f'<path d="M260,22 L322,98 L198,98 z" fill="#cfe2f6" stroke="#5b9be6" stroke-width="1.8" stroke-linejoin="round"/>'
    b += f'<text x="260" y="84" text-anchor="middle" font-size="11.5" font-weight="600" fill="{INK}">Free code</text>'
    b += f'<text x="492" y="92" text-anchor="end" font-size="10.5" font-weight="700" fill="{INK}">What people see</text>'
    b += f'<text x="492" y="118" text-anchor="end" font-size="10" fill="{MUTED}">What pays the bills</text>'
    b += f'<rect x="96" y="112" width="328" height="122" rx="40" fill="#4d8fe0" stroke="#2f6fbd" stroke-width="1.8"/>'
    b += f'<text x="260" y="152" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">Where the money is</text>'
    b += f'<text x="260" y="176" text-anchor="middle" font-size="12" fill="#eaf2fd">Hosting · Paid tiers</text>'
    b += f'<text x="260" y="198" text-anchor="middle" font-size="12" fill="#eaf2fd">Support · Community</text>'
    b += f'<text x="260" y="256" text-anchor="middle" font-size="10" fill="{MUTED}" font-style="italic">Give away the tip. Sell everything beneath it.</text>'
    return _svg(520, 264, b)


# ---------------------------------------------------------------------------- supporting diagrams
def three_doors():
    doors = [("CLI", "Command-line interface", "Type one command,\nget a result.", "Like a vending machine"),
             ("API", "Application programming\ninterface", "Send a request in a set\nformat, get data back.", "Like a takeout window"),
             ("MCP", "Model Context Protocol", "A standard plug any\ncompatible agent can use.", "Like a universal port")]
    b = ""
    for i, (t, full, how, ana) in enumerate(doors):
        x = 14 + i * 168
        b += f'<rect x="{x}" y="10" width="156" height="196" rx="12" fill="#fff" stroke="{M[3]}" stroke-width="1.6"/>'
        b += f'<rect x="{x}" y="10" width="156" height="52" rx="12" fill="{M[3]}"/><rect x="{x}" y="40" width="156" height="22" fill="{M[3]}"/>'
        b += f'<text x="{x + 78}" y="44" text-anchor="middle" font-size="20" font-weight="800" fill="#fff">{t}</text>'
        for j, ln in enumerate(full.split("\n")):
            b += f'<text x="{x + 78}" y="{84 + j*14}" text-anchor="middle" font-size="10" font-weight="700" fill="{INK}">{ln}</text>'
        for j, ln in enumerate(how.split("\n")):
            b += f'<text x="{x + 78}" y="{128 + j*15}" text-anchor="middle" font-size="10.5" fill="{SOFT}">{ln}</text>'
        b += f'<text x="{x + 78}" y="188" text-anchor="middle" font-size="9.5" font-style="italic" fill="{M[3]}">{ana}</text>'
    return _svg(520, 214, b)


def license_spectrum():
    b = f'<defs><linearGradient id="lg" x1="0" x2="1"><stop offset="0" stop-color="#cfe2f6"/><stop offset="1" stop-color="{M[8]}"/></linearGradient></defs>'
    b += f'<rect x="20" y="40" width="480" height="16" rx="8" fill="url(#lg)"/>'
    items = [(40, "Permissive", "Anyone may do almost\nanything, including\nresell it as a service."),
             (200, "Strong copyleft", "Run a modified version\nas a web service and\nyou must share changes."),
             (370, "Source-available", "Code is visible; offering\na competing service is\nnot allowed.")]
    for x, t, d in items:
        b += f'<circle cx="{x + 60}" cy="48" r="9" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
        b += f'<text x="{x + 60}" y="84" text-anchor="middle" font-size="11.5" font-weight="700" fill="{INK}">{t}</text>'
        for j, ln in enumerate(d.split("\n")):
            b += f'<text x="{x + 60}" y="{102 + j*14}" text-anchor="middle" font-size="9.5" fill="{SOFT}">{ln}</text>'
    b += f'<text x="20" y="24" font-size="9.5" font-weight="700" fill="{MUTED}">MAXIMUM ADOPTION</text>'
    b += f'<text x="500" y="24" text-anchor="end" font-size="9.5" font-weight="700" fill="{MUTED}">MAXIMUM PROTECTION</text>'
    return _svg(520, 152, b)


def stack_ladder():
    steps = [(1, "Start with a service", "Cash flow and learning, fast"), (4, "Package your method", "Sell it as a plugin"),
             (2, "Productize the system", "Sell it as a vertical harness"), (7, "Capture the data", "Insights no one else has"),
             (3, "Expose it to agents", "A headless API others pay to call")]
    b = ""
    for i, (k, t, s) in enumerate(steps):
        x = 10 + i * 100
        y = 150 - i * 30
        b += f'<rect x="{x}" y="{y}" width="96" height="{190 - y}" rx="6" fill="{M[k]}" opacity=".92"/>'
        b += f'<text x="{x + 48}" y="{y + 26}" text-anchor="middle" font-size="18" font-weight="800" fill="#fff">{k}</text>'
        words = t.split(" ")
        l1 = " ".join(words[:2]); l2 = " ".join(words[2:])
        b += f'<text x="{x + 48}" y="{y + 46}" text-anchor="middle" font-size="9.4" font-weight="700" fill="#fff">{l1}</text>'
        b += f'<text x="{x + 48}" y="{y + 58}" text-anchor="middle" font-size="9.4" font-weight="700" fill="#fff">{l2}</text>'
        sw = s.split(" ")
        half = (len(sw) + 1) // 2
        b += f'<text x="{x + 48}" y="{y + 76}" text-anchor="middle" font-size="8" fill="#fff" fill-opacity=".9">{" ".join(sw[:half])}</text>'
        b += f'<text x="{x + 48}" y="{y + 87}" text-anchor="middle" font-size="8" fill="#fff" fill-opacity=".9">{" ".join(sw[half:])}</text>'
    b += f'<line x1="10" y1="196" x2="506" y2="196" stroke="#cfc9bd" stroke-width="1.2"/>'
    b += f'<text x="10" y="212" font-size="9" fill="{MUTED}">Month 1</text><text x="506" y="212" text-anchor="end" font-size="9" fill="{MUTED}">Year 2+</text>'
    return _svg(520, 218, b)


# ---------------------------------------------------------------------------- cover & part art
def cover_art():
    W, H = 700, 1000
    b = ('<defs><linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#1b2744"/>'
         '<stop offset="1" stop-color="#0e1526"/></linearGradient>'
         '<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/>'
         '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>')
    b += f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    # fine grid
    for i in range(0, W + 1, 25):
        b += f'<line x1="{i}" y1="0" x2="{i}" y2="{H}" stroke="#ffffff" stroke-opacity=".035" stroke-width="1"/>'
    for j in range(0, H + 1, 25):
        b += f'<line x1="0" y1="{j}" x2="{W}" y2="{j}" stroke="#ffffff" stroke-opacity=".035" stroke-width="1"/>'
    ox, oy, S = 145, 112, 410
    b += f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" rx="22" fill="none" stroke="#ffffff" stroke-opacity=".22" stroke-width="1.4"/>'
    b += f'<line x1="{ox + S/2}" y1="{oy - 30}" x2="{ox + S/2}" y2="{oy + S + 30}" stroke="#d9ad5a" stroke-opacity=".55" stroke-width="1.2"/>'
    b += f'<line x1="{ox - 30}" y1="{oy + S/2}" x2="{ox + S + 30}" y2="{oy + S/2}" stroke="#d9ad5a" stroke-opacity=".55" stroke-width="1.2"/>'
    for r in (60, 130, 200):
        b += f'<circle cx="{ox + S/2}" cy="{oy + S/2}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity=".06" stroke-width="1"/>'
    pts = [(ox + POS[k][0] * S, oy + (1 - POS[k][1]) * S) for k in range(1, 9)]
    path = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
    b += f'<path d="{path}" fill="none" stroke="#d9ad5a" stroke-opacity=".7" stroke-width="1.3" stroke-dasharray="2 5" stroke-linecap="round"/>'
    sizes = {1: 15, 2: 13, 3: 12, 4: 14, 5: 12, 6: 13, 7: 15, 8: 12}
    for k, (x, y) in zip(range(1, 9), pts):
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sizes[k] * 3}" fill="{M[k]}" opacity=".16"/>'
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sizes[k] * 1.8}" fill="url(#glow)" opacity=".35"/>'
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sizes[k]}" fill="{M[k]}" stroke="#ffffff" stroke-opacity=".85" stroke-width="2"/>'
        b += f'<text x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">{k}</text>'
    b += f'<text x="{ox}" y="{oy + S + 26}" font-size="10" letter-spacing="2" fill="#ffffff" fill-opacity=".45">PERSON AT A SCREEN</text>'
    b += f'<text x="{ox + S}" y="{oy + S + 26}" text-anchor="end" font-size="10" letter-spacing="2" fill="#ffffff" fill-opacity=".45">AGENT IN A LOOP</text>'
    return (f'<svg class="cover-art" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="7in" height="10in" {FONT}>{b}</svg>')


def part_art(models):
    S = 520
    b = f'<rect x="0" y="0" width="{S}" height="{S}" rx="30" fill="none" stroke="#ffffff" stroke-opacity=".14" stroke-width="2"/>'
    b += f'<line x1="{S/2}" y1="0" x2="{S/2}" y2="{S}" stroke="#ffffff" stroke-opacity=".12" stroke-width="2"/>'
    b += f'<line x1="0" y1="{S/2}" x2="{S}" y2="{S/2}" stroke="#ffffff" stroke-opacity=".12" stroke-width="2"/>'
    for k, (x, y) in POS.items():
        cx, cy = x * S, (1 - y) * S
        if k in models:
            b += f'<circle cx="{cx}" cy="{cy}" r="46" fill="{M[k]}" opacity=".22"/>'
            b += f'<circle cx="{cx}" cy="{cy}" r="22" fill="{M[k]}" stroke="#fff" stroke-width="3"/>'
            b += f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-size="20" font-weight="800" fill="#fff">{k}</text>'
        else:
            b += f'<circle cx="{cx}" cy="{cy}" r="9" fill="#ffffff" opacity=".22"/>'
    return f'<svg class="part-art" xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 {S + 20} {S + 20}" width="4.3in" height="4.3in" {FONT}>{b}</svg>'


REGISTRY = {
    "hero1": hero1, "hero2": hero2, "hero3": hero3, "hero4": hero4, "hero5": hero5, "hero6": hero6, "hero7": hero7,
    "hero8": hero8, "three_doors": three_doors, "license_spectrum": license_spectrum, "stack_ladder": stack_ladder,
    "map_full": lambda: model_map(None, size=330, labels=True, axes=True),
    "map_mini": lambda: model_map("all", size=88),
}
