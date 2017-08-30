from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# show all restaurants+

@app.route('/')
@app.route('/restaurants/')
def all_restaurants():
    restaurants = session.query(Restaurant).all()
    if not restaurants:
        flash("There are no restaurants!")
        return render_template('restaurants.html', restaurants=restaurants)
    return render_template('restaurants.html', restaurants=restaurants)


# create a new restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == "POST":
        restaurant_name = Restaurant(name=request.form['name'])
        session.add(restaurant_name)
        session.commit()
        return redirect(url_for('all_restaurants'))
    else:
        return render_template('newRestaurant.html')


# edit & restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('all_restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant.id, restaurant_name=restaurant.name)


# delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant_to_delete = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(restaurant_to_delete)
        session.commit()
        return redirect(url_for('all_restaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('deleteRestaurant.html', restaurant=restaurant)


# show a restaurant menu
@app.route('/restaurants/<int:restaurant_id>/menu/', methods=['GET', 'POST'])
def showMenu(restaurant_id):
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', menu_items=menu_items)


# create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'],
                           price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    oldItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        if request.form["name"]:
            oldItem.name = request.form["name"]
            oldItem.description = request.form["description"]
            oldItem.course = request.form["course"]
            oldItem.price = str(request.form["price"])
        session.add(oldItem)
        session.commit()
        flash("new menu item updated!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

    else:
        menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        for menu_item in menu_items:
            if menu_item.id == menu_id:
                i = menu_item
        return render_template('editMenuItem.html', item=i)


# delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    oldItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(oldItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    return render_template('deleteMenuItem.html', item=oldItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
