from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgsafafasfda5415afd5a'

menu = [{"name": "Главная", "url": "/"},
        {"name": "Login", "url": "login"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]
fmenu = ["О компании", "Контакты", "ББ"]

@app.route("/")
def index():
    session.clear()
    return render_template('index.html',  menu=menu, fmenu=fmenu)

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "123" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    else:
        flash('Ошибка авторизации', category='error')
    return render_template('login.html', title="Авторизация", menu=menu)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', menu=menu, fmenu=fmenu)

@app.route("/about")
def about():
    return render_template('about.html', menu=menu, fmenu=fmenu)

@app.route("/profile/<username>")
def profile(username):
    # if 'userLogged' not in session or session['userLogged'] != username:
    #     abort(401)
    return render_template('user.html', username=username, menu=menu, fmenu=fmenu)

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404

if __name__ == "__main__":
    app.run(debug=True)
