#!/usr/bin/env python3

#  This application expects the numpy array of data to be in a particular format.  The array
#  must be 3 dimensional (3D) where:
#     1st Dimension - particle/body index number
#     2nd Dimension - x, y, z axis
#     3rd Dimension - the point as a float
#
#  Example array
#     [ [[5.0, 3.0, 0.0], [4.0, 6.0, 1.0], [3.0, 3.0, 3.0]],
#       [[4.3, 2.3, 1.2], [9.8, 8.6, 4.6], [8.9, 7.8, 4.2]] ]
#
#  Array Explained
#        | x0   x1  x2 |  | y0   y1  y2 |  | z0   z1  z2 |
#        -------------------------------------------------
#     [ [[5.0, 3.0, 0.0], [4.0, 6.0, 1.0], [3.0, 3.0, 3.0]],     <-- Particle 0
#       [[4.3, 2.3, 1.2], [9.8, 8.6, 4.6], [8.9, 7.8, 4.2]] ]    <-- Particle 1
#
#  This example has 2 particles/bodies; each with x, y, z axis.  Each axis has 3 points.
#  The first coordinate is (x0, y0, z0) then (x1, y1, z1) and finally (x2, y2, z2).
#
#  To get an np.array written to a file correctly, use this code.
#     fd = open("points.txt", "w")
#     fd.write(repr(yourNumpyArray))
#     fd.close()

import sys
import os
import re
from PyQt4 import QtGui, QtCore
import pyqtgraph.opengl as gl
import numpy as np

def verifyPoints(points):
   '''Verify the points are valid.  It needs to be a 3D numpy array.  The 2nd
      dimension needs to be exactly 3 in size.
      Array format is: 1st dimension is the particle
                       2nd dimension is the axes (X, Y, Z)
                       3rd dimension is the position value
      Input:  array of points <np.ndarray> [particle number [axis X, Y, Z [position value <float>]]]
      Output: True/False <bool>'''
   #  If the points' type, shape and 2nd dimension size is correct, return True
   if(type(points) == np.ndarray and len(points.shape) == 3 and points.shape[1] == 3): return(True)
   #  Otherwise, return False
   else: return(False)

class App(QtGui.QApplication):
   '''This is a main application.
      Input:  command line arguments <list>
      Output: None'''
   def __init__(self, points):
      #  Initialize the parent widget
      QtGui.QApplication.__init__(self, sys.argv)
      
      #  Set the application name
      self.setApplicationName("Submit Document")
      
      #  Create the main window
      self.mainWindow = MainWindow(points)
      
      #  Show the main window
      self.mainWindow.show()

class MainWindow(QtGui.QMainWindow):
   '''This is the main GUI window.  This is what contains all the QWidgets seen in the application.'''
   def __init__(self, points):
      '''Initialize the main window.
         Input:  None
         Output: None'''
      #  Initialize the parent widget
      QtGui.QMainWindow.__init__(self)
      
      #  Initialize this window
      self.setWindowTitle("nBody 3D Graph")
      
      #  Set the size of the main window
      self.resize(800, 600)
      
      #  Create a graph object
      self.graph = Graph(points)
      
      #  Set the graph object as the central widget of the main window
      self.setCentralWidget(self.graph)

class Graph(QtGui.QWidget):
   '''This is the graph widget.  It contains the 3D graph, the playback controls and
      status.'''
   #  The alpha color value
   colorAlpha = 1.0
   
