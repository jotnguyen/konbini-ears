"""Load a pack, fill in defaults, add romaji, and lint it."""
import re

import yaml

from speechkit.lang.kana import to_romaji

PARTICLES = {"は": "wa", "を": "o", "へ": "e"}
SPOKEN_PARTICLES = {"は": "わ", "を": "お", "へ": "え"}
_KANA_OK = re.compile(r"^[ぁ-ゖァ-ーー、。 ]+$")
_ID_OK = re.compile(r"^[a-z0-9-]+$")


def romaji(kana: str) -> str:
    words = []
    for tok in kana.split():
        tail = tok[-1] if tok[-1] in "、。" else ""
        core = tok[:-1] if tail else tok
        r = PARTICLES.get(core) or to_romaji(core)
        if r.endswith(("nichiha", "banha")):       # greetings keep the old particle spelling
            r = r[:-2] + "wa"
        words.append(r + {"、": ",", "。": ".", "": ""}[tail])
    return " ".join(words)


def spoken_kana(kana: str) -> str:
    """Kana to feed the voice when the kanji can't be trusted: particles as pronounced, no spaces."""
    return "".join(SPOKEN_PARTICLES.get(t, t) for t in kana.split())


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        pack = yaml.safe_load(f)
    for scene in pack["scenes"]:
        for step in scene["steps"]:
            step.setdefault("kind", "staff")
            step.setdefault("p", 1)
            step.setdefault("replies", [])
            for i, v in enumerate(step["say"]):
                v["id"] = f"{step['id']}.{i}"
                v["ro"] = romaji(v["kana"])
            for r in step["replies"]:
                r["ro"] = romaji(r["kana"])
    return pack


def lint(pack: dict) -> list[str]:
    problems, seen = [], set()

    def check_line(where: str, line: dict) -> None:
        if not line.get("ja"):
            problems.append(f"{where}: no ja")
        kana = line.get("kana", "")
        if not kana:
            problems.append(f"{where}: no kana")
        elif not _KANA_OK.match(kana):
            bad = sorted({c for c in kana if not _KANA_OK.match(c)})
            problems.append(f"{where}: kana has non-kana characters {bad}")
        elif not line["ro"].isascii():
            problems.append(f"{where}: romaji did not convert cleanly: {line['ro']}")

    for scene in pack["scenes"]:
        for step in scene["steps"]:
            sid = step.get("id", "?")
            if not _ID_OK.match(sid):
                problems.append(f"{sid}: id must be kebab-case")
            if sid in seen:
                problems.append(f"{sid}: duplicate id")
            seen.add(sid)
            if step["kind"] not in ("staff", "you"):
                problems.append(f"{sid}: unknown kind {step['kind']}")
            if not step.get("en"):
                problems.append(f"{sid}: no en")
            if not step["say"]:
                problems.append(f"{sid}: no variants")
            if not 0 < step["p"] <= 1:
                problems.append(f"{sid}: p must be in (0, 1]")
            for v in step["say"]:
                check_line(v["id"], v)
                ch = v.get("choices")
                if ch is not None and (len(ch) < 2 or len(set(ch)) != len(ch)):
                    problems.append(f"{v['id']}: choices need 2+ distinct entries")
            for j, r in enumerate(step["replies"]):
                check_line(f"{sid} reply {j}", r)
                if not r.get("en"):
                    problems.append(f"{sid} reply {j}: no en")
    return problems
