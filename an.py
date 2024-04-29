from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from anpr import recognize_plate

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Aryan'
app.config['MYSQL_PASSWORD'] = 'aryan'
app.config['MYSQL_DB'] = 'ANPR'

mysql = MySQL(app)

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and processing
@app.route('/recognize_plate', methods=['POST'])
def recognize_plate_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    username = request.form.get('username')
    status = request.form.get('status')

    plate_number = recognize_plate(image_file)

    # Insert data into MySQL database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO anpr_table (username, status, plate_number) VALUES (%s, %s, %s)", (username, status, plate_number))
    mysql.connection.commit()
    cur.close()

    return jsonify({'username': username, 'status': status, 'plate_number': plate_number}), 200

# Route to display data from the database
@app.route('/display_data')
def display_data():
    # Fetch data from the MySQL database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM anpr_table")
    data = cur.fetchall()
    print(data)  # Add this line for debug output
    cur.close()
    
    # Render HTML template with the fetched data
    return render_template('display_data.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
