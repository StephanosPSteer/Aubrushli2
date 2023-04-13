import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtCore import *

from sqlboiler import sqlboiler

from Aubrushli import Aubrushli

sb = sqlboiler()
current_dir,db_path = sb.getpaths()
#stylesfolder, currstyle, style_path = pathboiler.getstylepaths()

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'Sparcatus.Aubrushli.Aubrushli.2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class UI(QWidget):

    def __init__(self):
        super().__init__()
        #pb = pathboiler()
        #current_dir,db_path = pb.getkeypaths()


#         # create a layout
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowTitle("Aubrushli 2.0")
        self.setWindowIcon(QIcon(current_dir + "/assets/aubrushli2.ico"))
        mainlayout = QGridLayout()
        self.setLayout(mainlayout)

        # create a tab widget
        tabs = QTabWidget(self, tabShape=QTabWidget.TabShape.Triangular)
        #tabs = QTabWidget()
        mainlayout.addWidget(tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab1.setObjectName("Tab1")
        
        self.tab2.setObjectName("Tab2")
        self.tab3.setObjectName("Tab3")
        
        self.tab4.setObjectName("Tab4")
        self.tab5.setObjectName("Tab5")
        
        QDir.addSearchPath('assets', os.path.join(current_dir, 'assets'))
        #print(current_dir)
        aubrob = "QWidget#Tab1 {background-image: url(assets:aub_rob.svg); background-repeat: no-repeat;}"
        #print(aubrob)
        
        self.tab1.setStyleSheet(aubrob)
        self.tab2.setStyleSheet(aubrob.replace("1","2"))
        self.tab3.setStyleSheet(aubrob.replace("1","3"))
        self.tab4.setStyleSheet(aubrob.replace("1","4"))
        self.tab5.setStyleSheet(aubrob.replace("1","5"))
        
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()
        
        tabs.addTab(self.tab1,"Fountain Load")
        tabs.addTab(self.tab2,"Shotlist Generator")
        tabs.addTab(self.tab3,"Cast List")
        tabs.addTab(self.tab4,"Breakdown Summary")
        tabs.addTab(self.tab5,"Legacy Shotlist")

        mainlayout.addWidget(tabs, 0, 0, 2, 1)
       
        self.setLayout(mainlayout)


                # Load the style sheet
        with open("G:/Aubrushli_images_current/styles/aubrushli.qss", "r") as f:
            self.setStyleSheet(f.read())

    def tab1UI(self):
        
        col1layout =  QVBoxLayout()
        
        self.fountain_edit =QLineEdit('')
        self.fountain_label = QLabel('Open an unmodified fountain script to generate cast lists and shot lists:')
                
        self.fountain_browse = QPushButton('Browse')
        self.fountain_browse.clicked.connect(self.browse_fountain_file)

        col1layout.addWidget(self.fountain_label)
        col1layout.addWidget(self.fountain_edit)
        col1layout.addWidget(self.fountain_browse)

        self.big_CSV_edit = QLineEdit('')
        self.big_CSV_label = QLabel('Save CSV version of fountain File:')
                
        self.big_CSV_browse = QPushButton('Save')
        self.big_CSV_browse.clicked.connect(self.Save_big_CSV)

        col1layout.addWidget(self.big_CSV_label)
        col1layout.addWidget(self.big_CSV_edit)
        col1layout.addWidget(self.big_CSV_browse)

        self.status_bar1 = QStatusBar()
        #self.setStatusBar(self.status_bar)

        # Add a message to the status bar
        self.status_bar1.showMessage("Aubrushli 2.0")
        col1layout.addWidget(self.status_bar1)
        
        self.tab1.setLayout(col1layout)
		
    def tab2UI(self):
        col2layout =  QVBoxLayout()

        self.shot_gen_lab = QLabel('Generate shotlists of ALL scenes from an unmodified fountain Script')

 

        self.shot_def_edit = QLineEdit('')
        self.shot_def_label = QLabel('Select your shots definition File:')
                
        self.shot_def_browse = QPushButton('Browse')
                
        self.shot_def_browse.clicked.connect(self.browse_shot_def)
        col2layout.addWidget(self.shot_gen_lab)
        col2layout.addWidget(self.shot_def_label)
        col2layout.addWidget(self.shot_def_edit)
        col2layout.addWidget(self.shot_def_browse)


        self.save_folder_edit = QLineEdit('')        
        self.save_folder_label = QLabel('Choose folder to save the generated shotlists and generate!!!')
                
        self.save_folder_browse = QPushButton('Save')
        self.save_folder_browse.clicked.connect(self.generate_shotlists)

        
        col2layout.addWidget(self.save_folder_label)
        col2layout.addWidget(self.save_folder_edit)
        col2layout.addWidget(self.save_folder_browse)

        self.status_bar2 = QStatusBar()
        #self.setStatusBar(self.status_bar)

        # Add a message to the status bar
        self.status_bar2.showMessage("Aubrushli 2.0")
        col2layout.addWidget(self.status_bar2)
        
        self.tab2.setLayout(col2layout)

    def tab3UI(self):

        col3layout =  QVBoxLayout()

        self.cast_list_label = QLabel("Create a Cast List")
        self.cast_list_edit = QLineEdit()
        self.cast_list_browse = QPushButton("Save")
        self.cast_list_browse.clicked.connect(self.Save_cast_list)


        col3layout.addWidget(self.cast_list_label)
        #layout.addWidget(self.cast_list_checkbox)
        col3layout.addWidget(self.cast_list_edit)
        col3layout.addWidget(self.cast_list_browse)
        #layout.addWidget(self.cast_list_button)

        self.status_bar3 = QStatusBar()
        #self.setStatusBar(self.status_bar)

        # Add a message to the status bar
        self.status_bar3.showMessage("Aubrushli 2.0")
        col3layout.addWidget(self.status_bar3)
        
        self.tab3.setLayout(col3layout)

    def tab4UI(self):

        col4layout =  QVBoxLayout()
         # Create the breakdown summary button
        self.breakdown_summary_label = QLabel("Create A Breakdown Summary from a modified fountain script")
        self.breakdown_summary_browse_edit = QLineEdit()
        self.breakdown_summary_browse = QPushButton("Browse")
        self.breakdown_summary_edit = QLineEdit()
        self.breakdown_summary_save = QPushButton("Save")
        self.breakdown_summary_save.clicked.connect(self.on_breakdown_summary_save_clicked)
        self.breakdown_summary_browse.clicked.connect(self.on_breakdown_summary_browse_clicked)
        col4layout.addWidget(self.breakdown_summary_label)
        
        
        col4layout.addWidget(self.breakdown_summary_browse_edit)
        col4layout.addWidget(self.breakdown_summary_browse)
        col4layout.addWidget(self.breakdown_summary_edit)
        col4layout.addWidget(self.breakdown_summary_save)

        self.status_bar4 = QStatusBar()
        #self.setStatusBar(self.status_bar)

        # Add a message to the status bar
        self.status_bar4.showMessage("Aubrushli 2.0")
        col4layout.addWidget(self.status_bar4)
        
        self.tab4.setLayout(col4layout)

       
    def tab5UI(self):

        col5layout =  QVBoxLayout()

        self.OG_shot_list_label = QLabel("Create a Shot List from a modified fountain script")
        self.OG_shot_list_browse_edit = QLineEdit()
        self.OG_shot_list_browse = QPushButton("Browse")
        self.OG_shot_list_save_edit = QLineEdit()
        self.OG_shot_list_save = QPushButton("Save")
        self.OG_shot_list_save.clicked.connect(self.createlegacyshotlist)
        self.OG_shot_list_browse.clicked.connect(self.get_legacy_fountain_shot_file)
        col5layout.addWidget(self.OG_shot_list_label)
        col5layout.addWidget(self.OG_shot_list_browse_edit)
        col5layout.addWidget(self.OG_shot_list_browse)
        col5layout.addWidget(self.OG_shot_list_save_edit)
        col5layout.addWidget(self.OG_shot_list_save)
        #self.tab2.setTabText(2,"Breakdown Summary")

        self.status_bar5 = QStatusBar()
        #self.setStatusBar(self.status_bar)

        # Add a message to the status bar
        self.status_bar5.showMessage("Aubrushli 2.0")
        col5layout.addWidget(self.status_bar5)
        
        self.tab5.setLayout(col5layout)


    


    def browse_fountain_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'Fountain files (*.fountain)')
        if filename:
            self.fountain_edit.setText(filename[0])
            msgstr = filename[0] + " Loaded!!!"
            self.status_bar1.showMessage(msgstr)

    def generate_shotlists(self):

        fountainfile = self.fountain_edit.text()

        # Check if the input file exists
        if not os.path.exists(fountainfile):
            self.status_bar2.showMessage("fountain file does not exist")
            return
        
        shotsdeffile = self.shot_def_edit.text()

        # Check if the input file exists
        if not os.path.exists(shotsdeffile):
            self.status_bar2.showMessage("shot definition file does not exist")
            return

        foldername = QFileDialog.getExistingDirectory(self, 'Open Folder', current_dir)
        if foldername:
            
            aubshot = Aubrushli()

            aubshot.generateallshotlists(fountainfile, shotsdeffile, foldername)

            #generateallshotlists(self, fountainfile, shotvalsfile, outpath)

            self.save_folder_edit.setText(foldername)
            
            self.status_bar2.showMessage("SHOTLISTS SAVED AT " +  foldername)
  

    def browse_shot_def(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'CSV files (*.csv)')
        if filename:
            self.shot_def_edit.setText(filename[0])
            self.status_bar2.showMessage("LOADED " +  filename[0])

    def Save_big_CSV(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV of Fountain document", current_dir, "Text Files (*.csv)", options=options)
        
                # Get the input file name
        input_file_name = self.fountain_edit.text()

        # Check if the input file exists
        if not os.path.exists(input_file_name):
            self.status_bar1.showMessage("fountain file does not exist")
            return
        
        aubshot = Aubrushli()

        aubshot.createbigcsv(input_file_name, file_name)

        self.big_CSV_edit.setText(file_name)
        self.status_bar1.showMessage("Saved at " + file_name)

    def Save_cast_list(self):

        input_file_name = self.fountain_edit.text()

            # Check if the input file exists
        if not os.path.exists(input_file_name):
            self.status_bar3.showMessage("Input file does not exist")
            return

        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Cast List", current_dir, "Text Files (*.csv)", options=options)
        
        aubshot = Aubrushli()

        aubshot.create_cast_list(input_file_name, file_name)
            
        self.cast_list_edit.setText(file_name)
        # # Show a message that the cast list has been created
        self.status_bar3.showMessage("Cast list saved to " + file_name)

    def on_breakdown_summary_browse_clicked(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'Fountain files (*.fountain)')
        if filename:
            self.breakdown_summary_edit.setText(filename[0])
            self.status_bar4.showMessage(filename[0] + " loaded")

    def on_breakdown_summary_save_clicked(self):
        # Get the input file name
        fountainfile = self.breakdown_summary_edit.text()

        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Breakdown Summary", current_dir, "Text Files (*.csv)", options=options)
        

        # Check if the input file exists
        if not os.path.exists(fountainfile):
            self.status_bar4.showMessage("Input file does not exist")
            return
        
        if file_name:
        
            aubshot = Aubrushli()

            aubshot.create_breakdown_summary(fountainfile, file_name)

            self.breakdown_summary_edit.setText(file_name)
        # # Show a message that the cast list has been created
            self.status_bar4.showMessage("Breakdown Summary Created at " + file_name)

    def get_legacy_fountain_shot_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'Fountain files (*.fountain)')
        if filename:
            self.OG_shot_list_browse_edit.setText(filename[0])
            self.status_bar5.showMessage(filename[0] + " loaded")

    def createlegacyshotlist(self):
        fountainfile = self.OG_shot_list_browse_edit.text()

        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Breakdown Summary", current_dir, "Text Files (*.csv)", options=options)
        

        # Check if the input file exists
        if not os.path.exists(fountainfile):
            self.status_bar5.showMessage("Input file does not exist")
            return
        
        if file_name:
        
            aubshot = Aubrushli()

            aubshot.create_legacy_shotlist(fountainfile, file_name)

            self.OG_shot_list_save_edit.setText(file_name)
        # # Show a message that the cast list has been created
            self.status_bar5.showMessage("Legacy shotlist Created at " + file_name)
      


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('aubrushli2.ico'))
ui = UI()
ui.show()
sys.exit(app.exec_())

