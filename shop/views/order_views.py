from flask import Flask, request, render_template, redirect, url_for,flash,g
from flask import Blueprint
from ..models import CartItem,db,Order, OrderedItem
from datetime import datetime

bp = Blueprint('order', __name__, url_prefix='/order')


# 장바구니 페이지
@bp.route('/cart')
def cart():
    user_id = g.user.id if g.user else None
    cart_items = CartItem.query.all()
    total_price = sum(cart_item.price * cart_item.quantity for cart_item in cart_items)
    
    return render_template('product/cart.html', cart_items=cart_items, total_price=total_price, user_id=user_id)
    

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
    user_id = g.user.id if g.user else None
    # 새로운 주문 생성
    new_order = Order(user_id=user_id, order_date=datetime.now(), total_price=0, status='대기 중')
    db.session.add(new_order)
    db.session.commit()

    # 장바구니에서 선택된 음료를 주문 목록에 추가
    cart_items = CartItem.query.all()  # 장바구니에 담긴 음료 조회
    for cart_item in cart_items:
        ordered_item = OrderedItem(
            order=new_order,
            product=cart_item.product,
            price=cart_item.price,
            quantity=cart_item.quantity
        )
        new_order.total_price += ordered_item.price * ordered_item.quantity
        db.session.add(ordered_item)
    
    # 장바구니 비우기
    CartItem.query.delete()
    db.session.commit()

    return redirect(url_for('order.order_success',order_id=new_order.id))


@bp.route('/order_success/<int:order_id>')
def order_success(order_id):
    # 주문 정보를 가져오기
    order = Order.query.get(order_id)
    order_cancelled=False

    if order:
        return render_template('product/order_success.html', order=order)
    else:
        return render_template('product/order_success.html',order_cancelled=True)


@bp.route('/order_list')
def order_list():
    # 주문 목록 조회
    orders = Order.query.all()
    user_id = g.user.id if g.user else None
   
    return render_template('product/order_list.html', orders=orders, user_id=user_id)

@bp.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    order = Order.query.get(order_id)
    if order:
        order.status = "주문완료"
        db.session.commit()
      
    
    return redirect(url_for('order.order_list'))


@bp.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order.status = "주문취소"
        db.session.commit()
      
    
    return redirect(url_for('order.order_list'))


@bp.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get(order_id)

    if order:
        # 주문된 항목을 먼저 삭제
        for item in order.ordered_items:
            db.session.delete(item)
        
        # 주문 삭제
        db.session.delete(order)
        db.session.commit()
     
    return redirect(url_for('order.order_list'))

@bp.route('/delete_all_orders', methods=['POST'])
def delete_all_orders():
    orders = Order.query.all()  # 모든 주문 조회

    for order in orders:
        # 주문된 항목을 먼저 삭제
        for item in order.ordered_items:
            db.session.delete(item)
        
        # 주문 삭제
        db.session.delete(order)
    
    db.session.commit()
   

    return redirect(url_for('order.order_list'))
