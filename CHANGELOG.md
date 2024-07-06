# CHANGELOG

## v0.1.0 (2024-07-06)

### Feature

* feat: add gpt-based code review hook and update pre-commit config

- Adjusted argument formatting for check-yaml and ruff hooks in .pre-commit-config.yaml
- Introduced `review-code` hook with GPT integration for code review
- Added `python-semantic-release` as a dependency in pyproject.toml
- Added semantic release configuration in pyproject.toml for version management and changelog
- Exclude files from code review process and improved diff output generation in review_code.py ([`1ff84b6`](http://172.22.121.51:8929/gzhu-public/pre-commit-plugin/-/commit/1ff84b69c6074dbab766aba7f8d8bbd2e5c05c0c))

* feat: Integrate OpenAI GPT code review tool and setup pre-commit hooks

- Update .gitignore to include REVIEW.md, .ruff_cache, .mypy_cache, and .idea directories.
- Introduce pre-commit hooks for checking large files, TOML, YAML, end-of-file fixes, trailing whitespace, and integrating Ruff for linting and formatting.
- Add custom pre-commit hook to use GPT for code review.
- Implement diff generation and commit message recommendation functionalities using OpenAI GPT.
- Enhance Makefile for project setup, cleaning, styling, and linting operations. ([`69d6bb3`](http://172.22.121.51:8929/gzhu-public/pre-commit-plugin/-/commit/69d6bb3655815e9503f8c83b127eab13bbec8d44))
