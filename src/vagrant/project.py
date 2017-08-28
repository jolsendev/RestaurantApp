from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
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
    return render_template('restaurants.html', restaurants=restaurants)


# create a new restaurant
@app.route('/restaurants/new/')
def newResturant():
    return render_template('newRestaurant.html')


# edit & restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return render_template('editRestaurant.html', restaurant_id=restaurant_id)


# delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return "Edit restaurant"


# show a restaurant menu
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):

    return "Not Implemented" #render_template('menu.html', menu_items=items)


# create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/edit')
def editMenuItem(restaurant_id):
    return render_template('editMenuItem.html')


# delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8001)
