from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # Query the database for all the posts. Convert the data to a python list.
    posts = []
    all_post = db.session.query(BlogPost)
    for post in all_post.all():
        print('hello')
        posts.append(post)
    return render_template("index.html", all_posts=posts)

#  Add a route so that you can click on individual posts.
@app.route('/<post_id>/post')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.query(BlogPost).where(BlogPost.id == post_id).scalar()
    print(requested_post)
    print(post_id)
    return render_template("post.html", post=requested_post)


# app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)
class PostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
# add_new_post() to create a new blog post
@app.route('/new_post', methods=['GET', 'POST'])
def add_new_post():
    post= PostForm()
    if post.validate_on_submit():
        with app.app_context():
            new_post=  BlogPost(
                title=post.title.data,
                subtitle=post.subtitle.data,
                date=date.today().strftime("%B %d, %Y"),
                body=post.body.data,
                author=post.author.data,
                img_url=post.img_url.data
                )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('get_all_posts'))

    return render_template("make-post.html",post=post,el=1)


# edit_post() to change an existing blog post
@app.route('/edit_post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post1 = db.session.execute(db.select(BlogPost).where(BlogPost.id == id)).scalar()
    print(post1)
    print(id)
    edit_form = PostForm(
        title=post1.title,
        subtitle=post1.subtitle,
        author=post1.author,
        img_url=post1.img_url,
        body=post1.body,
    )

    if edit_form.validate_on_submit():
        with app.app_context():
            edit_post = db.session.query(BlogPost).where(BlogPost.id == id).scalar()
            edit_post.title = edit_form.title.data
            edit_post.subtitle = edit_form.subtitle.data
            edit_post.body = edit_form.body.data
            edit_post.author = edit_form.author.data
            edit_post.img_url = edit_form.img_url.data
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    return  render_template("make-post.html", post=edit_form)

# delete_post() to remove a blog post from the database
@app.route('/delete_post/<id>')
def delete_post(id):
    with app.app_context():
        delete_post = db.session.query(BlogPost).where(BlogPost.id == id).scalar()
        db.session.delete(delete_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
