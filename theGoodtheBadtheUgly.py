"""
Bare bones interface for sorting imagery
Mark Lundine, UGSG
"""

import os
import glob
import sys
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        sizeObject = QDesktopWidget().screenGeometry(-1)
        global screenWidth
        screenWidth = sizeObject.width()
        global screenHeight
        screenHeight = sizeObject.height()
        global bw1
        bw1 = int(screenWidth/15)
        global bw2
        bw2 = int(screenWidth/50)
        global bh1
        bh1 = int(screenHeight/15)
        global bh2
        bh2 = int(screenHeight/20)

        self.setWindowTitle("Image Sorter")
        self.home()

    def open_image(self, image_path, lab):
        global image_lab
        image_lab=lab
        try:
            image_lab.hide()
        except:
            pass
        
        image_lab = QLabel(self)
        pixmap = QPixmap(image_path)
        im_width = pixmap.width()
        im_height = pixmap.height()
        max_dim = max(im_width, im_height)
        max_screen = max(screenWidth, screenHeight)
        max_scale = int(max_screen/max_dim)
        scaleFac = 1
        small_pixmap = pixmap.scaled(im_width*max_scale, im_height*max_scale)
        image_lab.setPixmap(small_pixmap)
        image_lab.resize(int(pixmap.width()/scaleFac),int(pixmap.height()/scaleFac))
        self.vbox.addWidget(image_lab, 1, 1)
        image_lab.show()
        return image_lab

    def sort_image(self, class_label, image_path):
        """do stuff"""
        class_dir = os.path.join(os.path.dirname(image_path), class_label)
        try:
            os.mkdir(class_dir)
        except:
            pass
        image_name = os.path.basename(image_path)
        new_image_path = os.path.join(class_dir, image_name)
        shutil.move(image_path, new_image_path)
        return image_path, new_image_path

    def get_next_image(self, i, image_paths, image_lab):
        global idx
        idx = i+1
        global current_image
        current_image = image_paths[idx]
        self.open_image(current_image, image_lab)

    def undo(self, image_path, new_image_path):
        try:
            shutil.move(new_image_path, image_path)
        except:
            pass
        
    def select_folder(self, classes):
        global idx
        idx=0
        next_image = QPushButton('Next Image')
        undo = QPushButton('Undo')
        self.vbox.addWidget(next_image, 0, 1)
        self.vbox.addWidget(undo, 0, 2)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folderName:
            image_paths = glob.glob(folderName + '/*.jpg')+glob.glob(folderName+'/*.png')+glob.glob(folderName+'/*.jpeg')
            global current_image
            current_image = image_paths[idx]
            global image_lab
            image_lab = QLabel()
            image_lab = self.open_image(current_image, image_lab)
            i=0
            buttons = [None]*len(classes)
            for c in classes:
                b = QPushButton(c)
                self.vbox.addWidget(b, i, 2)
                buttons[i] = b
                i=i+1
            
            ##Actions
            next_image.clicked.connect(lambda: self.get_next_image(idx, image_paths, image_lab))
            #undo.clicked.connect(lambda: self.undo(image_path, new_image_path)
            ##class label buttons, if you add another class label, add another button click connection
            #good
            buttons[0].clicked.connect(lambda: self.sort_image(classes[0], current_image))
            #bad
            buttons[1].clicked.connect(lambda: self.sort_image(classes[1], current_image))
        
    def home(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QGridLayout()             # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)

        ##specify class labels here, these are classes for coastal satellite imagery
        classes = ['good', 'bad']

        open_directory = QPushButton('Select Image Directory')
        self.vbox.addWidget(open_directory, 0, 0)
        
        #Actions
        open_directory.clicked.connect(lambda: self.select_folder(classes))

        #Scroll policies
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)


## Function outside of the class to run the app   
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

## Calling run to run the app
run()
