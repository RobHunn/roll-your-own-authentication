"""Roll your own auth application"""

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, User
from form import RegUserForm
from flask_debugtoolbar import DebugToolbarExtension

###############################################################
#                     SET ENV VARS                            #
###############################################################
from shhh import dbconstr, victoriasecret
###############################################################
#                 ^^^ SET ENV VARS ^^^                        #
###############################################################

WTF_CSRF_SECRET_KEY = 'a_random_string'

app = Flask(__name__)
app.config["SECRET_KEY"] = f"{victoriasecret}"

debug = DebugToolbarExtension(app)

###############################################################
#                     MAKE YOUR CON TO DB                     #
###############################################################
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{dbconstr}@localhost:5432/auth"
###############################################################
#            ^^ You may need to make a database ^^     ^^     #
###############################################################

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
connect_db(app)

db.session.rollback()
db.drop_all()
db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def home():
    form = RegUserForm()
    return render_template("home.html", form=form)


@app.route('/secret/<user>')
def secret_page(user):
    return render_template('secret.html', user=user)


@app.route("/api/reg_user", methods=['GET', 'POST'])
def reg_user():
    form = RegUserForm()
    if form.validate_on_submit():
        res = requests.get(url, params=params, headers={method: 'POST'})
        print(res)
        new_user = User(
            username=request.json['username'],
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            email=request.json['email'],
            password=request.json['password']
        )
        db.session.add(new_user)
        db.session.commit()
        flash(
            f"User created, first={new_user.first_name}, last={new_user.last_name}, email={new_user.email} username={new_user.username}"
        )
        return redirect(url_for("secret"), user=new_user)
    else:
        return render_template("home", form=form)


if __name__ == "__main__":
    app.run()
