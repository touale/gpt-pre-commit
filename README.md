# gpt-pre-commit

## Description

`gpt-pre-commit` is a Python package designed to assist in code review before commits. It integrates OpenAI's capabilities to automatically review code changes, providing suggestions and improvements based on best practices.

`gpt-pre-commit` 是一个 Python 包，旨在协助提交之前的代码审查。它集成了 OpenAI 的功能，可以自动审查代码更改，并根据最佳实践提供建议和改进。

### Features

- Leverages OpenAI's GPT models to review code changes.
- Customizable review settings via pre-commit configurations.

### Install

Install the package using Poetry:

```bash
poetry add gpt-pre-commit # or pip install gpt-pre-commit
pre-commit install
```

---

### Usage

Step1: Configure the pre-commit hooks in your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/touale/gpt-pre-commit
  rev: v0.3.0
  hooks:
    - id: review-code
      allow_fail: true
      args: ["your model_name","--exclude" ,"pyproject.toml","poetry.lock",".env",".pre-commit-config.yaml","Makefile" ]
```

**How to set api_key and base_url of OpenAI?** There are three methods to choose from:
1. Set your OPENAI_API_KEY and OPENAI_API_URL as environment variables
    ```bash
    export OPENAI_API_KEY=your_api_key
    export OPENAI_API_URL=your_api_url
    pre-commit run -a -v
    ```
2. Set them in your `.env` file and run in `Makefile` .You can run the process with `make review`.
    ```
   # .env
   OPENAI_API_KEY=your_api_key
   OPENAI_API_URL=your_api_url
   ```

    ```
    #Makefile

    .PHONY: review
    include .env
    export
    review: ## Run the code review using pre-commit plugins.
        pre-commit run -a -v
    ```

3. Directly fill in the parameters in `.pre-commit-config.yaml`.(Not recommended)
    ```yaml
    - repo: local
      hooks:
        - id: review-code
          allow_fail: true
          args: ["--api_key", "your key", "--base_url", "$your url", "--output","REVIEW.md""]
    ```

Step2: run `pre-commit run -a -v` to run the code review.

Step3: open `REVIEW.md` to see the review result.
- You can set the `--output` parameter to save the review result to a file.
- default output file is `REVIEW.md`

---

### Dependencies

- Python 3.10+
- OpenAI API version 1.35.10+

### Development

Development dependencies include `ruff`, `mypy`, and `pre-commit`.

### License

This project is licensed under the MIT License.

### Authors

- touale <cpyu66@gmail.com>
