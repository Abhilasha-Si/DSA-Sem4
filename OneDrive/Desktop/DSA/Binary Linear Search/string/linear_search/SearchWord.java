public class SearchWord {
    public static String findSentence(String[] sentences, String word) {
        for (String s : sentences) {
            if (s.contains(word))
                return s;
        }
        return "Not Found";
    }

    public static void main(String[] args) {
        String[] sentences = {
            "Java is powerful",
            "I love programming",
            "Binary search is fast"
        };

        System.out.println(findSentence(sentences, "programming"));
    }
}

