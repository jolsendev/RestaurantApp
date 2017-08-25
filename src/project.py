from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name': 'Blue Burgers', 'id': '2'},
               {'name': 'Taco Hut', 'id': '3'}]

# Fake Menu Items
items = [
    {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'},
    {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert',
     'id': '2'},
    {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree',
     'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'},
    {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer',
     'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree'}


# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# show all restaurants
@app.route('/')
@app.route('/restaurants/')
def all_restaurants():
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
    return render_template('menu.html', menu_items=items)


# create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    return render_template('newMenuItem.html')


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
    app.run(host='0.0.0.0', port=80)
