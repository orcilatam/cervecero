from flask import Flask, render_template, request
import modelos.clase4

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/predictor", methods = ['POST'])
def predictor():
	X_n = int(request.form['X_n'])
	x_input = float(request.form['x_input'])
	y_hat = modelos.clase4.resultado(X_n, x_input)
	return render_template('predictor.html', y_hat = y_hat)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 9090)
