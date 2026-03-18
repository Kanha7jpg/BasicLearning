
import java.util.Scanner;

public class NumberStats {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        final int count = 5;
        int sum = 0;
        int min = Integer.MAX_VALUE;
        int max = Integer.MIN_VALUE;

        System.out.println("Enter " + count + " integers:");

        for (int i = 1; i <= count; i++) {
            System.out.print("Number " + i + ": ");
            int value = scanner.nextInt();

            sum += value;
            if (value < min) {
                min = value;
            }
            if (value > max) {
                max = value;
            }
        }

        double average = (double) sum / count;

        System.out.println("\nResults:");
        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);
        System.out.println("Minimum: " + min);
        System.out.println("Maximum: " + max);

        scanner.close();
    }
}
