# KE-001: After the trip, fold real encounters back into the pack

**Type:** content + polish
**Priority:** next
**Human-blocked:** yes. Steps 1–2 need the owner and the iPhone 8.
**Scope:** phrases to get by ([D2](../DECISIONS.md#d2--scope-phrases-to-get-by-nothing-bigger-2026-10-08)).
No new kinds of features.
**Status:** open. Waiting on the owner's return (2026-10-16).

## Why

The pack was written before anyone used it. The trip (2026-09-30 → 10-16) is the best data we'll
ever have about which lines actually come up, which ones were too easy, and which staff lines were
missing. Without it, the pack is guesswork.

## Plan

1. **[owner] Check it on the iPhone 8.** Open https://jotnguyen.github.io/konbini-ears/, tap Share →
   Add to Home Screen, then turn on airplane mode and reopen it. Note whether:
   - it opens offline
   - audio plays with the silent switch on
   - 1.5× sounds like real staff
   - anything looks broken on the small screen
2. **[owner] Hand over the trip notes.** Bring:
   - fragments staff said that the pack doesn't cover ("something like *…ka*")
   - lines that came up often
   - pack lines that never came up
   Rough notes are fine.
3. **[agent] Reconstruct and add.** For each fragment, work out the likely phrase. Ask the owner
   when there's more than one candidate. Add it as a new variant of an existing step where it
   fits, and as a new step only if it's a different question. Write the kana, a `key` and a
   `heard` note for each.
4. **[agent] Prune.** Lower the `p` of steps that never came up. Remove a step only if the owner
   says it's useless.
5. **[agent] Fix what step 1 found.** Changes to the page or the service worker go in
   `web/template.html` and `web/sw.js`. Bump `CACHE` in `sw.js` if you change how it caches.
6. **[agent] Build and publish.** Follow `docs/HANDOFF.md` → "How a change ships". Only new lines get
   recorded. Run `check` first and read the `reading:` lines.

## Possible additions, only if the trip notes support them

Each of these fits D2 (phrases to get by). Add one only if it's in the owner's notes or the owner
asks for it:
- ~~Train station, taxi, pharmacy counter~~: added on 2026-10-09 at the owner's request, with
  asking the way, temples and museums, and small talk (D9). Trip notes can still correct them.
- **Numbers drill:** more amounts as `choices` variants. Hearing prices is where people freeze.

## Out of scope (see DECISIONS.md)

Speech recognition (D1), a conversation partner or LLM features (D2, D7), accounts or sync
(D4), and Artifacts (D6).

## Acceptance criteria

- [ ] The owner confirms offline works on the iPhone 8, or the bug is fixed.
- [ ] Every fragment from the trip notes is either in the pack or listed in this ticket as
      "couldn't place".
- [ ] `scripts/build.sh check` passes; the build report lists any lines spoken from kana.
- [ ] The Pages site shows the new build date (Settings → Progress).
- [ ] The owner plays one scene on the phone with the new lines.

## Rollback

Every change is in the pack and the page. `git revert`, rebuild and `scripts/pages.sh` restore the
previous site. Cached clips are kept, so a rollback records nothing new.

## Comments

- **2026-10-08** — Opened at the end of the first build session. The owner likes the app as it is
  and wants it kept to getting-by phrases (D2).
- **2026-10-09** — The owner installed it on the iPhone 8 home screen, and it works. The pack was
  revised after an adversarial review (`docs/reviews/2026-10-09-japanese-pack.md`), which added 8
  high-frequency lines. Step 1 now only needs the offline check with airplane mode on.
