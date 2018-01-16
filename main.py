from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:helloworld@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'topsecret'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(9999))

    def __init__(self, title, body):
        self.title = title
        self.body = body


def is_empty(string):
    if len(string) == 0:
        return True


@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_entry = Blog(blog_title, blog_body)

        if is_empty(blog_title) or is_empty(blog_body):
            flash('Your blog entry must have a title and a body!', 'error')
            return redirect('/newpost')
        
        else:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog')

    else:
        return render_template('newpost.html', title="Add a Blog Entry")


@app.route('/blog', methods=['POST', 'GET'])
def show_entries():
    
    entries = Blog.query.all()
    return render_template(
        'blog.html', 
        title="Build a Blog", 
        entries=entries
        )    


@app.route('/', methods=['POST', 'GET'])
def index():
    
    return redirect('/blog') 


if __name__ == '__main__':
    app.run()