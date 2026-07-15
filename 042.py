from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://api.siliconflow.cn/v1"
)
MODEL_NAME = "deepseek-ai/DeepSeek-V4-Flash"


def ask_ai(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        ans_text = resp.choices[0].message.content
        return ans_text
    except Exception as e:
        return f"调用失败：{e}"


if __name__ == "__main__":
    ordinary_prompt = "什么是函数"
    structured_prompt = """
    【角色】你是面向零基础初学者的编程科普讲师
    【背景】编程新手刚入门，专业术语理解较为吃力
    【任务】解释编程里的函数到底是什么
    【要求】全程使用通俗日常语言进行讲解，搭配生活化实例，整体回答最多不超过5句话
    """

    print("=====普通Prompt输出结果=====")
    res1 = ask_ai(ordinary_prompt)
    print(res1)

    print("\n=====结构化Prompt输出结果=====")
    res2 = ask_ai(structured_prompt)
    print(res2)




