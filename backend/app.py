from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/hello")
def hello():
    return jsonify({"message": "你好，来自后端的问候！"})

if __name__ == "__main__":
    app.run(port=5000)