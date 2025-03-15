from flask import Flask, render_template, request
import re
import random
import string

app = Flask(__name__)


def generate_strong_password():
    length = 8
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(8))

def check_password_strength(password):
    suggestions = []

    # Regex-based password checks
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    is_repeated = bool(re.match(r"^(.)\1+$", password))  # Check for repeated characters

    # Check for common keyboard patterns
    weak_patterns = ["12345", "qwerty", "asdfgh", "zxcvbn", "abcdef"]
    if any(seq in password.lower() for seq in weak_patterns):
        return "Weak - Sequential Pattern ", "red", ["Avoid using easy-to-guess sequences."]

    if is_repeated:
        return "Weak - Repeated Characters ", "red", ["Avoid using the same character multiple times."]

    # Strength scoring
    strength = sum([has_upper, has_lower, has_digit, has_special])

    if strength == 4:
        return "Very Strong!", "green", []
    elif strength == 3:
        return "Strong ", "lightgreen", ["Try making your password longer."]
    elif strength == 2:
        return "Moderate ", "yellow", ["Add uppercase, numbers, and special characters."]
    else:
        return "Weak", "red", ["Use a mix of uppercase, lowercase, numbers, and special characters."]

@app.route("/", methods=["GET", "POST"])
def index():
    result, color, suggestions, password_input = None, None, None, ""

    if request.method == "POST":
        if "generate" in request.form:
            password_input = generate_strong_password()
        else:
            password_input = request.form.get("password", "")

        if password_input:
            result, color, suggestions_list = check_password_strength(password_input)
            suggestions = " ".join(suggestions_list) if suggestions_list else ""

    return render_template("index.html", result=result, color=color, suggestions=suggestions, password=password_input)

if __name__ == "__main__":
    app.run(debug=True)
