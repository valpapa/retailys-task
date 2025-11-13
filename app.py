from __future__ import annotations
import sys
from flask import Flask, Response
from functions import download_zip, number_of_products, name_of_products, name_of_parts

app = Flask(__name__)

ROOT = None

def get_root():
    global ROOT
    if ROOT is None:
        ROOT = download_zip()   # stáhne a naparsuje jen jednou
    return ROOT

#root = download_zip()

@app.route("/1")
def task1():
    root = get_root()
    return str(number_of_products(root)) + "\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.route("/2")
def task2():
    root = get_root()
    return (name_of_products(root))

@app.route("/3")
def task3():
    root = get_root()
    return (name_of_parts(root))


def cli_main():
    root = get_root()
    if len(sys.argv) < 2:
        print("Usage: python app.py {1|2|3}")
        sys.exit(1)
    sel = sys.argv[1]
    if sel == "1":
        print('Number of products is: ',number_of_products(root))
    elif sel == "2":
        print(name_of_products(root))
    elif sel == "3":
        print(name_of_parts(root))
    else:
        print("Please press 1/2/3.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        cli_main()
