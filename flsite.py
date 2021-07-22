from flask import Flask, render_template

app = Flask(__name__)

menu = ["Install", "First app", "Jiga"]
amenu = ["123", "456", "789"]
fmenu = ["О компании", "Контакты", "ББ"]

@app.route("/")
def index():
    return render_template('index.html', title="Про фласку", menu=menu, fmenu=fmenu)


@app.route("/about")
def about():
    return render_template('about.html', about="Свистит...", amenu=amenu, fmenu=fmenu)


if __name__ == "__main__":
    app.run(debug=True)
