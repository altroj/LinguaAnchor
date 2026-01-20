import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a sample German text file if it doesn't exist
SAMPLE_TEXT_PATH = os.path.join(UPLOAD_FOLDER, 'sample.md')
if not os.path.exists(SAMPLE_TEXT_PATH):
    with open(SAMPLE_TEXT_PATH, 'w', encoding='utf-8') as f:
        f.write("Das ist ein einfacher deutscher Text. Wir lernen Sprachen.")

@app.route('/', methods=['GET', 'POST'])
def index():
    content = ""
    
    # 1. Handle File Uploads
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                # Read the uploaded file immediately
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
    
    # 2. If no upload, load the sample text or the last uploaded text
    if not content:
        # For this demo, we always default to sample.md if nothing is POSTed
        with open(SAMPLE_TEXT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

    return render_template('index.html', text_content=content)

if __name__ == '__main__':
    app.run(debug=True)