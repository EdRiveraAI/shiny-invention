// Shared vocabulary and starter records for the product studio.
// Edit the lists here to match how you actually work — the page reads everything from this file.

/** Nine production stages; each counts equally toward a product's progress. */
export const stages = ['Concept & brief', 'Outline & scope', 'Content drafting', 'Spanish translation', 'Design & layout', 'Illustration & assets', 'Editing & proofreading', 'File export', 'Listing & launch'];

export const states = ['Not started', 'In progress', 'In review', 'Blocked', 'Complete'];

export const markets = ['Teachers Pay Teachers', 'Etsy', 'Welas website'];

/** Eight listing-readiness checks tracked per marketplace. */
export const checks = ['Title finalized', 'Description written', 'Keywords / tags added', 'Cover image uploaded', 'Preview pages uploaded', 'Price set', 'Product files uploaded', 'Listing proofread'];

export const qc = [
  'Content is developmentally appropriate for ages 3–5',
  'Spelling and grammar checked in English',
  'Spanish translation reviewed by a fluent speaker',
  'Page numbers and table of contents match',
  'Fonts, colors, and logo follow the Welas style',
  'Low-ink edition prints clearly in grayscale',
  'Images and clip art are licensed for commercial use',
  'PDFs open, are flattened, and have embedded fonts',
  'Editable files open correctly with fonts noted',
  'Terms of use and credits page included',
];

export const launch = [
  'Final files uploaded to every marketplace',
  'Listings published and links recorded',
  'Test download completed as a buyer',
  'Product added to the Welas website',
  'Email announcement scheduled',
  'Social posts scheduled',
  'Related products cross-linked',
  'Follow-up review date set',
];

export const templates: Record<string, string> = {
  brief: `PRODUCT BRIEF

Working title:
Age range: 3–5
Collection / volume:

Who is this for?
(Classroom teachers, homeschool families, bilingual programs…)

What problem does it solve?

Learning goals
1.
2.
3.

What's included
- Pages / activities:
- Languages: English, English–Spanish
- Editions: Full color, Low ink
- Formats: PDF, Editable

Materials teachers will need:

How it connects to the rest of the curriculum:

What "done" looks like:`,
  quality: `QUALITY-CONTROL REVIEW

Reviewed by:
Date:
Files reviewed (edition / version):

What I checked
- Content accuracy and age-appropriateness:
- English text:
- Spanish text:
- Layout and print test (color and low ink):
- Editable files:

Issues found
1.
2.

Fixes made:

Evidence (links, screenshots, print-test notes):

Decision: Ready / Needs another pass`,
  listing: `[One-sentence hook: what this resource helps children do]

WHAT'S INCLUDED
•
•
•

PERFECT FOR
• Preschool and Pre-K classrooms (ages 3–5)
• Bilingual and dual-language programs
• Homeschool families

WHY TEACHERS LOVE IT
• Low-prep and ready to print
• Full-color and low-ink editions
• English and English–Spanish versions

HOW TO USE IT

WHAT YOU'LL NEED

ABOUT WELAS EARLY LEARNING
Created by Noemi Rivera, a bilingual preschool educator with 25 years of classroom experience.

TERMS OF USE
For single-classroom or single-family use. Please purchase additional licenses to share.`,
  launch: `LAUNCH PLAN

Launch date:
Launch price / intro discount:

Before launch
- Final files uploaded:
- Listings previewed on desktop and phone:
- Test purchase / download:

Launch day
- Email announcement:
- Social posts:
- Website update:

After launch
- Check questions and reviews (day 3, day 7):
- Note what to improve in the next edition:

Links
- Marketplace listings:
- Promo graphics:`,
};

const editions = ['English', 'English–Spanish'].flatMap(language => ['Full color', 'Low ink'].flatMap(edition => ['PDF', 'Editable'].map(format => ({language, edition, format}))));

/** A blank product record. Pass a stable `id` for starter records; new products get a random one. */
export function makeProduct(title: string, kind = 'Supporting product', id: string = crypto.randomUUID()) {
  return {
    id,
    title,
    kind,
    owner: 'Noemi Rivera',
    priority: 'Normal',
    due: '',
    price: '',
    thumbnail: '',
    verified: false,
    weekly: '',
    blocker: '',
    notes: '',
    brief: '',
    review: '',
    launchNotes: '',
    stage: stages.map(name => ({name, status: 'Not started'})),
    deliverables: editions.map(e => ({...e, status: 'Not started', url: ''})),
    listings: markets.map(name => ({name, title: '', keywords: '', price: '', url: '', copy: '', checks: checks.map(() => false)})),
    qc: qc.map(() => false),
    launch: launch.map(() => false),
  };
}

/** The thirteen curriculum volumes, shown until a saved copy of each exists. */
export function seed() {
  return Array.from({length: 13}, (_, i) => {
    const n = String(i + 1).padStart(2, '0');
    return makeProduct(`Curriculum Volume ${i + 1}`, 'Curriculum suite', `curriculum-volume-${n}`);
  });
}