#    #  A list of color codes to use when displaying plots.  There are two colors (RGBA) per entry.
#    #  This is so when those two colors are different, the plot's colors will alternate.
#    colorCodes = [((0.8, 0.0, 0.0, colorAlpha), (0.8, 0.0, 0.0, colorAlpha)),
#                  ((0.0, 0.8, 0.0, colorAlpha), (0.0, 0.8, 0.0, colorAlpha)),
#                  ((0.0, 0.0, 0.8, colorAlpha), (0.0, 0.0, 0.8, colorAlpha)),
#                  ((0.8, 0.8, 0.0, colorAlpha), (0.8, 0.8, 0.0, colorAlpha)),
#                  ((0.8, 0.0, 0.8, colorAlpha), (0.8, 0.0, 0.8, colorAlpha)),
#                  ((0.0, 0.8, 0.8, colorAlpha), (0.0, 0.8, 0.8, colorAlpha)),
#                  ((0.8, 0.0, 0.0, colorAlpha), (0.0, 0.8, 0.0, colorAlpha)),
#                  ((0.0, 0.8, 0.0, colorAlpha), (0.0, 0.0, 0.8, colorAlpha)),
#                  ((0.0, 0.0, 0.8, colorAlpha), (0.8, 0.8, 0.0, colorAlpha)),
#                  ((0.8, 0.8, 0.0, colorAlpha), (0.8, 0.0, 0.8, colorAlpha))]
   
   #  A list of color codes to use when displaying plots.  There are two colors (RGBA) per entry.
   #  This is so when those two colors are different, the plot's colors will alternate.
   colorCodes = [((0.8, 0.0, 0.0, colorAlpha), (0.8, 0.0, 0.0, colorAlpha)),
                 ((0.0, 0.8, 0.0, colorAlpha), (0.0, 0.8, 0.0, colorAlpha)),
                 ((0.0, 0.0, 0.8, colorAlpha), (0.0, 0.0, 0.8, colorAlpha)),
                 ((0.8, 0.8, 0.0, colorAlpha), (0.8, 0.8, 0.0, colorAlpha)),
                 ((0.8, 0.0, 0.8, colorAlpha), (0.8, 0.0, 0.8, colorAlpha)),
                 ((0.0, 0.8, 0.8, colorAlpha), (0.0, 0.8, 0.8, colorAlpha)),
                 ((255/255.0, 140/255.0, 0/255.0, colorAlpha), (255/255.0, 140/255.0, 0/255.0, colorAlpha)),
                 ((219/255.0, 112/255.0, 147/255.0, colorAlpha), (219/255.0, 112/255.0, 147/255.0, colorAlpha)),
                 ((105/255.0, 105/255.0, 105/255.0, colorAlpha), (105/255.0, 105/255.0, 105/255.0, colorAlpha)),
                 ((106/255.0, 90/255.0, 205/255.0, colorAlpha), (106/255.0, 90/255.0, 205/255.0, colorAlpha))]
   
   def __init__(self, points = None):
      '''Initialize this class.
         Input:  points <np.array> [particle index [xyz coordinate [point <float>]]]
         Output: None'''
      #  Initialize the parent
      QtGui.QWidget.__init__(self)
      
      #  All of the points for all of the particles (these are precalculated)
      self.points = points
      
      #  Create a counter frame and set the frame's attributes
      self.counterFrame = QtGui.QFrame()
      self.counterFrame.setFrameShadow(QtGui.QFrame.Sunken)
      self.counterFrame.setFrameShape(QtGui.QFrame.Box)
      
      #  Create a controls frame and set the frame's attributes
      self.controlsFrame = QtGui.QFrame()
      self.controlsFrame.setFrameShadow(QtGui.QFrame.Raised)
      self.controlsFrame.setFrameShape(QtGui.QFrame.Panel)
      
      #  Create the layouts
      self.mainLayout = QtGui.QVBoxLayout(self)
      self.counterLayout = QtGui.QHBoxLayout(self.counterFrame)
      self.controlsLayout = QtGui.QHBoxLayout(self.controlsFrame)
      self.viewLayout = QtGui.QHBoxLayout()
      
      #  The starting time index (i.e. of the X number of points given, start at this one)
      self.initialPointIndex = 1
      
      #  The initial step size
      self.initialStepSize = 50
      
      #  The initial delay when "playing" the graph
      self.initialDelay = 40
      
      #  When fast-forwarding or rewinding, increase/decrease the timer's interval by this amount
      self.timerStepSize = 20
      
      #  Create a bold font
      self.boldFont = QtGui.QFont()
      self.boldFont.setBold(True)
      
      #  Create a counter label
      self.counterLabel = QtGui.QLabel("Counter")
      self.counterLabel.setFont(self.boldFont)
      
      #  Create a counter line edit
      self.counterLineEdit = QtGui.QLineEdit()
      self.counterLineEdit.setReadOnly(True)
      self.counterLineEdit.setAlignment(QtCore.Qt.AlignRight)
      self.counterLineEdit.setFixedWidth(QtGui.QFontMetrics(self.counterLineEdit.font()).width("0000000") + 20)
      
      #  Create a step size label
      self.stepSizeLabel = QtGui.QLabel("Step")
      self.stepSizeLabel.setFont(self.boldFont)
      
      #  Create a step size spin box
      self.stepSizeSpinBox = QtGui.QSpinBox()
      self.stepSizeSpinBox.setValue(self.initialStepSize)
      
      #  Create a timer label
      self.timerLabel = QtGui.QLabel("Time Interval (ms)")
      self.timerLabel.setFont(self.boldFont)
      
      #  Create a timer spin box
      self.timerSpinBox = QtGui.QSpinBox()
      self.timerSpinBox.setRange(0, 10000)
      self.timerSpinBox.setValue(self.initialDelay)
      
      #  Create a time slider
      self.timeSlider = QtGui.QSlider()
      self.timeSlider.setSingleStep(1)
      self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
      self.timeSlider.setEnabled(False)
      
      #  Create the graph view
      self.view = gl.GLViewWidget()
      
      #  Create the x, y, and z grids
      self.xGrid = gl.GLGridItem()
      self.yGrid = gl.GLGridItem()
      self.zGrid = gl.GLGridItem()
      
      #  Rotate the x and y grid
      self.xGrid.rotate(90, 0, 1, 0)
      self.yGrid.rotate(90, 1, 0, 0)
      
      #  Create x, y, and z axis (drawn as line plots)
      self.xAxis = gl.GLLinePlotItem(pos = np.array([[-10.0, 0.0, 0.0], [10.0, 0.0, 0.0]]), color = np.array([[1.0, 0.0, 0.0, 0.4], [1.0, 0.0, 0.0, 0.4]]), width = 3.0)
      self.yAxis = gl.GLLinePlotItem(pos = np.array([[0.0, -10.0, 0.0], [0.0, 10.0, 0.0]]), color = np.array([[0.0, 1.0, 0.0, 0.4], [0.0, 1.0, 0.0, 0.4]]), width = 3.0)
      self.zAxis = gl.GLLinePlotItem(pos = np.array([[0.0, 0.0, -10.0], [0.0, 0.0, 10.0]]), color = np.array([[0.0, 0.0, 1.0, 0.4], [0.0, 0.0, 1.0, 0.4]]), width = 3.0)
      
      #  Add the x, y, and z line plots to the view
      self.view.addItem(self.xAxis)
      self.view.addItem(self.yAxis)
      self.view.addItem(self.zAxis)
      
      #  A list of scatter plots
      self.scatterList = []
      
      #  A list of line plots
      self.lineList = []
      
      #  Add graph items to the view
      self.view.addItem(self.xGrid)
      self.view.addItem(self.yGrid)
      self.view.addItem(self.zGrid)
      
      #  Set the view's resize policy
      self.view.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
      
      #  Set the initial color values
      self.colors = []
      
      #  Create play and pause icons
      self.playIcon = QtGui.QIcon(sys.path[0] + "/icons/play.png")
      self.pauseIcon = QtGui.QIcon(sys.path[0] + "/icons/pause.png")
      
      #  Create control buttons and disable them by default
      self.playPauseButton = self.createIconButton(self.playIcon, tooltip = "Play")
      self.playPauseButton.setEnabled(False)
      self.ffButton = self.createIconButton(QtGui.QIcon(sys.path[0] + "/icons/fastforward.png"), tooltip = "Faster")
      self.ffButton.setEnabled(False)
      self.rewindButton = self.createIconButton(QtGui.QIcon(sys.path[0] + "/icons/rewind.png"), tooltip = "Slower")
      self.rewindButton.setEnabled(False)
      self.stepForwardButton = self.createIconButton(QtGui.QIcon(sys.path[0] + "/icons/stepforward.png"), tooltip = "Step Forward")
      self.stepForwardButton.setEnabled(False)
      self.stepBackwardButton = self.createIconButton(QtGui.QIcon(sys.path[0] + "/icons/stepbackward.png"), tooltip = "Step Backward")
      self.stepBackwardButton.setEnabled(False)
      
      #  Create the reverse button
      self.reverseButton = QtGui.QCheckBox("Reverse")
      self.reverseButton.setFont(self.boldFont)
      
      #  Create the reverse button
      self.loopButton = QtGui.QCheckBox("Loop")
      self.loopButton.setFont(self.boldFont)
      
      #  Create an exit button
      self.exitButton = QtGui.QPushButton("Exit")
      self.exitButton.setToolTip("Exit this application")
      self.exitButton.setFont(self.boldFont)
      
      #  Create a load button
      self.loadButton = QtGui.QPushButton("Load Points")
      self.loadButton.setToolTip("Load points to be shown on the graph")
      self.loadButton.setFont(self.boldFont)
      
      #  Turn on the main context menu
      self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
      
      #  Create a plot list widget
      self.plotListWidget = QtGui.QListWidget()
      self.plotListWidget.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
      self.plotListWidget.setVisible(False)
      
      #  Create context menu actions
      self.showPlotListAction = QtGui.QAction("Show Plot List", self)
      self.showPlotListAction.setCheckable(True)
      self.xAction = QtGui.QAction("Show X Grid", self)
      self.xAction.setCheckable(True)
      self.xAction.setChecked(True)
      self.yAction = QtGui.QAction("Show Y Grid", self)
      self.yAction.setCheckable(True)
      self.yAction.setChecked(True)
      self.zAction = QtGui.QAction("Show Z Grid", self)
      self.zAction.setCheckable(True)
      self.zAction.setChecked(True)
      self.separator = QtGui.QAction(self)
      self.separator.setSeparator(True)
      
      #  Add the actions to the context menu
      self.addActions([self.showPlotListAction, self.separator, self.xAction, self.yAction, self.zAction])
      
      #  Add widgets to the counter layout
      self.counterLayout.addWidget(self.counterLabel)
      self.counterLayout.addWidget(self.counterLineEdit)
      self.counterLayout.addSpacing(20)
      self.counterLayout.addWidget(self.stepSizeLabel)
      self.counterLayout.addWidget(self.stepSizeSpinBox)
      self.counterLayout.addStretch(0)
      self.counterLayout.addWidget(self.timerLabel)
      self.counterLayout.addWidget(self.timerSpinBox)
      
      #  Add widgets to the controls layout
      self.controlsLayout.addWidget(self.reverseButton)
      self.controlsLayout.addWidget(self.loopButton)
      self.controlsLayout.addStretch(0)
      self.controlsLayout.addWidget(self.stepBackwardButton)
      self.controlsLayout.addWidget(self.rewindButton)
      self.controlsLayout.addWidget(self.playPauseButton)
      self.controlsLayout.addWidget(self.ffButton)
      self.controlsLayout.addWidget(self.stepForwardButton)
      self.controlsLayout.addStretch(0)
      self.controlsLayout.addWidget(self.loadButton)
      self.controlsLayout.addWidget(self.exitButton)
      
      #  Add widgets to the view layout
      self.viewLayout.addWidget(self.view)
      self.viewLayout.addWidget(self.plotListWidget)
      
      #  Make sure the counter and controls don't take up too much vertical space
      self.counterFrame.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
      self.controlsFrame.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
      
      #  Add widgets and layouts to the main layout
      self.mainLayout.addWidget(self.counterFrame)
      self.mainLayout.addLayout(self.viewLayout)
      self.mainLayout.addWidget(self.timeSlider)
      self.mainLayout.addWidget(self.controlsFrame)
      
      #  Initialize the counter
      self.counterLineEdit.setText(str(self.timeSlider.value()))
      
      #  Create a timer (when this times out, the graph updates)
      self.timer = QtCore.QTimer()
      
      #  Set the timer's interval (in ms)
      self.timer.setInterval(self.timerSpinBox.value())
      
      #  Initilize the graph
      self.initializeGraph()
      
      #  Connect all the signals
      self.timer.timeout.connect(self.timeout)
      self.playPauseButton.clicked.connect(self.playPause)
      self.ffButton.clicked.connect(self.fastForward)
      self.rewindButton.clicked.connect(self.rewind)
      self.stepForwardButton.clicked.connect(self.stepForward)
      self.stepBackwardButton.clicked.connect(self.stepBackward)
      self.timerSpinBox.valueChanged[int].connect(self.timer.setInterval)
      self.loadButton.clicked.connect(self.loadPointsButtonClicked)
      self.exitButton.clicked.connect(exit)
      self.xAction.toggled.connect(self.showHideXGrid)
      self.yAction.toggled.connect(self.showHideYGrid)
      self.zAction.toggled.connect(self.showHideZGrid)
      self.showPlotListAction.toggled.connect(self.plotListWidget.setVisible)
      self.timeSlider.valueChanged.connect(self.timeSliderChanged)
      self.plotListWidget.itemChanged.connect(self.plotItemChanged)
      
   def calculateColors(self, pointCount, particleCount):
      '''Calculate the list of colors for every particle based
         on the point count and particle count given.
         Input:  number of points per particle axis <int>,
                 number of particles <int>
         Output: new color components <2D np.array> [particle <int> [red <float>, green <float>, blue <float>, alpha <float>]]'''
      #  A list of colors for every particle
      colors = []
      
      #  Go through each particle index (number)
      for particleNum in range(particleCount):
         #  There are only 10 colors, so get the 1's digit in case >10 particles are plotted
         number = int(str(particleNum)[-1])
         
         #  Alternating colors flag
         flag = False
         
         #  This is a list of colors for each particle
         particleColors = []
         
         #  Go through each point for particle's axis
         for point in range(pointCount):
            #  If the flag is False
            if(flag == False):
               #  Add color #1
               particleColors.append(self.colorCodes[number][0])
            #  Otherwise, flag is True
            else:
               #  Add color #2
               particleColors.append(self.colorCodes[number][1])
            
            #  If the modulo is 0
            if(point % 50 == 0):
               #  Toggle the flag
               flag = not flag
         
         #  Append the current particle's color list to the main colors list
         colors.append(particleColors)
      
      #  Return the converted colors list
      return(np.array(colors))

   def createIconButton(self, icon, text = "", tooltip = "", width = None, height = None, border = False):
      """Create a button that is only an icon.
         Input:  button icon (QIcon), tooltip text (string)
         Output: button (QPushButton)"""
      #  Create a button based on the given icon and text
      button = QtGui.QPushButton(icon, text)
      
      #  Set the button's tooltip
      button.setToolTip(tooltip)
      
      #  If the border flag is False
      if(border == False):
         #  Remove the button's border
         button.setStyleSheet("QPushButton { background: rgba(0,0,0,0); border-radius: 6px } QToolTip { opacity: 255 }")
         
      #  Remove any focus
      button.setFocusPolicy(QtCore.Qt.NoFocus)
      
      #  If specified set the button's size
      if(width != None and height != None):
         button.setIconSize(QtCore.QSize(width, height))
      elif(width != None):
         buttonHeight = int(button.size().height() * (width / button.size().width()))
         button.setIconSize(QtCore.QSize(width, buttonHeight))
      elif(height != None):
         buttonWidth = int(button.size().width() * (height / button.size().height()))
         button.setIconSize(QtCore.QSize(buttonWidth, height))
      
      return(button)

   def fastForward(self):
      '''Decrease the timer's timeout interval.'''
      self.timerSpinBox.setValue(self.timerSpinBox.value() - self.timerStepSize)

   def getNextPoints(self, reverse = False, initialize = False):
      '''Recalculate the plot arrays so they add or remove a point depending on the reverse flag.
         When the initialize flag is True, only set the plot points based on the current slider value.
         When the initialize flag is False, increment/decrement the slider and then set the plot points.
         Input:  reverse flag <bool>,
                 initialize flag <bool>
         Output: None'''
      #  If the initialize flag is False
      if(initialize == False):
         #  Get the step size
         step = self.stepSizeSpinBox.value()
         
         #  If not reversed (time is going forward)
         if(not reverse):
            #  Increment the time slider by the step size; maxing out at the number of points
            self.timeSlider.setValue(min(self.timeSlider.value() + step, len(self.points[0, 0, :])))
         #  Decrement the time slider by the step size; bottoming out at 1
         else:
            self.timeSlider.setValue(max(self.timeSlider.value() - step, 1))
      
      #  Go through each particle number 
      for particleNum in range(len(self.points)):
         #  Get the color list
         color = self.colors[particleNum][0:self.timeSlider.value()]
         
         #  Set the data for the current particle's line plot
         self.lineList[particleNum].setData(pos = self.points[particleNum].T[0:self.timeSlider.value()], color = color, width = 2.0)
         
         #  The size of the scatter plot point
         size = np.array([7.0, 10.0])
         
         #  Get the beginning and ending positions for the scatter plot
         posScatter = np.array([self.points[particleNum].T[0], self.points[particleNum].T[self.timeSlider.value() - 1]])
         
         #  Get the two colors
         colorScatter = np.array([color[0], color[-1]])
         
         #  Set the data for the current particle's scatter plot
         self.scatterList[particleNum].setData(pos = posScatter, color = colorScatter, size = size)

   def initializeGraph(self):
      '''Using the currently loaded points, initialize the graph.'''
      #  Block signals to the slider
      self.timeSlider.blockSignals(True)
      
      #  If there are points loaded
      if(type(self.points) == np.ndarray):
         #  If the timer is running, pause the timer (playback)
         if(self.timer.isActive() == True): self.playPause()
         
         #  Reset the slider to the initial value (0)
         self.timeSlider.setValue(0)
         self.counterLineEdit.setText("0")
         
         #  Set the spin box's range
         self.stepSizeSpinBox.setRange(1, len(self.points[0, 0, :]))
         
         #  Set the time slider's range
         self.timeSlider.setRange(1, len(self.points[0, 0, :]))
         
         #  Remove all the line plots from the view
         for item in self.lineList:
            self.view.removeItem(item)
         
         #  Remove all the scatter plots from the view
         for item in self.scatterList:
            self.view.removeItem(item)
         
         #  A list of scatter plots
         self.scatterList = []
         
         #  A list of line plots
         self.lineList = []
         
         #  For every particle to track
         for index in range(len(self.points)):
            #  Create a scatter plot
            scatter = gl.GLScatterPlotItem()
            
            #  Create a line plot
            line = gl.GLLinePlotItem()
            
            #  Add the scatter plot to the list
            self.scatterList.append(scatter)
            
            #  Add the line plot to the list
            self.lineList.append(line)
            
            #  Add the line plot to the graph view
            self.view.addItem(line)
            
            #  Add the scatter plot to the graph view
            self.view.addItem(scatter)
         
         #  Calculate the colors of the line plots
         self.colors = self.calculateColors(len(self.points[0, 0, :]), len(self.points))
         
         #  Remove all the items from the plot list widget
         for index in reversed(range(self.plotListWidget.count())):
            self.plotListWidget.takeItem(index)
         
         #  Create an "All Plots" item and set the properties of the item
         item = QtGui.QListWidgetItem("All Plots")
         item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
         item.setCheckState(QtCore.Qt.Checked)
         
         #  Add the "All Plots" item to the list widget
         self.plotListWidget.addItem(item)
         
         #  Keep track of the widest text that goes into the plot list widget
         maxTextWidth = 0
         
         #  Go through each particle index in the points
         for index in range(len(self.points)):
            #  Generate the text for this list entry
            text = "Plot " + str(index + 1)
            
            #  Create a list item with the text
            item = QtGui.QListWidgetItem(text)
            
            #  Set the properties of the item
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)
            
            #  Add the item to the plot list
            self.plotListWidget.addItem(item)
            
            #  Check if the latest text is also has the maximum width
            maxTextWidth = max(maxTextWidth, len(text))
         
         #  Margin value
         margins = 40
         
         #  Reize the width of the list widget
         self.plotListWidget.setFixedWidth(QtGui.QFontMetrics(self.plotListWidget.font()).width("X" * maxTextWidth) + margins)
         
         #  Get the intial points for each plot
         self.getNextPoints(initialize = True)
         
         #  Enable the controls
         self.playPauseButton.setEnabled(True)
         self.ffButton.setEnabled(True)
         self.rewindButton.setEnabled(True)
         self.stepBackwardButton.setEnabled(True)
         self.stepForwardButton.setEnabled(True)
         self.timeSlider.setEnabled(True)
         
         #  Calculate what the range of each axis should be (+axisLimit, -axisLimit) by finding the maximum value
         #  in the array and then adding 20% to it
         axisLimit = max(abs(self.points.max()), abs(self.points.min()))
         axisLimit = int(axisLimit * 1.20)
         
         #  Adjust the side of the x, y, and z axis so they fit the data
         self.xAxis.setData(pos = np.array([[-1 * axisLimit, 0.0, 0.0], [axisLimit, 0.0, 0.0]]), color = np.array([[1.0, 0.0, 0.0, 0.4], [1.0, 0.0, 0.0, 0.4]]), width = 3.0)
         self.yAxis.setData(pos = np.array([[0.0, -1 * axisLimit, 0.0], [0.0, axisLimit, 0.0]]), color = np.array([[0.0, 1.0, 0.0, 0.4], [0.0, 1.0, 0.0, 0.4]]), width = 3.0)
         self.zAxis.setData(pos = np.array([[0.0, 0.0, -1 * axisLimit], [0.0, 0.0, axisLimit]]), color = np.array([[0.0, 0.0, 1.0, 0.4], [0.0, 0.0, 1.0, 0.4]]), width = 3.0)
         
         #  Adjust the x grid to fit the data
         self.xGrid.resetTransform()
         self.xGrid.rotate(90, 0, 1, 0)
         self.xGrid.scale(x = axisLimit / 10.0, y = axisLimit / 10.0, z = axisLimit / 10.0)
         
         #  Adjust the y grid to fit the data
         self.yGrid.resetTransform()
         self.yGrid.rotate(90, 1, 0, 0)
         self.yGrid.scale(x = axisLimit / 10.0, y = axisLimit / 10.0, z = axisLimit / 10.0)
         
         #  Adjust the z grid to fit the data
         self.zGrid.resetTransform()
         self.zGrid.scale(x = axisLimit / 10.0, y = axisLimit / 10.0, z = axisLimit / 10.0)
         
      #  Unblock signals to the slider
      self.timeSlider.blockSignals(False)

   def loadPointsButtonClicked(self):
      '''When the load button is clicked, show a file dialog and open the new points.'''
      #  Create a file dialog
      dialog = QtGui.QFileDialog()
      
      #  If the user clicked on Select
      if(dialog.exec_() == dialog.Accepted):
         #  Get the selected file name
         selectedFile = dialog.selectedFiles()[0]
         
         #  Open the file and read in the contents
         with open(selectedFile, "r") as READ:
            pointsText = READ.read()
         
         try:
            #  Replace "array(" and ")" with nothing
            pointsText = pointsText.replace("array(", "")
            pointsText = pointsText.replace(")", "")
            
            #  Create a numpy array from the evaluated points
            points = np.array(eval(pointsText))
            
            #  If the points are verfied, set the new points
            if(verifyPoints(points) == True): self.points = points
            
            #  (Re)Initialize the graph
            self.initializeGraph()
         #  If parsing the points fails, show an error message and return
         except Exception as error:
            #  The title of the error message
            title = "Error Loading Points"
            
            #  The message of the error message
            message = "There was an error loading the points:\n\n" + str(error)
            
            #  Create and show the error message
            QtGui.QMessageBox.critical(self, title, message)
            return()

   def playPause(self):
      '''Start the timer so the graph gets updated with the data points.  Update the player icon.'''
      #  If the timer is active (running)
      if(self.timer.isActive()):
         #  Stop the timer
         self.timer.stop()
         
         #  Change the play/pause button to play
         self.playPauseButton.setIcon(self.playIcon)
         
         #  Set the tooltip
         self.playPauseButton.setToolTip("Play")
      #  Otherwise the timer is inactive (stopped)
      else:
         #  Start the timer
         self.timer.start()
         
         #  Change the play/pause button to pause
         self.playPauseButton.setIcon(self.pauseIcon)
         
         #  Set the tooltip
         self.playPauseButton.setToolTip("Pause")

   def plotItemChanged(self, item):
      '''When a plot item within the plot list widget changes (changes state from checked to unchecked).
         Input:  item <QListWidgetItem>
         Output: None'''
      #  Figure what the shown state should be
      show = item.checkState() == QtCore.Qt.Checked
      
      #  Search for the number in the item's text
      regEx = re.search("(\d+)", item.text())
      
      #  If a number was found
      if(regEx != None):
         #  Get the index from the text of the item
         index = int(regEx.group(1)) - 1
         
         #  Show/hide the plot depending on the show flag
         self.showHidePlot(index, show)
      #  Otherwise, show/hide all
      else:
         #  Go through each index in the list of plots
         for index in range(len(self.points)):
            #  Show/hide the plot
            self.showHidePlot(index, show)
         
         #  Go through each index in the plotListWidget item count
         for index in range(1, self.plotListWidget.count()):
            #  If show is True, check the plot item
            if(show == True): self.plotListWidget.item(index).setCheckState(QtCore.Qt.Checked)
            #  Otherwise, uncheck the plot item
            else: self.plotListWidget.item(index).setCheckState(QtCore.Qt.Unchecked)

   def rewind(self):
      '''Increase the timer's timeout interval by the timer step size.'''
      self.timerSpinBox.setValue(self.timerSpinBox.value() + self.timerStepSize)

   def showHidePlot(self, index, show):
      '''Show or hide the plots on the graph.
         Input:  index of plot <int>,
                 show flag <bool>
         Output: None'''
      #  Show/hide the line plot at the given index
      self.lineList[index].setVisible(show)
      
      #  Show/hide the scatter plot at the given index
      self.scatterList[index].setVisible(show)

   def showHideXGrid(self, show):
      '''Show or hide the X grid.
         Input:  show flag <bool>
         Output: None'''
      #  If show is True, add the X grid item
      if(show == True): self.view.addItem(self.xGrid)
      #  Otherwise, remove the X grid item
      elif(show == False): self.view.removeItem(self.xGrid)

   def showHideYGrid(self, show):
      '''Show or hide the Y grid.
         Input:  show flag <bool>
         Output: None'''
      #  If show is True, add the Y grid item to the view
      if(show == True): self.view.addItem(self.yGrid)
      #  Otherwise, remove the Y grid item from the view
      elif(show == False): self.view.removeItem(self.yGrid)

   def showHideZGrid(self, show):
      '''Show or hide the Z grid.
         Input:  show flag <bool>
         Output: None'''
      #  If show is True, add the Z grid item to the view
      if(show == True): self.view.addItem(self.zGrid)
      #  Otherwise, remove the Z grid item from the view
      elif(show == False): self.view.removeItem(self.zGrid)

   def stepBackward(self):
      '''Step the graph backwards in time if the timer isn't started.'''
      #  If the timer isn't running, update the graph with the reverse flag set to True
      if(not self.timer.isActive()): self.updateGraph(reverse = True)

   def stepForward(self):
      '''Step the graph forwards in time if the timer isn't started.'''
      #  If the timer isn't running, update the graph with the reverse flag set to False
      if(not self.timer.isActive()): self.updateGraph(reverse = False)

   def timeout(self):
      '''When the timer times out, update the graph with the current state of the reverse button.'''
      self.updateGraph(reverse = self.reverseButton.isChecked())

   def timeSliderChanged(self, value):
      '''When the slider's value changes.
         Input:  slider value <int>
         Output: None'''
      #  Set each of the plots' next points but don't update the slider
      self.getNextPoints(initialize = True)
      
      #  Update the counter with the current slider value
      self.counterLineEdit.setText(str(self.timeSlider.value()))

   def updateGraph(self, reverse = False):
      '''Update the graph with the current data points taking into account the
         given reverse flag.
         Input:  reverse flag <bool>
         Output: None'''
      #  If the time slider has reached its lowest value and playback is going in reverse
      if(self.timeSlider.value() <= 1 and reverse == True):
         #  If the looping button has not been checked and the timer is active (playback is running)
         if(self.loopButton.isChecked() == False and self.timer.isActive() == True):
            #  Pause the playback
            self.playPause()
         
         #  Uncheck the reverse button
         self.reverseButton.setChecked(False)
      #  Else if the time slider has reached its highest value and playback is going forward
      elif(self.timeSlider.value() >= len(self.points[0, 0, :]) and reverse == False):
         #  If the looping button has not been checked and the timer is active (playback is running)
         if(self.loopButton.isChecked() == False and self.timer.isActive() == True):
            #  Pause the playback
            self.playPause()
         
         #  Check the reverse button
         self.reverseButton.setChecked(True)
      #  Otherwise, get the next set of points with the given reverse flag
      else:
         self.getNextPoints(reverse = reverse)
      
      #  Update the counter's value
      self.counterLineEdit.setText(str(self.timeSlider.value()))

