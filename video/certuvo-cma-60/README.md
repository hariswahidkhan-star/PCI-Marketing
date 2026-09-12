# Certuvo — CMA preparation in one minute (0:51)

The features-first cut of the Certuvo CMA film: what you get with Certuvo, in
under a minute, for the website's course page, paid social and the top of a
landing page. Four scenes — a presenter hook, the four core features, the two AI
features, and a presenter close — in the same light treatment as the full film
(`../certuvo-cma`): off-white ground, white cards with a blue top rule, Certuvo
blue, the lecture's red for numbered tags and the progress bar.

| # | Scene | Starts | On screen |
|---|---|---|---|
| 1 | Hook (presenter) | 0:00 | "Preparing for the CMA? Here's how Certuvo gets you ready." + five feature chips |
| 2 | What you get | 0:05 | Practice exams · Progress tracking · Live study rooms · 24/7 chat support |
| 3 | AI inside | 0:23 | AI Question Forge (four-judge panel) · AI Coach (calls, reads your screen, auto-off in mocks, six languages) |
| 4 | Start (presenter) | 0:41 | "Pick your part. Start today — at certuvo.com", then the end card |

- **Voice:** ElevenLabs *Nassim*, `eleven_v3`, four new takes written for this
  length (`src/vo.py`).
- **Presenter:** the same Seedream portrait animated by HeyGen Avatar IV from the
  new hook and close takes (`assets/avatar-s1.mp4`, `assets/avatar-s4.mp4`).
- **Music, brand, fonts:** shared with the full film (`brand/`, `music/` are
  symlinks into `../certuvo-cma`).
- **Pipeline:** identical to the full film — `sync.py` measures the takes,
  `presenter.py` cuts the clips to frames, `scene.html` is cut to the voice, the
  probe suite must be clean at all four sizes, `build.sh` renders 4K, 1080p,
  9:16 and 1:1.

```bash
cd src && ./build.sh          # or HD_FIRST=1 ./build.sh
```

Every feature claim is the same wording as the full film and is traced to
certuvo.com in `../certuvo-cma/claims-register.md` §7. The end card carries the
trademark and independence line and "Preparation does not guarantee a pass."

## What is in `dist/`

`certuvo-cma-60-3840x2160-MASTER-{captions,clean}.mp4`,
`certuvo-cma-60-1920x1080-{captions,clean,silent}.mp4`,
`certuvo-cma-60-1080x1920-captions.mp4` (9:16), `certuvo-cma-60-1080x1080-captions.mp4`
(1:1), `.srt`/`.vtt`, poster and thumbnails, audio stems. Same encode settings
and −14 LUFS mix as the full film.
