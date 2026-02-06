public class PeakElement {
    public static int findPeak(int[] arr) {
        int left = 0, right = arr.length - 1;

        while (left <= right) {
            int mid = (left + right) / 2;

            boolean leftOK = (mid == 0 || arr[mid] > arr[mid - 1]);
            boolean rightOK = (mid == arr.length - 1 || arr[mid] > arr[mid + 1]);

            if (leftOK && rightOK)
                return arr[mid];

            if (mid > 0 && arr[mid] < arr[mid - 1])
                right = mid - 1;
            else
                left = mid + 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] arr = {1, 3, 20, 4, 1};
        System.out.println(findPeak(arr));
    }
}

