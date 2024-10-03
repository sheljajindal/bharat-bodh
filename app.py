from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)  # Use a securely generated key

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'bharat'
app.config['MYSQL_PASSWORD'] = 'Bodh_12345'
app.config['MYSQL_DB'] = 'bharatBodh'

# Initialize MySQL
mysql = MySQL(app)

# Hash password
def hash_password(password):
    return generate_password_hash(password)

# Authentication Route (handles both login and registration)

# Home Page Route
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/reg_log', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            cursor.close()
            
            if account and check_password_hash(account['password'], password):
                session['loggedin'] = True
                session['user_id'] = account['user_id']
                session['username'] = account['username']

                flash('Login successful!', 'success')
        
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM abstract_submission WHERE user_id = %s', (session['user_id'],))
                account = cursor.fetchone()
                cursor.close()
                if account:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM personal_information WHERE user_id = %s', (session['user_id'],))
                    account = cursor.fetchone()
                    cursor.close()
                    print(account,"SHELJASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                    return render_template('sucess_page.html',user_id=session['user_id'],tit=account['title'],first=account['first_name'],last=account['last_name'])
                else:    
                    return redirect('/personal_info')
            else:
                flash('Login failed. Invalid credentials!', 'error')
        
        elif 'register' in request.form:
            username = request.form['reg_username']
            password = request.form['reg_password']
            confirm_password = request.form['confirm_password']
            
            if password != confirm_password:
                flash('Passwords do not match!', 'error')
                return redirect('/reg_log')
            
            hashed_password = hash_password(password)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            
            if account:
                flash('Username already exists!', 'error')
                return redirect('/reg_log')
            
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            mysql.connection.commit()
            cursor.close()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect('/reg_log')
    
    return render_template('register.html')


@app.route('/personal_info', methods=['POST', 'GET'])
def personal_information():
    if 'loggedin' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect('/reg_log')

    if request.method == 'POST':
        # Fetch form data
        title = request.form.get('title')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        country_code = request.form.get('country_code')
        phone = request.form.get('phone')
        email = request.form.get('email')  # This will be autofilled from the session
        confirm_email = request.form.get('confirm_email')
        country = request.form.get('country')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        pincode = request.form.get('pincode')
        institution_name = request.form.get('institution_name')
        institution_state = request.form.get('institution_state')
        whatsapp_country_code = request.form.get('whatsapp_country_code')
        whatsapp_number = request.form.get('whatsapp_number')
        
        # Save some form values in the session
        session['title'] = title
        session['first_name'] = first_name
        session['last_name'] = last_name
        session['email'] = email
        session['institute_name'] = institution_name
        session['country_code']=country_code
        session['phone'] = phone
        print(dob,"SHELJA JINDAL")
        # Insert the form data into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            INSERT INTO personal_information 
            (user_id,title, first_name, last_name,birth_date, gender, phone_code, phone_no, email, country, address1, address2, pincode, institute_name, institute_address, whatsapp_code, whatsapp_no)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (session['user_id'],title, first_name, last_name, dob, gender, country_code, phone, email, country, address1, address2, pincode, institution_name, institution_state, whatsapp_country_code, whatsapp_number))
        mysql.connection.commit()
        cursor.close()

        flash('Personal Information Submitted Successfully!', 'success')
        return redirect('/abstract')

    
    return render_template("personal_info.html", email=session['username'])
@app.route('/abstract', methods=['POST', 'GET'])
def abstract_information():
    if 'loggedin' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect('/reg_log')

    if request.method == 'POST':
        abstract_type = request.form.get('abstract_type')
        designation = request.form.get('designation')
        department = request.form.get('department')
        institute_name = request.form.get('institute_name')
        co_authors_num = request.form.get('co_authors')  # Number of co-authors
        category = request.form.get('category')
        language = request.form.get('language')
        mode = request.form.get('mode')
        declaration = request.form.get('declaration') is not None  # Declaration checkbox
        mailing_list = request.form.get('mailing_list') is not None  # Mailing list checkbox

        # Extract co-author details dynamically based on the number selected
        co_author_name_1 = request.form.get('co_author_name_1')
        co_author_email_1 = request.form.get('co_author_email_1')
        co_author_name_2 = request.form.get('co_author_name_2')
        co_author_email_2 = request.form.get('co_author_email_2')
        co_author_name_3 = request.form.get('co_author_name_3')
        co_author_email_3 = request.form.get('co_author_email_3')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            INSERT INTO abstract_submission 
            (user_id, abstract_type, designation, institute_department,co_authors, co_author_name_1, co_author_email_1, co_author_name_2, co_author_email_2, co_author_name_3, co_author_email_3, category, language, mode, declaration, mailing_list)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        ''', (
            session['user_id'],  # User ID from session
            abstract_type,  # Form data (abstract type)
            designation,  # Designation from form
            department,co_authors_num,  # Department or institute from form
            co_author_name_1, co_author_email_1,  # Co-author 1
            co_author_name_2, co_author_email_2,  # Co-author 2
            co_author_name_3, co_author_email_3,  # Co-author 3
            category,  # Category selected in the form
            language,  # Language selection
            mode,  # Presentation mode (offline/online)
            declaration,  # True if declaration checkbox is checked
            mailing_list  # True if mailing list checkbox is checked
        ))
        # Commit the transaction and close the cursor
        mysql.connection.commit()
        cursor.close()

        # Flash message to confirm submission
        flash('Abstract submitted successfully!')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM personal_information WHERE user_id = %s', (session['user_id'],))
        account = cursor.fetchone()
        cursor.close()
        print(account,"SHELJASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        return render_template('sucess_page.html',user_id=session['user_id'],tit=account['title'],first=account['first_name'],last=account['last_name'])


    return render_template('abstract.html',first_name=session['first_name'],last_name=session['last_name'],email=session['username'],country_code=session['country_code'],phone=session['phone'],institute_name=session['institute_name'])

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Assuming you want to store these in a table called 'contact_messages'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            INSERT INTO contact_home (name, mail, subject, message)
            VALUES (%s, %s, %s, %s)
        ''', (name, email, subject, message))
        mysql.connection.commit()
        cursor.close()

        flash('Your message has been sent successfully!', 'success')
        return redirect('/') 
if __name__ == "__main__":
    app.run(debug=True)
