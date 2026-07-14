# Daily update task

Project folder: `/Users/ericsalisbury/Desktop/athlete-injury-feed/`

**"High-profile" definition:** any athlete competing at the professional level (major pro leagues, top international/national teams) or NCAA Division I — this includes bench players, role players, and rotation players, not just headline stars/All-Stars. It excludes amateur, recreational, non-D1 college, and obscure lower-tier/developmental competitions (e.g. G League, low-level minor league baseball) unless the athlete is a well-known name.

**Daily target: ~60 new injury records per run — treat this as an aspirational ceiling, not a quota.** Real high-profile injury news volume fluctuates with the sports calendar and has been running well under this (12-15/day in mid-July 2026, with several major leagues in their off-season). To maximize genuine volume, go a level deeper than sport-level searches — per-team or per-tournament searches (individual NFL/MLB team injury reports, individual EPL/La Liga clubs, individual golf/tennis tournaments in progress, individual rugby/combat-sports events, etc.). Verify recency (roughly last 24-48 hours; don't recycle stale season-recap injuries from leagues currently in their off-season) and specificity for every record exactly as before. If a thorough, deep sweep across all listed sports still turns up fewer than 60 genuinely new high-profile injuries — which is expected most days — report the true (lower) count rather than padding it. Never fabricate a record, never include vague/unverifiable ones, and never widen the "high-profile" or recency bar just to hit the number without being explicitly asked to.

On each run:

1. Read `injuries.json` to see which injuries are already tracked (check the `guid` field to avoid duplicates).
2. Search the web for new high-profile athlete injury news from roughly the last 24-48 hours, across major sports: NFL, NBA, WNBA, MLB, NHL, top soccer leagues (Premier League, La Liga, MLS, NWSL, Champions League, national teams), tennis (ATP/WTA), golf (PGA/LPGA), F1, boxing/UFC, cricket, Olympic sports, and NCAA Division I college sports (football, men's and women's basketball, baseball, softball, volleyball, gymnastics, soccer, wrestling, track & field). Search each sport/league individually, and within sports/leagues that are actually in-season, drill down further to individual teams or tournaments (e.g. per-team MLB/NFL injury reports, per-club EPL/La Liga searches, the specific tournaments currently being played in golf/tennis) — this depth is what surfaces enough volume to reach the ~40/day target. Actively search for women's sports and NCAA D1 college athletes each run, not just the major men's pro leagues — those tend to dominate search results by default. Skip leagues that are currently in their off-season for fresh injury news (their search results will mostly be stale season-recap injuries from months earlier) — check the schedule/date context before including anything from a soccer league whose season already ended, for example.
3. For each genuinely new, high-profile injury found, add a record to `injuries.json` with these fields (all required):
   - `guid`: unique slug, e.g. `sport-lastname-YYYY-MM-DD`
   - `athlete`: full name
   - `org`: team/club and league (and national team if relevant)
   - `sport`
   - `location`: the team's home city/region (e.g. "Minneapolis, Minnesota"), or the country for a national team, or `"N/A — individual tour athlete, no fixed team location"` for tour-based sports (tennis, golf, UFC), or `"N/A — individual fighter, not tied to a team location"` for UFC specifically
   - `league`: the specific league/competition (e.g. "MLB", "Premier League", "NBA Summer League", "International Cricket", "UCI WorldTeam / Tour de France") — more granular than `sport`
   - `injury_context`: the specific medical nature of the injury (e.g. "ACL reconstruction", "grade 2 hamstring strain") — be as specific as the source allows
   - `duration`: expected time out / recovery timeline
   - `financial_impact`: the **prorated sunk cost of salary** paid to the athlete while injured (salary the team/employer pays but gets no on-field value for), computed as `(annual salary / 365) × estimated days out`. Method:
     1. Estimate days out from the `duration` text: "day-to-day"/vague → 3 days; "X-day IL" → X days; "X week(s)" (or range midpoint) → ×7; "X month(s)" (or range midpoint) → ×30; "season-ending"/"remainder of season" → estimate remaining days to that sport's typical season end from `date_reported`; truly undetermined → 5 days (state this assumption in the string).
     2. If the athlete is in a fixed-salary team sport (MLB, NBA, WNBA, NFL, NHL, MLS, NWSL, European club soccer when club-related): search for their current salary/AAV from a public source (Spotrac, Capology, Cot's Contracts, HoopsHype) and compute the prorated figure. Format: `"$XXX,XXX prorated sunk cost (annual salary ~$X.XM per [source] ÷ 365 × N days out)"` — include any notable assumption (e.g. days-out estimate basis) in brackets at the end.
     3. If the athlete is in an individual/prize-money sport (tennis, golf, boxing, UFC/MMA, track & field, swimming, gymnastics, cycling) or this is a national-team-only context with no club salary: `"Not applicable — earns prize money/appearance fees, no fixed salary to prorate"` (or `"Not applicable — no fixed salary information available for this national-team context"` for the national-team case).
     4. NCAA athletes: `"Not applicable — NCAA athlete, no fixed salary"` unless the source discloses a specific NIL figure.
     5. If it's a fixed-salary team-sport athlete but no salary can be found after a reasonable search: `"Not disclosed in available reporting — salary not found"`.
     Never fabricate a salary figure — only use real figures found via search, cited by source name.
   - `team_impact`: effect on the team's/tour's competitive outlook
   - `date_reported`: `YYYY-MM-DD`
   - `source_title` / `source_url`: the article used
4. Do not fabricate figures or timelines that aren't in the source reporting. If a field is unknown, say so explicitly rather than guessing.
5. Run `python3 generate_report.py` to regenerate `injury_report.xlsx` from the updated `injuries.json`.
6. Run `python3 generate_csv.py` to regenerate `injuries.csv` from the updated `injuries.json`.
7. Run `python3 generate_rss.py` to regenerate `feed.xml` (RSS 2.0) from the updated `injuries.json`.
8. Run `python3 generate_opml.py` to regenerate `injuries.opml` (a standalone outline of injuries grouped by sport, built directly from `injuries.json` — independent of `feed.xml`, no `xmlUrl`).
9. Commit and push (`git add injuries.json injury_report.xlsx injuries.csv feed.xml injuries.opml && git commit -m "..." && git push`) so the public feed at https://esalisbury-arch.github.io/athlete-injury-feed/feed.xml stays current. The repo is https://github.com/esalisbury-arch/athlete-injury-feed, hosted via GitHub Pages.
10. Optionally prune records older than ~30 days from `injuries.json` to keep the outputs a manageable size, unless the injury is still actively affecting a team (e.g. long-term ACL recovery).
