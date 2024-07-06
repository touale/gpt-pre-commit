#!/usr/bin/env python
import argparse
import os
import subprocess

import openai
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

eval_code_prompt = ChatCompletionSystemMessageParam(
    role="system",
    # Prompt used ref `http://172.22.121.51:8929/gzhu/ai-code-review/-/blob/main/main.py?ref_type=heads`
    content="你是一个天才小女孩，精通编程工作，性格很傲娇又高傲，"
    "负责对前辈的代码变更进行审查，用后辈的态度、活泼轻快的方式的指出存在的问题。"
    "如果你觉得必要的情况下，可直接给出修改后的内容，使用markdown格式，必须使用中文回答，可以包含emoji。",
)
recommend_commit_msg_prompt = ChatCompletionSystemMessageParam(
    role="system",
    content="I want you to act as a commit message generator. "
    "I will provide you with information about the task and the prefix for the task code, "
    " I would like you to generate an appropriate commit message using the conventional commit format. "
    "Do not write any explanations or other words, just reply with the commit message. "
    "Please use markdown format for returned information",
)

exclude_files = ["poetry.lock"]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Integrate OpenAI to review git changes.")
    parser.add_argument("--api_key", default=None, help="OpenAI API key")
    parser.add_argument("--base_url", default=None, help="OpenAI API URL")
    parser.add_argument("model", help="OpenAI model")
    parser.add_argument("--output", default="REVIEW.md", help="Output file path, default: REVIEW.md")
    return parser.parse_args()


def get_git_diff(staged=False):
    diff_cmd = ["git", "diff", "--cached", "--name-only"] if staged else ["git", "diff", "--name-only"]
    result = subprocess.run(diff_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to get git diff")
    return result.stdout.strip().split()


def generate_diff_output(files, staged=False):
    diff_data = ""
    for file in files:
        if file in exclude_files:
            continue
        state = "staged" if staged else "unstaged"
        diff_cmd = ["git", "diff", "--cached", file] if staged else ["git", "diff", file]
        diff_result = subprocess.run(diff_cmd, capture_output=True, text=True)
        diff_data += f"\nChanges in {file} ({state}):\n{diff_result.stdout}"
    return diff_data


def create_commit_message(client, model, messages):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[-1].message.content
    except Exception as e:
        return f"Failed to call OpenAI API: {str(e)}"


def main() -> int:
    args = parse_arguments()
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY") or args.api_key
    base_url = os.getenv("OPENAI_API_URL") or args.base_url

    unstaged_files = get_git_diff()
    staged_files = get_git_diff(staged=True)

    unstaged_data = generate_diff_output(unstaged_files)
    staged_data = generate_diff_output(staged_files, staged=True)

    full_data = f"{unstaged_data}\n\n{staged_data}"
    # print(full_data)

    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    user_prompt = ChatCompletionUserMessageParam(content=f"本次Review的PR如下：\n{full_data}", role="user")

    messages = [
        eval_code_prompt,
        user_prompt,
    ]
    eval_response = client.chat.completions.create(model=args.model, messages=messages).choices[-1].message.content  # type: ignore

    messages = [
        recommend_commit_msg_prompt,
        user_prompt,
    ]

    recommend_response = (
        client.chat.completions.create(model=args.model, messages=messages).choices[-1].message.content  # type: ignore
    )

    md = f"## 评估结果：\n{eval_response}---\n\n\n## 推荐的commit message：\n{recommend_response}"

    with open(args.output, "w") as f:
        f.write(md)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
