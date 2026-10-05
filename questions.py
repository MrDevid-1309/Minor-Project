"""Question bank: MCQs (aptitude + technical) and coding problems with 'logic' reference."""

MCQS = [
    # ---------------- Aptitude ----------------
    {"id": 1, "cat": "aptitude", "q": "A train 120 m long passes a pole in 6 seconds. Its speed is?",
     "options": ["20 m/s", "25 m/s", "30 m/s", "12 m/s"], "ans": 0},
    {"id": 2, "cat": "aptitude", "q": "Find the next number: 2, 6, 12, 20, 30, ?",
     "options": ["40", "42", "44", "38"], "ans": 1},
    {"id": 3, "cat": "aptitude", "q": "If 20% of a number is 45, the number is?",
     "options": ["180", "225", "200", "250"], "ans": 1},
    {"id": 4, "cat": "aptitude", "q": "A can do a work in 10 days, B in 15 days. Together they finish in?",
     "options": ["5 days", "6 days", "8 days", "12 days"], "ans": 1},
    # ---------------- Technical ----------------
    {"id": 5, "cat": "technical", "q": "Which data structure uses LIFO order?",
     "options": ["Queue", "Stack", "Array", "Linked List"], "ans": 1},
    {"id": 6, "cat": "technical", "q": "Time complexity of binary search on a sorted array?",
     "options": ["O(n)", "O(n log n)", "O(log n)", "O(1)"], "ans": 2},
    {"id": 7, "cat": "technical", "q": "Which SQL clause is used to filter grouped results?",
     "options": ["WHERE", "HAVING", "ORDER BY", "LIMIT"], "ans": 1},
    {"id": 8, "cat": "technical", "q": "Which OOP concept hides internal implementation details?",
     "options": ["Inheritance", "Polymorphism", "Encapsulation", "Overloading"], "ans": 2},
]

# Each coding problem has:
#  - function name the student must write (Python)
#  - tests: list of (args, expected)
#  - reference: model explanation of the logic (used for NLP similarity)
#  - concepts: groups of synonyms; the student's logic should cover these ideas
CODING = [
    {
        "id": 101,
        "title": "Palindrome Check",
        "statement": "Write a function is_palindrome(s) that returns True if the string s is a palindrome, "
                     "ignoring case and non-alphanumeric characters. Example: 'A man, a plan, a canal: Panama' -> True.",
        "func": "is_palindrome",
        "starter": "def is_palindrome(s):\n    # write your code here\n    pass\n",
        "tests": [(["racecar"], True), (["Hello"], False),
                  (["A man, a plan, a canal: Panama"], True), ([""], True), (["ab"], False)],
        "reference": "First convert the string to lowercase and remove every character that is not a letter or digit. "
                     "Then compare the cleaned string with its reverse. If both are equal it is a palindrome. "
                     "Alternatively use two pointers, one at the start and one at the end, moving towards the center "
                     "and comparing characters in a loop. Time complexity is O(n).",
        "concepts": [
            ["lowercase", "lower case", "case insensitive", "ignore case", "lower()"],
            ["alphanumeric", "non-alphanumeric", "remove", "clean", "filter", "special character", "isalnum"],
            ["reverse", "reversed", "backward", "[::-1]", "two pointer", "two pointers", "start and end"],
            ["compare", "equal", "match", "same"],
            ["o(n)", "linear", "time complexity", "complexity"],
        ],
    },
    {
        "id": 102,
        "title": "Second Largest Number",
        "statement": "Write a function second_largest(nums) that returns the second largest DISTINCT number in a list. "
                     "Return None if it does not exist. Example: [4, 1, 7, 7, 3] -> 4.",
        "func": "second_largest",
        "starter": "def second_largest(nums):\n    # write your code here\n    pass\n",
        "tests": [([[4, 1, 7, 7, 3]], 4), ([[5]], None), ([[2, 2, 2]], None),
                  ([[10, 9, 8]], 9), ([[-1, -5, -3]], -3)],
        "reference": "Remove duplicate values using a set so only distinct numbers remain. If fewer than two distinct "
                     "numbers exist return None. Otherwise sort the numbers in descending order and pick the second element, "
                     "or traverse the list once while tracking the largest and second largest values and updating them "
                     "with comparisons. The single pass approach has time complexity O(n).",
        "concepts": [
            ["duplicate", "distinct", "unique", "set("],
            ["none", "less than two", "fewer than two", "edge case", "empty", "not exist"],
            ["sort", "sorted", "descending", "traverse", "iterate", "loop", "single pass", "one pass"],
            ["largest", "maximum", "max", "second"],
            ["compare", "update", "track", "variable"],
            ["o(n)", "linear", "time complexity", "complexity"],
        ],
    },
]
