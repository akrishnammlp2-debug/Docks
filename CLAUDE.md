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
- Today is a "Now" stack (v5.65): each card gets a score for the time of day, only the top few show (Settings › Cards on Today, default 5), the rest wait under "More today". A card with nothing to say returns '' (batteries only when low, cat food only near reorder). Don't repeat on Today what another card already shows.
- Look (v5.68): each section's page title sits on a soft band of its menu colour (`--sec`); only "do this now" cards (.hero, .cat-due) are tinted, other cards are quiet outlined; glance tiles are chips; doodles only on Today and Off duty; section headings use line icons (SH_ICO) instead of emoji; the cat is Fudge, her cream-peach long-haired Persian, drawn from her photo (NAP_CAT asleep, AWAKE_CAT, PEEK_CAT) in empty states; motion is subtle and off under Reduce Motion.
- Colours (v5.69): status colours have one meaning each (--st-done sage, --st-soon amber, --st-over soft red, --st-info sky); rings take their section colour; dark mode is warm charcoal with night versions of the section colours; amber (--amber) is rare (focus, milestone, just-ticked); night tint after 10 PM and on quiet mornings (switchable); season/festival colour (--season) only on the top-bar edge and the Home greeting.
- Habit plant (v5.70): a day counts at ≥75% of that day's habits (every-N habits count only when done); stages at 0/1/3/6/10/15/21 good days, then a new seed; never wilts. Grows from `settings.plantStart`; `plantSeen` drives the grow animation and toast.
- Animations (v5.70): tick draw, swipe bounce, spring sheets, awake cat, viva 3D flip, count-up numbers, one-time pulse on due items, short festival flicker/snow. Nothing loops forever. `settings.animOn` and iPhone Reduce Motion turn all of it off.
- **Never restyle the tab bar's colours**: it shows the season/festival colours and she likes it that way (22 Nov 2026). The Home banner keeps its size.
- Sheet headers: Cancel (or nothing) on the left, Save / Add / Done on the right. Always.
- **Never jump back to the top** when a sheet grows in place (next step, show answer, reveal more): call `openSheet(html, true)` so the scroll position stays, then bring the newly shown part into view. Only a brand-new sheet starts at the top (23 Nov 2026).
- Music, NBA and Dota 2 live inside Off duty (tabs at the top); the side menu groups are Daily, Academics, Hospital, Life, App.
- To-dos and due reminders can be swiped right to finish (`data-swipe` + `data-swipe-act`). OT rows are not swipeable (the table scrolls sideways).
- **Any colour or theme change:** check that all text is readable in BOTH light and dark mode (`tools/contrast_check.py`) before pushing.

## Privacy
- Never commit patient names, hospital numbers (UHID) or anything identifying in plain text.
- Private data goes only through `tools/lock.mjs` into `data/private/*.enc.json`. Unlocked private files must never be committed.

## Keeping it tidy
- Run `node tools/tidy.mjs` after data updates. Its rules: OT lists and NBA games kept 5 days; painting and fact of the day 15 days; Academics › Articles 7 days.
- Never remove SLCM records or any academic data (bites, topics, schedule).
- NBA and Dota 2 feeds update only when she pulls down to refresh — no scheduled background runs. Dota 2: tier 1 matches and patch updates only.

## Thesis tracker (Academics › Thesis, v5.85)
- Thesis: intrathecal fentanyl vs buprenorphine as adjuvant to 0.5% levobupivacaine heavy, spinal anaesthesia, elderly TURP. One of the most important things for her MD exams.
- She sends a **"urology list"** in chat. It is separate from the OT list: never put it into `data/ot.json`, never confuse the two.
- From the urology list take **only cases with TURP** in the procedure (also "transurethral resection of prostate"). **Not TURBT**, not bladder tumour. **Only pure TURP: never combined procedures like TURP + hemorrhoidectomy** (25 Nov 2026). **Never add KHSB ward cases** (ward column KHSB… / KHS…; 25 Nov 2026). Keep every detail of each case and its date.
- Add them with `node tools/thesis.mjs add <plain.json>` (plain file outside the repo; the tool writes public rows to `data/thesis.json` and locks name · age sex · UHID into `data/private/thesis-<date>.enc.json`). A date already there needs `--replace`.
- Recruited / Not recruited, then (for recruited cases only) Done / Not done in OT, are her own choices in the app (`state.thesisRec` 'y'/'n'; `state.thesisDone` date = done, 'no' = not done, '' = not marked), synced between devices. Never set them for her. Recruited cases are sometimes not done in OT, so both options stay.
- Random sequence: private file `thesis-seq` (70 numbers = rows 2–36 of her random_sequence.xlsx read row by row, ending 10, 19; first 34 used before the tracker, so the tracker starts at 27, 66, 13, 63 …). Keep it private (allocation concealment). The app gives each open case the next free number in date order; a number is used up only when the case is recruited AND done (`state.thesisNo` locks it). Recruited but not done in OT: the case comes off the list and its number passes to the next patient. Not recruited: no number, the case stays on the list greyed out with all its details. Never hand-assign numbers in data files.
- Reasons (`state.thesisWhy`, keys `<id>~r` / `<id>~o`) feed the CONSORT counts card; Export list for Excel writes a CSV on her phone (names stay on device). Today shows a reminder for unmarked thesis cases today/tomorrow (`settings.thesisToday`).
- **Review of literature** (`data/thesis-rol.json`, second tab of Thesis): only articles verified on PubMed; findings paraphrased from abstracts; Vancouver `cite`, `title`, `doi`, `pmid`, `theme`, `use`, optional `drive` link to her Drive "Thesis Work" folder. Add new papers here when she asks; never remove. `guide` holds the writing steps.
- Thesis data is never pruned.

## Academic content
- Always double-check academic facts against sources before writing them. Never invent an article, DOI or PMID.
- **Bite-size notes** (`data/bites.json`): one note per topic, in her own-words revision style (summary, 3–6 sections, "Points for the exam / viva", pearl, real refs). Asking again updates the same note. A message ending in "BS" means: answer, then save the bite.
- **Articles** (`data/articles.json`): every academic question adds the single most relevant article (BJA Education / major anaesthesia journals preferred, verified on PubMed).
- **Case prep** (`data/caseprep.json`): procedure groups matched to OT list procedure names by `match` regexes; short anaesthetic points, linked bite ids, and 1–2 articles verified on PubMed. When a new kind of case shows up on OT lists often, add a group (verify facts and DOIs first).
- **OT calculators** (`pageCalc` in index.html): formulas and limits are sourced on the page. Never change a dose or formula without checking a primary source and re-running the worked examples.
- **ECG & ABG flashcards** (v5.79): one ECG + one ABG a day on Today and in Academics. ECG cases live in `data/ecg.json` (vignette, drawn strip settings in `leads`, findings, management, pearl, `src`); check every fact against the named source before adding, never remove cases. ABGs are generated from `ABG_SC` in index.html and explained by `abgRead()`; after changing either, run `node tools/flash_test.mjs`.
- **Academic schedule** (`data/schedule.json`): whenever sessions are added, every session that has a topic gets a `read` list of 1–3 verified articles (BJA Education preferred). Skip sessions with no topic (Clancon, OSCE, open journal club). See the `rule` field in that file.
