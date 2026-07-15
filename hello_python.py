print("欢迎使用计算器")
while True:
    num1 = float(input("请输入第一个数字: "))
    operator = input("请输入运算符: ")
    num2 = float(input("请输入第二个数字: "))
    if operator == "+":
        print(num1 + num2)
    elif operator == "-":
         print(num1 - num2)
    elif operator == "*":
        print(num1 * num2)
    elif operator == "/":
        if num2 == 0:
            print("除数不能为0")
        else:
            print(num1 / num2)
    else:
        print("暂不支持该运算")
    flag = input("是否继续计算: y/n")
    if flag != "y":
        break


