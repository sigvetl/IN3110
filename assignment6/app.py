from flask import Flask, Response, render_template, request, redirect, url_for
from web_visualization import plot_reported_cases, plot_cumulative_cases, plot_both
import altair as alt
import tempfile

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def menu():
    #lag en meny som sender videre til sidene
    if request.method == "POST":
        county = request.form.get('county')
        return render_template("chart.html", county=county)
    return render_template('chart.html', county='All counties')

@app.route("/plot.json/<county>")
def plot_layered(county):

    chart = plot_both(county)
    tmp = tempfile.NamedTemporaryFile(suffix='.json')
    chart.save(tmp.name)
    with open(tmp.name) as file:
        return file.read()

"""
@app.route("/reported_cases")
def plot_cases():
    chart = plot_reported_cases(request.args.get('county'))
    chart.save("templates/cases.html")
    return render_template('cases.html')

@app.route("/cumulative_cases")
def plot_cumulative():
    chart = plot_cumulative_cases(request.args.get('county'))
    chart.save("templates/cumulative.html")
    return render_template('cumulative.html')

@app.route("/both_cases")

    chart = plot_both(request.args.get('county'))
    chart.save("templates/both.html")
    return render_template('both.html')
"""


if __name__ =="__main__":
    app.run(debug=True)
