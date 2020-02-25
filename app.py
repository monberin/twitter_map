from flask import Flask, render_template, request, redirect, url_for
import friends
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    print("INDEX")
    if request.method == "GET":
        print("GET")
        return render_template("index.html")

    if request.method == "POST":
        print("POST")
        try:
            if request.form['contents'] != '':
                friends.main(request.form['contents'])
                return redirect(url_for('map'))
            else:
                return redirect(url_for('fail'))
        except:
            return redirect(url_for('fail'))
    else:
      return redirect(url_for('fail'))


@app.route("/map", methods=["GET"])
def map():
    return render_template("map.html")

@app.route("/fail", methods=["GET"])
def fail():
    return render_template("fail.html")

if __name__ == "__main__":
    app.run(debug=True)
