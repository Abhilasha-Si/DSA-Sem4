package org.example;
class StackArray
{
    int max = 5;
    int stack[] = new int[max];
    int top = -1;

    void push(int value)
    {
        if(top == max - 1)
        {
            System.out.println("Stack Overflow");
        }
        else
        {
            top++;
            stack[top] = value;
            System.out.println(value + " pushed into stack");
        }
    }

    void pop()
    {
        if(top == -1)
        {
            System.out.println("Stack Underflow");
        }
        else
        {
            System.out.println(stack[top] + " popped from stack");
            top--;
        }
    }

    void display()
    {
        if(top == -1)
        {
            System.out.println("Stack is empty");
        }
        else
        {
            for(int i = top; i >= 0; i--)
            {
                System.out.println(stack[i]);
            }
        }
    }

    public static void main(String args[])
    {
        StackArray s = new StackArray();

        s.push(10);
        s.push(20);
        s.push(30);

        s.display();

        s.pop();

        s.display();
    }
}





