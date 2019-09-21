# Graph Extractor

A simple Python 3 script for coordinate extraction from an image of a graph.
There are test images in the folder that can be used as a demo.

## Prerequisites

Make sure you have `Python 3` installed.

Before you run the script, install the requirements by running:
```pip install -r requirements.txt```.

## Usage

**IMPORTANT**: the image has to be in the same folder as the script.

1) Run `python Graph_Extractor.py -i <image_name_with_extension_type>`
2) Enter minimum and maximum values for `x` and `y` axes
3) Enter scale type (`lin` and `log` supported)
4) Double click on graph **origin** *(bottom left corner)* and **ending** *(upper right corner)*
5) Press **escape** to confirm the selection
6) Every next double click will print the coordinates to the console
