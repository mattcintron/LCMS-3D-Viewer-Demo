This project was designed to showcase the power of Mayavi and its 3D visualization tools as well as provide our LCMS data 
scientists over at the Lab a quick in house tool for reading in and viewing their data. The data is shown in full 3D and after render there is usually zero delay on intractability.

Current charting dose use a down-sampling algorithm to make data load quicker but data is almost entirely persevered as with
Mayavi a down-sampling of only 1.2 is usually needed on most data sets. For example on a run of 90MB with 2500000 points we will render a chart that has 2million plus points after the data is modified. 

To Use-
1 open up a virtual environment in python 3.6 or higher

2 move in code

3 run requirements file – for Mayavi you will also need to have C++ visual studios tools installed and a link to it in your path vars – see this for more info- 
https://docs.enthought.com/mayavi/mayavi/installation.html

4- Use line 43 to set your target data
data = pd.read_csv("Your File Here.csv")

5- run the Mayavi LCMS 3D Demo.py file

Lead Developer: Matthew Cintron
Sub Developer: Steven Yang
