from flask import Flask, render_template, request
from abg import ABGInterpreter

app = Flask(__name__)

# home
@app.route('/')
def index():
    return render_template('index.html')

# interpretation results static page
@app.route('/interpret', methods=['POST'])
def interpret():
    interpreter = ABGInterpreter(float(request.form['ph']), float(request.form['co2']), float(request.form['hco3']), float(request.form['potassium']), float(request.form['spo2']))
    interpreter.ph_classifier()
    main_res = interpreter.main_interpretation()
    potassium_res = interpreter.peripheral_interpretation()[0]
    spo2_res = interpreter.peripheral_interpretation()[1]
    return render_template('results.html', main_res=main_res, potassium_res=potassium_res, spo2_res=spo2_res)

if __name__ == '__main__':
    app.run(debug=True)