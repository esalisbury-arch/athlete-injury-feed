# Daily update task

Project folder: `/Users/ericsalisbury/Desktop/athlete-injury-feed/`

**"High-profile" definition:** any athlete competing at the professional level (major pro leagues, top international/national teams) or NCAA Division I — this includes bench players, role players, and rotation players, not just headline stars/All-Stars. It excludes amateur, recreational, non-D1 college, and obscure lower-tier/developmental competitions (e.g. G League, low-level minor league baseball) unless the athlete is a well-known name.

**Daily target: ~40 new injury records per run.** To hit that volume, sport-level searches alone (e.g. "NFL injury news") aren't enough — go a level deeper with per-team or per-tournament searches (e.g. individual NFL/MLB team injury reports, individual EPL/La Liga clubs, individual golf/tennis tournaments in progress) so coverage isn't limited to whatever a handful of generic queries surface. Treat this as a volume floor, not a quality target: verify recency (roughly last 24-48 hours; don't recycle stale season-recap injuries from leagues currently in their off-season) and specificity for every record exactly as before. If a thorough, deep sweep across all listed sports still turns up fewer than 40 genuinely new high-profile injuries, report the true (lower) count rather than padding it — never fabricate a record, and never include vague/unverifiable ones just to hit the number.

On each run:

1. Read `injuries.json` to see which injuries are already tracked (check the `guid` field to avoid duplicates).
2. Search the web for new high-profile athlete injury news from roughly the last 24-48 hours, across major sports: NFL, NBA, WNBA, MLB, NHL, top soccer leagues (Premier League, La Liga, MLS, NWSL, Champions League, national teams), tennis (ATP/WTA), golf (PGA/LPGA), F1, boxing/UFC, cricket, Olympic sports, and NCAA Division I college sports (football, men's and women's basketball, baseball, softball, volleyball, gymnastics, soccer, wrestling, track & field). Search each sport/league individually, and within sports/leagues that are actually in-season, drill down further to individual teams or tournaments (e.g. per-team MLB/NFL injury reports, per-club EPL/La Liga searches, the specific tournaments currently being played in golf/tennis) — this depth is what surfaces enough volume to reach the ~40/day target. Actively search for women's sports and NCAA D1 college athletes each run, not just the major men's pro leagues — those tend to dominate search results by default. Skip leagues that are currently in their off-season for fresh injury news (their search results will mostly be stale season-recap injuries from months earlier) — check the schedule/date context before including anything from a soccer league whose season already ended, for example.
3. For each genuinely new, high-profile injury found, add a record to `injuries.json` with these fields (all required):
   - `guid`: unique slug, e.g. `sport-lastname-YYYY-MM-DD`
   - `athlete`: full name
   - `org`: team/club and league (and national team if relevant)
   - `sport`
   - `injury_context`: the specific medical nature of the injury (e.g. "ACL reconstruction", "grade 2 hamstring strain") — be as specific as the source allows
   - `duration`: expected time out / recovery timeline
   - `financial_impact`: salary, contract, or prize-money impact if reported; otherwise `"Not disclosed in available reporting"` — never invent a number
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
