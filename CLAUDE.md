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
- Look (v5.68): each section's page title sits on a soft band of its menu colour (`--sec`); only "do this now" cards (.hero, .cat-due) are tinted, other cards are quiet outlined; glance tiles are chips; doodles only on Today and Off duty; section headings use line icons (SH_ICO) instead of emoji; the sleepy cat (NAP_CAT) appears in empty states; motion is subtle and off under Reduce Motion.
- Colours (v5.69): status colours have one meaning each (--st-done sage, --st-soon amber, --st-over soft red, --st-info sky); rings take their section colour; dark mode is warm charcoal with night versions of the section colours; amber (--amber) is rare (focus, milestone, just-ticked); night tint after 10 PM and on quiet mornings (switchable); season/festival colour (--season) only on the top-bar edge and the Home greeting.
- Habit plant (v5.70): a day counts at ≥75% of that day's habits (every-N habits count only when done); stages at 0/1/3/6/10/15/21 good days, then a new seed; never wilts. Grows from `settings.plantStart`; `plantSeen` drives the grow animation and toast.
- Animations (v5.70): tick draw, swipe bounce, spring sheets, awake cat, viva 3D flip, count-up numbers, one-time pulse on due items, short festival flicker/snow. Nothing loops forever. `settings.animOn` and iPhone Reduce Motion turn all of it off.
- **Never restyle the tab bar's colours**: it shows the season/festival colours and she likes it that way (22 Nov 2026). The Home banner keeps its size.
- Sheet headers: Cancel (or nothing) on the left, Save / Add / Done on the right. Always.
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

## Academic content
- Always double-check academic facts against sources before writing them. Never invent an article, DOI or PMID.
- **Bite-size notes** (`data/bites.json`): one note per topic, in her own-words revision style (summary, 3–6 sections, "Points for the exam / viva", pearl, real refs). Asking again updates the same note. A message ending in "BS" means: answer, then save the bite.
- **Articles** (`data/articles.json`): every academic question adds the single most relevant article (BJA Education / major anaesthesia journals preferred, verified on PubMed).
- **Case prep** (`data/caseprep.json`): procedure groups matched to OT list procedure names by `match` regexes; short anaesthetic points, linked bite ids, and 1–2 articles verified on PubMed. When a new kind of case shows up on OT lists often, add a group (verify facts and DOIs first).
- **OT calculators** (`pageCalc` in index.html): formulas and limits are sourced on the page. Never change a dose or formula without checking a primary source and re-running the worked examples.
- **Academic schedule** (`data/schedule.json`): whenever sessions are added, every session that has a topic gets a `read` list of 1–3 verified articles (BJA Education preferred). Skip sessions with no topic (Clancon, OSCE, open journal club). See the `rule` field in that file.
