from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Secret key for session management and flash messages
app.config['SECRET_KEY'] = 'a8f5f167f44f4964e6c998dee827110c'

# Ensure instance folder exists
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instances')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_path, 'example.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- MODEL ----------------
class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    contact = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Hotel {self.name}>"


# Create tables if the db/table does not already exist
with app.app_context():
    db.create_all()


# ---------------- ROUTES ----------------

# READ - list all hotels
@app.route('/')
def index():
    hotels = Hotel.query.all()
    return render_template('index.html', hotels=hotels)


# CREATE - add a new hotel
@app.route('/add', methods=['POST'])
def add_hotel():
    name = request.form.get('name')
    location = request.form.get('location')
    rooms = request.form.get('rooms')
    price_per_night = request.form.get('price_per_night')
    contact = request.form.get('contact')

    if not all([name, location, rooms, price_per_night, contact]):
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))

    new_hotel = Hotel(
        name=name,
        location=location,
        rooms=int(rooms),
        price_per_night=float(price_per_night),
        contact=contact
    )
    db.session.add(new_hotel)
    db.session.commit()
    flash('Hotel registered successfully!', 'success')
    return redirect(url_for('index'))


# UPDATE - edit an existing hotel
@app.route('/update/<int:hotel_id>', methods=['POST'])
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)

    hotel.name = request.form.get('name')
    hotel.location = request.form.get('location')
    hotel.rooms = int(request.form.get('rooms'))
    hotel.price_per_night = float(request.form.get('price_per_night'))
    hotel.contact = request.form.get('contact')

    db.session.commit()
    flash('Hotel updated successfully!', 'success')
    return redirect(url_for('index'))


# DELETE - remove a hotel
@app.route('/delete/<int:hotel_id>')
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)