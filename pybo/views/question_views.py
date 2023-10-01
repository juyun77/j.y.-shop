from flask import Blueprint, render_template,request, url_for ,g, flash
from pybo.forms import QuestionForm
from werkzeug.utils import redirect
from pybo.models import Question
from datetime import datetime
from .. import db
from ..models import Question,CartItem
from ..forms import QuestionForm

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    cart_items = CartItem.query.all()
    return render_template('question/question_list.html', question_list=question_list, cart_items=cart_items)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question) 

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method =='POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, price=form.price.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)



@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))


@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    question_id = int(request.form.get('question_id'))
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity'))
   

    # 선택한 음료 정보를 가져옵니다. 이 예시에서는 Question 모델을 사용합니다.
    question = Question.query.get(question_id)

    if question and quantity >= 1:
        # 장바구니에 음료를 추가합니다. 이 예시에서는 CartItem 모델을 사용합니다.
        cart_item = CartItem(question_id=question_id, price=price, quantity=quantity,question=question)
        db.session.add(cart_item)
        db.session.commit()
        
    
      

    return redirect('/order/cart')