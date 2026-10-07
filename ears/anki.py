"""The same pack as an Anki deck. Staff lines quiz audio -> meaning (the front is sound only);
your lines quiz meaning -> Japanese. One sub-deck per scene."""
import os
import zlib

import genanki

MODEL_ID = 1728300001          # fixed: changing these makes Anki treat the deck as new
DECK_ID_BASE = 1728300100

CSS = """
.card { font-family: "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif; text-align: center;
        font-size: 20px; color: #1b2230; background: #f7f6f2; }
.nightMode.card, .night_mode .card { color: #ecebe6; background: #15171c; }
.kind { font-size: 12px; letter-spacing: .14em; text-transform: uppercase; opacity: .6; margin-bottom: 14px; }
.en { font-size: 24px; line-height: 1.3; }
.jp { font-size: 34px; line-height: 1.35; margin: 10px 0 4px; }
.kana { font-size: 17px; opacity: .7; }
.ro { font-size: 17px; font-style: italic; opacity: .8; margin-top: 4px; }
.key, .heard, .replies { font-size: 15px; margin: 14px auto 0; max-width: 32em; line-height: 1.45; text-align: left; }
.key { padding: 8px 12px; border-radius: 8px; background: rgba(0, 150, 110, .13); }
.heard { opacity: .8; }
"""

FRONT = """
{{#Listen}}<div class="kind">What did they say?</div>{{Audio}}{{/Listen}}
{{^Listen}}<div class="kind">Say it in Japanese</div><div class="en">{{English}}</div>{{/Listen}}
"""

BACK = """
{{FrontSide}}<hr id="answer">
{{#Listen}}<div class="en">{{English}}</div>{{/Listen}}
<div class="jp">{{Japanese}}</div><div class="kana">{{Kana}}</div><div class="ro">{{Romaji}}</div>
{{^Listen}}{{Audio}}{{/Listen}}
{{#Key}}<div class="key"><b>Listen for</b> {{Key}}</div>{{/Key}}
{{#Heard}}<div class="heard"><b>At speed</b> {{Heard}}</div>{{/Heard}}
{{#Replies}}<div class="replies"><b>You can say</b><br>{{Replies}}</div>{{/Replies}}
"""

FIELDS = ["Key ID", "English", "Japanese", "Kana", "Romaji", "Audio", "Listen", "Key", "Heard", "Replies"]

MODEL = genanki.Model(
    MODEL_ID, "Konbini Ears line",
    fields=[{"name": f} for f in FIELDS],
    templates=[{"name": "Card", "qfmt": FRONT, "afmt": BACK}],
    css=CSS,
)


def build_apkg(pack: dict, manifests: dict, audio_dir: str, out_path: str) -> int:
    staff, you = pack["voices"]["staff"], pack["voices"]["you"]
    media, decks, n = set(), [], 0
    for i, sc in enumerate(pack["scenes"], start=1):
        deck = genanki.Deck(DECK_ID_BASE + zlib.crc32(sc["id"].encode()) % 1_000_000,
                            f"{pack['title']}::{i:02d} {sc['title']}")
        for st in sc["steps"]:
            listen = st["kind"] == "staff"
            replies = "<br>".join(f"{r['ja']} — {r['ro']} — {r['en']}" for r in st["replies"])
            for j, v in enumerate(st["say"]):
                # Rotate voices across variants so the deck isn't one speaker.
                voice = staff[j % len(staff)] if listen else you
                name = manifests.get(voice, {}).get(v["id"])
                if name:
                    media.add(os.path.join(audio_dir, name))
                deck.add_note(genanki.Note(
                    model=MODEL,
                    fields=[v["id"], v.get("en") or st["en"], v["ja"], v["kana"], v["ro"],
                            f"[sound:{name}]" if name else "", "1" if listen else "",
                            st.get("key", ""), st.get("heard", ""), replies],
                    guid=genanki.guid_for("konbini-ears", v["id"]),
                    tags=[sc["id"], st["kind"]],
                ))
                n += 1
        decks.append(deck)
    pkg = genanki.Package(decks)
    pkg.media_files = sorted(media)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    pkg.write_to_file(out_path)
    return n
