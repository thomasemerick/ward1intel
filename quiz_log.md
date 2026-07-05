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
