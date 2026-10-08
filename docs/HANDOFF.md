# Hand-off: Konbini Ears

_Last updated: 2026-10-08. The owner is in Japan until 2026-10-16 and uses the app on an iPhone 8._

## State now

- **Live:** https://jotnguyen.github.io/konbini-ears/ is the `gh-pages` branch, holding `index.html`, `manifest.webmanifest`, `icons/`,
  `sw.js` and `konbini-ears.apkg`. It was checked at phone size in a desktop browser on 2026-10-07:
  the page loads, audio plays, all 336 clips decode, and the service worker cached the page.
  The owner installed it on the iPhone 8 home screen on 2026-10-08 and it works. Not yet checked:
  opening it offline with airplane mode on.
- **Pack:** `packs/ja-service.yaml` has 7 scenes and 76 steps, 360 clips in all. It was revised on 2026-10-09 after an
  adversarial review (`docs/reviews/2026-10-09-japanese-pack.md`). Before that it had 140 staff lines, 18 your-turn lines and
  55 replies. Staff lines are recorded in `jf_alpha` and `jm_kumo` at speed 1.0, your lines in
  `jm_kumo`. 14 lines are spoken from kana because OpenJTalk misreads their kanji; the full list is
  in `dist/report-ja-service.json`.
- **Repo:** public on `main`, with no open branches or PRs. CI hasn't been set up.
- **Artifact copy:** https://claude.ai/artifact/4BXk3QBMyPseSErv7P1LMb. The owner decided to keep
  it, but it's not the main copy: **the owner can't open Artifacts on the phone.** Phone
  deliverables go to GitHub Pages. The copy is built with `scripts/artifact.sh` and isn't updated
  automatically.

## How a change ships

The laptop (`C:\Users\J\konbini-ears`) is where you edit and run git. The OCI VM
(`~/Projects/konbini-ears`) is where you build, because pyopenjtalk and the Japanese voices don't
run on Windows, and this laptop has no Python or Node. The VM copy is **not** a git checkout; sync
it with tar.

```bash
# 1. edit packs/ja-service.yaml or web/template.html, commit, push
# 2. sync to the VM and build (clips are cached; only new or changed lines are recorded)
tar --exclude=.git --exclude=audio --exclude=dist -cf - . | ssh oci 'cd ~/Projects/konbini-ears && tar -xf - && sed -i "s/\r$//" scripts/*.sh && scripts/build.sh check packs/ja-service.yaml && scripts/build.sh build packs/ja-service.yaml'
# 3. copy the outputs back and publish
scp oci:Projects/konbini-ears/dist/konbini-ears-ja-service.{html,apkg} dist/
bash scripts/pages.sh ja-service
```

`check` has to pass lint before a build. Any `reading:` lines it prints are expected; they're the
lines that will be spoken from kana.

## Rules

- **Stay at 2 CPUs on the VM (the default).** Frigate on that VM is the home security camera
  while the owner is away. On 2026-10-07, 3 CPUs plus a CI job pushed the load to 5 on 4 cores.
  About 350 clips take 20–25 minutes.
- **This isn't a homelab stack.** Never touch `/opt/stacks`, `~/oci-homelab` or the deploy lease
  from here.
- **No AI attribution in commits.** The git identity is `jotnguyen` with the noreply email, set in
  this repo's config.
- **The pack is public.** Keep anything personal (names, hometown, hotels) out of it. Personal
  phrases go in nihongo-kit, which is private.
- **Kana:** write it spaced into words, with particles は/を/へ as their own tokens. Romaji is
  generated from it.

## Open items, in order

Scope is phrases to get by (see `docs/DECISIONS.md`, D2). The next piece of work is
**[`docs/tickets/KE-001-after-the-trip.md`](tickets/KE-001-after-the-trip.md)**: test on the iPhone 8, then fold
the trip notes into the pack. The items below are smaller or optional.

1. **[agent, optional] Better voices.** Kokoro is cleaner than a real cashier. Options: re-record
   with `jf_gongitsune`/`jf_nezumi` for variety, try VOICEVOX (check that it has an arm64 build), or
   add the owner's own recordings. A recording would be one more audio key per line in the
   manifest.
2. **[agent, optional] A CI lint job:** `python -m ears check` without the reading check, so no
   2 GB image is needed in CI.
3. **[parked, D7] The "didn't catch it" loop.** Type a half-heard fragment, an LLM reconstructs the
   phrase, and it joins the pack. It needs an API key and a server; build it only if the app gets
   daily use. It could also be a product hook (see the README).

## Gotchas already paid for

- `git worktree add` on Windows refuses a directory that already exists (even an empty one from
  `mktemp -d`). `pages.sh` uses `$(mktemp -d)/site`.
- Inside an Artifact, `confirm()` silently returns false. Reset uses a second tap instead.
- `ssh oci '... &'` hangs the ssh call. Start background builds with `setsid nohup ... < /dev/null &`.
