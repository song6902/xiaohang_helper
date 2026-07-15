"""
配置模块：API地址、密钥、模型名等
"""

# 硅基流动API配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-zsqfhguyckidiqwzvcayrtoylpmjqjknqqkmxlmcbkmiukam"  # 替换成你自己的硅基流动的API Key
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# 请求头
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# 请求超时时间（秒）
REQUEST_TIMEOUT = 30

# 12个推荐问题，按身份分组
PRESET_QUESTIONS = {
    "新生": [
        "报到那天先去哪？需要带什么材料？",
        "学费什么时候交？多少钱？",
        "宿舍是4人间还是6人间？有空调吗？",
        "有人冒充辅导员要我转钱怎么办？",
    ],
    "在校生": [
        "怎么开在读证明？去哪里盖章？",
        "校园卡丢了怎么补办？要带什么？",
        "转专业怎么转？需要什么条件？",
        "图书馆几点开门几点关门？",
    ],
    "教师": [
        "差旅费怎么报销？需要什么发票？",
        "调课怎么申请？流程是什么？",
        "教室多媒体设备坏了找谁修？",
        "科研项目去哪申报？什么时候截止？",
    ],
}
