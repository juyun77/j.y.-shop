from shop import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name= db.Column(db.String(100), nullable=False)
    address= db.Column(db.String(200), nullable=False)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime(), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 주문 상태 (예: "대기 중", "완료됨" 등)

class OrderedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', backref='ordered_items')
    product = db.relationship('Product', backref='ordered_items')