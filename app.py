from flask import Flask, render_template, request
import barcode
from barcode.writer import ImageWriter
from pathlib import Path

app = Flask(__name__)

def generate_barcode(data, dpi, name):
    code = barcode.get_barcode_class('code128')
    code_instance = code(data, writer=ImageWriter())
    save_path = Path('static') / f'{name}'
    code_instance.save(save_path, {"dpi": dpi})
    return save_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['data']
    dpi = int(request.form['dpi'])
    name = request.form['name']

    if not data:
        return render_template('index.html', error='Please enter data!')

    try:
        image_path = generate_barcode(data, dpi, name)
        print(f"Image path: {image_path}")  # Add this line for debugging
        return render_template('result.html', image_name=f'{name}.png')
    except Exception as e:
        print(f"Error: {e}")  # Add this line for debugging
        return render_template('index.html', error=f'Error: {e}')


if __name__ == '__main__':
    app.run(debug=True)
