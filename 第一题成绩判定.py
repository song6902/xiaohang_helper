while True:
    a = input("请输入百分制成绩,想要退出按q: ")
    if a == "q":
        break
    try:
        score = int(a)
    except ValueError:
        continue
    if score < 0 or score > 100:
        print("成绩无效")
    elif 90 <= score <= 100:
        print("A（优秀）")
    elif 80 <= score <= 89:
        print("B（良好）")
    elif 70 <= score <= 79:
        print("C（中等）")
    elif 60 <= score <= 69:
        print("D（及格）")
    else:
        print("E（不及格）")