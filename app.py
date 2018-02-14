import os
from flask import Flask, request, render_template, url_for, send_from_directory, redirect
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(f)
			return redirect(url_for('uploaded_file', filename=filename))
		else: 
			return ("Invalid file format") 
	else:
		# print("Please upload a valid image file.")
		return render_template('index.html')

@app.route('/show/<filename>')
def uploaded_file(filename):
	return render_template('index.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
	app.run(debug=True)

