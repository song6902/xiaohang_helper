import requests

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = ""  # 硅基流动控制台创建的 Key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 对话历史
messages = []

print("AI 学习助手（输入 quit 退出）")
print("=" * 40)

while True:
    user_input = input("\n你：")

    if user_input.lower() == "quit":
        print("再见！")
        break

    # 把用户消息加入历史
    messages.append({"role": "user", "content": user_input})

    # 发送请求（带上完整对话历史）
    data = {
        "model": "moonshotai/Kimi-K2.7-Code",
        "messages": messages
    }
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    # 把 AI 回答加入历史
    messages.append({"role": "assistant", "content": answer})
    print(f"\nAI: {answer}")