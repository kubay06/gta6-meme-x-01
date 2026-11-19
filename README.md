# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/kubay06/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/kubay06/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty. Lucia planned a heist — Jason put his AI agent to work instead. "BABE, CANCEL THE HEIST." / "THE AGENT GOT PAID." The picture shows make.fun's real ghost mascot (from the press kit) handing the payout in through the getaway car's window. The post is the entry: it is posted on X from a public account with make.fun and the play code in its text, and this repository hands in the post's address in `POST.json`.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `POST.json` from this repository to `/output/POST.json` — that is all the program has to do. Replace the placeholder in `POST.json` with the real post address (`https://x.com/adibhask/status/<id>`) after posting.

---

<sub>Entered on [make.fun](https://make.fun/?ref=18a0yax6&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
