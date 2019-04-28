from flask import Flask, render_template, request
from before_dashboard_code import compute_price_increase

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        distance = float(request.form['distance'])
        age = float(request.form['age'])
        population = float(request.form['population'])
        energy_rating = int(request.form['energy_rating'])
        result = compute_price_increase(
            distance, age, population, energy_rating)

        return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
