# Signal-Interpolation-and-Curve-Fitting-Accuracy-and-Efficacy-Illustrator
## Desktop Application - Written in Python (pyqt5)
- Curve fitting and interpolation are among the most usable tools in signal procesing and data science.
- Illustrating tradeoff between order of polynomial (polynomial interpolation), number of chunks signal is divided into and overlapping percentage between chunks in terms of accuracy and efficacy.
- Illustrating functionalities of interpolation & curve fitting, curve fitting error map and extrapolation.

# Features
- Browsing signal of 1000 samples.
- Performing curve fitting using spline, polynomial or cubic interpolation, each with their basic settings. Shown as dotted line over original signal.
- Controlling number of chunks signal is divided into, interpolation order, and percentage of overlapping between chunks accordingly.
- Showing mean-squared error of curve fitting and fitted equation of each chunk in latex format.
- Generating error map for fitting process, where x and y axes are chosen out of curve fitting parameters:
1) Polynomial interpolation order
2) Number of chunks
3) Overlapping percentage between chunks

As error map is performed with 2 of the previous parameters and the third is taken as a constant value from the user.                
Note: Error map functionality is put in a lower-priority thread as it is a lengthy process.
- Showing error map generation progress via progress bar.
- Cancelling, pausing and resuling error map via buttons changing their functionality according to error map status.
- Cuttiing a percentage of signal from its end and extrapolating it based available portion of signal.

# Preview 


https://user-images.githubusercontent.com/73616568/171068773-39c4b775-f1aa-47fd-a750-33573caf7f77.mp4

