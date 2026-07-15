def load_scores(filename):
    students = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                name, score = line.split(',')
                students.append({"name": name, "score": int(score)})
        return students
    except FileNotFoundError:
        print("没有找到对应的文件")
        return []

def get_average(students):
    total = sum(item["score"] for item in students)
    return total / len(students) if students else 0

def get_max_info(students):
    return max(students, key=lambda x:x["score"])

def get_min_info(students):
    return min(students, key=lambda x:x["score"])

if __name__ == "__main__":
    data = load_scores("scores.txt")
    print(f"一共读取了{len(data)}位学生成绩")
    avg_score = get_average(data)
    print(f"平均分：{avg_score:.2f}")
    max_stu = get_max_info(data)
    print(f"最高分：{max_stu['name']}，分数{max_stu['score']}")
    min_stu = get_min_info(data)
    print(f"最低分：{min_stu['name']}，分数{min_stu['score']}")