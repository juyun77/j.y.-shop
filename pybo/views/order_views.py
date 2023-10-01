from flask import Flask, request, render_template, redirect, url_for
from flask import Blueprint
from ..models import Question,CartItem,db

bp = Blueprint('order', __name__, url_prefix='/')

# 장바구니 페이지
@bp.route('/cart')
def cart():
    cart_items = CartItem.query.all()
    total_price = sum(cart_item.price * cart_item.quantity for cart_item in cart_items)
    
    return render_template('question/cart.html', cart_items=cart_items, total_price=total_price)
    

# 수량 업데이트
@bp.route('/update_quantity/<int:cart_item_id>', methods=['POST'])
def update_quantity(cart_item_id):
    cart_item = CartItem.query.get(cart_item_id)
    new_quantity = int(request.form.get('quantity'))

    if new_quantity >= 1:
        cart_item.quantity = new_quantity
        db.session.commit()

    return redirect('/cart')

# 장바구니에서 항목 삭제
@bp.route('/remove_item/<int:cart_item_id>', methods=['POST'])
def remove_item(cart_item_id):
    cart_item = CartItem.query.get(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    return redirect('/cart')
