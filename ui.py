import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from contang.data_loader import load_2d_csv, load_3d_csv
from contang.interpolation import interpolate_1d, interpolate_2d
from contang.geometry import select_contact_ring
from contang.angle_calc import fit_circle, compute_contact_angle

# layout and config
st.set_page_config(page_title="Contact Angle Estimator", layout="wide")
st.title("Contact Angle Estimator")

# sidebar inputs
st.sidebar.header("I. Upload Your Data")
csv_2d = st.sidebar.file_uploader("Upload 2D CSV", type="csv")
csv_3d = st.sidebar.file_uploader("Upload 3D CSV", type="csv")

st.sidebar.header("II. Plane Fit Parameters")
a = st.sidebar.number_input("a (slope in x)", value=0.2)
b = st.sidebar.number_input("b (slope in y)", value=-0.3)
d = st.sidebar.number_input("d (offset)", value=1.0)

# run button
run_analysis = st.sidebar.button("Run Analysis")

# main output section
if run_analysis:
    if not csv_2d or not csv_3d:
        st.error("Please upload both 2D and 3D CSV files before running.")
    else:
        with st.spinner("Loading and processing data..."):
            # load 2D and 3D data
            x, y = load_2d_csv(csv_2d)
            x3, y3, z3 = load_3d_csv(csv_3d)

            df_3d = pd.DataFrame({'x': x3, 'y': y3, 'z': z3})
            df_3d['square'] = df_3d['x']**2 + df_3d['y']**2

        st.success("Data loaded!")

        st.subheader("2D Contour Plot")
        fig1, ax1 = plt.subplots()
        ax1.scatter(x, y, s=5)
        ax1.set_aspect('equal')
        ax1.set_title("2D Interface Profile")
        st.pyplot(fig1)

        st.subheader("3D Contour Projection (Top View)")
        fig2, ax2 = plt.subplots()
        ax2.scatter(x3, y3, s=1)
        ax2.set_aspect('equal')
        ax2.set_title("Top View of 3D Surface")
        st.pyplot(fig2)

        with st.spinner("Selecting top and bottom contact rings..."):
            top_df = select_contact_ring(df_3d, (a, b, d), 0.5, 0.75)
            bot_df = select_contact_ring(df_3d, (a, b, d), 1.5, 1.75)
            top_df = top_df.loc[top_df['square'] < 19**2].reset_index(drop=True)

        st.success("Contact rings identified.")

        st.subheader("Top and Bottom Contact Ring Plots")
        fig3, ax3 = plt.subplots(1, 2, figsize=(12, 5))
        ax3[0].scatter(top_df['x'], top_df['y'], s=10, color='red')
        ax3[0].set_title("Top Contact Ring")
        ax3[0].set_aspect('equal')

        ax3[1].scatter(bot_df['x'], bot_df['y'], s=10, color='blue')
        ax3[1].set_title("Bottom Contact Ring")
        ax3[1].set_aspect('equal')

        st.pyplot(fig3)

        with st.spinner("Fitting circles and calculating angle..."):
            z_top, r_top = fit_circle(top_df)
            z_bot, r_bot = fit_circle(bot_df)
            angle = compute_contact_angle(z_top, r_top, z_bot, r_bot)

        st.success("Analysis complete!")

        st.subheader("Final Result")
        st.metric(label="Estimated Contact Angle", value=f"{angle:.2f}")
