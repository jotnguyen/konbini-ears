"""Record every line with speech-kit. Staff lines in each staff voice, your lines in one voice.

Before recording, ask OpenJTalk how it will read the kanji. If that disagrees with the kana in the
pack, speak the kana instead (particles as pronounced), so a misread kanji never reaches the ear.
"""
from speechkit.lang.ja import ojt_reading
from speechkit.lang.kana import to_kata
from speechkit.tts import build_audio

from .data import _KANA_OK, spoken_kana

_STRIP = str.maketrans("", "", " 、。？！?!")


def pick_text(line: dict) -> tuple[str, str | None]:
    want = to_kata(line["kana"]).translate(_STRIP)
    got = ojt_reading(line["ja"]).translate(_STRIP)
    if got == want:
        return line["ja"], None
    return spoken_kana(line["kana"]), f"{line['ja']}: OpenJTalk reads {got}, pack says {want}; speaking the kana"


def lines(pack: dict):
    """Yield (audio key, line, kind) for everything that needs a clip."""
    for scene in pack["scenes"]:
        for step in scene["steps"]:
            for v in step["say"]:
                yield v["id"], v, step["kind"]
            for r in step["replies"]:
                yield "r:" + r["ja"], r, "you"


def record(pack: dict, audio_dir: str, speed: float) -> tuple[dict, list[str]]:
    """Returns ({voice: {key: file}}, problems)."""
    staff_voices, you_voice = pack["voices"]["staff"], pack["voices"]["you"]
    jobs: dict[str, dict[str, dict]] = {v: {} for v in {*staff_voices, you_voice}}
    problems = []
    for key, line, kind in lines(pack):
        if not _KANA_OK.match(line.get("kana", "")):
            continue                      # lint reports it
        text, problem = pick_text(line)
        if problem and problem not in problems:
            problems.append(problem)
        for voice in (staff_voices if kind == "staff" else [you_voice]):
            jobs[voice][key] = {"id": key, "text": text}
    manifests = {}
    for voice, items in jobs.items():
        manifests[voice], _ = build_audio(list(items.values()), audio_dir, voice, speed)
    return manifests, problems
