from flask import render_template, request, redirect, url_for, session, Blueprint
from database import Note, User, db, Comment
from decorators import login_required
from toolbox import CommentForm, CardForm

note = Blueprint('note',__name__)


#论坛首页
@note.route('/notes/', methods = ['GET','POST'])
# @login_required
def notes():
    context = {
        'cards': Note.query.order_by('-create_time').all()
    }

    return render_template('note.html', **context)


#发布帖子
@note.route('/posts/', methods = ['GET', 'POST'])
@login_required
def card():

    if request.method == 'GET':

        card_from = CardForm()

        return render_template('cards.html', form=card_from)

    else:
        title = request.form.get('title')

        content = request.form.get('content')

        note = Note(title=title, content=content)

        user_id = session.get('user_id')

        user = User.query.filter(User.id == user_id).first()

        note.author = user

        db.session.add(note)

        db.session.commit()

        return redirect(url_for('note.notes'))


#详情
@note.route('/detail/<note_id>/')
@login_required
def detail(note_id):

    # comment_form = CommentForm()

    note_model = Note.query.filter(Note.id == note_id).first()

    return render_template('detail.html', note = note_model)


#评论
@note.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():

    content = request.form.get('comment_content')

    note_id = request.form.get('note_id')

    comment = Comment(content=content)

    user_id = session['user_id']

    user = User.query.filter(User.id == user_id).first()

    comment.author = user

    note = Note.query.filter(Note.id == note_id).first()

    comment.note = note

    db.session.add(comment)

    db.session.commit()

    return redirect(url_for('note.detail', note_id=note_id))

