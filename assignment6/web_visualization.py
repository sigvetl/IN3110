"""
This module reads datasets containing covid-19 cases in all counties in Norway
and creates visual representations of the data with altair charts.

The generated plots are visualized on a Flask app.
"""
#This docstring needs to stay on top of the document for documentation with sphinx

import pandas as pd
import sys
import altair as alt
import tempfile
from flask import Flask, Response, render_template, request

def __read_csv(county, start=None, end=None):
    """
    Private function reading the selected csv file (default - antall-meldte-covid-19-allcounties.csv)
    and transforming the data into a panda dataframe.
    Error checks that the selected name is a valid file, checks that the start date is before the end
    date and sets the start and end to first and last value of dataset if a value is not specified.
    Checks that selected dates are available in dataset.

    Args:
        county(str): Name of a county or all counties
        start(str): Start date in the format "%d.%m.%Y"
        end(str): En date in the format "%d.%m.%Y"

    Returns:
        cases(pandas.core.frame.DataFrame): Data from csv-file with the selected date-interval

    Raises:
        FileNotFoundError: Prints an error message if the county cannot be found within the .csv files

        ValueError: Prints a message if the end date is before the start date.
            If the selected values are out of bounds with the values in the .csv file,
            a message with the interval to be selected from are printed.
            If the format of the suplied date does not correspond with the format,
            the format and an example are printed.
    """
    try:
        county = county.lower().replace(" ", "")
        print(county)
        cases = pd.read_csv(
            f"data/antall-meldte-covid-19-{county}.csv",
            sep=";",
            parse_dates=["Dato"],
            date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"))

    except FileNotFoundError:
        errormsg = "\n\033[1mNot a valid selection. Please select one of the following:\033[0m\n\n"\
        +"All counties\nAgder\nInnlandet\nMøre og Romsdal\nNordland\nOslo\nRogaland\n"\
        +"Troms og Finnmark\nTrøndelag\nVestfold og Telemark\nVestland\nViken"
        print(errormsg)
        sys.exit(1)

    try:
        startdate = pd.to_datetime(start, format="%d.%m.%Y")
        enddate = pd.to_datetime(end, format="%d.%m.%Y")

        if start and end and startdate > enddate:
            print("End date must be after start date")
            raise ValueError

        if start==None:
            startdate = cases["Dato"].iloc[0]
        if end==None:
            enddate = cases["Dato"].iloc[-1]

        if not (((startdate >= cases["Dato"].iloc[0]) and (startdate < cases["Dato"].iloc[-1]))
        and ((enddate > cases["Dato"].iloc[0]) and (enddate <= cases["Dato"].iloc[-1]))):
            print("Data does not exist for selected data range.\n"
            + f"Please choose a date range from {cases['Dato'].iloc[0]} to {cases['Dato'].iloc[-1]}")
            raise ValueError

    except ValueError:
        print("Please enter valid dates for start and end in the format \"%d.%m.%Y\", e.g 20.03.2020")
        sys.exit(1)

    #global int representing number of dates in dataset. Is used within the plotting functions to
    #select spacing of the plot
    global n
    n = cases.Dato.size

    return cases.loc[(cases["Dato"] >= startdate) & (cases["Dato"] <= enddate)]

def __read_csv_map():
    """
    Private function that reads the .csv file containing the number of cases per 100k inhabitants

    Returns:
        data(pandas.core.frame.DataFrame): The data contained in the .csv file

    Raises:
        FileNotFoundError: Prints a message and exits if the file is not found.
    """
    try:
        data = pd.read_csv(
            "data/antall-meldte-tilfeller.csv",
            sep=";")
    except FileNotFoundError:
        print("Not a valid file")
        sys.exit(1)

    return data

def norway_plot():
    """
    Makes a map plot of norway with the data of number of cases per 100k inhabitants in each county

    Returns:
        (Altair.Chart): A chart in the form of a map with the number of cases per 100k
            in each county visualized with color.
    """
    df = __read_csv_map()
    #transform Insidens into float
    df["Insidens"] = pd.to_numeric(df["Insidens"].str.replace(",", "."))
    counties = alt.topo_feature("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/norway/norway-new-counties.json", "Fylker")
    nearest = alt.selection(type="single", on="mouseover", fields=["properties.navn"], empty="none")

    fig = alt.Chart(counties).mark_geoshape().encode(
	tooltip=[
	    alt.Tooltip("properties.navn:N", title="County"),
	    alt.Tooltip("Insidens:Q", title="Cases per 100k capita"),
	],
    color=alt.Color("Insidens:Q", scale=alt.Scale(scheme="reds"),
	   legend=alt.Legend(title="Cases per 100k capita")),
	stroke=alt.condition(nearest, alt.value("gray"), alt.value(None)),
	opacity=alt.condition(nearest, alt.value(1), alt.value(0.8)),
    ).transform_lookup(
	lookup="properties.navn",
	from_=alt.LookupData(df, "Category", ["Insidens"])
    ).properties(
	width=500,
	height=600,
	title="Number of cases per 100k in every county",
    ).add_selection(nearest)

    return fig

def plot_reported_cases(county="all counties", start=None, end=None):
    """
    Gets a dataframe by calling __read_csv with the selected arguments.
    Turns this data into a plot of new cases over dates.

    Args:
        county(str): Name of a county or all counties. Default value is all counties.
        start(str): Start date in the format "%d.%m.%Y". Default value is None and translates to first date in dataset.
        end(str): En date in the format "%d.%m.%Y". Default value is None and translates to first date in dataset.
    Returns:
        (Altair.Chart): A chart with the number of cases plotted against the dates.
    """
    cases = __read_csv(county, start, end)
    nearest_bar = alt.selection(type='single', on='mouseover',
                        fields=['Dato'], empty='none')
    chart = alt.Chart(cases).mark_bar(opacity=0.8, size=n/len(cases)+1).encode(
        alt.X('Dato', title='Date'),
        alt.Y('Nye tilfeller', title='New cases'),
        tooltip=[alt.Tooltip('Dato', title='Date'), alt.Tooltip('Nye tilfeller', title='New cases')],
        opacity=alt.condition(nearest_bar, alt.value(1), alt.value(0.8))
    ).properties(title=f"Number of reported COVID-19 cases in {county} by specimen collection date",
        width=600,
        height=500
    ).add_selection(nearest_bar)

    return chart

def plot_cumulative_cases(county="all counties", start=None, end=None):
    """
    Gets a dataframe by calling __read_csv with the seelcted arguments.
    Creates a plot of cumulative cases over dates.

    Args:
        county(str): Name of a county or all counties.
            Default value is all counties.
        start(str): Start date in the format "%d.%m.%Y".
            Default value is None and translates to first date in dataset.
        end(str): En date in the format "%d.%m.%Y".
            Default value is None and translates to first date in dataset.
    Returns:
        (Altair.Chart): A chart with the cumulative number of cases plotted against the dates.
    """
    cases = __read_csv(county, start, end)
    nearest_line = alt.selection(type='single', on='mouseover',
                        fields=['Dato'], empty='none')
    chart = alt.Chart(cases).mark_line(size=3).encode(
        alt.X('Dato', title='Date'),
        #Bredere linje
        alt.Y('Kumulativt antall', title='Cumulative number of cases'),
        tooltip=[alt.Tooltip('Dato', title='Date'), alt.Tooltip('Kumulativt antall', title='Cumulative number of cases')],
        size=alt.condition(nearest_line, alt.value(5), alt.value(3))
    ).properties(
    title=f"Cumulative number of reported COVID-19 cases in {county} by specimen collection date",
    width=600,
    height=500
    ).add_selection(nearest_line)

    return chart

def plot(county="all counties", start=None, end=None):
    cases = plot_reported_cases(county, start, end)
    cumulative = plot_cumulative_cases(county, start, end)
    x = alt.layer(cases, cumulative).resolve_scale(
        y = 'independent'
    )
    x.show()

def plot_both(county="all counties", start=None, end=None):
    """
    Gets a dataframe by calling __read_csv with the seelcted arguments.
    Creates a plot of cumulative cases over one y-axis and new cases over the other y-axis

    Args:
        county(str): Name of a county or all counties. Default value is all counties.
        start(str): Start date in the format "%d.%m.%Y". Default value is None and translates to first date in dataset.
        end(str): En date in the format "%d.%m.%Y". Default value is None and translates to first date in dataset.
    Returns:
        (Altair.Chart): A chart with the number of cases and cumulative number of cases plotted against the dates.
    """
    cases = __read_csv(county, start, end)
    nearest_line = alt.selection(type='single', on='mouseover',
                        fields=["Dato"], empty='none')
    nearest_bar = alt.selection(type='single', on='mouseover',
                        fields=["Dato"], empty='none')
    base = alt.Chart(cases).encode(
        alt.X('Dato', title='Date'),
    ).properties(title=f"Number of reported COVID-19 cases in {county} by specimen collection date"
    )

    line =  base.mark_line(color='red').encode(
        alt.Y('Kumulativt antall', axis=alt.Axis(title='Cumulative number of cases')),
        tooltip=[alt.Tooltip('Dato', title='Date'),
        alt.Tooltip('Kumulativt antall', title='Cumulative number of cases')],
        size=alt.condition(nearest_line, alt.value(5), alt.value(3))
    ).add_selection(nearest_line)

    bar = base.mark_bar(size=n/len(cases)+0.5).encode(
        alt.Y('Nye tilfeller', axis=alt.Axis(title='New cases')),
        tooltip=[alt.Tooltip('Dato', title='Date'),
        alt.Tooltip('Nye tilfeller', title='New cases')],
        opacity=alt.condition(nearest_bar, alt.value(1), alt.value(0.7))
    ).add_selection(nearest_bar)

    layered = alt.layer(line, bar).resolve_scale(
        y = 'independent'
    ).properties(width=600, height=500)

    return layered

#Initialize the flask app
app = Flask(__name__, static_url_path='/docs', static_folder='docs/_build/html/')

@app.route("/", methods=['GET', 'POST'])
def menu():
    """
    Creates and renders a chart with all counties if method = get.
    Creates and renders a chart with selected county from dropdown if method = post

    Returns:
        render_template: Renders the template with the specified county if the request is POST
            If the request is get, such as in the first instance, it renders with county=all counties
    """
    #lag en meny som sender videre til sidene
    if request.method == "POST":
        county = request.form.get('county')
        return render_template("chart.html", county=county)
    return render_template('chart.html', county='All counties')

@app.route("/plot.json/<county>")
def plot_layered(county):
    """
    Creates the plot of new cases/cumulative cases over dates and
    returns a string of the configuration.

    Args:
        county(str): The county to make the plot for

    Returns:
        (.json str): A string of the plot configuration
    """
    chart = plot_both(county)
    tmp = tempfile.NamedTemporaryFile(suffix='.json')
    chart.save(tmp.name)
    with open(tmp.name) as file:
        return file.read()

@app.route("/norway_plot")
def plot_norway():
    """
    Renders the html-template map.html with the plot configuaration from norway_plot.json

    Returns:
        render_template: Renders the template with the generated json map plot
    """
    return render_template('map.html')

@app.route("/norway_plot.json")
def plot_norway_get_json():
    """
    Creates the map plot and returns the string of the plot configuration

    Returns:
        (.json str): a string of the plot configuration
    """
    map = norway_plot()
    tmp = tempfile.NamedTemporaryFile(suffix='.json')
    map.save(tmp.name)
    with open(tmp.name) as file:
        return file.read()

#documentation
@app.route('/help')
@app.route('/<path:path>')
def serve_sphinx_docs(path='index.html'):
    return app.send_static_file(path)

if __name__ =="__main__":
    app.run(debug=True)
