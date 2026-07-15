from openai import OpenAI

client = OpenAI(
    api_key="sk-zsqfhguyckidiqwzvcayrtoylpmjqjknqqkmxlmcbkmiukam",
    base_url="https://api.siliconflow.cn/v1"
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Pro",
    messages=[
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好,3句话介绍郑州航空工业管理学院"}
    ]
)
print(response.choices[0].message.content)
total_tokens = response.usage.total_tokens
print(total_tokens)
