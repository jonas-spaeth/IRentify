import streamlit as st
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt


matplotlib.use('Agg')

# Test: Linechart from a dataframe


st.header("IR Spectra Identify")

label = 'Tolerance?'
tolerance = st.number_input('tolerance (must be larger 0', min_value=1, value=5)

peaks = "0"
peaks = st.text_input('tolerance')
if len(peaks) > 0:
    peaks = [float(p.strip()) for p in peaks.split(',')]

    st.subheader("Your measured peaks:")
    st.write(peaks)

    st.subheader("Result")

    df = pd.read_excel("Wellenzahlen-Tool.xls")[["zahl", "stoff"]]
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



    if len(counts_sorted) > 0:
        analyze_drug = counts_sorted.index[0]

        print(analyze_drug)

        fig = plt.figure(figsize=(10, 5))
        theory = df[df["stoff"] == analyze_drug].zahl
        for t in theory:
            plt.axvline(t, c="k", lw=5)

        for p in peaks:
            plt.axvline(p, c="r", lw=2, ls="--")
        plt.title(f"Red: measured, Black: {analyze_drug}")
        fig.show()
