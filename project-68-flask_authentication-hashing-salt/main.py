from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)

# Login Manager flask-login:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



# CREATE TABLE IN DB


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 
 
with app.app_context():
    db.create_all()



@app.route('/')
def home():

    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method =='POST':
        name = request.form.get("name")
        email = request.form.get("email")
        passw= request.form.get("password")
        password = generate_password_hash(passw, method='pbkdf2:sha256', salt_length=8)
        print(name, email, password)
        with app.app_context():
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        return render_template("secrets.html",name=name)

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        print(request.form.get('email'))
        with app.app_context():
            user = db.session.execute(db.select(User).where(User.email == request.form.get("email"))).scalar()
            if user:
                # controllo hash della password
                if check_password_hash(user.password, request.form.get("password")):
                    login_user(user)
                    return redirect(url_for('secrets'))
                else:
                    flash("Wrong password")
            else:
                flash("Wrong email, try again")
    return render_template("login.html")



# TODO: add login_required decorator, ridirige al login perchè necessario per accedere la pagina secrets
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        directory="static",path="files/cheat_sheet.pdf"
    )



if __name__ == "__main__":
    app.run(debug=True)
