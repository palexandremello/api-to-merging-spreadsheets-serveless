from flask import Flask
from flask import request
import pandas as pd
from joblib import Parallel, delayed
import time

app = Flask(__name__)


app.config["UPLOAD_FOLDER"] = "uploads/"

app.config["ALLOWED_EXTENSIONS"] = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in app.config["ALLOWED_EXTENSIONS"]


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


def read_xlsx(spreadsheet):
    return pd.read_excel(spreadsheet)


@app.route("/spreadsheet", methods=["GET", "POST"])
def spreadsheet():
    if request.method == "POST":
        files = request.files.getlist("spreadsheet")
        start = time.time()
        for file in files:
            print(pd.read_excel(file.read()).shape)
        end = time.time()
        return {"body": f"{end - start}"}


@app.route("/spreadsheet_parallel", methods=["GET", "POST"])
def spreadsheet_parallel():
    if request.method == "POST":
        files = request.files.getlist("spreadsheet")
        start = time.time()
        df = Parallel(n_jobs=-1, verbose=10)(delayed(read_xlsx)(file.read()) for file in files)
        df = pd.concat(df, ignore_index=True)
        end = time.time()
        print(df)
        return {"body": f"{end - start} seconds"}
