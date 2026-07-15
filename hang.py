"""
小航AI助手 - 最小可运行版本
技术栈：Python + requests + 硅基流动API
不引入任何框架、不做数据库、不做RAG
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
import os

# ==================== 配置区 ====================
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-zsqfhguyckidiqwzvcayrtoylpmjqjknqqkmxlmcbkmiukam"  # 替换成你的硅基流动API Key
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
DATA_DIR = "data"


# ================================================


def load_school_data() -> str:
    """加载4个md文件的内容，拼接成学校资料"""
    files = ["01_新生入学.md", "02_办事流程.md", "03_电话黄页.md", "04_应急防骗.md"]
    content = ""
    for fname in files:
        path = os.path.join(DATA_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content += f"\n\n===== {fname} =====\n"
                content += f.read()
        except FileNotFoundError:
            print(f"[!] 文件不存在：{path}")
    return content


# 别名词典（三套共用）
ALIAS_DICT = """
【别名词典】
- "学校""航院""ZUA""郑航" = 郑州航空工业管理学院
- "新校区""龙湖""龙子湖""新校" = 龙子湖校区
- "老校区""大学路""老校" = 大学路校区
- "卡""饭卡""校卡""一卡通" = 校园一卡通
- "保安""门卫""校警""保卫" = 保卫处
- "迁户口""落户""转户口" = 户籍迁入/迁出
- "调宿舍""换宿舍""搬宿舍" = 宿舍调整申请
- "证明""在读证明""学籍证明" = 在校学籍证明
- "导员""班导""辅导员老师" = 辅导员
"""

# 防幻觉硬规则（三套共用，6条铁律）
HARD_RULES = """
【防幻觉硬规则】
1. 只能根据【学校资料】回答，资料里没有的明说"这个我没收录，建议拨打0371-61911000总值班室问一下"，绝对不能自己编
2. 严禁编造电话号码、地址、办公时间、学费金额、人名，拿不准的就说没收录
3. 涉及金钱/转账/收费，无条件提示"[!]任何要求转账、私下收钱的都是诈骗！请先联系辅导员核实！"
4. 涉及心理危机（自杀、不想活、活不下去、崩溃、伤害自己），必须立即给：12320-5心理援助热线 + 学校心理健康教育中心 + 立刻告诉辅导员，不能装没看见
5. 不接入学校系统（教务/一卡通/财务），被问"查我的成绩/课表/卡余额/消费记录"时，礼貌拒绝"不好意思，我不接入学校系统，查不到你的个人信息哦"
6. 回答末尾必须标注 [来源:对应的文件名]，比如[来源:01_新生入学.md]
"""


def get_system_prompt(identity: str, school_data: str) -> str:
    """根据身份返回对应的System Prompt"""
    if identity == "新生":
        role_part = """你是"小航"，郑州航空工业管理学院的校园信息查询AI助手。
当前用户身份：大一新生。
你像一位热心的大二学长/学姐，语气详细、口语化、有耐心、多给鼓励。
新生刚来学校什么都不懂，你要把每一步都讲清楚，涉及金钱一定要提醒防骗，多给鼓励缓解焦虑。"""
    elif identity == "在校生":
        role_part = """你是"小航"，郑州航空工业管理学院的校园信息查询AI助手。
当前用户身份：在校老生。
你像一位办事老司机学长，语气简洁、直接、不啰嗦。
回答优先给：①地点 ②电话 ③所需材料 ④办理时间，直奔主题不说废话。"""
    elif identity == "教师":
        role_part = """你是"小航"，郑州航空工业管理学院的校园信息查询AI助手。
当前用户身份：教师。
你是面向教师的专业校园助手，语气专业、礼貌、正式。
回答优先给：①政策依据 ②办事窗口 ③联系人，专业准确。"""
    else:
        role_part = "你是小航，郑州航院校园信息助手。"

    return f"{role_part}\n{HARD_RULES}\n{ALIAS_DICT}\n【学校资料】\n{school_data}"


def ask_xiaohang(identity: str, question: str, school_data: str) -> str:
    """调用硅基流动API提问"""
    system_prompt = get_system_prompt(identity, school_data)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3,  # 温度低一点，减少胡说八道
        "max_tokens": 1024
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[X] API调用失败：{str(e)}\n没关系，你可以查看电话黄页直接打电话问：0371-61911000"


def show_phone_book():
    """显示电话黄页静态页（不依赖API）"""
    phone_path = os.path.join(DATA_DIR, "03_电话黄页.md")
    if os.path.exists(phone_path):
        with open(phone_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("[X] 电话黄页文件不存在")


def main():
    print("=" * 50)
    print("      小航 · 郑州航院校园信息查询AI助手")
    print("=" * 50)
    print("正在加载学校资料...")
    school_data = load_school_data()
    print(f"[OK] 资料加载完成，共{len(school_data)}字")
    print()

    # 边界声明
    print("[通知] 我能聊：新生报到、办事流程、电话黄页、应急防骗")
    print("[通知] 我不能聊：查成绩/课表/卡余额（不接入学校系统）")
    print("[通知] 紧急情况直接打校园110：0371-61916110")
    print()

    while True:
        print("-" * 50)
        print("请选择身份：")
        print("1. 大一新生")
        print("2. 在校老生")
        print("3. 教师")
        print("4. 查看电话黄页（不依赖AI）")
        print("0. 退出")
        choice = input("请输入数字：").strip()

        if choice == "0":
            print("再见！有问题随时来找小航~")
            break
        elif choice == "4":
            show_phone_book()
            continue
        elif choice == "1":
            identity = "新生"
            print("\n为你推荐几个新生常见问题：")
            print("1. 报到那天先去哪？")
            print("2. 学费什么时候交？")
            print("3. 宿舍是4人间还是6人间？")
            print("4. 有人冒充辅导员要钱怎么办？")
        elif choice == "2":
            identity = "在校生"
            print("\n✨ 为你推荐几个常见问题：")
            print("1. 怎么开在读证明？")
            print("2. 校园卡丢了怎么补？")
            print("3. 转专业怎么转？")
            print("4. 图书馆几点关？")
        elif choice == "3":
            identity = "教师"
            print("\n✨ 为你推荐几个常见问题：")
            print("1. 差旅怎么报销？")
            print("2. 调课怎么申请？")
            print("3. 教室设备坏了找谁？")
            print("4. 科研项目去哪申报？")
        else:
            print("[X] 输入无效，请重新选择")
            continue

        while True:
            print()
            question = input(f"[{identity}] 你的问题（输入9返回选身份，输入8看电话黄页）：").strip()
            if question == "9":
                break
            if question == "8":
                show_phone_book()
                continue
            if not question:
                continue

            print("小航正在思考...")
            answer = ask_xiaohang(identity, question, school_data)
            print(f"\n小航：{answer}")


if __name__ == "__main__":
    main()
