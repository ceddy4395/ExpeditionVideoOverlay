import os

import pandas as pd
import tkinter as tk
# from tkinter import *
import folium
from folium.plugins import FastMarkerCluster
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy
from dotenv import load_dotenv
load_dotenv()
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import MaxNLocator

csv_path = os.getenv("CSV_FILE")

def read_csv_file(csv_path):
    try:
        df = pd.read_csv(csv_path, low_memory=False)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        exit(1)

    df = df[(df['Lat'].notna()) & (df['Lon'].notna())]

    try:
        df['Utc'] = pd.to_datetime(df['Utc'], unit='d', origin='1899-12-30')
    except Exception as e:
        print(f"Error converting 'Utc' to datetime: {e}")
        exit(1)

    damping_factor = 5
    df = df.iloc[::damping_factor]
    return df

df = read_csv_file(csv_path)

locations = df[['Lat', 'Lon']]

m = folium.Map(location=locations.mean().to_list(), zoom_start=13)
m.add_child(FastMarkerCluster(locations.values.tolist()))
m.save('map.html')

    # List of all possible variables to plot
all_variables = df.columns.tolist()

# Create a new Tkinter window
selection_window = tk.Tk()

# Create a dictionary to hold the Checkbutton variables
check_vars = {var: tk.IntVar() for var in all_variables}

# Create a check button for each variable
for var in all_variables:
    checkbutton = tk.Checkbutton(selection_window, text=var, variable=check_vars[var])
    checkbutton.pack()

# Create a list to hold the selected variables
variables = []

# Create an "OK" button
def on_ok_clicked():
    # Add the selected variable to the variables list
    variables.extend([var for var, value in check_vars.items() if value.get()])
    # Close the selection window
    selection_window.destroy()

ok_button = tk.Button(selection_window, text="OK", command=on_ok_clicked)
ok_button.pack()

selection_window.mainloop()

root = tk.Tk()

# Create a Tkinter variable
tkvar = tk.StringVar(root)

# Dictionary with options
choices = { 'Option1','Option2','Option3'}
tkvar.set('Option1') # set the default option

popupMenu = tk.OptionMenu(root, tkvar, *choices)
popupMenu.pack()

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

# link function to change dropdown
tkvar.trace('w', change_dropdown)

# Create the figure with smaller size
fig, axs = plt.subplots(len(variables), figsize=(5, len(variables)*2.5))

# Initialize the data arrays
x_data = []
y_data = [[] for _ in range(len(variables))]

# Create a line object for each plot
lines = [ax.plot([], [])[0] for ax in axs]

# Function to initialize the plot

def init():
    for line in lines:
        line.set_data([], [])
    return lines
    return line,


# Convert 'Utc' to datetime
df['Utc'] = pd.to_datetime(df['Utc'])


def update(frame):
    x_data.append(df['Utc'].iloc[frame])
    for i, line in enumerate(lines):
        y_data[i].append(df[variables[i]].iloc[frame])
        y_smooth = gaussian_filter1d(y_data[i], sigma=2)
        line.set_data(x_data, y_smooth)

        # Set x limits to current frame plus or minus 50
        if frame > 50:
            axs[i].set_xlim(left=df['Utc'].iloc[frame-50], right=df['Utc'].iloc[frame+50])
        else:
            axs[i].set_xlim(left=df['Utc'].iloc[0], right=df['Utc'].iloc[frame+50])

        # Set y limits to min and max of current y data
        axs[i].set_ylim(min(y_smooth), max(y_smooth))

        # Fill between the line and the x axis
        axs[i].fill_between(x_data, y_smooth, color='skyblue', alpha=0.4)

        # Limit the number of labels on the y-axis to 4
        axs[i].yaxis.set_major_locator(MaxNLocator(4))
        # After updating all lines, update the legend
        for ax in axs:
            ax.legend(loc='upper right', frameon=False, ncol=2, fontsize=10)
    return lines
# Create the animation
ani = animation.FuncAnimation(fig, update, frames=range(len(df)), init_func=init, blit=True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Add the navigation toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack()

root.mainloop()
