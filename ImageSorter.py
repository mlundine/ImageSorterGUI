import os
import glob
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

    def open_image(self, image_path, old_label=None):
        if old_label!=None:
            old_label.hide()
        label = QLabel(self)
        pixmap = QPixmap(image_path)
        scaleFac = 1
        small_pixmap = pixmap.scaled(int(screenWidth/2), int(screenWidth/2))
        label.setPixmap(small_pixmap)
        label.resize(int(pixmap.width()/scaleFac),int(pixmap.height()/scaleFac))
        self.vbox.addWidget(label, 1, 1)
        label.show()
        return label

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

    def get_next_image(self, i, image_paths, image_lab):
        global idx
        idx = i+1
        global current_image
        current_image = image_paths[idx]
        self.open_image(current_image, old_label=image_lab)
        
    def select_folder(self, classes):
        global idx
        idx=0
        next_image = QPushButton('Next Image')
        self.vbox.addWidget(next_image, 0, 1)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folderName:
            image_paths = glob.glob(folderName + '/*.jpg')
            global current_image
            current_image = image_paths[idx]
            image_lab = self.open_image(current_image)
            i=0
            buttons = [None]*len(classes)
            for c in classes:
                b = QPushButton(c)
                self.vbox.addWidget(b, 2, i)
                buttons[i] = b
                i=i+1
            
            ##Actions
            next_image.clicked.connect(lambda: self.get_next_image(idx, image_paths, image_lab))

            ##class label buttons, if you add another class label, add another button click connection
            #clear
            buttons[0].clicked.connect(lambda: self.sort_image(classes[0], current_image))
            #whitewater
            buttons[1].clicked.connect(lambda: self.sort_image(classes[1], current_image))
            #snow_ice
            buttons[2].clicked.connect(lambda: self.sort_image(classes[2], current_image))
            #warped_color_space
            buttons[3].clicked.connect(lambda: self.sort_image(classes[3], current_image))
            #big_gaps
            buttons[4].clicked.connect(lambda: self.sort_image(classes[4], current_image))
            #other
            buttons[5].clicked.connect(lambda: self.sort_image(classes[5], current_image))
        
    def home(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QGridLayout()             # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.widget.setLayout(self.vbox)

        ##specify class labels here, these are classes for coastal satellite imagery
        classes = ['clear', 'whitewater', 'snow_ice', 'warped_color_space', 'big_gaps', 'other']

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
