import os 

from flask import Blueprint, render_template, request, url_for
from helloflask.models import Question
from helloflask.forms import QuestionForm, AnswerForm

from datetime import datetime 
from werkzeug.utils import redirect, secure_filename
from .. import db

from PIL import Image

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    # image_ori = Image.open("/Users/macbookpro/uncoding/pyflask/helloflask/static/upload_files/" + question.image_file)
    # resize_img = image_ori.resize((500, 500))
    # resize_img.save('/Users/macbookpro/uncoding/pyflask/helloflask/static/upload_files/resizeimg.jpeg')
    # print(question)
    resize_image( question.image_file, "resizeimg.jpeg")
    return render_template('question/question_detail.html', question=question, form=form, img="resizeimg.jpeg")

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()    
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['file1']
        # os.makedirs(image_path, exist_ok=True)
        save_to = f'/Users/macbookpro/uncoding/pyflask/helloflask/static/upload_files/{secure_filename(file.filename)}'
        print(save_to, os.path.abspath(save_to))
        file.save(os.path.join(save_to))
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), image_file=secure_filename(file.filename))
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

def resize_image(filename, ref_filename):
    base_width = 500
    img = Image.open("/Users/macbookpro/uncoding/pyflask/helloflask/static/upload_files/" + filename)
    wpercent = (base_width/float(img.size[0]))
    hsize = int((float(img.size[1] * float(wpercent))))
    img = img.resize((base_width, hsize), Image.ANTIALIAS)
    img.save("/Users/macbookpro/uncoding/pyflask/helloflask/static/upload_files/" + ref_filename)
