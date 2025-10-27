"""
TantraQuest Flask Prototype (with Admin Upload Panel)
----------------------------------------------------
1. Run: python app.py
2. Visit:
   - Player: http://127.0.0.1:5000
   - Admin:  http://127.0.0.1:5000/admin
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import random

app = Flask(__name__)
app.secret_key = "tantraquest_secret_key"

DATA_FILE = "tantraquest_blocks.json"

# -----------------------------
# Load or Initialize TantraQuest Data
# -----------------------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        BLOCKS = json.load(f)
else:
    BLOCKS = []

random.shuffle(BLOCKS)


# -----------------------------
# Helper Functions
# -----------------------------
def save_blocks():
    """Save current data to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(BLOCKS, f, ensure_ascii=False, indent=4)


def get_block(index):
    if 0 <= index < len(BLOCKS):
        return BLOCKS[index]
    return None


# -----------------------------
# Player Routes
# -----------------------------
@app.route("/")
def index():
    session["score"] = 0
    session["current"] = 0
    return redirect(url_for("play"))


@app.route("/play", methods=["GET", "POST"])
def play():
    current = session.get("current", 0)
    score = session.get("score", 0)

    block = get_block(current)
    if not block:
        return redirect(url_for("result"))

    feedback = None
    correct = None

    if request.method == "POST":
        selected = request.form.get("tantrayukti")
        correct_tantrayukti = next(
            (t["name"] for t in block["tantrayuktis"] if t["is_correct"]), None
        )

        if selected == correct_tantrayukti:
            feedback = "? Correct! " + block["feedback"]
            score += block["points"]
            correct = True
        else:
            feedback = f"? Incorrect. The correct Tantrayukti is: {correct_tantrayukti}."
            correct = False

        # Update session
        session["score"] = score
        session["current"] = current + 1

        return render_template(
            "play.html",
            block=block,
            feedback=feedback,
            correct=correct,
            score=score,
            next_url=url_for("play"),
            last=(current + 1 == len(BLOCKS)),
        )

    return render_template(
        "play.html",
        block=block,
        feedback=feedback,
        score=score,
        last=(current + 1 == len(BLOCKS)),
    )


@app.route("/result")
def result():
    score = session.get("score", 0)
    return render_template("result.html", score=score, total=len(BLOCKS))


# -----------------------------
# Admin Upload Panel
# -----------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        concept = request.form["concept"]
        pratijna = request.form["pratijna"]
        points = int(request.form.get("points", 10))
        feedback = request.form["feedback"]

        # Tantrayuktis (up to 4)
        tantrayuktis = []
        for i in range(1, 5):
            name = request.form.get(f"t{i}_name")
            definition = request.form.get(f"t{i}_def")
            is_correct = request.form.get("correct") == f"t{i}"
            if name and definition:
                tantrayuktis.append(
                    {"name": name, "definition": definition, "is_correct": is_correct}
                )

        # Validate
        if not concept or not pratijna or len(tantrayuktis) < 2:
            flash("Please fill all required fields and at least 2 Tantrayuktis.", "error")
            return redirect(url_for("admin"))

        new_block = {
            "id": len(BLOCKS) + 1,
            "concept": concept,
            "pratijna": pratijna,
            "tantrayuktis": tantrayuktis,
            "points": points,
            "feedback": feedback,
        }

        BLOCKS.append(new_block)
        save_blocks()
        flash(f"? Block added successfully: {concept}", "success")
        return redirect(url_for("admin"))

    return render_template("admin.html", blocks=BLOCKS)


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
