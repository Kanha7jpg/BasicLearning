def calculator():
    print("Simple Python Calculator")
    print("Operations: +, -, *, /")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("Enter expression (e.g. 3 + 5): ").strip()
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break

            # Parse input
            for op in ['+', '-', '*', '/']:
                if op in user_input:
                    parts = user_input.split(op)
                    if len(parts) == 2:
                        a, b = float(parts[0].strip()), float(parts[1].strip())
                        if op == '+':
                            print(f"Result: {a + b}\n")
                        elif op == '-':
                            print(f"Result: {a - b}\n")
                        elif op == '*':
                            print(f"Result: {a * b}\n")
                        elif op == '/':
                            if b == 0:
                                print("Error: Division by zero!\n")
                            else:
                                print(f"Result: {a / b}\n")
                        break
            else:
                print("Invalid expression. Try again.\n")

        except ValueError:
            print("Invalid numbers. Try again.\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    calculator()