# gpt-pre-commit

## Description

`gpt-pre-commit` is a Python package designed to assist in code review before commits. It integrates OpenAI's capabilities to automatically review code changes, providing suggestions and improvements based on best practices.

### Features

- Leverages OpenAI's GPT models to review code changes.
- Customizable review settings via pre-commit configurations.

### Installation

Install the package using Poetry:

```bash
poetry add gpt-pre-commit
pre-commit install
```

### Usage

Configure the pre-commit hooks in your `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: review-code
      name: gpt review code
      entry: review-code
      language: python
      pass_filenames: false
      args: ["api_key","base_url","model_name"]
```

### Dependencies

- Python 3.10+
- OpenAI API version 1.35.10+

### Development

Development dependencies include `ruff`, `mypy`, and `pre-commit`.

### License

This project is licensed under the MIT License.

### Authors

- touale <cpyu66@gmail.com>
