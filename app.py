
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (name TEXT, department TEXT, year TEXT, section TEXT, password TEXT)''')
conn.commit()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        section = request.form['section']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        cursor.execute('INSERT INTO users (name, department, year, section, password) VALUES (?, ?, ?, ?, ?)', 
                       (name, department, year, section, password))
        conn.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute('SELECT * FROM users WHERE name=? AND password=?', (username, password))
        user = cursor.fetchone()
        
        if user:
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(debug=True)
