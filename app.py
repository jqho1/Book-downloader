from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        results = search_libgen(query)
        return render_template("results.html", results=results)

    return render_template("index.html")

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(os.path.join(os.getcwd()), filename)

if __name__ == "__main__":
    app.run(debug=True)
