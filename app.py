from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import sqlite3
import torch
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production

# Load the Ollama fine-tuned model
model_path = "/Users/sony/Desktop/vscode/project_code/models/ollama_finetuned"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Hash password for storing securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("chatbot"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

@app.route("/chatbot")
def chatbot():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 403

    user_input = request.json.get("input", "")
    user_id = session["user_id"]

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            output = model.generate(inputs["input_ids"], max_length=150)
            response = tokenizer.decode(output[0], skip_special_tokens=True)

        conn = get_db_connection()
        conn.execute("INSERT INTO interactions (user_id, user_input, bot_response) VALUES (?, ?, ?)", (user_id, user_input, response))
        conn.commit()
        conn.close()

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
