from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    important = db.Column(db.Boolean, default=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note_text = request.form['text']
        note_important = 'important' in request.form
        new_note = Note(text=note_text, important=note_important)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        notes = Note.query.all()
        return render_template('index.html', notes=notes)


@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Note).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
