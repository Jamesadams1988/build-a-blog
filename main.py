from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()

    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False

@app.route("/")
def index():
    return redirect("/blog")

@app.route("/blog")
def display_blog_entries():
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('post.html', title="Blog Entry", entry=entry)

    sort = request.args.get('sort')
    if (sort=="newest"):
        all_entries = Blog.query.order_by(Blog.created.desc()).all()
    else:
        all_entries = Blog.query.all()   
    return render_template('allposts.html', title="All Entries", all_entries=all_entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry = Blog(new_entry_title, new_entry_body)

        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()

            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
        else:
            flash("Please check your entry for errors. Both a title and a body are required.")
            return render_template('new.html',
                title="Create new blog entry",
                new_entry_title=new_entry_title,
                new_entry_body=new_entry_body)

    else: 
        return render_template('new.html', title="Create new blog entry")

if __name__ == '__main__':
    app.run()