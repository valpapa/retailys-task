from __future__ import annotations
import sys
from flask import Flask, Response, request
from functions import number_of_products, name_of_products, name_of_parts

app = Flask(__name__)

@app.route("/1")
def task1():
    n = number_of_products()
    return Response(f"{n}\n", mimetype="text/plain; charset=utf-8")

@app.route("/2")
def task2():
    limit = request.args.get("limit", default=100, type=int)
    text = name_of_products(limit=limit)
    return Response(text, mimetype="text/plain; charset=utf-8")

@app.route("/3")
def task3():
    limit = request.args.get("limit", default=100, type=int)
    text = name_of_parts(limit=limit)
    return Response(text, mimetype="text/plain; charset=utf-8")

def cli_main():
    if len(sys.argv) < 2:
        print("Usage: python app.py {1|2|3} [limit]")
        sys.exit(1)
    sel = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    if sel == "1":
        print("Number of products is:", number_of_products())
    elif sel == "2":
        print(name_of_products(limit=limit), end="")
    elif sel == "3":
        print(name_of_parts(limit=limit), end="")
    else:
        print("Please press 1/2/3.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        cli_main()
