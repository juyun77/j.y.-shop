from flask import Blueprint, render_template,request, url_for ,g, flash, request
from shop.forms import ProductForm
from werkzeug.utils import redirect
from datetime import datetime
from .. import db
from ..models import User,Product,CartItem
from ..forms import ProductForm

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/list/')
def _list():
    product_list = Product.query.order_by(Product.id)
    cart_items = CartItem.query.all()
    return render_template('product/product_list.html', product_list=product_list, cart_items=cart_items)


@bp.route('/detail/<int:product_id>/')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/product_detail.html', product=product)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = ProductForm()
    if request.method =='POST' and form.validate_on_submit():
        product = Product(image=form.subject.data, name=form.content.data, price=form.price.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('product/product_form.html', form=form)



@bp.route('/modify/<int:product_id>', methods=('GET', 'POST'))
def modify(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':  # POST 요청
        form = ProductForm()
        if form.validate_on_submit():
            form.populate_obj(product)
            db.session.commit()
            return redirect(url_for('product.detail', product_id=product_id))
    else:  # GET 요청
        form = ProductForm(obj=product)
    return render_template('product/product_form.html', form=form)

@bp.route('/delete/<int:product_id>')
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product._list'))


@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity'))

    # 선택한 음료 정보를 가져옵니다. 이 예시에서는 product 모델을 사용합니다.
    product = Product.query.get(product_id)

    if product and quantity >= 1:
        
        user_id = g.user.id if g.user else None
        # 이미 장바구니에 있는지 확인
        existing_cart_item = CartItem.query.filter_by(product_id=product_id, user_id=user_id).first()

        if existing_cart_item:
            # 이미 장바구니에 있는 경우, 수량만 업데이트
            existing_cart_item.quantity += quantity
        else:
            # 장바구니에 없는 경우, 새로운 항목 추가
            cart_item = CartItem(user_id=user_id, product_id=product_id, price=price, quantity=quantity, product=product)
            db.session.add(cart_item)

        db.session.commit()

    return redirect('/order/cart')

@bp.route('/search')
def search():
    # URL에서 검색어 파라미터를 가져옴
    search_term = request.args.get('search')
    
    # 검색어와 일치하는 상품을 필터링하여 가져옴 (예: Product 모델의 name 필드를 검색)
    product_list = Product.query.filter(Product.name.like(f"%{search_term}%")).all()
    
    # 검색 결과를 템플릿에 전달
    return render_template('product/product_list.html', product_list=product_list, search_term=search_term)