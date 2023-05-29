'''
Author: Marcin Szpytma
Date Created: 17/03/2022
Date Modified 23/05/2022

Description
Python script to generate heatmaps of element sensitive PIXE mapping on cancer tissues
'''
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.cbook as cbook
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from pathlib import Path


class HeatmapGenerator:
    def __init__(self, file_name):
        self.data = None
        self.selected_element = None
        self.dimension1 = None
        self.dimension2 = None
        self.file_name = file_name

    def read_csv(self):
        try:
            self.data = pd.read_csv(self.file_name, sep=';')
            if not self.data.empty:
                print(f"File from path {self.file_name} has been successfully read")
        except Exception as err:
            print(f"Error: {err}")

    def check_data(self):
        print(self.data.head(5))

    def list_elements(self):
        for element_name in self.data.columns[2:]:
            print(element_name)

    def select_element(self):
        self.selected_element = input("Select specific element for mapping:\n")

    def set_dimensions(self):
        self.dimension1 = input("First dimension for reshape:\n")
        self.dimension2 = input("Second dimension for reshape:\n")

    def generate_heatmap(self):
        element_array = np.asarray(self.data[self.selected_element]).reshape(
            int(self.dimension1), int(self.dimension2)
        )
        element_heatmap = self.data.pivot(
            index="row", columns="column", values=self.selected_element
        )

        fig = plt.figure(figsize=(16, 16))
        sns.set(font_scale=4)
        ax = sns.heatmap(
            element_array,
            cbar_kws={"orientation": "vertical", "label": "counts [a.u]"},
            cmap="jet",
        )
        ax.set(xticklabels=[], yticklabels=[])
        scalebar = ScaleBar(4.1, "um")
        plt.gca().add_artist(scalebar)
        plt.tight_layout()
        plt.show()

        return fig

    def save_heatmap(self, fig):
        save_confirm = input(
            "If you want to save the picture, enter YES. Or NO if you do not wish to save it\n"
        )
        if save_confirm == "YES":
            try:
                fig.savefig(f"{self.selected_element}Map.png", dpi=300)
                print("File saved successfully")
            except Exception as err:
                print(f"Error: {err}")
        elif save_confirm == "NO":
            print("File won't be saved")
        else:
            print("Invalid input. File won't be saved")


if __name__ == "__main__":
    file_name = input("Insert file name/path to the .csv file:\n")
    heatmap_generator = HeatmapGenerator(file_name)
    heatmap_generator.read_csv()
    
    # Check the data
    heatmap_generator.check_data()
    
    # List the elements present in the data
    heatmap_generator.list_elements()

    # Select a specific element for mapping
    heatmap_generator.select_element()
    
    # Set the dimensions for the heatmap
    heatmap_generator.set_dimensions()
    
    # Generate the heatmap
    generated_heatmap = heatmap_generator.generate_heatmap()
    
    # Save the heatmap if desired
    heatmap_generator.save_heatmap(generated_heatmap)