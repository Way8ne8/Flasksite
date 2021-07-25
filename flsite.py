import sqlite3, os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

fmenu = ["О компании", "Контакты", "ББ"]

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            res = dbase.addCont(request.form['username'], request.form['email'], request.form['message'])
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', menu=dbase.getMenu(), fmenu=fmenu)

@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "123" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] != "123" and request.form['psw'] != "123":
        flash('Ошибка авторизации', category='error')
    return render_template('login.html', title="Авторизация", menu=menu)

@app.route("/about")
def about():
    return render_template('about.html', menu=menu, fmenu=fmenu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    print(render_template('user.html', username=username, menu=menu, fmenu=fmenu))
    return render_template('user.html', username=username, menu=menu, fmenu=fmenu)

# @app.errorhandler(404)
# def pageNotFount(error):
#     return render_template('page404.html', title="Страница не найдена", menu=menu), 404

if __name__ == "__main__":
    app.run(debug=True)
