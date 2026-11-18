# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Kimtigrn/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Kimtigrn/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image summing up Tuesday 17 November 2026's world news, as a
front-page poster: Ukraine's strike collapses a span of the Kerch Bridge
to Crimea, Iran fires drones at a US radar base in Bahrain, China confirms
a Xi–Trump–Putin summit in Shenzhen, the Pentagon fails its ninth audit,
Britain sanctions settlement builders, and Japan scrambles jets. Entry for
the make.fun bounty `news-image-20261117` — an AI image judge compares the
entries two at a time and ranks them by win rate.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) copies the
poster `entry.png` (1024×1024, 131 KB) to `$MAKEFUN_OUTPUT_DIR/entry.png`.
Both runs write the same bytes.

## How the image was made

`render_poster.py` draws the poster with Pillow from the verified news of
the day (run it locally: `python3 render_poster.py`). Every story was
checked against real reporting dated 17 November 2026:

- **Kerch Bridge** — Ukraine's strike collapses a road span; Zelenskyy
  calls it "an unprecedented operation"; Russia hits Kyiv's bridges in
  reply. (BBC, Al Jazeera)
- **Iran / the Gulf** — Iran fires drones at the US radar base in Bahrain
  (intercepted, no casualties); tankers hit mines near Hormuz. (Reuters)
- **China** — Beijing confirms the first Xi–Trump–Putin meeting, Thursday
  in Shenzhen on the APEC sidelines. (Outlook India)
- **United States** — the Pentagon fails its ninth straight audit; $4.8
  trillion in assets unverified, though 14 of 25 units pass for the first
  time. (Military Times, The Hill)
- **Britain** — the UK sanctions eight Israeli firms building settlements
  in the occupied West Bank. (Just Security)
- **Japan** — fighter jets scrambled after suspected Russian aircraft enter
  Japanese airspace. (Just Security)

Stories that happened before 17 November (the JPMorgan outage, the ULA
Vulcan failure, the Supreme Court's DEI order) were left out on purpose:
the contest is about 17 November alone.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
