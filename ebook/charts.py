"""Generate the book's charts as SVG (text converted to paths) into build/charts/."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

OUT = Path(__file__).parent / "build" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

for f in font_manager.findSystemFonts():
    if "Inter" in Path(f).name:
        font_manager.fontManager.addfont(f)

INK = "#1d2433"
SOFT = "#4a5263"
MUTED = "#8a8f9c"
GRID = "#e6e2da"
NAVY = "#16213a"
GOLD = "#c9973b"
M = {1: "#c8553d", 2: "#3a66a8", 3: "#1f8178", 4: "#74589a", 5: "#b98424", 6: "#b5426f", 7: "#4d7a37", 8: "#4a5a70"}
NAMES = {
    1: "Software-enabled services", 2: "Vertical agent harnesses", 3: "Headless AI software", 4: "Agent-native systems",
    5: "Taste-led niche products", 6: "Ambient consumer agents", 7: "Proprietary data products", 8: "Open-source-core products",
}

plt.rcParams.update({
    "font.family": "Inter", "font.size": 8.5, "text.color": INK, "axes.labelcolor": SOFT, "axes.edgecolor": "#c9c4ba",
    "xtick.color": SOFT, "ytick.color": SOFT, "axes.titleweight": "bold", "axes.titlesize": 9.5, "axes.titlecolor": INK,
    "axes.titlelocation": "left", "axes.titlepad": 12, "svg.fonttype": "path", "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False, "legend.fontsize": 7.8, "figure.dpi": 100,
})

W = 5.3  # text width in inches


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.04, transparent=True)
    plt.close(fig)


def money(v):
    return f"${v/1000:.0f}K" if v >= 1000 else f"${v:.0f}"


# 1. Firm economics -----------------------------------------------------------
def ch1_economics():
    fig, ax = plt.subplots(figsize=(W, 2.9))
    labels = ["Traditional firm\n(4 staff)", "AI-native firm\n(1 owner + AI)"]
    staff = np.array([22400, 6500])
    tools = np.array([600, 1200])
    overhead = np.array([4200, 1800])
    profit = np.array([4800, 22500])
    x = np.arange(2)
    w = 0.46
    parts = [(staff, "Salaries & labor", "#b9bfcc"), (tools, "Software & AI tools", "#8d97ab"),
             (overhead, "Office & overhead", "#5f6b82"), (profit, "Owner profit", M[1])]
    bottom = np.zeros(2)
    for vals, lab, col in parts:
        ax.bar(x, vals, w, bottom=bottom, color=col, label=lab, edgecolor="white", linewidth=0.8)
        bottom += vals
    for i, p in enumerate(profit):
        ax.text(x[i] + w / 2 + 0.04, bottom[i] - p / 2, f"Profit {money(p)}\n{p/32000:.0%} margin",
                va="center", ha="left", fontsize=8, fontweight="bold", color=M[1])
    ax.set_xticks(x, labels)
    ax.set_xlim(-0.5, 1.95)
    ax.set_ylim(0, 36000)
    ax.yaxis.set_major_formatter(lambda v, _: money(v))
    ax.set_ylabel("Monthly amount")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.45, -0.17), fontsize=7.2, handlelength=1.1)
    ax.set_title("Same $32,000 in monthly revenue, very different businesses")
    save(fig, "ch1_economics")


def ch1_capacity():
    fig, ax = plt.subplots(figsize=(W, 1.55))
    vals = [12, 45]
    labs = ["Traditional bookkeeper", "Bookkeeper + AI system"]
    ax.barh(labs, vals, color=["#b9bfcc", M[1]], height=0.55)
    for i, v in enumerate(vals):
        ax.text(v + 0.8, i, f"{v} clients", va="center", fontsize=8.2, fontweight="bold", color=[SOFT, M[1]][i])
    ax.set_xlim(0, 55)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Small-business clients one person can serve each month (illustrative)")
    ax.set_title("Capacity per person")
    save(fig, "ch1_capacity")


# 2. Wrapper vs harness ---------------------------------------------------------
def ch2_moat():
    fig, ax = plt.subplots(figsize=(W, 2.6))
    t = np.arange(6)
    labels = ["Launch", "+6 mo", "+12 mo", "+18 mo", "+24 mo", "+30 mo"]
    wrapper = [60, 52, 38, 26, 17, 10]
    harness = [45, 55, 66, 76, 85, 92]
    ax.plot(t, harness, color=M[2], lw=2.4, marker="o", ms=4, label="True harness (tools, knowledge, rules, memory, workflows)")
    ax.plot(t, wrapper, color="#b8433a", lw=2.4, marker="o", ms=4, ls="--", label="Thin wrapper (a prompt and a nice screen)")
    for xi in (1, 2.5, 4):
        ax.axvline(xi, color=GOLD, lw=0.8, ls=":")
    ax.text(1.05, 98, "new model\nreleased", fontsize=6.6, color=GOLD, va="top")
    ax.set_xticks(t, labels)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Value to customer (index)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), fontsize=7.2)
    ax.set_title("Better models kill wrappers and strengthen harnesses")
    save(fig, "ch2_moat")


def ch2_timesaved():
    fig, ax = plt.subplots(figsize=(W, 1.85))
    cats = ["Sorting photos", "Writing narratives", "Formatting report", "Review & delivery"]
    before = [35, 95, 30, 20]
    after = [3, 10, 2, 15]
    cols = ["#d3d7df", "#9aa3b5", "#6b7690", M[2]]
    for row, data in enumerate([before, after]):
        left = 0
        for c, v, col in zip(cats, data, cols):
            ax.barh(row, v, left=left, color=col, edgecolor="white", height=0.56, label=c if row == 0 else None)
            left += v
        ax.text(left + 3, row, f"{left} min", va="center", fontsize=8.4, fontweight="bold", color=[SOFT, M[2]][row])
    ax.set_yticks([0, 1], ["Without harness", "With harness"])
    ax.invert_yaxis()
    ax.set_xlim(0, 210)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Minutes per inspection report (illustrative)")
    ax.legend(loc="upper center", ncol=4, bbox_to_anchor=(0.45, -0.38), fontsize=7, handlelength=1)
    ax.set_title("Where the time goes")
    save(fig, "ch2_timesaved")


# 3. Agent volume ----------------------------------------------------------------
def ch3_volume():
    fig, ax = plt.subplots(figsize=(W, 1.75))
    labs = ["A person searching", "One AI agent at work"]
    vals = [20, 2000]
    ax.barh(labs, vals, color=["#b9bfcc", M[3]], height=0.55)
    ax.set_xscale("log")
    ax.set_xlim(1, 20000)
    for i, v in enumerate(vals):
        ax.text(v * 1.25, i, f"{v:,} tool calls / day", va="center", fontsize=8.2, fontweight="bold", color=[SOFT, M[3]][i])
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Requests per day (log scale, illustrative)")
    ax.set_title("Agents are software's heaviest users")
    save(fig, "ch3_volume")


def ch3_bill():
    fig, ax = plt.subplots(figsize=(W, 2.3))
    calls = np.linspace(0, 200000, 400)
    free = 1000
    bill = np.maximum(calls - free, 0) / 1000 * 1.0
    capped = np.minimum(bill, 120)
    ax.plot(calls / 1000, bill, color=M[3], lw=2.2, label="Pay-as-you-go: $1 per 1,000 calls after 1,000 free")
    ax.plot(calls / 1000, capped, color=GOLD, lw=1.8, ls="--", label="Same plan with a $120 monthly spending cap")
    ax.set_xlabel("Calls per month (thousands)")
    ax.set_ylabel("Customer's monthly bill")
    ax.yaxis.set_major_formatter(lambda v, _: f"${v:.0f}")
    ax.set_ylim(0, 210)
    ax.legend(loc="upper left", fontsize=7.2)
    ax.set_title("Usage pricing grows with the customer; caps keep it predictable")
    save(fig, "ch3_bill")


# 4. Leverage --------------------------------------------------------------------
def ch4_leverage():
    fig, ax = plt.subplots(figsize=(W, 2.35))
    labs = ["One-to-one coaching\n13 clients x $500/mo", "Group program\n60 members x $150/mo", "Plugin membership\n1,000 members x $49/mo"]
    vals = [6500, 9000, 49000]
    cols = ["#b9bfcc", "#8d97ab", M[4]]
    ax.bar(range(3), vals, color=cols, width=0.56)
    for i, v in enumerate(vals):
        ax.text(i, v + 1200, f"${v:,}", ha="center", fontsize=8.6, fontweight="bold", color=[SOFT, SOFT, M[4]][i])
    ax.set_xticks(range(3), labs, fontsize=7.4)
    ax.set_ylim(0, 58000)
    ax.yaxis.set_major_formatter(lambda v, _: money(v))
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Monthly revenue")
    ax.set_title("Monthly revenue from the same 20 hours a week (illustrative)")
    save(fig, "ch4_leverage")


# 5. True fans -------------------------------------------------------------------
def ch5_fans():
    fig, ax = plt.subplots(figsize=(W, 2.4))
    fans = np.arange(0, 3001, 50)
    for price, col, lab in [(39, "#d8c49c", "$39 / year"), (60, "#c9a45e", "$60 / year"), (100, M[5], "$100 / year")]:
        ax.plot(fans, fans * price, color=col, lw=2.2, label=lab)
    ax.axvline(1000, color=NAVY, lw=0.9, ls=":")
    ax.scatter([1000], [100000], color=M[5], zorder=5, s=26)
    ax.annotate("1,000 true fans x $100\n= $100,000 a year", (1000, 100000), xytext=(1250, 168000), fontsize=7.6,
                fontweight="bold", color=M[5], arrowprops=dict(arrowstyle="-", color=M[5], lw=0.8))
    ax.yaxis.set_major_formatter(lambda v, _: money(v))
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:,.0f}")
    ax.set_xlabel("Paying fans")
    ax.set_ylabel("Annual revenue")
    ax.set_xlim(0, 3000)
    ax.set_ylim(0, 310000)
    ax.legend(loc="upper left", title="Average spend per fan", title_fontsize=7.4)
    ax.set_title("You don't need millions of customers")
    save(fig, "ch5_fans")


def donut(name, labels, vals, colors, title, center):
    fig, ax = plt.subplots(figsize=(W, 2.35))
    ax.axis("equal")
    ax.grid(False)
    wedges, _ = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.36, edgecolor="white", linewidth=1.5), radius=1.0, center=(-0.9, 0))
    ax.text(-0.9, 0.06, center[0], ha="center", va="center", fontsize=11, fontweight="bold", color=INK)
    ax.text(-0.9, -0.2, center[1], ha="center", va="center", fontsize=6.8, color=MUTED)
    for i, (lab, v, c) in enumerate(zip(labels, vals, colors)):
        y = 0.72 - i * 0.36
        ax.add_patch(plt.Rectangle((0.55, y - 0.07), 0.14, 0.14, color=c, transform=ax.transData))
        ax.text(0.8, y, f"{v}%", va="center", fontsize=9, fontweight="bold", color=INK)
        ax.text(1.18, y, lab, va="center", fontsize=8, color=SOFT)
    ax.set_xlim(-2.0, 3.4)
    ax.set_ylim(-1.1, 1.1)
    ax.set_title(title)
    save(fig, name)


def ch5_mix():
    donut("ch5_mix", ["Pro subscriptions", "Affiliate commissions", "Sponsors", "Merch & purchases", "Events & meetups"],
          [58, 16, 12, 9, 5], [M[5], "#d5b06a", "#8a6a2c", "#e7d3a8", "#5b4a2a"],
          "A healthy niche-product revenue mix (illustrative)", ("5", "income streams"))


# 6. Retention -------------------------------------------------------------------
def ch6_retention():
    fig, ax = plt.subplots(figsize=(W, 2.5))
    wk = np.arange(13)
    toy = [100, 58, 36, 24, 16, 12, 10, 8, 7, 6, 5, 5, 4]
    ritual = [100, 84, 76, 71, 68, 66, 65, 64, 63, 62, 62, 61, 61]
    ax.plot(wk, ritual, color=M[6], lw=2.4, label="Tied to a weekly ritual (team schedule, family plans)")
    ax.plot(wk, toy, color=MUTED, lw=2.2, ls="--", label="Novelty assistant (fun to try)")
    ax.axhline(40, color=GOLD, lw=0.9, ls=":")
    ax.text(12.1, 42, "40% target", fontsize=7, color=GOLD, ha="right")
    ax.axvline(4, color=NAVY, lw=0.7, ls=":")
    ax.text(4.15, 96, "week 4\ncheckpoint", fontsize=6.8, color=NAVY, va="top")
    ax.set_xticks(wk)
    ax.set_xlabel("Weeks after a group adds the assistant")
    ax.set_ylabel("Groups still active (%)")
    ax.set_ylim(0, 105)
    ax.legend(loc="upper center", fontsize=7.2, bbox_to_anchor=(0.5, -0.2))
    ax.set_title("The novelty trap, drawn as a retention curve (illustrative)")
    save(fig, "ch6_retention")


# 7. Data value -------------------------------------------------------------------
def ch7_confidence():
    fig, ax = plt.subplots(figsize=(W, 2.35))
    n = np.arange(1, 201)
    err = 2400 / np.sqrt(n)
    ax.fill_between(n, -err, err, color=M[7], alpha=0.16, lw=0)
    ax.plot(n, err, color=M[7], lw=1.8)
    ax.plot(n, -err, color=M[7], lw=1.8)
    ax.axhline(0, color=INK, lw=0.6)
    ax.axvspan(0, 8, color="#b8433a", alpha=0.08, lw=0)
    ax.text(10, 1900, "Too few data points to publish\n(privacy and accuracy risk)", fontsize=7, color="#b8433a")
    ax.text(120, 520, "Each new contribution\nmakes the answer sharper", fontsize=7, color=M[7])
    ax.yaxis.set_major_formatter(lambda v, _: f"{'+' if v > 0 else ''}${v:,.0f}")
    ax.set_xlabel("Verified contributions in one zip code and job type")
    ax.set_ylabel("Uncertainty of the average price")
    ax.set_xlim(0, 200)
    ax.set_title("Why more data is worth more: the local-average example")
    save(fig, "ch7_confidence")


# 8. Open source -------------------------------------------------------------------
def ch8_mix():
    donut("ch8_mix", ["Hosted cloud subscriptions", "Paid business features", "Support contracts", "Sponsorships & services"],
          [70, 17, 9, 4], [M[8], "#7f8da2", "#b2bccb", GOLD],
          "Where an open-source-core company's revenue typically comes from (illustrative)", ("Below", "the waterline"))


def ch8_funnel():
    fig, ax = plt.subplots(figsize=(W, 2.25))
    stages = ["Visitors to the code repository", "Downloads & self-hosted installs", "Hosted-cloud sign-ups", "Paying customers"]
    vals = [100000, 8000, 1500, 180]
    cols = ["#d5dae2", "#aab4c3", "#7f8da2", M[8]]
    for i, (s, v, c) in enumerate(zip(stages, vals, cols)):
        width = np.log10(v) / np.log10(100000)
        ax.barh(i, width, left=(1 - width) / 2, color=c, height=0.78)
        ax.text(0.5, i, f"{v:,}", ha="center", va="center", fontsize=8.6, fontweight="bold", color="white" if i >= 2 else INK)
        ax.text(1.04, i, s, va="center", fontsize=7.8, color=SOFT)
    ax.set_xlim(0, 1.85)
    ax.invert_yaxis()
    ax.axis("off")
    ax.set_title("A typical open-source funnel over the first year (illustrative)")
    save(fig, "ch8_funnel")


# 9. Choosing ---------------------------------------------------------------------
LIFT = {1: 1.6, 2: 3.0, 3: 4.2, 4: 1.7, 5: 2.0, 6: 3.1, 7: 3.0, 8: 4.1}
MONTHS = {1: 1.5, 2: 4.5, 3: 4.5, 4: 2.0, 5: 6.0, 6: 6.0, 7: 12.0, 8: 9.0}
BUDGET = {1: (100, 300), 2: (100, 500), 3: (25, 350), 4: (50, 450), 5: (50, 150), 6: (50, 400), 7: (50, 1000), 8: (50, 350)}


def ch9_bubble():
    fig, ax = plt.subplots(figsize=(W, 3.3))
    pos = {1: (1.5, 1.4), 2: (3.0, 4.4), 3: (4.25, 4.6), 4: (1.95, 2.6), 5: (2.15, 6.0), 6: (3.15, 6.3), 7: (3.0, 12.0), 8: (4.1, 9.0)}
    for k in range(1, 9):
        s = BUDGET[k][1] * 1.3 + 160
        x, y = pos[k]
        ax.scatter(x, y, s=s, color=M[k], alpha=0.9, edgecolor="white", linewidth=1.2, zorder=3)
        ax.text(x, y, str(k), ha="center", va="center", fontsize=8.2, fontweight="bold", color="white", zorder=4)
    for i, k in enumerate(range(1, 9)):
        ax.text(5.25, 13.2 - i * 1.0, f"{k}", fontsize=7.6, fontweight="bold", color=M[k], va="center")
        ax.text(5.45, 13.2 - i * 1.0, NAMES[k], fontsize=7.2, color=INK, va="center")
    ax.set_xlim(0.8, 5.0)
    ax.set_ylim(0, 14)
    ax.set_xticks([1, 2, 3, 4, 5], ["Low", "Low-med", "Medium", "Med-high", "High"])
    ax.set_xlabel("Technical lift")
    ax.set_ylabel("Typical months to first revenue")
    ax.text(5.25, 4.6, "Bubble size =\ntop of monthly\nstarter budget", fontsize=6.6, color=MUTED, va="top")
    ax.set_title("Effort vs. speed: the eight models compared (estimates)")
    save(fig, "ch9_bubble")


def ch9_budget():
    fig, ax = plt.subplots(figsize=(W, 2.75))
    for i, k in enumerate(range(1, 9)):
        lo, hi = BUDGET[k]
        ax.plot([lo, hi], [i, i], color=M[k], lw=7, solid_capstyle="round")
        ax.text(hi + 22, i, f"${lo}-${hi:,}", va="center", fontsize=7.4, color=SOFT)
    ax.set_yticks(range(8), [f"{k}. {NAMES[k]}" for k in range(1, 9)], fontsize=7.4)
    ax.invert_yaxis()
    ax.set_xlim(0, 1300)
    ax.xaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Estimated monthly starter budget (before revenue)")
    ax.set_title("What it costs to start each model")
    save(fig, "ch9_budget")


def ch10_gantt():
    fig, ax = plt.subplots(figsize=(W, 2.5))
    tasks = [("Inventory & choose your model", 0, 1, NAVY), ("Validate with 10 conversations", 1, 2, "#3a66a8"),
             ("Build the smallest version", 2, 4, "#1f8178"), ("First 3-5 users or clients", 4, 4, "#b98424"),
             ("Improve, price & charge", 8, 4, "#c8553d"), ("Weekly review (every week)", 0, 13, "#c9c4ba")]
    for i, (t, s, d, c) in enumerate(tasks):
        ax.barh(i, d, left=s, color=c, height=0.55, alpha=0.95 if i < 5 else 0.6)
        ax.text(-0.25, i, t, ha="right", va="center", fontsize=7.6, color=INK)
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_xlim(0, 13)
    ax.set_xticks(range(0, 14), [f"W{w}" if w else "" for w in range(0, 14)], fontsize=6.8)
    ax.grid(axis="y", visible=False)
    for m, lab in [(4.3, "Day 30"), (8.6, "Day 60"), (12.9, "Day 90")]:
        ax.axvline(m, color=GOLD, lw=0.8, ls=":")
        ax.text(m, -0.85, lab, fontsize=6.8, color=GOLD, ha="center")
    ax.spines["left"].set_visible(False)
    ax.set_title("Your first 90 days at a glance", pad=16)
    save(fig, "ch10_gantt")


if __name__ == "__main__":
    for fn in [ch1_economics, ch1_capacity, ch2_moat, ch2_timesaved, ch3_volume, ch3_bill, ch4_leverage, ch5_fans, ch5_mix,
               ch6_retention, ch7_confidence, ch8_mix, ch8_funnel, ch9_bubble, ch9_budget, ch10_gantt]:
        fn()
    print("charts:", len(list(OUT.glob("*.svg"))))
