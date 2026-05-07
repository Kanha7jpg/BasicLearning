import java.util.Scanner;

public class Calculator {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Simple Java Calculator");
        boolean running = true;

        while (running) {
            System.out.println();
            System.out.println("Choose an operation:");
            System.out.println("1) Add");
            System.out.println("2) Subtract");
            System.out.println("3) Multiply");
            System.out.println("4) Divide");
            System.out.println("5) Modulo");
            System.out.println("6) Power");
            System.out.println("7) Exit");
            System.out.print("Enter choice (1-7): ");

            String choice = sc.nextLine().trim();

            switch (choice) {
                case "1":
                    doBinaryOp(sc, "+");
                    break;
                case "2":
                    doBinaryOp(sc, "-");
                    break;
                case "3":
                    doBinaryOp(sc, "*");
                    break;
                case "4":
                    doBinaryOp(sc, "/");
                    break;
                case "5":
                    doBinaryOp(sc, "%");
                    break;
                case "6":
                    doBinaryOp(sc, "^");
                    break;
                case "7":
                    running = false;
                    break;
                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }

        System.out.println("Goodbye!");
        sc.close();
    }

    private static void doBinaryOp(Scanner sc, String op) {
        try {
            System.out.print("Enter first number: ");
            double a = Double.parseDouble(sc.nextLine().trim());
            System.out.print("Enter second number: ");
            double b = Double.parseDouble(sc.nextLine().trim());

            double result;
            switch (op) {
                case "+":
                    result = a + b;
                    break;
                case "-":
                    result = a - b;
                    break;
                case "*":
                    result = a * b;
                    break;
                case "/":
                    if (b == 0) {
                        System.out.println("Error: Division by zero.");
                        return;
                    }
                    result = a / b;
                    break;
                case "%":
                    if (b == 0) {
                        System.out.println("Error: Division by zero.");
                        return;
                    }
                    result = a % b;
                    break;
                case "^":
                    result = Math.pow(a, b);
                    break;
                default:
                    System.out.println("Unknown operation");
                    return;
            }

            if (result == (long) result) {
                System.out.printf("Result: %d\n", (long) result);
            } else {
                System.out.printf("Result: %s\n", trimTrailingZeros(result));
            }

        } catch (NumberFormatException e) {
            System.out.println("Invalid number entered. Please try again.");
        }
    }

    private static String trimTrailingZeros(double value) {
        String s = Double.toString(value);
        if (s.indexOf('.') < 0) return s;
        // Remove trailing zeros and optional trailing dot
        s = s.replaceAll("(?:\\.0+|(?<=\\.\\d*)0+)$", "");
        return s;
    }
}
