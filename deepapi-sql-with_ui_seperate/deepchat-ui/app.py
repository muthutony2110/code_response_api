from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def chat_ui():
    return render_template("chat.html")  # Your UI file

if __name__ == "__main__":
    app.run(port=8600)
