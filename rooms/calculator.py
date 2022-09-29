playing = True

# add your code here!

while playing:
    # calculator = operation
    a = int(input("Choose a number:\n"))
    b = int(input("Choose another one:\n"))
    operation = input(
        "Choose an operation:\n    Options are: + , - , * or /.\n    Write 'exit' to finish.\n"
    )

    if operation == "+":
        print(a + b)
        # return stop == False
    elif operation == "-":
        print(a - b)
    elif operation == "*":
        print(a * b)
    elif operation == "/":
        print(a / b)
    elif operation == "exit":
        break
