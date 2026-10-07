"""python -m ears check PACK   |   python -m ears build PACK [--out dist] [--audio audio]"""
import argparse
import datetime
import json
import os
import sys

from .data import lint, load


def main() -> int:
    ap = argparse.ArgumentParser(prog="ears")
    ap.add_argument("cmd", choices=["check", "build"])
    ap.add_argument("pack")
    ap.add_argument("--out", default="dist")
    ap.add_argument("--audio", default="audio")
    args = ap.parse_args()

    pack = load(args.pack)
    problems = lint(pack)
    for p in problems:
        print("lint:", p, file=sys.stderr)
    if problems:
        return 1
    steps = [st for sc in pack["scenes"] for st in sc["steps"]]
    n_lines = sum(len(st["say"]) + len(st["replies"]) for st in steps)
    print(f"pack ok: {len(pack['scenes'])} scenes, {len(steps)} steps, {n_lines} lines")

    from .audio import lines, pick_text
    readings = [msg for _, line, _ in lines(pack) if (msg := pick_text(line)[1])]
    for r in dict.fromkeys(readings):
        print("reading:", r)
    if args.cmd == "check":
        return 0

    from .anki import build_apkg
    from .audio import record
    from .page import build_page
    manifests, readings = record(pack, args.audio, pack.get("speed", 1.0))
    base = os.path.splitext(os.path.basename(args.pack))[0]
    build = {"at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
             "pack": base, "lines": n_lines}
    size = build_page(pack, manifests, args.audio, "web/template.html",
                      os.path.join(args.out, f"konbini-ears-{base}.html"), build)
    notes = build_apkg(pack, manifests, args.audio, os.path.join(args.out, f"konbini-ears-{base}.apkg"))
    with open(os.path.join(args.out, f"report-{base}.json"), "w", encoding="utf-8") as f:
        json.dump({"build": build, "spoken_from_kana": readings}, f, ensure_ascii=False, indent=1)
    print(f"page: {size / 1e6:.1f} MB; anki: {notes} notes; {len(readings)} lines spoken from kana")
    return 0


if __name__ == "__main__":
    sys.exit(main())
