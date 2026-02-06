import java.util.Arrays;

public class MissingPositive {
    public static int findMissing(int[] arr) {
        boolean[] present = new boolean[arr.length + 1];

        for (int num : arr) {
            if (num > 0 && num <= arr.length)
                present[num] = true;
        }

        for (int i = 1; i <= arr.length; i++) {
            if (!present[i])
                return i;
        }
        return arr.length + 1;
    }

    public static void main(String[] args) {
        int[] arr = {3, 4, -1, 1};
        System.out.println(findMissing(arr));
    }
}

