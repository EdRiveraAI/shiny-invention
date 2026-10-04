# Selling Ship Check (seller notes — not shipped to customers)

`build.sh` leaves this file out of the customer zip.

## 1. Before you sell

- [ ] Replace the placeholders: `Your Name` in `.claude-plugin/plugin.json`, the bracketed
      fields in `LICENSE.md`, and `support@example.com` in `README.md`.
- [ ] Have a lawyer review `LICENSE.md` (it's a starting template).
- [ ] Test the skill by hand in **both** tools on 3–5 real repositories (a Node app, a Python
      app, something with Docker). Check that it triggers on "is this ready to ship?" and that
      the reports are accurate. Tune the `description` in `SKILL.md` if it doesn't trigger.
- [ ] Record a 60–90 second demo: messy repo → `/ship-check` → report → "fix the top 3" → new
      score. This video is your main sales asset.
- [ ] Run `./build.sh` to produce `dist/ship-check-1.0.0.zip`.

## 2. The reality of selling skills

A skill is plain text plus a script, so a buyer *can* share the files. Plan for that:

- **Sell convenience, updates, and support**, not secrecy. Most businesses pay rather than
  pirate a $29–$149 tool.
- **Ship updates often** (new checks, new stacks). Recent versions are what buyers come back for.
- **Team/Company tiers** are where the money is: companies prefer to license properly.
- **Later, a hosted tier** (optional): move premium checks or report history to an API that
  needs a key. The skill becomes the free/cheap front end and the API becomes the subscription.
  That's the only way to truly prevent sharing.

## 3. Where to sell

| Option | Notes |
|---|---|
| **Lemon Squeezy** or **Paddle** | Merchant of record: they handle global VAT/sales tax. Digital download + optional license keys. Best default. |
| **Gumroad** | Fastest setup, and creators already sell prompt and skill packs there. |
| **Your own site + Stripe** | Most control; you handle tax yourself (or with Stripe Tax). |
| **Skill directories/marketplaces** | Many are free-only; use them to list a *free lite version* that links to the paid one. |

Set up the product as a digital download (the zip), turn on license keys if the platform
offers them, and include the support email in the receipt.

## 4. Suggested pricing

| Tier | Price | Includes |
|---|---|---|
| Personal | $29–$49 one-time | 1 user, 12 months of updates |
| Team | $149/year | Up to 10 users, CI usage, priority support |
| Company | $499/year | Whole organization, onboarding call |

Start low to get reviews and testimonials, then raise prices for new buyers.

## 5. Free "lite" version (your marketing funnel)

Publish a free `ship-check-lite` on GitHub and in skill directories: the scanner only, without
the guided review checklist, fix mode, or report template. Make its report end with:
"Full audit (auth, injection, performance, deployment, 60+ checks): <your link>".

## 6. Launch plan

1. Landing page: headline ("Know if your app is ready to launch in 5 minutes"), demo video,
   sample report, pricing, FAQ (what's sent where: nothing leaves the machine except what your
   agent already sends to its model).
2. Post the demo on X/Twitter, LinkedIn, r/ClaudeAI, r/ChatGPTCoding, r/SaaS, r/indiehackers,
   Hacker News (Show HN), and Product Hunt.
3. Write SEO posts: "pre-launch security checklist for Next.js", "is my Django app production
   ready", etc. Each one ends with the skill.
4. Give free licenses to 10–20 developers and YouTubers who make AI-coding content in exchange
   for honest reviews.
5. Offer agencies a Company license: they can run it on every client project.

## 7. Shipping updates

1. Bump `VERSION` in `scripts/scan.py`, `metadata.version` in `SKILL.md`, and `version` in
   `plugin.json`; add a `CHANGELOG.md` entry.
2. `./build.sh` and upload the new zip to your store. Most platforms let past buyers download
   the latest file.
3. Email buyers what's new. Every update is a reason to renew.
