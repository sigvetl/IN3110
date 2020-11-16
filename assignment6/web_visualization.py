#import numpy as np
import pandas as pd
import sys
import altair as alt
from altair_saver import save

#Hardcoded n to select spacing in graphs
n=263
#Need more thorough error checking
def read_csv(county, start=None, end=None):
    try:
        county = county.lower().replace(" ", "")
        cases = pd.read_csv(
            f"data/antall-meldte-covid-19-{county}.csv",
            sep=";",
            parse_dates=["Dato"],
            date_parser=lambda col: pd.to_datetime(col, format="%d.%m.%Y"))

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
        print("Please enter valid dates for start and end")
        sys.exit(1)

    return cases.loc[(cases["Dato"] >= startdate) & (cases["Dato"] <= enddate)]


def plot_reported_cases(county="all counties", start=None, end=None):
    cases = read_csv(county, start, end)
    chart = alt.Chart(cases).mark_bar(size=n/len(cases)).encode(
        x = 'Dato',
        y = 'Nye tilfeller',
        tooltip=['Dato', 'Nye tilfeller']
    ).properties(title=f"Number of reported COVID-19 cases in {county} by specimen collection date"
    ).interactive()
    return chart


def plot_cumulative_cases(county="all counties", start=None, end=None):
    cases = read_csv(county, start, end)
    chart = alt.Chart(cases).mark_line().encode(
        x = 'Dato',
        #Bredere linje
        y = 'Kumulativt antall',
        tooltip=['Dato', 'Kumulativt antall']
    ).properties(thickness=3,
    title=f"Cumulative number of reported COVID-19 cases in {county} by specimen collection date")

    return chart

def plot_both(county="all counties", start=None, end=None):
    cases = read_csv(county, start, end)
    base = alt.Chart(cases).encode(
        alt.X('Dato', axis=alt.Axis(title='Date')), tooltip=['Dato', 'Kumulativt antall', 'Nye tilfeller']
    ).properties(title=f"Number of reported COVID-19 cases in {county} by specimen collection date")

    line =  base.mark_line(color='red').encode(
        alt.Y('Kumulativt antall', axis=alt.Axis(title='Kumulativt antall'))
    )

    bar = base.mark_bar(opacity=0.5, size=n/len(cases)).encode(
    alt.Y('Nye tilfeller', axis=alt.Axis(title='Nye tilfeller'))
    )

    x = alt.layer(line, bar).resolve_scale(
        y = 'independent'
    )

    return x


#chart = plot_reported_cases(start="01.03.2020", end="01.10.2020")
#chart = plot_cumulative_cases()
#chart.show()
#a = plot_both()
#a.save("chart.json")
