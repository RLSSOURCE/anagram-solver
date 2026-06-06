from flask import Flask, request

app = Flask(__name__)


def sort_word(word):
    return "".join(sorted(word.lower()))


def load_words():
    words = []
    with open("/usr/share/dict/words", "r") as file:
        for line in file:
            word = line.strip().lower()
            if word.isalpha():
                words.append(word)
    return words


word_list = load_words()


def find_anagrams(user_word):
    user_sorted = sort_word(user_word)
    matches = []

    for word in word_list:
        if sort_word(word) == user_sorted and word != user_word.lower():
            matches.append(word)

    return sorted(matches)


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    searched_word = ""

    if request.method == "POST":
        searched_word = request.form.get("word", "")
        results = find_anagrams(searched_word)

    return f"""
    <html>
    <head>
        <title>Anagram Solver</title>
    </head>
    <body style="font-family: Arial; max-width: 700px; margin: 50px auto;">
        <h1>🔤 Anagram Solver</h1>
        <p>Enter a word and find its anagrams.</p>

        <form method="POST">
            <input 
                type="text" 
                name="word" 
                placeholder="Example: listen"
                value="{searched_word}"
                style="padding: 10px; width: 70%; font-size: 16px;"
            >
            <button type="submit" style="padding: 10px; font-size: 16px;">
                Solve
            </button>
        </form>

        <h2>Results</h2>
        <p>Found {len(results)} anagrams.</p>
        <ul>
            {"".join(f"<li>{word}</li>" for word in results[:50])}
        </ul>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)