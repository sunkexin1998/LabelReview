import os.path

import pandas as pd

actions = [
    "anc95/ChatGPT-CodeReview",  # 1
    "coderabbitai/ai-pr-reviewer",  # 3
    "mattzcarey/code-review-gpt",  #2
    "aidar-freeed(merged)/ai-codereviewer",  # 4
    "kxxt/chatgpt-action",  # 5

    "cirolini/genai-code-review",  # 6
    "microsoft/gpt-review",  # 8
    "truongnh1992/gemini-ai-code-reviewer",  # 9
    "feiskyer/ChatGPT-Reviewer",  # 10

    "adshao/chatgpt-code-review-action",  # 11
    "tmokmss/bedrock-pr-reviewer",  # 12
    "Integral-Healthcare/robin-ai-reviewer",  # 13
    "presubmit/ai-reviewer",  # 14

    "gvasilei/AutoReviewer",  # 16
    "unsafecoerce/chatgpt-action",  # 17
    "magnificode-ltd/chatgpt-code-reviewer",  # 19
    "ca-dp/code-butler",  # 20
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def remove_bom(s: str) -> str:
    BOM = '\ufeff'
    if s.startswith(BOM):
        return s[len(BOM):]
    return s


def query(file_path,commit_id):
    for AI_reviewer in actions:
        AI_reviewer_refined_for_path = AI_reviewer.replace("/", "_")
        directory_for_AI_reviewer = f"{BASE_DIR}/_data/{AI_reviewer_refined_for_path}"
        crawling_directory = f"{directory_for_AI_reviewer}/crawled_data"
        source_fname = f"{crawling_directory}/reviewed_file_versions(2).parquet"
        if not os.path.exists(source_fname):
            continue;
        source = pd.read_parquet(source_fname)
        matched_row = source[
            (source["Diff_Path"] == file_path)
            & (source["Commit_id"] == commit_id)
            ]
        content = ""
        for _,row in matched_row.iterrows():
            content = remove_bom(row["File_Content"])
            print(row)
            break;
        if content:
            break;

    # Print the file's comment
    print(content)

    # Save the file's comment
    file_path = file_path.replace("/","_")
    output_path = f"{BASE_DIR}/file_at_commit/{file_path}_at_{commit_id}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] Saved file content to: {output_path}")

if __name__ == "__main__":
    file_path = "rpc/handlers.go"
    commit_id = "9359cdf1837fa6bf84632f6ccc8dfb05de0f7296"
    query(file_path, commit_id)