def main():
   '''The main function that is run when this file is executed (as opposed to imported).
      Input:  None
      Output: None'''
   #  Set the points to None initially
   points = None
   
   #  If a file is given at the command line and the file exists
   if(len(sys.argv) == 2 and os.path.isfile(sys.argv[1])):
      #  The path to the points file
      pointsFile = sys.argv[1]
      
      #  Print a message
      print("Loading points.  Please wait...")
      
      try:
         #  Open the file and read in the contents
         with open(pointsFile, "r") as READ:
            pointsText = READ.read()
         
         #  Replace "array(" and ")" with nothing
         pointsText = pointsText.replace("array(", "")
         pointsText = pointsText.replace(")", "")
         
         #  Create a numpy array from the evaluated points
         points = np.array(eval(pointsText))
         
         #  If the points are verfied, set the new points
         if(verifyPoints(points) == False): raise Exception("Verfication Failed")
      except Exception as error:
         print("ERROR loading the points file.\n")
         print("   Error Message: " + str(error))
         points = None
   else:
      print("No points file given.")
   
   #  Set the graphics system to native
   QtGui.QApplication.setGraphicsSystem("native")
   
   #  Create the application
   app = App(points)
   
   #  Start the application loop
   sys.exit(app.exec_())

#  This piece of code only executes if this file is executed from the command line.
#  It is not run if this file is imported from another file.
if(__name__ == "__main__"):
   main()
