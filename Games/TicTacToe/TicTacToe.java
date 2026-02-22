import java.util.Scanner;

public class TicTacToe {

    // The board is a 3x3 grid stored as a simple array
    static char[] board = {'1','2','3','4','5','6','7','8','9'};
    static char currentPlayer = 'X';

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int movesCount = 0;
        boolean gameOver = false;

        System.out.println("Welcome to Tic-Tac-Toe!");
        System.out.println("Players take turns. X goes first.");
        System.out.println("Enter the number of the cell where you want to place your mark.\n");

        while (!gameOver) {
            printBoard();
            System.out.print("Player " + currentPlayer + ", choose a cell (1-9): ");

            // Get player input
            int choice = -1;
            if (scanner.hasNextInt()) {
                choice = scanner.nextInt();
            } else {
                scanner.next(); // clear invalid input
            }

            // Validate input
            if (choice < 1 || choice > 9) {
                System.out.println("Invalid input! Please enter a number between 1 and 9.\n");
                continue;
            }

            int index = choice - 1;
            if (board[index] == 'X' || board[index] == 'O') {
                System.out.println("That cell is already taken! Try another.\n");
                continue;
            }

            // Place the mark
            board[index] = currentPlayer;
            movesCount++;

            // Check for a winner
            if (checkWinner()) {
                printBoard();
                System.out.println("🎉 Player " + currentPlayer + " wins! Congratulations!");
                gameOver = true;
            } else if (movesCount == 9) {
                printBoard();
                System.out.println("It's a draw! Well played by both!");
                gameOver = true;
            } else {
                // Switch player
                currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            }
        }

        scanner.close();
    }

    // Print the current board state
    static void printBoard() {
        System.out.println();
        System.out.println(" " + board[0] + " | " + board[1] + " | " + board[2]);
        System.out.println("---+---+---");
        System.out.println(" " + board[3] + " | " + board[4] + " | " + board[5]);
        System.out.println("---+---+---");
        System.out.println(" " + board[6] + " | " + board[7] + " | " + board[8]);
        System.out.println();
    }

    // Check all winning combinations
    static boolean checkWinner() {
        int[][] winCombos = {
            {0, 1, 2}, // top row
            {3, 4, 5}, // middle row
            {6, 7, 8}, // bottom row
            {0, 3, 6}, // left column
            {1, 4, 7}, // middle column
            {2, 5, 8}, // right column
            {0, 4, 8}, // diagonal
            {2, 4, 6}  // diagonal
        };

        for (int[] combo : winCombos) {
            if (board[combo[0]] == currentPlayer &&
                board[combo[1]] == currentPlayer &&
                board[combo[2]] == currentPlayer) {
                return true;
            }
        }
        return false;
    }
}