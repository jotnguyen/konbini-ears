# Decisions

Why Konbini Ears is shaped the way it is. Each entry records the decision, why it was made, and
what would make us revisit it. Add new entries at the bottom; don't rewrite old ones. If a decision
changes, add a new entry that supersedes the old one.

## D1 — Listening first, not speaking (2026-10-07)

**Decision:** The core drill is hearing a staff line and picking what it meant. Speaking is a
self-graded "Your turn" step, with no speech recognition.

**Why:** In Japan, the owner's real problem was not understanding fast staff speech (袋, 温め,
お飲み物は…), not being understood. Talking into a phone and scoring the pronunciation (the
original oci-homelab TICKET-019 plan, with Whisper) trains the wrong skill.

**Revisit if:** listening stops being the bottleneck and the owner wants feedback on their own
pronunciation. Whisper is still planned in oci-homelab TICKET-019 for that case.

## D2 — Scope: phrases to get by, nothing bigger (2026-10-08)

**Decision:** The app teaches the short, formulaic exchanges of daily life as a visitor: shops,
food, hotels, transport. It is not a general Japanese course, a conversation partner, or a
grammar tool.

**Why:** The owner said they like it as it is: "just learning conversational phrases to get by".
Service talk is a small, closed world, which is what makes it drillable and keeps the pack honest.

**Revisit if:** the owner asks for more. Until then, new work means more scenes, better lines and
better audio, not new kinds of features.

## D3 — Scenes, not flashcards; Anki deck as a bonus (2026-10-07)

**Decision:** The main experience is a scene run: steps in order, each kept with probability `p`,
with a random wording and a random voice. Every build also produces an Anki deck.

**Why:** A flashcard plays the same clip every time, so you learn the recording. In a shop you
don't know which question is coming, the wording changes, and nobody slows down. The deck is for
people who already review in Anki.

## D4 — One YAML pack in, static files out (2026-10-07)

**Decision:** All content lives in `packs/*.yaml`. The build produces a single HTML file with every
clip inlined, plus an `.apkg`. There is no server, no account, and no database. Progress lives in
the browser's localStorage.

**Why:** It has to work offline on a phone in a subway, and cost nothing to run. The pack is the
product: the engine knows nothing about Japanese beyond the reading helpers, so another language
only needs a pack and a speech-kit voice.

## D5 — Audio: Kokoro through speech-kit, kana fallback (2026-10-07)

**Decision:** Clips come from Kokoro-82M via `jotnguyen/speech-kit`, in two voices (`jf_alpha`,
`jm_kumo`) at speed 1.0, and the app speeds them up at playback (1.0–1.5×). Before recording, the
build asks OpenJTalk how it will read each line. If that disagrees with the pack's kana, the line is
spoken from the kana.

**Why:** It's free, runs on the CPU, and is good enough to start with. The reading check caught real
errors on the first run, such as 辛い read as *tsurai* and 次の方 as *tsugi no hou*. A third voice
was dropped because recording took too long on the shared VM.

**Revisit if:** the clean TTS voice proves too easy compared with real staff. The options are in the
backlog ticket.

## D6 — Ship to GitHub Pages, not claude.ai Artifacts (2026-10-07)

**Decision:** The phone copy is https://jotnguyen.github.io/konbini-ears/ (the `gh-pages` branch),
with a network-first service worker for offline use. The repo is public.

**Why:** The owner's phone is an iPhone 8. It can't run the Claude app, so it can't open Artifacts.
Pages needs no login, and on the free plan it needs a public repo. The pack has nothing personal in
it; personal phrases stay in the private nihongo-kit.

## D7 — Not a SaaS, for now (2026-10-07)

**Decision:** This stays a personal learning tool and an open-source project.

**Why:** Generic phrase content is a commodity, and survival-phrase apps already exist. The one
part that could be a product is the loop from real life back into practice: type a half-heard
fragment, an LLM reconstructs the phrase, and it joins your drills with audio. That needs an API
key and a server, which goes against D4.

**Revisit if:** the owner uses the app daily and keeps wishing for that loop.
