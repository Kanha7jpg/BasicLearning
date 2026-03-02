import java.util.Scanner;

public class RomanConverter {

    // Roman to Integer conversion
    public static int romanToInt(String s) {
        if (s == null || s.isEmpty()) return -1;

        s = s.toUpperCase().trim();
        
        int[] values = new int[256]; // ASCII-based lookup
        values['I'] = 1;
        values['V'] = 5;
        values['X'] = 10;
        values['L'] = 50;
        values['C'] = 100;
        values['D'] = 500;
        values['M'] = 1000;

        int result = 0;
        int prevValue = 0;

        for (int i = s.length() - 1; i >= 0; i--) {
            char c = s.charAt(i);
            if (values[c] == 0) return -1; // invalid character

            int currValue = values[c];

            if (currValue < prevValue) {
                result -= currValue;
            } else {
                result += currValue;
            }
            prevValue = currValue;
        }

        // Basic validation: result should be positive and reasonable
        if (result < 1 || result > 3999) return -1;

        return result;
    }

    // Integer to Roman conversion
    public static String intToRoman(int num) {
        if (num < 1 || num > 3999) {
            return "Number out of range (1–3999)";
        }

        // Ordered from largest to smallest
        String[] romanSymbols = {
            "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"
        };
        int[] values = {
            1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
        };

        StringBuilder roman = new StringBuilder();

        for (int i = 0; i < values.length; i++) {
            while (num >= values[i]) {
                roman.append(romanSymbols[i]);
                num -= values[i];
            }
        }

        return roman.toString();
    }

    // Simple validator for Roman numeral format (optional strict check)
    public static boolean isValidRoman(String s) {
        if (s == null || s.isEmpty()) return false;
        return s.matches("^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== Roman <-> Integer Converter ===\n");

        while (true) {
            System.out.println("Choose conversion:");
            System.out.println("  1) Roman numeral → Number");
            System.out.println("  2) Number → Roman numeral");
            System.out.println("  0) Exit");
            System.out.print("\nEnter choice (0-2): ");

            String choiceStr = scanner.nextLine().trim();

            if (choiceStr.equals("0")) {
                System.out.println("Goodbye!");
                break;
            }

            if (!choiceStr.equals("1") && !choiceStr.equals("2")) {
                System.out.println("Invalid choice. Please enter 0, 1, or 2.\n");
                continue;
            }

            if (choiceStr.equals("1")) {
                // Roman → Int
                System.out.print("Enter Roman numeral (e.g. MCMXCIV): ");
                String roman = scanner.nextLine().trim().toUpperCase();

                if (!isValidRoman(roman)) {
                    System.out.println("→ Warning: Looks like an invalid Roman numeral format");
                }

                int number = romanToInt(roman);

                if (number == -1) {
                    System.out.println("→ Invalid Roman numeral or out of range (1-3999)\n");
                } else {
                    System.out.println("→ " + roman + " = " + number + "\n");
                }
            } 
            else {
                // Int → Roman
                System.out.print("Enter number (1–3999): ");
                String input = scanner.nextLine().trim();

                try {
                    int num = Integer.parseInt(input);
                    String roman = intToRoman(num);
                    System.out.println("→ " + num + " = " + roman + "\n");
                } catch (NumberFormatException e) {
                    System.out.println("→ Please enter a valid integer.\n");
                }
            }
        }

        scanner.close();
    }
}