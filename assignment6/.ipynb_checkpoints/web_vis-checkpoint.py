import numpy as np
import pandas as pd
import sys
import altair as alt
from altair_saver import save

#Need more thorough error checking
def read_csv(county, start=None, end=None):
    try:
        county = county.lower().replace(" ", "")
        cases = pd.read_csv(
            f"data/antall-meldte-covid-19-{county}.csv",
            sep=";",
            parse_dates=["Dato"],
            date_parser=lambda col: pd.to_datetime(col, format="%d.%m.%Y"))
        print(cases.head(2))

    except FileNotFoundError:
        errormsg = "Not a valid selection. Please select one of the following:\n"\
        +"All counties\nAgder\nInnlandet\nMøre og Romsdal\nNordland\nOslo\nRogaland\n"\
        +"Troms og Finnmark\nTrøndelag\nVestfold og Telemark\nVestland\nViken"
        print(errormsg)
        sys.exit(1)

    try:
        startdate = pd.to_datetime(start, format="%d.%m.%Y")
        enddate = pd.to_datetime(end, format="%d.%m.%Y")
        print(startdate)
        print(enddate)

        if start and end and startdate > enddate:
            print("End date must be after start date")
            raise ValueError

        if start==None:
            startdate = cases["Dato"].iloc[0]
            print(startdate)
        if end==None:
            enddate = cases["Dato"].iloc[-1]
            print(enddate)
        """
        if (startdate not in cases.Dato.values) or (enddate not in cases.Dato.values):
            print(cases.Dato.values)
            raise ValueError
        """
    except ValueError:
        print("Please enter valid dates for start and end")
        sys.exit(1)

    return cases.loc[(cases["Dato"] >= startdate) & (cases["Dato"] <= enddate)]


def plot_reported_cases(county="all counties", start=None, end=None):
    cases = read_csv(county, start, end)
    alt.renderers.enable('mimetype')
    alt.Chart(cases).mark_bar().encode(
        x = cases['Dato'],
        y = cases['Nye tilfeller']
    )
    print(cases)
    

def plot_cumulative_cases():
    pass

def plot_both():
    pass

def example():
    source = pd.DataFrame({
        'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
    })

    chart = alt.Chart(source).mark_bar().encode(
        x='a',
        y='b'
    )
    return chart

plot_reported_cases()
chart = example()
chart
