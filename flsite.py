from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = ["Install", "First app", "Jiga"]
amenu = ["123", "456", "789"]
fmenu = ["О компании", "Контакты", "ББ"]

@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', title="Про фласку", menu=menu, fmenu=fmenu)

@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', about="Свистит...", amenu=amenu, fmenu=fmenu)

@app.route("/profile/<username>")
def profile(username):
    # return f"Пользователь: {username}"
    return render_template('user.html', username=username)

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username="selfedu"))

if __name__ == "__main__":
    app.run(debug=True)
