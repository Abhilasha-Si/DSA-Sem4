
import java.util.Stack;

class SortStack {

    public static void sort(Stack<Integer> stack) {
        if (!stack.isEmpty()) {
            int top = stack.pop();
            sort(stack);
            insertSorted(stack, top);
        }
    }

    private static void insertSorted(Stack<Integer> stack, int value) {
        if (stack.isEmpty() || stack.peek() <= value) {
            stack.push(value);
            return;
        }

        int top = stack.pop();
        insertSorted(stack, value);
        stack.push(top);
    }
}