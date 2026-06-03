# Manual archive install + runtime verification for external skills

Use this pattern when a user provides upstream install docs for a skill repo and Hermes cannot install directly from a raw `SKILL.md` URL.

## When to use
- `hermes skills install <raw-url>` cannot fetch the skill
- The upstream repo is a single-skill repository distributed as a zip archive
- The skill ships helper scripts and expects a post-install runtime probe

## Durable workflow
1. Read the upstream install doc first; do not assume Hermes-native install is the intended path.
2. Download the repository archive (`main.zip` or a pinned release archive).
3. Extract it and copy the full skill directory into `~/.hermes/skills/<skill-name>/`.
   - Copy the whole directory, not only `SKILL.md`; bundled `scripts/`, examples, `.env.example`, and runtime templates may be required.
4. If the skill includes multiple runtime entrypoints (for example Python / Node / shell CLIs), run the upstream probe or entry test on each available runtime.
5. Persist the selected runtime in the skill directory when the upstream format expects it (for example `runtime.conf`).
6. Verify installation from Hermes, not only from the filesystem:
   - `skill_view(name='<skill-name>')` should succeed
   - `hermes skills list` should show the skill as enabled
7. If the user asked to make that skill the default workflow for a class of tasks, state that future turns should prefer that skill operationally. Do not claim the built-in Hermes `web_search` tool itself was globally remapped unless you actually changed Hermes config/code to do that.

## AnySearch-shaped example
- Upstream raw-URL install may fail even when the repo archive is reachable.
- A working fallback is:
  - download `https://github.com/<owner>/<repo>/archive/refs/heads/main.zip`
  - extract
  - copy into `~/.hermes/skills/anysearch/`
  - run each available CLI's `doc` or entry-test command
  - choose the best runtime and write `runtime.conf`
  - run one real search as a final verification

## Pitfall
Do not overstate the result of a skill install. Installing a search skill and choosing to use it by default in future turns is different from reconfiguring Hermes internals so every built-in search tool automatically routes through that skill.