from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables in the database
def create_tables():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS contact_entries (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        message TEXT NOT NULL
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        amount REAL NOT NULL,
                        upi_id TEXT NOT NULL,
                        status TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Home page route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        # Insert data into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO contact_entries (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)',
                     (name, email, phone, subject, message))
        conn.commit()
        conn.close()

        flash('Message submitted successfully!', 'success')
        return redirect(url_for('contact'))  # Redirect to avoid form resubmission

    return render_template('contact.html')

# Payment page route
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        upi_id = request.form['upi_id']
        amount = request.form['amount']

        # Validate UPI ID
        if '@' not in upi_id:
            flash('Invalid UPI ID. Please try again.', 'danger')
            return redirect(url_for('payment'))

        # Save payment information in the database
        conn = get_db_connection()
        conn.execute('INSERT INTO payments (name, email, amount, upi_id, status) VALUES (?, ?, ?, ?, ?)',
                     (name, email, amount, upi_id, 'Pending'))
        conn.commit()
        conn.close()

        # Redirect to UPI link for payment (dummy implementation)
        upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        flash('Payment initiated successfully! Complete the payment in your UPI app.', 'success')
        return redirect(upi_link)  # Redirect to the UPI payment app

    return render_template('payment.html')

if __name__ == '__main__':
    create_tables()  # Ensure the table is created before running the app
    app.run(debug=True)
