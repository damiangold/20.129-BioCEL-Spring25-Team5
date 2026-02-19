import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# HELPER FUNCTIONS

def find_nearest(array, value):
    """
    Returns the value in the array that is the closest to a given value.
    """
    array = np.asarray(array)
    # get the index of the closest value
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# START OF PROGRAM

# first, read and import the csv file
PATH_TO_PLASMID_CSV: str = r"C:\Gro\Gro_Exercise_1\output\exercise1_2\constitutive_transfect_3_plasmids_1_complex.csv"
IDEAL_TIME_POINTS: list = [20, 40, 60]      # the time points in minutes to select
COLORS = ["blue", "green", "red"]
PROTEINS_OF_INTEREST = ["bfp", "yfp", "rfp"]

# read the df frame
df = pd.read_csv(PATH_TO_PLASMID_CSV)

# gain the closest time points to each of the ideal time points
closest_time_points: list = [find_nearest(df["time"], ideal_time_point) for ideal_time_point in IDEAL_TIME_POINTS]

# filter the df table for the closest time points and save the time and protein expression
indexed_headers = ["time"] + PROTEINS_OF_INTEREST
filtered_df = df[df["time"].isin(closest_time_points)][indexed_headers]

# plot the data frame as histograms separated by time and protein
fig, axes = plt.subplots(len(closest_time_points), 3, figsize=(12, 4 * len(closest_time_points)))
# convert axes to a 2D array if it is a 1D array from only one time point
if len(closest_time_points) == 1:
    axes = axes.reshape(1, -1)

# iterate over each row (time point) and plot
for row, time_point in enumerate(closest_time_points):
    time_data = filtered_df[filtered_df["time"] == time_point]
    # for each row, iterate over columns (proteins of interst) and plot
    for col, (protein, color) in enumerate(zip(PROTEINS_OF_INTEREST, COLORS)):
        ax = axes[row, col]
        ax.hist(time_data[protein], bins=20, color=color, alpha=0.7, edgecolor="black")
        ax.set_title(f"Protein Copies of {protein.upper()} at {time_point} min")
        ax.set_xlabel("Number of Protein Copies")
        ax.set_ylabel("Frequency")

# add spacing so labels are legible
plt.tight_layout(pad=3.0)
plt.show()
