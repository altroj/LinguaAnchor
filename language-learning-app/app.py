import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
LIBRARY_FOLDER = os.path.join('library', 'german')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LIBRARY_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LIBRARY_FOLDER'] = LIBRARY_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    # 1. List available German texts in the library
    library_files = [f for f in os.listdir(app.config['LIBRARY_FOLDER']) if f.endswith('.md')]
    
    text_content = ""
    source_type = "none" # 'library', 'upload', or 'none'

    # 2. Handle File Uploads (User's own text)
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                with open(filepath, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                source_type = 'upload'

    # 3. Handle Library Selection (User clicked a text from the list)
    selected_file = request.args.get('text')
    if selected_file:
        filepath = os.path.join(app.config['LIBRARY_FOLDER'], selected_file)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                text_content = f.read()
            source_type = 'library'

    return render_template('index.html', 
                           text_content=text_content, 
                           library_files=library_files,
                           source_type=source_type)

if __name__ == '__main__':
    app.run(debug=True)