import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from contang.data_loader import load_2d_csv, load_3d_csv, sq, plane_without_particle
from contang.interpolation import interpolate_1d, interpolate_2d, fit_plane
from contang.geometry import select_contact_ring
from contang.angle_calc import fit_circle, compute_contact_angle

# layout and config
st.set_page_config(page_title="Contact Angle Estimator", layout="wide")
st.title("Contact Angle Estimator")

# sidebar inputs
st.sidebar.header("I. Upload Your Data")
csv_2d = st.sidebar.file_uploader("Upload 2D CSV", type="csv")
csv_3d = st.sidebar.file_uploader("Upload 3D CSV", type="csv")

# st.sidebar.header("II. Plane Fit Parameters")
# a = st.sidebar.number_input("a (slope in x)", value=0.2)
# b = st.sidebar.number_input("b (slope in y)", value=-0.3)
# d = st.sidebar.number_input("d (offset)", value=1.0)

st.sidebar.header("II. Bottom Contact Circle Bounds")
smalmax = st.sidebar.number_input("Highest Distance", value=1.75)
smalmin = st.sidebar.number_input("Lowest Distance", value=1.5)

st.sidebar.header("III. Top Contact Circle Bounds")
bigmax = st.sidebar.number_input("Highest Distance", value=0.75)
bigmin = st.sidebar.number_input("Lowest Distnace", value=0.5)

st.sidebar.header("IV. Particle Size")
R = st.sidebar.number_input("Radius", value=16)


# run button
run_analysis = st.sidebar.button("Run Analysis")

# main output section
if run_analysis:
    if not csv_2d or not csv_3d:
        st.error("Please upload both 2D and 3D CSV files before running.")
    else:
        with st.spinner("Loading and processing data..."):
            # load 2D and 3D data
            R = 16
            x, y = load_2d_csv(csv_2d)
            x3, y3, z3 = load_3d_csv(csv_3d)

            df_3d = pd.DataFrame({'x': x3, 'y': y3, 'z': z3})

        st.success("Data loaded!")

        st.subheader("2D Contour Plot")
        fig1, ax1 = plt.subplots(2, 1)
        ax1[0].scatter(x, y, s=5)
        ax1[0].set_aspect('equal')
        ax1[0].set_title("2D Interface Profile")
        interpolated = interpolate_2d(x3, y3, z3, resolution=1000)
        ax1[1].scatter(interpolated[0], interpolated[2], s=5)
        ax1[1].set_aspect('equal')
        ax1[1].set_title("2D Interface Profile interpolated")
        st.pyplot(fig1)

        st.subheader("3D Contour Projection (Top View)")
        fig2, ax2 = plt.subplots()
        ax2.scatter(x3, y3, s=1)
        ax2.set_aspect('equal')
        ax2.set_title("Top View of 3D Surface")
        st.pyplot(fig2)
        

        tobe_fitted = plane_without_particle(df_3d, R)
        xf, yf, zf = list (tobe_fitted['x']), list (tobe_fitted['y']), list (tobe_fitted['z'])
        fit_params = fit_plane(xf, yf, zf)
        
        st.write(fit_params)
        st.success("the plane is fitted!")

        # add plot of the fit

        with st.spinner("Selecting top and bottom contact rings..."):
            top_df = select_contact_ring(df_3d, fit_params, bigmin, bigmax)
            bot_df = select_contact_ring(df_3d, fit_params, smalmin, smalmax)
            top_df = top_df.loc[sq(top_df) < 19**2].reset_index(drop=True)

        st.success("Contact rings identified.")

        st.subheader("Top and Bottom Contact Ring Plots")
        fig3, ax3 = plt.subplots(1, 2, figsize=(12, 5))
        ax3[0].scatter(top_df['x'], top_df['z'], s=10, color='red')
        ax3[0].set_title("Top Contact Ring")
        ax3[0].set_aspect('equal')

        ax3[1].scatter(bot_df['x'], bot_df['z'], s=10, color='blue')
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
