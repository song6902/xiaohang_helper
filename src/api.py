"""
API调用模块：封装硅基流动API请求
"""
import requests
from .config import API_URL, HEADERS, MODEL_NAME, REQUEST_TIMEOUT


def ask_ai(system_prompt: str, user_question: str) -> str:
    """调用硅基流动API获取AI回答
    返回：回答文本，或者错误提示
    """
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
        "temperature": 0.3,  # 低温度，回答更稳定，不容易胡说
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=data,
            timeout=REQUEST_TIMEOUT
        )

        # 处理HTTP状态码
        if response.status_code == 401:
            return "[ERROR_401] API Key失效，请检查你的硅基流动Key是否正确"
        elif response.status_code != 200:
            return f"[ERROR_{response.status_code}] API异常，状态码：{response.status_code}"

        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        return answer

    except requests.exceptions.Timeout:
        return "[ERROR_TIMEOUT] AI响应超时，请稍后再试"
    except requests.exceptions.ConnectionError:
        return "[ERROR_NETWORK] 网络连接失败，请检查你的网络"
    except (KeyError, IndexError):
        return "[ERROR_FORMAT] AI返回格式异常，请重试"
    except Exception as e:
        return f"[ERROR_UNKNOWN] 发生未知错误：{str(e)}"
