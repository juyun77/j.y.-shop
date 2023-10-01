from flask import Flask, request, render_template, redirect, url_for,flash
from flask import Blueprint
from ..models import Question,CartItem,db,Order, OrderedItem
from datetime import datetime

bp = Blueprint('order', __name__, url_prefix='/order')



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

    return redirect('/order/cart')

# 장바구니에서 항목 삭제
@bp.route('/remove_item/<int:cart_item_id>', methods=['POST'])
def remove_item(cart_item_id):
    cart_item = CartItem.query.get(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
   
    return redirect('/order/cart')


@bp.route('/create_order', methods=['POST'])
def create_order():
    # 새로운 주문 생성
    new_order = Order(create_date=datetime.now(), total_price=0, status="대기 중")
    db.session.add(new_order)
    db.session.commit()

    # 장바구니에서 선택된 음료를 주문 목록에 추가
    cart_items = CartItem.query.all()  # 장바구니에 담긴 음료 조회
    for cart_item in cart_items:
        ordered_item = OrderedItem(
            order=new_order,
            question=cart_item.question,
            price=cart_item.price,
            quantity=cart_item.quantity
        )
        new_order.total_price += ordered_item.price * ordered_item.quantity
        db.session.add(ordered_item)
    
    # 장바구니 비우기
    CartItem.query.delete()
    db.session.commit()

    flash('주문이 생성되었습니다.', 'success')
    return redirect(url_for('order.order_list'))

@bp.route('/order_list')
def order_list():
    # 주문 목록 조회
    orders = Order.query.all()
   
    return render_template('question/order_list.html', orders=orders)
