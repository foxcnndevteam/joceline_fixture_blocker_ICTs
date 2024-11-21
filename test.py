for i in range(0, 10):
    print("count: " + str(i))
    with open("./test.txt", "r") as f1:
        with open("./test.txt", "w") as f2:
            f2.write(f1.read() + str(True))
