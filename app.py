"""Roll your own auth application"""

from flask import Flask, request, redirect, render_template, url_for, flash, json, jsonify, session
from models import db, connect_db, User
from form import RegUserForm, LoginForm
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError

###############################################################
#                     SET ENV VARS                            #
###############################################################
from shhh import dbconstr, victoriasecret
###############################################################
#                 ^^^ SET ENV VARS ^^^                        #
###############################################################

app = Flask(__name__)

###############################################################
#                     MAKE YOUR CON TO DB                     #
###############################################################
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{dbconstr}@localhost:5432/auth"
###############################################################
#            ^^ You may need to make a database ^^     ^^     #
###############################################################


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = f"{victoriasecret}"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)


# db.session.rollback()
# db.drop_all()
# db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def home():
    return redirect("/register")


@app.route('/user/<string:username>')
def user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = (
        db.session.query(
            User.first_name,
            User.last_name,
            User.username,
            User.email
        )
        .filter(User.username == username)
        .first()
    )
    print(user)
    return render_template('user.html', user=user)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(f"/user/{session['username']}")

    form = RegUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        try:
            db.session.commit()
        except IntegrityError:
            if User.query.get(username):
                db.session.rollback()
                form.username.errors.append(
                    'Username already taken! #seatsTaken!')
                return render_template('register.html', form=form)

            elif User.query.get(username):
                db.session.rollback()
                form.email.errors.append('email already in use...')
                return render_template('register.html', form=form)

        session['username'] = user.username
        flash(
            f"User created... first={user.first_name}, last={user.last_name}, email={user.email} username={user.username}"
        )
        return redirect(url_for("user", username=session['username']))

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Show login form or hndle login """

    if "username" in session:
        return redirect(f"/user/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back {user.username}!")
            session['username'] = user.username
            return redirect(f"/user/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout route."""
    # [session.pop(key) for key in list(session.keys()) if key != '_flashes']
    session.pop("username")
    return redirect("/login")


if __name__ == "__main__":
    app.run()
