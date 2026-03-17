package org.example;
import java.util.Stack;
public class ValidBrackets {
    public static boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            }
            else {
                if (stack.isEmpty()) {
                    return false;
                }
                char top = stack.pop();
                if (c == ')' && top != '(')
                    return false;
                if (c == '}' && top != '{')
                    return false;
                if (c == ']' && top != '[')
                    return false;
            }
        }
        return stack.isEmpty();
    }
    public static void main(String[] args) {
        String str = "[({})]";
        if (isValid(str))
            System.out.println("Valid Brackets");
        else
            System.out.println("Invalid Brackets");
    }
}