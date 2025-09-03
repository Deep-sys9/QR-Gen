from flask import Flask, render_template, request, redirect, url_for, send_file, session
import qrcode
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session



@app.route('/', methods=['GET'])
def index():
	qr_generated = session.pop('qr_generated', False)
	return render_template('index.html', qr_generated=qr_generated)

@app.route('/generate', methods=['POST'])
def generate():
	text = request.form.get('qrtext')
	if not text:
		return redirect(url_for('index'))
	session['qr_text'] = text
	session['qr_generated'] = True
	return redirect(url_for('index'))

@app.route('/download')
def download():
	text = session.get('qr_text')
	if not text:
		return redirect(url_for('index'))
	img = qrcode.make(text)
	buf = BytesIO()
	img.save(buf, format='PNG')
	buf.seek(0)
	return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

@app.route('/qr_image')
def qr_image():
	text = session.get('qr_text')
	if not text:
		return '', 404
	img = qrcode.make(text)
	buf = BytesIO()
	img.save(buf, format='PNG')
	buf.seek(0)
	return send_file(buf, mimetype='image/png')

# About page
@app.route('/about')
def about():
	return render_template('about.html')

# Donate page
@app.route('/donate')
def donate():
	return render_template('donate.html')

if __name__ == '__main__':
	app.run(debug=True)