
from flask import Flask, flash, render_template, redirect, request, url_for

from models import Children, Wishlist, db

app = Flask(__name__)
app.config.from_object('config')

# Create database
with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/')
def index():
    children = Children.query.outerjoin(Wishlist).all()
    return render_template('index.html', children=children)


@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        list_status = request.form['list_status']
        children = Children(
            name=name,
            age=age,
            gender=gender,
            address=address,
            list_status=list_status,
        )
        db.session.add(children)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_child.html')


@app.route('/edit_child/<int:child_id>', methods=['GET', 'POST'])
def edit_child(child_id):
    children = Children.query.get(child_id)
    if request.method == 'POST':
        children.name = request.form['name']
        children.age = request.form['age']
        children.gender = request.form['gender']
        children.address = request.form['address']
        children.list_status = request.form['list_status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_child.html', children=children)


@app.route('/remove_child/<int:child_id>', methods=['GET', 'POST'])
def remove_child(child_id):
    children = Children.query.get(child_id)
    if request.method == 'POST':
        db.session.delete(children)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('remove_child.html', children=children)


@app.route('/edit_wishlist/<int:child_id>', methods=['GET', 'POST'])
def edit_wishlist(child_id):
    children = Children.query.join(Wishlist).all()
    wishlist = Wishlist.query.filter_by(child_id=child_id).all()
    if request.method == 'POST':
        item = request.form['gift']
        wishlist = Wishlist(
            item=item,
            child_id=child_id,
        )
        db.session.add(wishlist)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_wishlist.html', children=children, wishlist=wishlist)


if __name__ == "__main__":
    app.run(debug=True)