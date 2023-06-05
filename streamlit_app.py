import streamlit as st
import matplotlib
import pandas as pd

matplotlib.use('Agg')

# Test: Linechart from a dataframe


st.header("IR Spectra Identify")

label = 'Tolerance?'
peaks = "0"
peaks = st.text_input('tolerance')
peaks = [float(p) for p in peaks.split(',')]

st.write(peaks)


df = pd.read_excel("Wellenzahlen-Tool.xls")[["zahl", "stoff"]]
tolerance = 4
potentials = []
for p in peaks[:]:
    diff = df["zahl"] - p
    df_sorted = df.iloc[diff.abs().argsort()]
    foo = df_sorted[(df_sorted["zahl"] - p).abs() < tolerance]
    potentials += foo["stoff"].to_list()
counts = pd.Series(potentials).groupby(potentials).count()
counts_sorted = counts.sort_values(ascending=False)

st.write(counts_sorted[counts_sorted > 2])

st.markdown("---")
