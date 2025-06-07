import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import contang.main as cg

# layout and config
st.set_page_config(page_title="Contact Angle Estimator", layout="wide")
st.title("Contact Angle Estimator")

# sidebar inputs
st.sidebar.header("I. Upload Your Data")
csv_2d = st.sidebar.file_uploader("Upload 2D CSV", type="csv")
csv_3d = st.sidebar.file_uploader("Upload 3D CSV", type="csv")

st.sidebar.header("II. Bottom Contact Circle Bounds")
bot_upper_bound = st.sidebar.number_input("Maximum Distance", value=1.75)
bot_lower_bound = st.sidebar.number_input("Minimum Distance", value=1.5)

st.sidebar.header("III. Top Contact Circle Bounds")
top_upper_bound = st.sidebar.number_input("Maximum Distance", value=0.75)
top_lower_bound = st.sidebar.number_input("Minimum Distnace", value=0.5)

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
            # load raw data and interpolate
            x, y, new_x, y_interp, x3, y3, z3, grid_x, grid_y, grid_z, df = cg.load_and_interpolate_data(csv_2d, csv_3d)
        st.success("Data loaded!")

        st.subheader("2D Contour Plot")
        fig1, ax1 = plt.subplots(2, 1)
        ax1[0].scatter(x, y, s=5)
        ax1[0].set_aspect('equal')
        ax1[0].set_title("2D Interface Profile")
        ax1[1].scatter(new_x, y_interp, s=5)
        ax1[1].set_aspect('equal')
        ax1[1].set_title("2D Interface Profile interpolated")
        st.pyplot(fig1)

        st.subheader("3D Contour Projection (Top View)")
        fig2, ax2 = plt.subplots()
        contour = ax2.contourf(grid_x, grid_y, grid_z, levels=30, cmap='plasma', alpha=0.5)
        fig2.colorbar(contour, ax=ax2, label='Z')
        ax2.set_aspect('equal')
        ax2.set_title("Top View of 3D Surface")
        st.pyplot(fig2)
        
        # fit the plane
        fit_params = cg.fit_surface_plane(df, R)
        
        st.write(fit_params)
        st.success("The plane is fitted!")

        # plot of the fitted plane to be added

        with st.spinner("Selecting top and bottom contact rings..."):
            top_df, bot_df = cg.select_top_ring(df, fit_params, R, top_lower_bound, top_upper_bound, bot_lower_bound, bot_upper_bound)

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
            angle = cg.calculate_angle_from_rings(top_df, bot_df)

        st.success("Analysis complete!")

        st.subheader("Final Result")
        st.metric(label="Estimated Contact Angle", value=f"{angle:.2f}")
