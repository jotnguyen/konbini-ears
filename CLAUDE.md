# CLAUDE.md: konbini-ears

Read `docs/HANDOFF.md` first. It has the current state, the build-and-publish loop (edit on the
laptop, build on the OCI VM, publish to GitHub Pages), the rules, and the open items.

The three rules that bite:
- The owner uses an iPhone 8 with no Claude app. **Ship phone things to GitHub Pages, not claude.ai
  Artifacts.**
- Builds run on the VM capped at 2 CPUs. Frigate shares that host.
- The repo is public: no personal details in the pack, and no AI attribution in commits.
