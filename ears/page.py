"""Render web/template.html with the pack and every clip inlined: one file, offline once loaded."""
import base64
import json
import os

STEP_KEYS = ("id", "kind", "p", "en", "key", "heard", "note")
LINE_KEYS = ("id", "ja", "kana", "ro", "en", "choices", "key", "heard")


def build_page(pack: dict, manifests: dict, audio_dir: str, template: str, out_path: str,
               build: dict) -> int:
    clips, index = [], {}

    def clip(voice: str, key: str):
        name = manifests.get(voice, {}).get(key)
        if not name:
            return None
        if name not in index:
            with open(os.path.join(audio_dir, name), "rb") as f:
                clips.append(base64.b64encode(f.read()).decode("ascii"))
            index[name] = len(clips) - 1
        return index[name]

    staff, you = pack["voices"]["staff"], pack["voices"]["you"]

    def line(src: dict, key: str, voices: list[str]) -> dict:
        row = {k: src[k] for k in LINE_KEYS if src.get(k) not in (None, "")}
        row["a"] = {v: i for v in voices if (i := clip(v, key)) is not None}
        return row

    scenes = []
    for sc in pack["scenes"]:
        steps = []
        for st in sc["steps"]:
            row = {k: st[k] for k in STEP_KEYS if st.get(k) not in (None, "")}
            row["say"] = [line(v, v["id"], staff if st["kind"] == "staff" else [you]) for v in st["say"]]
            row["replies"] = [line(r, "r:" + r["ja"], [you]) for r in st["replies"]]
            steps.append(row)
        scenes.append({"id": sc["id"], "title": sc["title"], "blurb": sc.get("blurb", ""), "steps": steps})

    data = {"title": pack["title"], "subtitle": pack.get("subtitle", ""), "lang": pack.get("lang", "ja"),
            "voices": staff, "scenes": scenes, "build": build}
    with open(template, encoding="utf-8") as f:
        html = f.read()
    marker = "/*__KE_DATA__*/"
    if marker not in html:
        raise ValueError(f"template is missing the {marker} marker")
    payload = ("window.KE=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
               + "window.KE_AUDIO=" + json.dumps(clips, separators=(",", ":")) + ";")
    html = html.replace(marker, payload)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return os.path.getsize(out_path)
