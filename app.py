from flask import Flask, render_template, request, redirect, url_for, session
from models import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    if 'cart' not in session:
        session['cart'] = {}
    
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    
    cart = session.get('cart', {})
    
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)