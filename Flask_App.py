# Import Modules
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_mysqldb import MySQL
import secrets
from datetime import datetime
from datetime import date
import random
import string
import os
from werkzeug.utils import secure_filename
import re
from flask_mail import Mail, Message


app = Flask(__name__)

app.secret_key = secrets.token_hex(8)
# Set the session app object
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pms.write@gmail.com'
app.config['MAIL_PASSWORD'] = 'iwhchxznwifqddkv'
app.config['MAIL_DEFAULT_SENDER'] = 'pms.write@gmail.com'

# Configure the MySQL and OAuth instances
mysql = MySQL(app)

mail = Mail(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'pranikmedicalservices.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'pranikmedicalser'
app.config['MYSQL_PASSWORD'] = 'pms@1504'
app.config['MYSQL_DB'] = 'pranikmedicalser$default'



# Generate a random verification code and store it in the session
def generate_verification_code():
    verification_code = ''.join(random.choices(string.digits, k=6))
    session['verification_code'] = verification_code
    return verification_code


# ------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------


@app.route("/")
def home():
    if 'loggedin' in session:
        return redirect(url_for('index'))
    session['error']=''
    return render_template("home.html")

@app.route('/about')
def about():
    if 'loggedin' in session:
        return redirect(url_for('index'))
    return render_template("about.html")

@app.route("/contact")
def contact():
    if 'loggedin' in session:
        return redirect(url_for('contact_us'))
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/terms-condition")
def terms_condition():
    if 'loggedin' in session:
        return redirect(url_for('terms_condition_user'))
    return render_template("terms-condition.html")

@app.route("/terms-condition-user")
def terms_condition_user():
    if 'loggedin' not in session:
        return redirect(url_for('terms_condition'))
    return render_template("terms-condition-user.html")

@app.route("/coming-soon")
def coming_soon():
    if 'loggedin' not in session:
        return render_template('coming.html')

    return render_template("coming-soon.html")


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']

    # Send thank you email
    send_thank_you_email(email)

    return redirect(url_for('home'))

def send_thank_you_email(email):
    message = Message('Thank You for Subscribing', recipients=[email])
    message.body = f"Dear Subscriber,\n\nThank you for subscribing to our newsletter! We're excited to have you on board and look forward to sharing valuable updates, news, and offers with you.\n\nIf you have any questions or need assistance, feel free to reach out to our team. Stay tuned for exciting content!\n\nBest regards,\nThe PMS Team"

    try:
        mail.send(message)
        print("Thank you email sent successfully")
    except Exception as e:
        print(f"Failed to send thank you email: {str(e)}")


@app.route("/unauthorized")
def unauthorized():
    if 'loggedin' not in session:
        return redirect(url_for('home'))
    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')
    error = session.get('error')

    return render_template("404.html", error=error, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

@app.route("/index")
def index():
    if 'loggedin' not in session:
        return redirect(url_for('logout'))

    session['error']=''

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    return render_template("index.html", name=name, profile=profile, user=user, url=url, dashboard=dashboard)

@app.route("/about-us")
def about_us():
    if 'loggedin' not in session:
        return redirect(url_for('about'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    return render_template('about-us.html', name=name, profile=profile, user=user, url=url, dashboard=dashboard)

@app.route("/contact-us")
def contact_us():
    if 'loggedin' not in session:
        return redirect(url_for('contact'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    return render_template('contact-us.html', name=name, profile=profile, user=user, url=url, dashboard=dashboard)




# /login-phone
# /forgot-password


# Search Doctors for unregistered users:

@app.route('/search-doctors-pms', methods=['GET', 'POST'])
def search_doctors_pms():

    if request.method == 'POST':
        name = request.form["name"]
        location = request.form["location"]
        doctor_id = request.form["doctor_id"]

        # Construct the SQL query and parameters based on the search criteria
        query = "SELECT * FROM registered_doctors WHERE "
        conditions = []
        params = []

        if name and name != "":
            conditions.append("Name LIKE %s")
            params.append(f"%{name}%")

        if location and location != "":
            conditions.append("Clinic_Address LIKE %s OR City LIKE %s OR State LIKE %s OR Address_Line1 LIKE %s OR Address_Line2 LIKE %s")
            params.extend([f"%{location}%", f"%{location}%", f"%{location}%", f"%{location}%", f"%{location}%"])

        if doctor_id and doctor_id != "":
            conditions.append("Doctor_ID LIKE %s")
            params.append(f"%{doctor_id}%")

        if conditions:
            query += " OR ".join(conditions)
        else:
            query += "1"  # Dummy condition to retrieve all doctors if no specific criteria are provided

        # Execute the query and fetch the search results
        cur = mysql.connection.cursor()
        cur.execute(query, tuple(params))
        rows = cur.fetchall()

        # Count the number of doctors found
        num_doctors_found = len(rows)
        msg = f"{num_doctors_found} Doctors found:" if location else ""
        msg1 = f" in {location}" if location else ""

        if num_doctors_found == 0:
            return render_template('search-not-found.html')

        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of doctor data dictionaries
        doctor_data_list = []
        for row in rows:
            doctor_data = dict(zip(column_names, row))
            # Filter out None values from the doctor_data dictionary
            doctor_data = {k: v for k, v in doctor_data.items() if v is not None}
            doctor_data_list.append(doctor_data)

        cur.close()

        # Render the search results on the search.html template
        return render_template('search-only.html', search_results=doctor_data_list, msg=msg, msg1=msg1)

    # Render the search form template for GET requests
    return render_template('home.html')



# ------------------------------------------------------------------------------------------------------------------------------

# APPOINMENTS RECORDS FOR REGISTERED PATIENTS:

# ------------------------------------------------------------------------------------------------------------------------------


@app.route('/search-doctors', methods=['GET', 'POST'])
def search_doctors():
    l=['patient','doctor','admin']
    if session.get('user_type') not in l:
        return redirect(url_for('search_doctors_pms'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    if request.method == 'POST':
        name = request.form["name"]
        location = request.form["location"]
        doctor_id = request.form["doctor_id"]

        # Construct the SQL query and parameters based on the search criteria
        query = "SELECT * FROM registered_doctors WHERE "
        conditions = []
        params = []

        if name and name != "":
            conditions.append("Name LIKE %s")
            params.append(f"%{name}%")

        if location and location != "":
            conditions.append("Clinic_Address LIKE %s OR City LIKE %s OR State LIKE %s OR Address_Line1 LIKE %s OR Address_Line2 LIKE %s")
            params.extend([f"%{location}%", f"%{location}%", f"%{location}%", f"%{location}%", f"%{location}%"])

        if doctor_id and doctor_id != "":
            conditions.append("Doctor_ID LIKE %s")
            params.append(f"%{doctor_id}%")

        if conditions:
            query += " OR ".join(conditions)
        else:
            query += "1"  # Dummy condition to retrieve all doctors if no specific criteria are provided

        # Execute the query and fetch the search results
        cur = mysql.connection.cursor()
        cur.execute(query, tuple(params))
        rows = cur.fetchall()

        # Count the number of doctors found
        num_doctors_found = len(rows)
        msg = f"{num_doctors_found} Doctors found:" if location else ""
        msg1 = f" in {location}" if location else ""

        if num_doctors_found == 0:
            return render_template("search_not_found.html", name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of doctor data dictionaries
        doctor_data_list = []
        for row in rows:
            doctor_data = dict(zip(column_names, row))
            # Filter out None values from the doctor_data dictionary
            doctor_data = {k: v for k, v in doctor_data.items() if v is not None}
            doctor_data_list.append(doctor_data)

        cur.close()

        # Render the search results on the search.html template
        return render_template('search.html', search_results=doctor_data_list, msg=msg, msg1=msg1, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    # Render the search form template for GET requests
    return redirect(url_for('index'))



@app.route('/book-appointment/<string:doctor_id>', methods=['GET', 'POST'])
def book_appointment(doctor_id):
    if session.get('user_type') != 'patient':
        session['error'] = "You are not an authorized patient. Only authorized patients have access to this page."
        return redirect(url_for('unauthorized'))

    # Retrieve the doctor's details based on the doctor ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM registered_doctors WHERE Doctor_ID = %s", (doctor_id,))
    row = cur.fetchone()

    column_names = [desc[0] for desc in cur.description]  # Get the column names
    doctor_data = dict(zip(column_names, row))

    # Filter out None values from the doctor_data dictionary
    doctor_data = {k: v for k, v in doctor_data.items() if v is not None}
    cur.close()

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    if request.method == 'POST':
        # Retrieve the form data for the appointment details
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        insurance = request.form.get('insurance', 'No')
        reason = request.form['reason']
        symptoms = request.form['symptoms']

        patient_id = session['patient_id']


        if appointment_time == '':
            date_error = "Please select time."

            return render_template('booking.html', doctor_data=doctor_data, date_error=date_error, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Check if the appointment date is in the past
        selected_date = datetime.strptime(appointment_date, '%d/%m/%Y').date()
        current_date = datetime.now().date()
        if selected_date < current_date:
            date_error = "Please select a date in the present or future."
            return render_template('booking.html', doctor_data=doctor_data, date_error=date_error, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Change the date format to 'YYYY-MM-DD' for MySQL
        appointment_date_mysql = selected_date.strftime('%Y-%m-%d')

        # Change the time format to 'HH:MM:SS' for MySQL
        appointment_time_mysql = datetime.strptime(appointment_time, '%I:%M %p').strftime('%H:%M:%S')

        # Check if the appointment already exists
        cur = mysql.connection.cursor()
        query = """
            SELECT * FROM appointments
            WHERE Patient_ID = %s AND Doctor_ID = %s AND Appointment_Date = %s
        """
        cur.execute(query, (patient_id, doctor_id, appointment_date_mysql))
        existing_appointment = cur.fetchone()

        if existing_appointment:
            # An appointment with the same doctor, date, and time already exists
            error_message = "Your appointment is already booked with this doctor."
            return render_template('booking.html', doctor_data=doctor_data, date_error=error_message, name=name, profile=profile, user=user, url=url, dashboard=dashboard)



        # Store the appointment details in session

        session['doctor_id'] = doctor_id
        session['appointment_date_view'] = appointment_date
        session['appointment_time_view'] = appointment_time
        session['appointment_date'] = appointment_date_mysql
        session['appointment_time'] = appointment_time_mysql
        session['insurance'] = insurance
        session['reason'] = reason
        session['symptoms'] = symptoms


        # Redirect to the payment page
        return redirect(url_for('payment', doctor_id=doctor_id))

    # Render the appointment booking form with the doctor's details and today's date
    return render_template('booking.html', doctor_data=doctor_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)


@app.route('/book-appointment/<string:doctor_id>/payment', methods=['GET', 'POST'])
def payment(doctor_id):
    if session.get('user_type') != 'patient':
        session['error'] = "You are not an authorized patient. Only authorized patients have access to this page."
        return redirect(url_for('unauthorized'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')
    email = session.get('patient_email')

    # Retrieve the appointment data from session
    patient_id = session['patient_id']
    doctor_id = session['doctor_id']
    appointment_date = session['appointment_date_view']
    appointment_time = session['appointment_time_view']
    appointment_date_mysql = session['appointment_date']
    appointment_time_mysql = session['appointment_time']
    insurance = session['insurance']
    reason = session['reason']
    symptoms = session['symptoms']

    # Retrieve the doctor's details based on the doctor ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM registered_doctors WHERE Doctor_ID = %s", (doctor_id,))
    row = cur.fetchone()

    column_names = [desc[0] for desc in cur.description]  # Get the column names
    doctor_data = dict(zip(column_names, row))

    # Filter out None values from the doctor_data dictionary
    doctor_data = {k: v for k, v in doctor_data.items() if v is not None}
    print(doctor_data.keys())  # Add this line to print the keys
    cur.close()

    # Check if the 'Fee' key is present in the dictionary
    if 'Fee' in doctor_data:
        if doctor_data['Fee'] != None:
            doctor_fee = float(doctor_data['Fee'])
        else:
            doctor_fee = 0.0
    else:
        doctor_fee = 100.0

    booking_fee_amount = 2.0
    tax_amount = (doctor_fee * 3) / 100
    total_fee = doctor_fee + booking_fee_amount + tax_amount

    if request.method == 'POST':
        # Perform payment validation and processing here
        #payment = request.form["payment"]
        #print(payment)

        # Save the appointment details with the doctor ID
        # Insert the appointment data into the appointments table
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO appointments (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time, Insurance, Reason, Symptoms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        appointment_values = (
            patient_id,
            doctor_id,
            appointment_date_mysql,
            appointment_time_mysql,
            insurance,
            reason,
            symptoms
        )

        cur.execute(query, appointment_values)
        mysql.connection.commit()
        cur.close()

        #session.pop('patient_id', None)
        session.pop('doctor_id', None)
        session.pop('appointment_date_view', None)
        session.pop('appointment_time_view', None)
        session.pop('appointment_date', None)
        session.pop('appointment_time', None)
        session.pop('insurance', None)
        session.pop('reason', None)
        session.pop('symptoms', None)


        if 'Name' in doctor_data:
            doctor_name = doctor_data['Name']
        else:
            doctor_name = "Unknown"

         # Send email to the patient with appointment details
        msg = Message('Appointment Confirmation', recipients=[email])

        msg.body = f"Dear {name},\n\nThank you for booking an appointment with Pranik Medical Services (PMS).\n\nYour appointment details are as follows:\n\nDoctor: {doctor_name}\nAppointment Date: {appointment_date}\nAppointment Time: {appointment_time}\n\nWe look forward to seeing you!\n\nBest regards,\nThe PMS Team"
        mail.send(msg)

        # Redirect to a success page or show a success message
        return render_template('successful.html', doctor=doctor_data, appointment_date=appointment_date, appointment_time=appointment_time, name=name, profile=profile, user=user, url=url, dashboard=dashboard)


        # Redirect to a success page or show a success message
        return render_template('successful.html', doctor=doctor_data, appointment_date = appointment_date, appointment_time = appointment_time, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    return render_template('payment.html', doctor=doctor_data,doctor_id = doctor_id, appointment_date = appointment_date, appointment_time = appointment_time,
                          doctor_fee = doctor_fee, booking_fee=booking_fee_amount, tax=tax_amount, total_fee=total_fee, name=name, profile=profile, user=user, url=url, dashboard=dashboard)



# ------------------------------------------------------------------------------------------------------------------------------

# PATIENTS RECORDS:

@app.route("/patient-register", methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        full_name = request.form["fullname"]
        email = request.form["email"]
        phone_no = request.form["phone"]
        password = request.form["password"]

        # Regular expression patterns
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        phone_pattern = r'^\d{10}$'
        password_pattern = r'^.{8,}$'

        # Validate email
        if not re.match(email_pattern, email):
            error_message = "Invalid email address. Please enter a valid email."
            return render_template("patient-register.html", error=error_message)

        # Validate phone number
        if not re.match(phone_pattern, phone_no):
            error_message = "Invalid phone number. Please enter a 10-digit phone number."
            return render_template("patient-register.html", error=error_message)

        # Validate password
        if not re.match(password_pattern, password):
            error_message = "Invalid password. Password should be at least 8 characters long."
            return render_template("patient-register.html", error=error_message)

        # Check if the patient already exists in the database
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_patients WHERE Email = %s OR Phone = %s"
        cur.execute(query, (email, phone_no))
        row = cur.fetchone()

        if row is not None:
            column_names = [desc[0] for desc in cur.description]  # Get the column names
            patient_data = dict(zip(column_names, row))
            cur.close()
            # Check if email or phone number is already registered
            if patient_data['Email'] == email:
                error_message = "Email is already registered."
            else:
                error_message = "Phone number is already registered."
            return render_template("patient-register.html", error=error_message)
        cur.close()

        # Generate a unique patient ID
        patient_id = generate_patient_id(full_name)

        # Register the patient if not already registered
        cur = mysql.connection.cursor()
        query = "INSERT INTO registered_patients (Name, Email, Phone, Password, Patient_ID) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (full_name, email, phone_no, password, patient_id))

        mysql.connection.commit()
        cur.close()


        # Send registration email to the user
        msg = Message('Registration Confirmation', recipients=[email])
        msg.body = f"Dear {full_name},\n\nThank you for registering with Pranik Medical Services (PMS).\n\nYou can now log in to access all the services and features offered by PMS.\n\nWe look forward to serving you!\n\nBest regards,\nThe PMS Team"
        mail.send(msg)

        return render_template('success.html')

    return render_template("patient-register.html")


def generate_patient_id(full_name):
    # Generate random digits
    random_digits = ''.join(random.choices(string.digits, k=4))

    # Get the current date and time
    now = datetime.now()
    day_digit = str(now.day)[0]
    month_digit = str(now.month)[0]
    minute_digit = str(now.minute)[0]
    second_digit = str(now.second)[0]

    # Create the patient ID by combining name characters, digits, and the date
    patient_id = f"{full_name[:3].upper()}{random_digits}{day_digit}{month_digit}{minute_digit}{second_digit}"

    return patient_id


@app.route('/patient-dashboard')
def patient_dashboard():
    if session['user_type'] == 'patient':
        email = session['email']  # Retrieve the logged-in doctor's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_patients WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        column_names = [desc[0] for desc in cur.description]  # Get the column names
        patient_data = dict(zip(column_names, row))
        cur.close()

        # Check if the 'Profile_URL' key exists in the row_dict dictionary
        if 'Profile_URL' in patient_data and patient_data['Profile_URL'] is not None:
            session['profile_pms'] = 'patients/' + patient_data['Profile_URL']
        if 'Name' in patient_data and patient_data['Name'] is not None:
            session['name_pms'] = patient_data['Name']

        # Get user information from the session
        name = session.get('name_pms')
        profile = session.get('profile_pms')
        user = session.get('user_pms')
        url = session.get('url_pms')
        dashboard = session.get('dashboard_pms')

        patient_id = patient_data['Patient_ID']

        cur = mysql.connection.cursor()
        query = """
            SELECT appointments.*, registered_doctors.Name AS Doctor_Name, registered_doctors.Profile_URL AS Profile_URL, registered_doctors.Doctor_ID, registered_doctors.Specialization AS Specialization
            FROM appointments
            JOIN registered_doctors ON appointments.Doctor_ID = registered_doctors.Doctor_ID
            WHERE Patient_ID = %s
            ORDER BY Appointment_Date >= CURDATE() DESC, Appointment_Date ASC
        """
        cur.execute(query, (patient_id,))

        rows = cur.fetchall()
        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of appointment data dictionaries
        appointment_data_list = []
        for row in rows:
            appointment_data = dict(zip(column_names, row))
            # Filter out None values from the appointment_data dictionary
            appointment_data = {k: v for k, v in appointment_data.items() if v is not None}
            appointment_data_list.append(appointment_data)

        cur.close()
        amount_paid = "--"

        # Render the doctor dashboard template
        return render_template('patient-dashboard.html', appointment_data_list=appointment_data_list, amount_paid=amount_paid, patient_data=patient_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)
    else:
        session['error'] = "You are not an authorized patient. Only authorized patients have access to this page."
        return redirect(url_for('unauthorized'))



@app.route("/patient-profile-settings", methods=['GET', 'POST'])
def patient_profile_settings():
    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    if session['user_type'] == 'patient':
        if request.method == 'POST':
            # Get the updated patient data from the form
            name = request.form['name']
            dob = request.form['dob']
            blood_group = request.form['blood_group']
            phone = request.form['phone']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            pincode = request.form['pincode']
            country = request.form['country']

            email = session['email']  # Retrieve the logged-in patient's email from the session

            # Construct the SQL query and parameters based on the updated fields
            query = "UPDATE registered_patients SET"
            params = []

            if name:
                query += " Name = %s,"
                params.append(name)

            if dob:
                query += " Date_of_Birth = %s,"
                params.append(dob)

            if blood_group:
                query += " Blood_Group = %s,"
                params.append(blood_group)

            if phone:
                query += " Phone = %s,"
                params.append(phone)

            if address:
                query += " Address = %s,"
                params.append(address)

            if city:
                query += " City = %s,"
                params.append(city)

            if state:
                query += " State = %s,"
                params.append(state)

            if pincode:
                query += " Pin_Code = %s,"
                params.append(pincode)

            if country:
                query += " Country = %s,"
                params.append(country)

            # Remove the trailing comma from the query
            query = query.rstrip(',')

            # Add the WHERE clause to update the specific patient's record
            query += " WHERE Email = %s"
            params.append(email)

            # Update the patient data in the database
            cur = mysql.connection.cursor()
            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()

            # Handle image upload
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    email = session['email']
                    cur = mysql.connection.cursor()
                    # Generate a secure filename and specify the upload folder path
                    filename = secure_filename(session['patient_id'] + os.path.splitext(photo.filename)[1])
                    upload_folder = os.path.join(app.root_path, 'static', 'assets', 'img', 'patients')

                    # Save the uploaded image with the patient_id as the filename
                    photo.save(os.path.join(upload_folder, filename))

                    # Update the image filename in the database
                    cur = mysql.connection.cursor()
                    query = "UPDATE registered_patients SET Profile_URL = %s WHERE Email = %s"
                    cur.execute(query, (filename, email))
                    mysql.connection.commit()
                    cur.close()

            # Redirect to the patient dashboard or any other appropriate page
            return redirect(url_for('patient_dashboard'))

        # Retrieve the patient's data from the database for display
        email = session['email']  # Retrieve the logged-in patient's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_patients WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        if row:
            column_names = [desc[0] for desc in cur.description]  # Get the column names
            patient_data = dict(zip(column_names, row))

            # Filter out None values from the patient_data dictionary
            patient_data = {k: v for k, v in patient_data.items() if v is not None}

            session['patient_id'] = patient_data['Patient_ID']
            cur.close()

            # Render the patient profile settings template with the patient's data
            return render_template('patient-profile-settings.html', patient_data=patient_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    else:
        session['error'] = "You are not an authorized patient. Only authorized patients have access to this page."
        return redirect(url_for('unauthorized'))


@app.route('/patient-change-password', methods=['GET', 'POST'])
def patient_change_password():
    if session.get('user_type') != 'patient':
        session['error'] = "You are not an authorized patient. Only authorized patients have access to this page."
        return redirect(url_for('unauthorized'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    # Retrieve the patient's data from the database for display
    f_email = session['email']  # Retrieve the logged-in patient's email from the session
    cur = mysql.connection.cursor()
    query = "SELECT * FROM registered_patients WHERE Email = %s"
    cur.execute(query, (f_email,))
    row = cur.fetchone()

    column_names = [desc[0] for desc in cur.description]  # Get the column names
    patient_data = dict(zip(column_names, row))
    session['old_password'] = patient_data['Password']
    cur.close()

    if request.method == 'POST':
        # Access the form data
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Perform validation
        # Example: Check if the old password matches the current password for the patient
        if old_password != session['old_password']:
            error_message = "Old password is incorrect."
            return render_template('patient-change-password.html', error=error_message, patient_data=patient_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Example: Check if the new password meets the desired criteria
        if new_password != confirm_password:
            error_message = "New password and confirm password do not match."
            return render_template('patient-change-password.html', error=error_message, patient_data=patient_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Update the password in the database for the patient
        patient_id = patient_data['Patient_ID']
        update_password_in_p_database(patient_id, new_password)

        success_message = "Password changed successfully."
        return render_template('patient-change-password.html', error=success_message, patient_data=patient_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    return render_template('patient-change-password.html', patient_data=patient_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

def update_password_in_p_database(patient_id, new_password):
    cur = mysql.connection.cursor()
    query = "UPDATE registered_patients SET Password = %s WHERE Patient_ID = %s"
    cur.execute(query, (new_password, patient_id))
    mysql.connection.commit()
    cur.close()





# -----------------------------------------------------------------------------------------------------------------------------


# DOCTORS RECORDS:

@app.route("/doctor-register", methods=['GET', 'POST'])
def doctor_register():
    if request.method == 'POST':
        # Handle the POST request for the "/doctor-register" URL
        name = request.form['name']
        gender = request.form["gender"]
        clinic_name = request.form["clinic_name"]
        clinic_address = request.form["clinic_address"]
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Regular expression patterns
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        phone_pattern = r'^\d{10}$'
        password_pattern = r'^.{8,}$'

        # Validate email
        if not re.match(email_pattern, email):
            error = "Invalid email address. Please enter a valid email."
            return render_template("doctor-register.html",error=error)

        # Validate phone number
        if not re.match(phone_pattern, phone):
            error = "Invalid phone number. Please enter a 10-digit phone number."
            return render_template("doctor-register.html",error=error)

        # Validate password
        if not re.match(password_pattern, password):
            error = "Invalid password. Password should be at least 8 characters long."
            return render_template("doctor-register.html",error=error)

        # Check if the patient already exists in the database
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_doctors WHERE Email = %s OR Phone = %s"
        cur.execute(query, (email, phone))
        row = cur.fetchone()

        if row is not None:
            column_names = [desc[0] for desc in cur.description]  # Get the column names
            doctor_data = dict(zip(column_names, row))
            cur.close()
            # Check if email or phone number is already registered
            if doctor_data['Email'] == email:
                error_message = "Email is already registered."
            else:
                error_message = "Phone number is already registered."
            return render_template("patient-register.html", error=error_message)
        cur.close()

        # Generate a verification code
        verification_code = generate_verification_code()

        # Send verification email
        msg = Message('Account Verification', recipients=[email])
        msg.body = f"Your verification code is: {verification_code}"
        mail.send(msg)

        print(verification_code)

        # Generate a unique doctor ID
        doctor_id = generate_doctor_id(name)

        # Store user data, verification code, and doctor ID in the session
        session['doctor_id'] = doctor_id
        session['doctor_name'] = name
        session['gender'] = gender
        session['clinic_name'] = clinic_name
        session['clinic_address'] = clinic_address
        session['doctor_email'] = email
        session['doctor_phone'] = phone
        session['doctor_password'] = password
        session['verification_code'] = verification_code

        return redirect(url_for('verify', email=email))

    return render_template("doctor-register.html")


@app.route('/verify/<email>', methods=['GET', 'POST'])
def verify(email):
    if request.method == 'POST':
        verification_code = request.form['verification_code']

        # Retrieve the stored verification code and doctor ID from the session
        stored_verification_code = session.get('verification_code')
        doctor_id = session.get('doctor_id')

        # Compare the codes
        if verification_code == stored_verification_code:
            # Code is correct, store doctor data in the database
            name = session['doctor_name']
            gender = session['gender']
            clinic_name = session['clinic_name']
            clinic_address = session['clinic_address']
            email = session['doctor_email']
            phone = session['doctor_phone']
            password = session['doctor_password']

            # Insert doctor data into the database
            cur = mysql.connection.cursor()
            query = "INSERT INTO registered_doctors (Doctor_ID, Name, Gender, Clinic_Name, Clinic_Address, Email, Phone, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (doctor_id, name, gender, clinic_name, clinic_address, email, phone, password))

            mysql.connection.commit()
            cur.close()

            # Clear the session data
            session.pop('doctor_id', None)
            session.pop('doctor_name', None)
            session.pop('gender',None)
            session.pop('clinic_name',None)
            session.pop('clinic_address',None)
            session.pop('doctor_email', None)
            session.pop('doctor_phone', None)
            session.pop('doctor_password', None)
            session.pop('verification_code', None)

            # Send registration email to the user
            msg = Message('Registration Confirmation', recipients=[email])
            msg.body = f"Dear Dr. {name},\n\nThank you for registering with Pranik Medical Services (PMS).\n\nYou can now log in to access all the services and features offered by PMS.\n\nWe look forward to serving you!\n\nBest regards,\nThe PMS Team"
            mail.send(msg)

            return render_template('success.html')
        else:
            error = 'Incorrect OTP'
            # Code is incorrect, display an error message
            return render_template('verify.html', email=email, error=error)

    return render_template('verify.html', email=email, error=False)


def generate_doctor_id(name):
    # Generate random digits
    random_digits = ''.join(random.choices(string.digits, k=4))

    # Get the current date and time
    now = datetime.now()
    day_digit = str(now.day)[0]
    month_digit = str(now.month)[0]
    minute_digit = str(now.minute)[0]
    second_digit = str(now.second)[0]

    # Create the doctor ID by combining name characters, digits, and the date
    doctor_id = f"{name[:3].upper()}{random_digits}{day_digit}{month_digit}{minute_digit}{second_digit}"

    return doctor_id

@app.route('/doctor-profile/<string:doctor_id>', methods=['GET', 'POST'])
def doctor_profile(doctor_id):
    # Retrieve the doctor's details based on the doctor ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM registered_doctors WHERE Doctor_ID = %s", (doctor_id,))
    row = cur.fetchone()

    column_names = [desc[0] for desc in cur.description]  # Get the column names
    doctor_data = dict(zip(column_names, row))

    # Filter out None values from the doctor_data dictionary
    doctor_data = {k: v for k, v in doctor_data.items() if v is not None}
    cur.close()

    # Check if the 'Fee' key is present in the dictionary
    if 'Fee' in doctor_data:
        if doctor_data['Fee'] is not None:
            doctor_fee = float(doctor_data['Fee'])
        else:
            doctor_fee = 0.0
    else:
        doctor_fee = 100.0

    today_date = date.today()

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    # Check user
    l = ['patient', 'doctor', 'admin']
    if session.get('user_type') not in l:
        return render_template('doctor-profile-non-user.html', today_date=today_date, doctor=doctor_data, doctor_fee=doctor_fee, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    # Render the appointment booking form with the doctor's details and today's date
    return render_template('doctor-profile.html', today_date=today_date, doctor=doctor_data, doctor_fee=doctor_fee, name=name, profile=profile, user=user, url=url, dashboard=dashboard)


@app.route('/doctor-dashboard')
def doctor_dashboard():
    if session['user_type'] == 'doctor':
        email = session['email']  # Retrieve the logged-in doctor's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_doctors WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        column_names = [desc[0] for desc in cur.description]  # Get the column names
        doctor_data = dict(zip(column_names, row))
        cur.close()

        # Check if the 'Profile_URL' key exists in the row_dict dictionary
        if 'Profile_URL' in doctor_data and doctor_data['Profile_URL'] is not None:
            session['profile_pms'] = 'doctors/' + doctor_data['Profile_URL']
        if 'Name' in doctor_data and doctor_data['Name'] is not None:
            session['name_pms'] = doctor_data['Name']

        # Get user information from the session
        name = session.get('name_pms')
        profile = session.get('profile_pms')
        user = session.get('user_pms')
        url = session.get('url_pms')
        dashboard = session.get('dashboard_pms')

        doctor_id = doctor_data['Doctor_ID']

        cur = mysql.connection.cursor()
        query = """
            SELECT appointments.*, registered_patients.Name AS Patient_Name, registered_patients.Profile_URL AS Profile_URL, registered_patients.Patient_ID
            FROM appointments
            JOIN registered_patients ON appointments.Patient_ID = registered_patients.Patient_ID
            WHERE Doctor_ID = %s
        """
        cur.execute(query, (doctor_id,))
        rows = cur.fetchall()
        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of appointment data dictionaries
        appointment_data_list = []
        for row in rows:
            appointment_data = dict(zip(column_names, row))
            # Filter out None values from the appointment_data dictionary
            appointment_data = {k: v for k, v in appointment_data.items() if v is not None}
            appointment_data_list.append(appointment_data)

        cur.close()
        total_patient = len(rows)


        today_date = date.today()  # Get the current date
        amount_paid = "--"

        # Split appointments into today's patients and upcoming patients
        today_patients = []
        upcoming_patients = []
        for appointment in appointment_data_list:
            appointment_date = appointment['Appointment_Date']
            if appointment_date == today_date:
                today_patients.append(appointment)
            elif appointment_date > today_date:
                upcoming_patients.append(appointment)

        total_today_patients = len(today_patients)
        total_upcoming_patients = len(upcoming_patients)



        # Render the doctor dashboard template
        return render_template('doctor-dashboard.html',amount_paid=amount_paid, today_date=today_date, total_upcoming_patients=total_upcoming_patients, total_today_patients=total_today_patients, doctor_data=doctor_data, today_patients=today_patients, upcoming_patients=upcoming_patients, total_patient=total_patient, name=name, profile=profile, user=user, url=url, dashboard=dashboard)
    else:
        session['error'] = "You are not an authorized doctor. Only authorized doctors have access to this page."
        return redirect(url_for('unauthorized'))



@app.route('/doctor-profile-settings', methods=['GET', 'POST'])
def doctor_profile_settings():
    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    if session['user_type'] == 'doctor':
        if request.method == 'POST':
            # Get the updated doctor data from the form
            name = request.form['name']
            phone = request.form['phone']
            qualification = request.form['qualification']
            specialization = request.form['specialization']
            clinic_name = request.form['clinic_name']
            clinic_address = request.form['clinic_address']
            fees = request.form['fees']
            about_clinic = request.form['about_clinic']
            address_line1 = request.form['address_line1']
            address_line2 = request.form['address_line2']
            city = request.form['city']
            state = request.form['state']
            registration_number = request.form['registration_number']
            year = request.form['year']
            email = session['email']  # Retrieve the logged-in doctor's email from the session

            # Construct the SQL query and parameters based on the updated fields
            query = "UPDATE registered_doctors SET"
            params = []

            if name:
                query += " Name = %s,"
                params.append(name)

            if phone:
                query += " Phone = %s,"
                params.append(phone)

            if qualification:
                query += " Qualification = %s,"
                params.append(qualification)

            if specialization:
                query += " Specialization = %s,"
                params.append(specialization)

            if clinic_name:
                query += " Clinic_Name = %s,"
                params.append(clinic_name)

            if fees:
                query += " Fee = %s,"
                params.append(fees)

            if clinic_address:
                query += " Clinic_Address = %s,"
                params.append(clinic_address)

            if about_clinic:
                query += " About_Clinic = %s,"
                params.append(about_clinic)

            if address_line1:
                query += " Address_Line1 = %s,"
                params.append(address_line1)

            if address_line2:
                query += " Address_Line2 = %s,"
                params.append(address_line2)

            if city:
                query += " City = %s,"
                params.append(city)

            if state:
                query += " State = %s,"
                params.append(state)

            if registration_number:
                query += " Registration_Number = %s,"
                params.append(registration_number)

            if year:
                query += " Year = %s,"
                params.append(year)

            # Remove the trailing comma from the query
            query = query.rstrip(',')

            # Add the WHERE clause to update the specific doctor's record
            query += " WHERE Email = %s"
            params.append(email)

            # Update the doctor data in the database
            cur = mysql.connection.cursor()
            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()

            # Handle image upload
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    email = session['email']
                    cur = mysql.connection.cursor()
                    # Generate a secure filename and specify the upload folder path
                    filename = secure_filename(session['doctor_id'] + os.path.splitext(photo.filename)[1])
                    upload_folder = os.path.join(app.root_path, 'static', 'assets', 'img', 'doctors')

                    # Save the uploaded image with the doctor_id as the filename
                    photo.save(os.path.join(upload_folder, filename))

                    # Update the image filename in the database
                    cur = mysql.connection.cursor()
                    query = "UPDATE registered_doctors SET Profile_URL = %s WHERE Email = %s"
                    cur.execute(query, (filename, email))
                    mysql.connection.commit()
                    cur.close()

            # Redirect to the doctor dashboard or any other appropriate page
            return redirect(url_for('doctor_dashboard'))

        # Retrieve the doctor's data from the database for display
        email = session['email']  # Retrieve the logged-in doctor's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_doctors WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        if row:
            column_names = [desc[0] for desc in cur.description]  # Get the column names
            doctor_data = dict(zip(column_names, row))

            # Filter out None values from the doctor_data dictionary
            doctor_data = {k: v for k, v in doctor_data.items() if v is not None}

            session['doctor_id'] = doctor_data['Doctor_ID']
            cur.close()

            # Render the doctor profile settings template with the doctor's data
            return render_template('doctor-profile-settings.html', doctor_data=doctor_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)


    else:
        session['error'] = "You are not an authorized doctor. Only authorized doctors have access to this page."
        return redirect(url_for('unauthorized'))


@app.route('/doctor-change-password', methods=['GET', 'POST'])
def doctor_change_password():
    if session.get('user_type') != 'doctor':
        session['error'] = "You are not an authorized doctor. Only authorized doctors have access to this page."
        return redirect(url_for('unauthorized'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    # Retrieve the doctor's data from the database for display
    email = session['email']  # Retrieve the logged-in doctor's email from the session
    cur = mysql.connection.cursor()
    query = "SELECT * FROM registered_doctors WHERE Email = %s"
    cur.execute(query, (email,))
    row = cur.fetchone()

    column_names = [desc[0] for desc in cur.description]  # Get the column names
    doctor_data = dict(zip(column_names, row))
    session['old_password'] = doctor_data['Password']
    cur.close()

    if request.method == 'POST':
        # Access the form data
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Perform validation
        # Example: Check if the old password matches the current password for the doctor
        if old_password != session['old_password']:
            error_message = "Old password is incorrect."
            return render_template('doctor-change-password.html', error=error_message,doctor_data=doctor_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Example: Check if the new password meets the desired criteria
        if new_password != confirm_password:
            error_message = "New password and confirm password do not match."
            return render_template('doctor-change-password.html', error=error_message,doctor_data=doctor_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Update the password in the database for the doctor
        doctor_id = doctor_data['Doctor_ID']
        update_password_in_d_database(doctor_id, new_password)

        success_message = "Password changed successfully."
        return render_template('doctor-change-password.html', error=success_message,doctor_data=doctor_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    return render_template('doctor-change-password.html', doctor_data=doctor_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

def update_password_in_d_database(doctor_id, new_password):
    cur = mysql.connection.cursor()
    query = "UPDATE registered_doctors SET Password = %s WHERE Doctor_ID = %s"
    cur.execute(query, (new_password, doctor_id))
    mysql.connection.commit()
    cur.close()


# ------------------------------------------------------------------------------------------------------------------------------

# ADMINS RECORDS:

# ------------------------------------------------------------------------------------------------------------------------------

@app.route("/admin-register", methods=['GET', 'POST'])
def admin_register():
    if session['user_type'] == 'admin':
        email = session['email']  # Retrieve the logged-in admin's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_admins WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        column_names = [desc[0] for desc in cur.description]  # Get the column names
        admin_data = dict(zip(column_names, row))
        cur.close()

        # Check if the 'Profile_URL' key exists in the row_dict dictionary
        if 'Profile_URL' in admin_data and admin_data['Profile_URL'] is not None:
            session['profile_pms'] = 'admins/' + admin_data['Profile_URL']
        if 'Name' in admin_data and admin_data['Name'] is not None:
            session['name_pms'] = admin_data['Name']

        # Get user information from the session
        name = session.get('name_pms')
        profile = session.get('profile_pms')
        user = session.get('user_pms')
        url = session.get('url_pms')
        dashboard = session.get('dashboard_pms')


        if request.method == 'POST':
            full_name = request.form["fullname"]
            email = request.form["email"]
            phone_no = request.form["phone"]
            password = request.form["password"]

            # Regular expression patterns
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            phone_pattern = r'^\d{10}$'
            password_pattern = r'^.{8,}$'

            # Validate email
            if not re.match(email_pattern, email):
                error_message = "Invalid email address. Please enter a valid email."
                return render_template("admin-register.html", error=error_message, admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

            # Validate phone number
            if not re.match(phone_pattern, phone_no):
                error_message = "Invalid phone number. Please enter a 10-digit phone number."
                return render_template("admin-register.html", error=error_message,admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

            # Validate password
            if not re.match(password_pattern, password):
                error_message = "Invalid password. Password should be at least 8 characters long."
                return render_template("admin-register.html", error=error_message,admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

            # Check if the admin already exists in the database
            cur = mysql.connection.cursor()
            query = "SELECT * FROM registered_admins WHERE Email = %s OR Phone = %s"
            cur.execute(query, (email, phone_no))
            row = cur.fetchone()

            if row is not None:
                column_names = [desc[0] for desc in cur.description]  # Get the column names
                admin_data = dict(zip(column_names, row))
                cur.close()
                # Check if email or phone number is already registered
                if admin_data['Email'] == email:
                    error_message = "Email is already registered."
                else:
                    error_message = "Phone number is already registered."
                return render_template("admin-register.html", error=error_message,admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)
            cur.close()

            # Generate a unique admin ID
            admin_id = generate_admin_id(full_name)

            # Register the admin if not already registered
            cur = mysql.connection.cursor()
            query = "INSERT INTO registered_admins (Name, Email, Phone, Password, Admin_ID) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (full_name, email, phone_no, password, admin_id))

            mysql.connection.commit()
            cur.close()

            success_message = "Admin Registered Successful"

            return render_template("admin-register.html", error=success_message,admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        return render_template("admin-register.html",admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)


    else:
        session['error'] = "You are not an authorized admin. Only authorized admins have access to this page."
        return redirect(url_for('unauthorized'))


def generate_admin_id(full_name):
    # Generate random digits
    random_digits = ''.join(random.choices(string.digits, k=4))

    # Get the current date and time
    now = datetime.now()
    day_digit = str(now.day)[0]
    month_digit = str(now.month)[0]
    minute_digit = str(now.minute)[0]
    second_digit = str(now.second)[0]

    # Create the admin ID by combining name characters, digits, and the date
    admin_id = f"{full_name[:3].upper()}{random_digits}{day_digit}{month_digit}{minute_digit}{second_digit}"

    return admin_id


@app.route('/admin-dashboard')
def admin_dashboard():
    if session['user_type'] == 'admin':
        email = session['email']  # Retrieve the logged-in admin's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_admins WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        column_names = [desc[0] for desc in cur.description]  # Get the column names
        admin_data = dict(zip(column_names, row))
        cur.close()

        # All Doctors records
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_doctors"
        cur.execute(query)
        rows = cur.fetchall()
        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of doctor data dictionaries
        doctor_data_list = []
        for row in rows:
            doctor_data = dict(zip(column_names, row))
            # Filter out None values from the doctor_data dictionary
            doctor_data = {k: v for k, v in doctor_data.items() if v is not None}
            doctor_data_list.append(doctor_data)

        cur.close()

        # All Patients records
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_patients"
        cur.execute(query)
        rows = cur.fetchall()
        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of patient data dictionaries
        patient_data_list = []
        for row in rows:
            patient_data = dict(zip(column_names, row))
            # Filter out None values from the patient_data dictionary
            patient_data = {k: v for k, v in patient_data.items() if v is not None}
            patient_data_list.append(patient_data)

        cur.close()

        # Check if the 'Profile_URL' key exists in the admin_data dictionary
        if 'Profile_URL' in admin_data and admin_data['Profile_URL'] is not None:
            session['profile_pms'] = 'admins/' + admin_data['Profile_URL']
        if 'Name' in admin_data and admin_data['Name'] is not None:
            session['name_pms'] = admin_data['Name']

        # Get user information from the session
        name = session.get('name_pms')
        profile = session.get('profile_pms')
        user = session.get('user_pms')
        url = session.get('url_pms')
        dashboard = session.get('dashboard_pms')

        admin_id = admin_data['Admin_ID']

        cur = mysql.connection.cursor()
        query = """
            SELECT registered_doctors.Name AS Doctor_Name, registered_doctors.Profile_URL AS Doctor_Profile_URL, registered_doctors.Doctor_ID, registered_doctors.Doctor_ID, registered_doctors.Specialization, registered_patients.Name AS Patient_Name, registered_patients.Profile_URL AS Patient_Profile_URL, registered_patients.Patient_ID, appointments.Appointment_Date, appointments.Appointment_Time
            FROM appointments
            JOIN registered_doctors ON appointments.Doctor_ID = registered_doctors.Doctor_ID
            JOIN registered_patients ON appointments.Patient_ID = registered_patients.Patient_ID
            ORDER BY appointments.Appointment_Date ASC
        """
        cur.execute(query)

        rows = cur.fetchall()
        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Prepare the list of appointment data dictionaries
        appointment_data_list = []
        for row in rows:
            appointment_data = dict(zip(column_names, row))
            # Filter out None values from the appointment_data dictionary
            appointment_data = {k: v for k, v in appointment_data.items() if v is not None}
            appointment_data_list.append(appointment_data)

        cur.close()

        total_appointment = len(appointment_data_list)
        total_doctor = len(doctor_data_list)
        total_patient = len(patient_data_list)
        revenue = total_appointment*2

        # Render the admin dashboard template
        return render_template('admin-dashboard.html',total_appointment=total_appointment, total_patient=total_patient, total_doctor=total_doctor, revenue = revenue, doctor_data_list=doctor_data_list, patient_data_list=patient_data_list, appointment_data_list=appointment_data_list, admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)
    else:
        session['error'] = "You are not an authorized admin. Only authorized admins have access to this page."
        return redirect(url_for('unauthorized'))





@app.route("/admin-profile-settings", methods=['GET', 'POST'])
def admin_profile_settings():
    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    if session['user_type'] == 'admin':
        if request.method == 'POST':
            # Get the updated admin data from the form
            name = request.form['name']
            phone = request.form['phone']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            pincode = request.form['pincode']
            country = request.form['country']
            qualification = request.form['qualification']
            job = request.form['job']

            email = session['email']  # Retrieve the logged-in admin's email from the session

            # Construct the SQL query and parameters based on the updated fields
            query = "UPDATE registered_admins SET"
            params = []

            if name:
                query += " Name = %s,"
                params.append(name)

            if qualification:
                query += " Qualification = %s,"
                params.append(qualification)

            if job:
                query += " Job_Profile = %s,"
                params.append(job)

            if phone:
                query += " Phone = %s,"
                params.append(phone)

            if address:
                query += " Address = %s,"
                params.append(address)

            if city:
                query += " City = %s,"
                params.append(city)

            if state:
                query += " State = %s,"
                params.append(state)

            if pincode:
                query += " Pin_Code = %s,"
                params.append(pincode)

            if country:
                query += " Country = %s,"
                params.append(country)

            # Remove the trailing comma from the query
            query = query.rstrip(',')

            # Add the WHERE clause to update the specific admin's record
            query += " WHERE Email = %s"
            params.append(email)

            # Update the admin data in the database
            cur = mysql.connection.cursor()
            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()

            # Handle image upload
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    email = session['email']
                    cur = mysql.connection.cursor()
                    # Generate a secure filename and specify the upload folder path
                    filename = secure_filename(session['admin_id'] + os.path.splitext(photo.filename)[1])
                    upload_folder = os.path.join(app.root_path, 'static', 'assets', 'img', 'admins')

                    # Save the uploaded image with the admin_id as the filename
                    photo.save(os.path.join(upload_folder, filename))

                    # Update the image filename in the database
                    query = "UPDATE registered_admins SET Profile_URL = %s WHERE Email = %s"
                    cur.execute(query, (filename, email))
                    mysql.connection.commit()
                    cur.close()

            # Redirect to the admin dashboard or any other appropriate page
            return redirect(url_for('admin_dashboard'))

        # Retrieve the admin's data from the database for display
        email = session['email']  # Retrieve the logged-in admin's email from the session
        cur = mysql.connection.cursor()
        query = "SELECT * FROM registered_admins WHERE Email = %s"
        cur.execute(query, (email,))
        row = cur.fetchone()

        if row:
            column_names = [desc[0] for desc in cur.description]  # Get the column names
            admin_data = dict(zip(column_names, row))

            # Filter out None values from the admin_data dictionary
            admin_data = {k: v for k, v in admin_data.items() if v is not None}

            session['admin_id'] = admin_data['Admin_ID']
            cur.close()

            # Render the admin profile settings template with the admin's data
            return render_template('admin-profile-settings.html', admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    else:
        session['error'] = "You are not an authorized admin. Only authorized admins have access to this page."
        return redirect(url_for('unauthorized'))



@app.route('/admin-change-password', methods=['GET', 'POST'])
def admin_change_password():
    if session.get('user_type') != 'admin':
        session['error'] = "You are not an authorized admin. Only authorized admins have access to this page."
        return redirect(url_for('unauthorized'))

    # Get user information from the session
    name = session.get('name_pms')
    profile = session.get('profile_pms')
    user = session.get('user_pms')
    url = session.get('url_pms')
    dashboard = session.get('dashboard_pms')

    # Retrieve the admin's data from the database for display
    email = session['email']  # Retrieve the logged-in admin's email from the session
    cur = mysql.connection.cursor()
    query = "SELECT * FROM registered_admins WHERE Email = %s"
    cur.execute(query, (email,))
    row = cur.fetchone()

    column_names = [desc[0] for desc in cur.description]  # Get the column names
    admin_data = dict(zip(column_names, row))
    session['old_password'] = admin_data['Password']
    cur.close()

    if request.method == 'POST':
        # Access the form data
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Perform validation
        # Example: Check if the old password matches the current password for the admin
        if old_password != session['old_password']:
            error_message = "Old password is incorrect."
            return render_template('admin-change-password.html', error=error_message, admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Example: Check if the new password meets the desired criteria
        if new_password != confirm_password:
            error_message = "New password and confirm password do not match."
            return render_template('admin-change-password.html', error=error_message, admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

        # Update the password in the database for the admin
        admin_id = admin_data['Admin_ID']
        update_password_in_p_database(admin_id, new_password)

        success_message = "Password changed successfully."
        return render_template('admin-change-password.html', error=success_message, admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

    return render_template('admin-change-password.html', admin_data=admin_data, name=name, profile=profile, user=user, url=url, dashboard=dashboard)

def update_password_in_p_database(admin_id, new_password):
    cur = mysql.connection.cursor()
    query = "UPDATE registered_admins SET Password = %s WHERE Admin_ID = %s"
    cur.execute(query, (new_password, admin_id))
    mysql.connection.commit()
    cur.close()





# -----------------------------------------------------------------------------------------------------------------------------


# LOGIN RECORDS:

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        # User is already logged in, redirect to a logged-in page
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        user_type = request.form['user_type']
        password = request.form['password']

        if user_type == 'patient':
            session['user_type'] = 'patient'
            # Check if the user exists in the registered_patients table
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM registered_patients WHERE Email = %s", (email,))
            row = cur.fetchone()

            if row is None:
                # User not found, display an error message
                error_message = "User not found. Please Signup."
                cur.close()
                return render_template('login.html', error=error_message)

            # Create a dictionary using column names as keys
            columns = [desc[0] for desc in cur.description]
            row_dict = dict(zip(columns, row))
            row_dict = {k: v for k, v in row_dict.items() if v is not None}

            # Check if the password is correct
            if password != row_dict.get('Password'):
                # Incorrect password, display an error message
                error_message = "Invalid credentials. Please try again."
                cur.close()
                return render_template('login.html', error=error_message)

            # Password is correct, continue with the authentication process for the patient

            # Store user information in the session
            session['loggedin'] = True
            session['user_type'] = 'patient'
            session['email'] = email

            # Check if the 'Profile_URL' key exists in the row_dict dictionary
            if 'Profile_URL' in row_dict:
                session['profile_pms'] = 'patients/' + row_dict['Profile_URL']
            else:
                session['profile_pms'] = 'patients/default.png'  # Provide a default value or handle the case when the key is missing
            if 'Date_of_Birth' in row_dict:
                session['dob_pms'] = row_dict['Date_of_Birth']
            if 'City' in row_dict:
                session['city_pms'] = row_dict['City']
            if 'State' in row_dict:
                session['state_pms'] = row_dict['State']

            session['patient_id'] = row_dict['Patient_ID']
            session['name_pms'] = row_dict['Name']
            session['patient_email'] = row_dict['Email']
            session['user_pms'] = 'Patient'
            session['url_pms'] = '/patient-profile-settings'
            session['dashboard_pms'] = '/patient-dashboard'

            cur.close()

            # Redirect to the patient dashboard
            return redirect(url_for('patient_dashboard'))

        elif user_type == 'doctor':
            session['user_type'] = 'doctor'
            # Check if the user exists in the registered_doctors table
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM registered_doctors WHERE Email = %s", (email,))
            row = cur.fetchone()

            if row is None:
                # User not found, display an error message
                error_message = "User not found. Please Signup."
                cur.close()
                return render_template('login.html', error=error_message)

            # Create a dictionary using column names as keys
            columns = [desc[0] for desc in cur.description]
            row_dict = dict(zip(columns, row))
            row_dict = {k: v for k, v in row_dict.items() if v is not None}

            # Check if the password is correct
            if password != row_dict.get('Password'):
                # Incorrect password, display an error message
                error_message = "Invalid credentials. Please try again."
                cur.close()
                return render_template('login.html', error=error_message)

            # Password is correct, continue with the authentication process for the doctor

            # Store user information in the session
            session['loggedin'] = True
            session['user_type'] = 'doctor'
            session['email'] = email

            # Save some data for all pages
            # Check if the 'Profile_URL' key exists in the row_dict dictionary
            if 'Profile_URL' in row_dict:
                session['profile_pms'] = 'doctors/' + row_dict['Profile_URL']
            else:
                session['profile_pms'] = 'doctors/default.png'  # Provide a default value or handle the case when the key is missing
            if 'Qualification' in row_dict:
                session['qualification_pms'] = row_dict['Qualification']
            if 'Specialization' in row_dict:
                session['specialization_pms'] = row_dict['Specialization']

            session['name_pms'] = row_dict['Name']
            session['user_pms'] = 'Doctor'
            session['url_pms'] = '/doctor-profile-settings'
            session['dashboard_pms'] = '/doctor-dashboard'

            cur.close()

            return redirect(url_for('doctor_dashboard'))

        elif user_type == 'admin':
            session['user_type'] = 'admin'
            # Check if the user exists in the registered_admins table
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM registered_admins WHERE Email = %s", (email,))
            row = cur.fetchone()

            if row is None:
                # User not found, display an error message
                error_message = "User not found. Please Signup."
                cur.close()
                return render_template('login.html', error=error_message)

            # Create a dictionary using column names as keys
            columns = [desc[0] for desc in cur.description]
            row_dict = dict(zip(columns, row))
            row_dict = {k: v for k, v in row_dict.items() if v is not None}

            # Check if the password is correct
            if password != row_dict.get('Password'):
                # Incorrect password, display an error message
                error_message = "Invalid credentials. Please try again."
                cur.close()
                return render_template('login.html', error=error_message)

            # Password is correct, continue with the authentication process for the admin

            # Store user information in the session
            session['loggedin'] = True
            session['user_type'] = 'admin'
            session['email'] = email

            # Check if the 'Profile_URL' key exists in the row_dict dictionary
            if 'Profile_URL' in row_dict:
                session['profile_pms'] = 'admins/' + row_dict['Profile_URL']
            else:
                session['profile_pms'] = 'admins/default.png'  # Provide a default value or handle the case when the key is missing
            if 'Qualification' in row_dict:
                session['qualification_pms'] = row_dict['Qualification']
            if 'Job_Profile' in row_dict:
                session['job_profile_pms'] = row_dict['Job_Profile']

            session['name_pms'] = row_dict['Name']
            session['user_pms'] = 'Admin'
            session['url_pms'] = '/admin-profile-settings'
            session['dashboard_pms'] = '/admin-dashboard'
            session['Admin_ID'] = row_dict['Admin_ID']


            cur.close()

            # Redirect to the admin dashboard
            return redirect(url_for('admin_dashboard'))

    # Render the login template
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the login page
    return redirect(url_for('home'))



# Generate OTP
def generate_otp():
    # Generate a 4-digit OTP
    otp = ''.join(random.choices(string.digits, k=4))
    return otp


def send_otp_email(email, otp):
    msg = Message("OTP for Password Reset", recipients=[email])
    msg.body = f"Your OTP for password reset is: {otp}"
    mail.send(msg)


@app.route('/resend-otp', methods=['GET', 'POST'])
def resend_otp():
    # Generate a new OTP
    new_otp = generate_otp()

    # Update the session with the new OTP
    session['otp'] = new_otp

    # Send the OTP to the user's email
    send_otp_email(session['email'], new_otp)

    success_message = "OTP has been resent"

    # Return a response indicating success
    return render_template('email-otp.html', error=success_message)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if 'loggedin' in session:
        # User is already logged in, redirect to a logged-in page
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        user_type = request.form['user_type']

        cur = mysql.connection.cursor()

        if user_type == 'patient':
            session['user_type'] = 'patient'
            # Check if the user exists in the registered_patients table
            cur.execute("SELECT * FROM registered_patients WHERE Email = %s", (email,))
            row = cur.fetchone()

        elif user_type == 'doctor':
            session['user_type'] = 'doctor'
            # Check if the user exists in the registered_doctors table
            cur.execute("SELECT * FROM registered_doctors WHERE Email = %s", (email,))
            row = cur.fetchone()

        elif user_type == 'admin':
            session['user_type'] = 'admin'
            # Check if the user exists in the registered_admins table
            cur.execute("SELECT * FROM registered_admins WHERE Email = %s", (email,))
            row = cur.fetchone()

        if row is None:
            # User not found, display an error message
            error_message = "Account not found. Please Signup."
            cur.close()
            return render_template('forgot-password.html', error=error_message)

        # Generate OTP
        otp = generate_otp()

        # Store user information in the session
        session['email'] = email
        session['otp'] = otp

        cur.close()

        # Send OTP via email
        send_otp_email(email, otp)


        return redirect(url_for('email_otp_verification'))

    return render_template('forgot-password.html')


@app.route('/email-otp-verification', methods=['GET', 'POST'])
def email_otp_verification():
    if 'email' not in session:
        # Email not found in session, redirect to the forgot password page
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        entered_otp = request.form['digit-1'] + request.form['digit-2'] + request.form['digit-3'] + request.form['digit-4']

        if 'otp' not in session:
            # OTP not found in session, redirect to the forgot password page
            return redirect(url_for('forgot_password'))

        if entered_otp == session['otp']:
            # OTP is correct, allow the user to reset the password
            return redirect(url_for('reset_password'))

        # OTP is incorrect, display an error message
        error_message = "Invalid OTP. Please try again."
        return render_template('email-otp.html', error=error_message)

    return render_template('email-otp.html', email=session['email'])


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'email' not in session:
        # Email not found in session, redirect to the forgot password page
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            # Passwords do not match, display an error message
            error_message = "Passwords do not match. Please try again."
            return render_template('reset-password.html', error=error_message)

        # Validate password
        password_pattern = r'^.{8,}$'
        if not re.match(password_pattern, password):
            error_message = "Invalid password. Password should be at least 8 characters long."
            return render_template('reset-password.html', error=error_message)

        # Update the user's password in the database
        user_type = session.get('user_type')
        email = session.get('email')

        cur = mysql.connection.cursor()

        if user_type == 'patient':
            # Update the password for patient user type
            cur.execute("UPDATE registered_patients SET Password = %s WHERE Email = %s", (password, email))

        elif user_type == 'doctor':
            # Update the password for doctor user type
            cur.execute("UPDATE registered_doctors SET Password = %s WHERE Email = %s", (password, email))

        elif user_type == 'admin':
            # Update the password for admin user type
            cur.execute("UPDATE registered_admins SET Password = %s WHERE Email = %s", (password, email))

        mysql.connection.commit()
        cur.close()

        # Password reset successful, redirect to login page
        return render_template('password-changed-successful.html')

    # Render the reset-password template
    return render_template('reset-password.html')


@app.route('/contact-form', methods=['POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        services = request.form.get('services')
        message = request.form.get('message')

        # Create the email message
        subject = 'New Contact Form Submission'
        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nServices: {services}\nMessage: {message}"
        recipients = ['pranikmedicalservices@gmail.com']

        # Send the email
        msg = Message(subject=subject, body=body, recipients=recipients)
        mail.send(msg)

        return 'Message sent successfully'
    return redirect(url_for('contact'))


# ------------------------------------------------------------------------------------------------------------------------------





if __name__ == "__main__":
    #app.run(ssl_context='adhoc')
    app.run()
