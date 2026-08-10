# Python Quiz Log

## Format preference (per Thomas, set 2026-07-05)
For each topic/question, run three passes in this order:
1. Multiple choice (warm-up / ease in)
2. Open-ended — how it applies (real recall test)
3. Multiple choice again (confirm it stuck)
Apply this structure to daily quizzes and retests going forward.

Repo paths:
- Ward 1 Intel: /Users/blaw/ward1intel (connected folder)
- Viztas: /Users/blaw/nflappsbyte (connected 2026-07-05; NFL analytics — app.py, pages/1_NFL_Draft.py, pages/2_OL_Continuity.py, historical_ol.py, olincumbents.py, pfr_scraper.py, roster_check.py)

## 2026-07-05
Score: 1/5
Repo quizzed: Ward 1 Intel (score_precincts.py, Home.py)
Missed:
- wavg() mechanics: why fillna(0) on weight col (NaN propagation) vs. the sum()==0 zero-division guard
- list comprehension for column reordering (cols = [...] + [c for c in df.columns if c not in [...]])
- dict comprehension syntax ({k: v*2 for k,v in d.items() if v>1})
- groupby .agg() vs .apply(): agg can't see multiple columns at once, needed for weighted averages
- pytest structure: test_*.py / test_* functions, no class needed, pytest.approx for floats
Retest on: 2026-07-07 (2-day), then 2026-07-12 (7-day), then 2026-07-19 (14-day)
Covered: pandas groupby+weighted aggregation, list/dict comprehensions, column reordering pattern, pytest basics

Same-day MC retest (2026-07-05): 5/5 on all 5 missed topics. Recognition only, not recall — keep original 2026-07-07 retest in open-ended form to confirm real retention.

## 2026-07-07
Score: 1/5
Repos quizzed: Viztas (pfr_scraper.py, olincumbents.py) + Ward 1 Intel retest topics — first day both repos used in one session
Missed:
- set vs list for dedup: O(n) list membership check (`if x not in links`) vs O(1) set lookup, and the "set for lookup + list for order" pairing pattern
- groupby().apply() lambda scope: what `x` represents inside `.apply(lambda x: ...)` on a single-column groupby (said full DataFrame, it's actually the grouped Series/sub-frame)
- dict comprehension syntax: MISSED A THIRD TIME (also missed 2026-07-05 and before). Flagging — swap tomorrow's quiz slot for a focused 10-min drill instead of another retest.
- requests error handling: try/except + raise_for_status() + timeout pattern for handling failed HTTP requests in a scrape loop; gave the default behavior back instead of the fix
Passed retest: groupby .agg() vs .apply() — correctly explained why agg can't do weighted avg across two columns at once. Retention confirmed, continue original schedule: next retest 2026-07-12 (7-day mark)
Retest on: 2026-07-09 (2-day) — set vs list dedup, apply() lambda scope, requests error handling
Covered: web scraping dedup patterns (BeautifulSoup link collection), groupby single-column apply mechanics, requests exception handling, pfr_scraper.py, olincumbents.py

Outstanding drill: dict comprehension syntax missed 3x (2026-07-05, and before) — do a focused 10-min drill on this instead of folding it into a normal quiz slot.

## 2026-07-09
Score: 0.5/5
Repo quizzed: none — folders were not connected in this session yet, so this ran as a fundamentals-only quiz (no code invented, per hard rule). Scheduled 2-day retest (set vs list dedup, apply() lambda scope, requests error handling) was NOT covered today — carry forward.
Missed:
- list comprehension vs generator expression: memory (build-all vs lazy one-at-a-time) and when to use each
- try/except/else/finally: said else runs "if preceding conditions not met" — actually else runs only when the try block raises NO exception; that's distinct from except
- pandas groupby.agg() vs groupby.transform(): said "one column vs two columns / weighting" — actually agg collapses to one row per group, transform broadcasts the group stat back to original row shape/index
- pytest naming convention: said "runTest" — actually test_*.py files, test_* functions
Partial: requests non-200 handling — said "exceptions" but no specifics (missing raise_for_status() or status_code check)
Retest on: 2026-07-11 (2-day) — list comp vs generator, groupby agg vs transform, pytest naming; 2026-07-16 (7-day)
Covered: none from repos this session

Folders connected mid-conversation same day (2026-07-09): Viztas confirmed as /Users/blaw/nflappsbyte, Ward 1 Intel confirmed as /Users/blaw/ward1intel. Both available going forward — resume normal 2-codebase-question format tomorrow, rotate repo, and fold in the carried-forward 2026-07-07 retest topics plus the dict comprehension drill.

## 2026-07-16 (ad hoc, not the daily quiz)
Score: 10/10 (MC only, 10 questions, single-topic — deviates from standard 5-question mixed format and 3-pass MC/open-ended/MC structure; Thomas explicitly requested this scope)
Repo quizzed: Ward 1 Intel (map_ward1.py — full file, walked through 100 lines at a time first)
Missed: none
Covered: geopandas read_file/GeoDataFrame, filter+.copy() to avoid SettingWithCopyWarning, merge on Precinct, branca LinearColormap vmin/vmax interpolation without explicit index, late-binding closure bug + default-arg fix (c=color), folium DivIcon vs default marker, geometry.centroid for label placement, m.save() producing static HTML consumed by Home.py's components.html()

Note: this was recognition-level (MC only). Per the 3-pass preference, consider an open-ended follow-up on the closure bug and the .copy()/SettingWithCopyWarning topic to confirm real recall, not just recognition.

Outstanding — NOT covered today, still due: 7-day retest from 2026-07-09 (list comp vs generator, groupby agg vs transform, pytest naming). Carry forward to next daily quiz.
