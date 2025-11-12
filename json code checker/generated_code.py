from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('index.html', bookings=bookings)

@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (name, date, time) VALUES (?, ?, ?)', (name, date, time))
        conn.commit()
        conn.close()
        return "Booking added successfully!"
    else:
        return render_template('bookings.html')

if __name__ == '__main__':
    app.run(debug=True)