# Inemuri (formerly Docks / Study Desk) — rules for Claude

Personal iPhone web app for Apoorva, a 3rd-year anaesthesia resident. Hosted on GitHub Pages from this repo.
Single-page app: `index.html` (+ `sw.js`, `manifest.webmanifest`); content lives in `data/*.json`.
It is built only for her and will never be monetised.

## How to work with her
- She is not a developer. Use plain, step-by-step language. Work in small batches: plan → her OK → build → test → feedback.
- Bigger changes: describe the plan first and wait for her OK. Data-only updates (OT lists, bites, schedules, articles) can go straight in.
- Commit messages are short and plain ("Bites: <title>", "December academic program: ..."). Push to `main`.
- When she says "Bye", she is shutting her PC off and going to work.
- Once her Claude usage passes 85%, don't start expensive updates unless truly necessary.

## Design rules (keep these in every change)
- One owner per kind of data; offline-first; daily features must work offline.
- Honest failure messages; warm, non-blaming wording; quiet defaults; every behaviour can be switched off.
- No mood tracking. The app never moves money.
- Uncluttered home screen. Panel instructions / "How it works" go under Settings, never inside the panels.
- Any long list shows only the first 3–5 items (depending on space) with a "More" option.
- Wide tables (e.g. OT list) keep every column and scroll sideways.
- Progress is shown as a ring with the percentage inside; at 100% it turns into a smiley face.
- Festive tab bar: subtle and clean, unique per festival; translucent, frosty, scattered motifs; nothing placed on the home button.
- **Any colour or theme change:** check that all text is readable in BOTH light and dark mode (`tools/contrast_check.py`) before pushing.

## Privacy
- Never commit patient names, hospital numbers (UHID) or anything identifying in plain text.
- Private data goes only through `tools/lock.mjs` into `data/private/*.enc.json`. Unlocked private files must never be committed.

## Keeping it tidy
- Run `node tools/tidy.mjs` after data updates. Its rules: OT lists and NBA games kept 5 days; painting and fact of the day 15 days; Academics › Articles 7 days.
- Never remove SLCM records or any academic data (bites, topics, schedule).
- NBA and Dota 2 feeds update only when she pulls down to refresh — no scheduled background runs. Dota 2: tier 1 matches and patch updates only.

## Academic content
- Always double-check academic facts against sources before writing them. Never invent an article, DOI or PMID.
- **Bite-size notes** (`data/bites.json`): one note per topic, in her own-words revision style (summary, 3–6 sections, "Points for the exam / viva", pearl, real refs). Asking again updates the same note. A message ending in "BS" means: answer, then save the bite.
- **Articles** (`data/articles.json`): every academic question adds the single most relevant article (BJA Education / major anaesthesia journals preferred, verified on PubMed).
- **Academic schedule** (`data/schedule.json`): whenever sessions are added, every session that has a topic gets a `read` list of 1–3 verified articles (BJA Education preferred). Skip sessions with no topic (Clancon, OSCE, open journal club). See the `rule` field in that file.
