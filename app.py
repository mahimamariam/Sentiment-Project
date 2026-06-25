from flask import Flask, render_template, request, redirect, url_for, Response
import joblib
import sqlite3
import csv
from io import StringIO
from datetime import datetime

app = Flask(__name__)

model = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

DB_NAME = "sentiment_history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            analysis TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM history").fetchone()[0]

    positive = cursor.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Positive'"
    ).fetchone()[0]

    negative = cursor.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Negative'"
    ).fetchone()[0]

    neutral = cursor.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Neutral'"
    ).fetchone()[0]

    recent = cursor.execute("""
        SELECT * FROM history
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    def percent(value):
        return round((value / total) * 100, 2) if total > 0 else 0

    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_percent": percent(positive),
        "negative_percent": percent(negative),
        "neutral_percent": percent(neutral),
        "recent": recent,
    }


def generate_ai_explanation(text, prediction, confidence):
    if confidence < 45:
        return (
            "The AI is not highly confident about this prediction. "
            "The sentence contains mostly factual or informational language "
            "without strong emotional words, so it is classified as Neutral.",
            "neutral",
        )

    positive_words = [
        "love", "excellent", "amazing", "happy", "good", "great",
        "helpful", "perfect", "satisfied", "recommend", "friendly",
        "beautiful", "awesome", "best", "enjoyed", "clean",
        "comfortable", "fast", "quality", "support", "resolved"
    ]

    negative_words = [
        "bad", "worst", "hate", "terrible", "poor", "disappointed",
        "slow", "crash", "crashes", "problem", "frustrating",
        "failed", "confusing", "broken", "useless", "angry",
        "unstable", "refund", "issue", "waste", "not received"
    ]

    neutral_words = [
        "meeting", "scheduled", "uploaded", "report", "document",
        "monday", "weather", "pages", "delivered", "class",
        "starts", "contains", "tomorrow", "today", "information"
    ]

    text_lower = text.lower()

    matched_positive = [word for word in positive_words if word in text_lower]
    matched_negative = [word for word in negative_words if word in text_lower]
    matched_neutral = [word for word in neutral_words if word in text_lower]

    if prediction == "Positive":
        color = "positive"

        if matched_positive:
            analysis = (
                "The AI predicted Positive sentiment because the text contains positive words such as "
                + ", ".join(matched_positive[:3])
                + ". These words usually express satisfaction, appreciation, comfort, or approval."
            )
        else:
            analysis = (
                "The AI predicted Positive sentiment based on the overall sentence pattern. "
                "The feedback appears to express a favorable or appreciative opinion."
            )

    elif prediction == "Negative":
        color = "negative"

        if matched_negative:
            analysis = (
                "The AI predicted Negative sentiment because the text contains negative words such as "
                + ", ".join(matched_negative[:3])
                + ". These words usually express dissatisfaction, complaint, criticism, or frustration."
            )
        else:
            analysis = (
                "The AI predicted Negative sentiment based on the overall sentence pattern. "
                "The feedback appears to express dissatisfaction or criticism."
            )

    else:
        color = "neutral"

        if matched_neutral:
            analysis = (
                "The AI predicted Neutral sentiment because the text contains informational words such as "
                + ", ".join(matched_neutral[:3])
                + ". The sentence appears factual rather than emotional."
            )
        else:
            analysis = (
                "The AI predicted Neutral sentiment because the text does not strongly express positive or negative emotion."
            )

    return analysis, color


@app.route("/")
def home():
    stats = get_dashboard_stats()
    return render_template("index.html", stats=stats)


@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["text"].strip()

    if text == "":
        return redirect(url_for("home"))

    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0].capitalize()

    probabilities = model.predict_proba(vector)[0]
    confidence = round(max(probabilities) * 100, 2)

    if confidence < 45:
        prediction = "Neutral"

    total_words = len(text.split())
    characters = len(text)

    analysis, color = generate_ai_explanation(text, prediction, confidence)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history (text, prediction, confidence, analysis, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (text, prediction, confidence, analysis, created_at),
    )

    conn.commit()
    conn.close()

    stats = get_dashboard_stats()

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        analysis=analysis,
        color=color,
        text=text,
        total_words=total_words,
        characters=characters,
        stats=stats,
    )


@app.route("/history")
def history():
    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        records = cursor.execute(
            """
            SELECT * FROM history
            WHERE text LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%",),
        ).fetchall()
    else:
        records = cursor.execute("""
            SELECT * FROM history
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template("history.html", records=records, search=search)


@app.route("/analytics")
def analytics():
    stats = get_dashboard_stats()
    return render_template("analytics.html", stats=stats)


@app.route("/delete/<int:id>")
def delete_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("history"))


@app.route("/clear-history")
def clear_history():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")

    conn.commit()
    conn.close()

    return redirect(url_for("history"))


@app.route("/export-csv")
def export_csv():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM history ORDER BY id DESC").fetchall()
    conn.close()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        ["ID", "Text", "Prediction", "Confidence", "Analysis", "Created At"]
    )

    for row in records:
        writer.writerow(
            [
                row["id"],
                row["text"],
                row["prediction"],
                row["confidence"],
                row["analysis"],
                row["created_at"],
            ]
        )

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = (
        "attachment; filename=sentiment_history.csv"
    )

    return response


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)