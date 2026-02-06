import java.util.Scanner;

public class ReverseString {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String input = sc.nextLine();

        StringBuilder sb = new StringBuilder();
        sb.append(input);
        sb.reverse();

        String result = sb.toString();
        System.out.println(result);
    }
}
