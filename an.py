from flask import Flask, render_template, request, jsonify
from anpr import recognize_plate

app = Flask(__name__)

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
    plate_number = recognize_plate(image_file)
    print('asndasdkjashdkjasbdkjas')
    print(plate_number)
    return jsonify({'plate_number': plate_number}), 200

if __name__ == '__main__':
    app.run(debug=True)
