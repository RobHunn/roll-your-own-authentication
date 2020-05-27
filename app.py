"""Roll your own auth application"""

from flask import Flask, request, redirect, render_template, url_for, flash, json, jsonify
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

# db.session.rollback()
# db.drop_all()
# db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def home():
    form = RegUserForm()
    return render_template("home.html", form=form)


@app.route('/secret/<string:user>')
def secret_page(user):
    user = (
        db.session.query(
            User.first_name,
            User.last_name,
            User.username,
            User.email
        )
        .filter(User.username == user)
        .first()
    )
    return render_template('secret.html', user=user)


@app.route("/api/reg_user", methods=['POST'])
def reg_user():
    form = RegUserForm()
    if form.validate_on_submit():
        new_user = User(
            username=request.form['username'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            password=request.form['password'],
        )
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            flash(
                f"User created, first={new_user.first_name}, last={new_user.last_name}, email={new_user.email} username={new_user.username}"
            )
            print('********** redirecting now')
            return redirect(url_for("secret_page", user=new_user.username))
        else:
            db.session.rollback()
            print('errorrrrrr')
            return redirect(url_for('home'))

    else:
        print('form not vaildated')
        return render_template('home.html', form=form)


# if __name__ == "__main__":
#     app.run()
