# CLAUDE.md: konbini-ears

Read these in order:
1. `docs/HANDOFF.md` for the current state, the build-and-publish loop (edit on the laptop, build
   on the OCI VM, publish to GitHub Pages) and the rules.
2. `docs/DECISIONS.md` for why it's built this way. The scope is phrases to get by, nothing
   bigger.
3. The open ticket in `docs/tickets/`.

The three rules that bite:
- The owner uses an iPhone 8 with no Claude app. **Ship phone things to GitHub Pages, not claude.ai
  Artifacts.**
- Builds run on the VM capped at 2 CPUs. Frigate shares that host.
- The repo is public: no personal details in the pack, and no AI attribution in commits.
