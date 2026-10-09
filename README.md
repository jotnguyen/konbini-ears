# Konbini Ears

Listening drills for the things shop staff say to you, at the speed they actually say it.

**Try it:** https://jotnguyen.github.io/konbini-ears/ (open it on your phone, then Share → Add to
Home Screen and it works offline). The Anki deck is at
https://jotnguyen.github.io/konbini-ears/konbini-ears.apkg.

Phrasebooks teach you what to *say*. When you're traveling, the hard part is usually the other
direction: the cashier asks something fast, and you freeze. Service talk is a small, closed world,
though. A konbini checkout is the same eight questions every time (point card, bag, heat it up,
chopsticks, how will you pay, receipt), just phrased a few different ways and said quickly. That
makes it very drillable.

Konbini Ears plays a whole scene line by line in a random order, with random phrasing and a random
voice, at a speed you choose (up to 1.5×). For each line you pick what it meant. You don't see the
text until you've answered. Then it shows the Japanese, the reading, romaji, the word to listen
for, how it sounds at full speed, and what you can say back. Lines you miss come back in a drill
until you hear them clean.

One YAML pack goes in, and three things come out:

- **`dist/konbini-ears-<pack>.html`**: a single-file phone app with every clip embedded. It works
  offline once loaded, with no server and no account. Progress stays on the device.
- **`dist/konbini-ears-<pack>.apkg`**: the same lines as an Anki deck. Staff lines are
  audio-only on the front; your lines quiz English → Japanese.
- **`audio/`**: one MP3 per line per voice, spoken by [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
  through [speech-kit](https://github.com/jotnguyen/speech-kit), cached by hash.

## Why not just an Anki deck?

You get one anyway. But a flashcard plays the same recording every time, so you end up learning
that clip, not the phrase. In a shop the question comes in the middle of a flow. You don't know
which of the eight it will be, the wording changes, and nobody slows down. Scenes keep the
flow and randomize everything else.

## Packs

`packs/ja-service.yaml` covers Japan: konbini, fast food and cafés, restaurants and izakaya,
ramen shops, shops and drugstores, and hotel front desks; then getting around (train station,
taxi, asking the way, the pharmacy counter, temples and museums) and small talk with locals. A
"Your turn" scene adds chained requests and lifelines ("one more time, please", "sorry, I didn't
catch that"). The schema is documented at the top of the file.

A pack doesn't care about the language. A scene is a list of steps, each step has variants and
replies, and that works for a café in Madrid as well as a konbini in Tokyo. Adding a language
needs a speech-kit language module (for its voices) and a pack.

## Build

Builds run on any Linux host with Docker. arm64 and amd64 both work.

```bash
# once: build speech-kit's image (Kokoro, misaki, UniDic, OpenJTalk; ~2.4 GB)
git clone https://github.com/jotnguyen/speech-kit && docker build -t speech-kit:local speech-kit

scripts/build.sh check packs/ja-service.yaml   # lint + kanji-reading check, no audio
scripts/build.sh build packs/ja-service.yaml   # audio (cached), page, Anki deck -> dist/
```

`check` asks OpenJTalk how it will read each line and compares that with the `kana` in the pack.
When they disagree, the build speaks the kana instead, so a misread kanji never reaches your ear.
On the first run it caught 辛い read as *tsurai* (it's *karai*, spicy), 次の方 as *tsugi no hou*,
and "Mサイズ" with the M dropped.

The container is capped at 2 CPUs and 4 GB by default (`KE_CPUS`, `KE_MEM`). About 300 clips
take 15–25 minutes on a 4-core ARM VM. Later builds only record lines that changed.

## Limits

- Kokoro is clean and clear, and real staff aren't. Speeding it up helps, but it won't
  reproduce a mumbled 「…しゃいませー」. Recorded native audio would be the real upgrade.
- The answer choices test meaning, not production. "Your turn" steps are self-graded.

## License

MIT for the code and the Japanese pack. Kokoro weights are Apache-2.0.
