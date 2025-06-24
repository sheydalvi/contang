
# contang

**contang** is a data processing pipeline designed to extract meaningful physical insights — specifically the contact angle — from unorganized simulation data. It is tailored for use in physics-based simulations involving interfacial systems, where understanding wetting behavior and geometry is essential.

## Purpose

This tool takes raw numerical simulation output and processes it through a robust analysis pipeline to compute the contact angle of an interfacial particle.

## How It Works

The pipeline automates the ingestion, filtering, and transformation of simulation data to detect the fluid interface and calculate the contact angle through geometric analysis.

The calculation involves:
- Parsing raw simulation outputs and increasing numerical resolution by data interpolation
- Identifying the interface deformation coordinates
- Fitting curves and planes to the numerical data
- Computing the contact angle at the interface

## Streamlit UI

The application includes an interactive Streamlit interface (`ui.py`) that offers an intuitive, notebook-like user experience. Users can:
- Upload simulation output files
- Select parameters for processing
- Visualize fluid shapes and angles
- Download results

## File Structure

```code
contang/            # core logic and processing pipeline
data/               # example input files for testing
ui.py               # streamlit UI interface
requirements.txt    # dependencies
.gitignore
```

## Inputs and Outputs

**Inputs:**  
Two csv files from simulation output:
- `sample_2d.csv`: a 2D slice of the interface (like a line for interface and a circle for the particle)
- `sample_3d.csv`: 3D data file containing all the data points representing interface plane and particle sphere

**Outputs:**  
- Processed plots of the fluid interface
- Calculated contact angle values

## How to Use

Clone the repository:

```bash
git clone https://github.com/sheydalvi/contang.git
cd contang
```
Install the required dependencies:

```bash
pip install -r requirements.txt
```
Launch the UI on the browser:

```bash
streamlit run ui.py
```
Example Run
To try it out, use the sample input files in the data/ directory. Upload these files when prompted by the UI, and the pipeline will generate plots and calculate the contact angle.
