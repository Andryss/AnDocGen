# Agent Guide

This is the single source of instructions for AI agents working on AnDocGen.
Do not add separate agent workflow documents under `docs/`; keep that directory
for project documentation and historical report materials.

## Canonical Commands

- Run tests: `.venv/bin/pytest`
- Run coverage gate: `.venv/bin/pytest --cov=andocgen --cov-report=term-missing --cov-fail-under=85`
- Run lint: `.venv/bin/ruff check .`
- Validate config: `.venv/bin/andocgen config validate --config config.example.yaml`

Do not run formatters or generators that rewrite tracked files unless the user
explicitly asked for regenerated artifacts.

For a narrower development loop, run the specific test file first, then run the
full coverage and lint gate before committing. Generated documentation runs are
not part of the required gate for this stage.

## Repository Boundaries

- Source code lives in `src/andocgen/`.
- Tests live in `tests/`; prefer fixture projects under `tests/fixtures/` over
  constructing source files inline.
- Historical report files live in `docs/first_report/` and are read-only.
- Current project docs live directly under `docs/`.
- Example generated documentation is a baseline artifact only when it is already
  tracked by git.

## Workflow

Before editing:

1. Check repository state with `git status --short --branch`.
2. Read the files that own the behavior being changed.
3. Run a narrow baseline test when the change touches existing behavior.
4. Add or update tests before production code for behavior changes.

During implementation:

- Keep changes scoped to the subsystem under work.
- Add fixture projects under `tests/fixtures/` when a parser, call graph, or
  pipeline scenario needs source files.
- Use `apply_patch` for manual edits.
- Do not rewrite tracked generated docs unless the user explicitly asks for a
  regeneration pass.
- Do not edit `docs/first_report/**`; it is an archive of the first report.

## Generated Artifacts

- `.andocgen/logs/summary.txt` and `detail.json` are useful for comparing
  committed example baselines.
- `.andocgen/logs/llm_responses.jsonl` is diagnostic trace data. Treat prompt
  and response content as sensitive when `log_llm_content: true`.
- Local untracked generated docs, `.andocgen` directories, `__pycache__`, and
  coverage outputs should not be committed by default.

For a generated output directory, inspect files in this order:

1. `.andocgen/logs/summary.txt` - high-level counts, elapsed time, fallback count.
2. `.andocgen/logs/detail.json` - parse, generation, validation, and fallback issues.
3. `.andocgen/logs/llm_responses.jsonl` - per-attempt LLM request/response metadata.
4. `.andocgen/cache/checksums.json` - source, docblock, and dependency hashes.

Markdown files such as `README.md`, `module.py.md`, and package-level
`README.md` files are user-facing documentation output. In `examples/` and
`eval/`, tracked generated docs can be used as baseline artifacts for manual
comparison.

Use `.venv/bin/andocgen clean --config path/to/config.yaml` to remove the
runtime `.andocgen` directory under the configured output directory. The command
does not remove rendered Markdown documentation.

## Example Runs

Use mock configs for fast local checks:

```bash
.venv/bin/andocgen inspect ./examples/mini_calculator --config config.example.yaml
.venv/bin/andocgen generate ./examples/mini_calculator --config config.example.yaml --dry-run
```

Use Ollama or OpenAI-compatible configs only when the user asks to compare real
model behavior or regenerate baseline examples.

## Implementation Rules

- Keep the existing modular shape: `base.py` -> `factory.py` ->
  `implementations/`.
- Keep Markdown as the output format and JSON as the LLM contract.
- Do not restore legacy Markdown LLM parsing.
- Prefer small focused modules over adding more responsibilities to
  `pipeline.py`.
- Validate structured data before formatting; do not validate rendered Markdown
  as a separate source of truth.
