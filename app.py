from flask import Flask, render_template, request, send_from_directory
from libgen_scraper import search_libgen, download_book
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query", None)
    if query:
        results = search_libgen(query)
        return render_template("results.html", results=results)

    return render_template("index.html")

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(os.path.join(os.getcwd()), filename)

@app.route("/download_book/<int:book_index>", methods=["GET"])
def download_book_route(book_index):
    query = request.args.get("query", "")
    results = search_libgen(query)
    book_row = results[book_index]
    download_book(book_row)
    return "Book downloaded successfully"

if __name__ == "__main__":
    app.run(debug=True)
