import random
random_number = random.randint(1, 100)
count = 0

while count < 7:
    a = int(input("请输入您猜测的数字"))
    count += 1
    if a < random_number:
        print("您输入的数字太小了")
    elif a > random_number:
        print("您输入的数字太大了")
    else:
        print(f"恭喜您,您只用了{count}次就猜对了")
        break
else:
    print("很遗憾您七次没有猜对")
print("随机生成的数字是: ",random_number)