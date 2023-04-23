import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sqlite3

from sqlboiler import sqlboiler

from Aubrushli import Aubrushli

from fdx2aub import fdx2aub

sb = sqlboiler()
current_dir,db_path = sb.getpaths()
#stylesfolder, currstyle, style_path = pathboiler.getstylepaths()

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'Sparcatus.Aubrushli.Aubrushli.2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initui()


    def initui(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowTitle("Aubrushli 2.1")
        self.setWindowIcon(QIcon(current_dir + "/assets/aubrushli2.ico"))
        wid = QWidget(self)
        self.setCentralWidget(wid)
        mainlayout = QGridLayout()
        #self.setLayout(mainlayout)
        wid.setLayout(mainlayout)

        # create a tab widget
        self.tabs = QTabWidget(self, tabShape=QTabWidget.TabShape.Triangular)
        #tabs = QTabWidget()
        mainlayout.addWidget(self.tabs)

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
        
        self.tabs.addTab(self.tab1,"Production/Screenplay Load")
        self.tabs.addTab(self.tab2,"Shotlist Generator")
        self.tabs.addTab(self.tab3,"Cast List")
        self.tabs.addTab(self.tab4,"Breakdown Summary")
        self.tabs.addTab(self.tab5,"Legacy Shotlist")

        mainlayout.addWidget(self.tabs, 0, 0, 2, 1)
       

        with open(os.path.join(current_dir, 'styles/aubrushli.qss'), "r") as f:
            self.setStyleSheet(f.read())
        self.endis()

    def tab1UI(self):
        self.rows = []
        self.col1layout =  QVBoxLayout()

        self.prodlabel = QLabel('Please Select/Enter new production')
        self.col1layout.addWidget(self.prodlabel)

        self.sqlsel()

        self.prodaddlabel = QLabel(self)
        self.prodaddlabel.setText("Enter New Production:")
        self.prodtext_box = QLineEdit(self)
        self.prodbutton = QPushButton("Add", self)
        self.prodbutton.clicked.connect(self.add_production)

        
        self.col1layout.addWidget(self.prodaddlabel)
        self.col1layout.addWidget(self.prodtext_box)
        self.col1layout.addWidget(self.prodbutton)
        
        self.fountain_edit =QLineEdit('')
        self.fountain_label = QLabel('Open an unmodified fountain or final draft script to generate cast lists and shot lists:')
                
        self.fountain_browse = QPushButton('Browse')
        self.fountain_browse.clicked.connect(self.browse_fountain_file)

        self.col1layout.addWidget(self.fountain_label)
        self.col1layout.addWidget(self.fountain_edit)
        self.col1layout.addWidget(self.fountain_browse)

        self.big_CSV_edit = QLineEdit('')
        self.big_CSV_label = QLabel('Save CSV version of fountain/final draft File:')
                
        self.big_CSV_browse = QPushButton('Save')
        self.big_CSV_browse.clicked.connect(self.Save_big_CSV)

        self.col1layout.addWidget(self.big_CSV_label)
        self.col1layout.addWidget(self.big_CSV_edit)
        self.col1layout.addWidget(self.big_CSV_browse)

        self.status_bar1 = QStatusBar()
    

        # Add a message to the status bar
        self.status_bar1.showMessage("Aubrushli 2.1")
        self.col1layout.addWidget(self.status_bar1)


        
        self.tab1.setLayout(self.col1layout)
        

		
    def tab2UI(self):
        col2layout =  QVBoxLayout()

        self.shot_gen_lab = QLabel('Generate shotlists of ALL scenes from an unmodified fountain/final draft Script')

 

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
        self.status_bar2.showMessage("Aubrushli 2.1")
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
        self.status_bar3.showMessage("Aubrushli 2.1")
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
        self.status_bar4.showMessage("Aubrushli 2.1")
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
        self.status_bar5.showMessage("Aubrushli 2.1")
        col5layout.addWidget(self.status_bar5)
        
        self.tab5.setLayout(col5layout)

    def sqlins(self, prodname):
        # Connect to the database file or create it if it doesn't exist
        current_dir = os.path.dirname(os.path.abspath(__file__))

        

        connection = sqlite3.connect(current_dir + "/aubrushli.db")
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        # Define the data to insert
        ProductionName = prodname
        # Execute the insert query
        cursor.execute("INSERT INTO production (ProductionName) VALUES (?)", (ProductionName,))
        # Commit the transaction to the database
        connection.commit()
        # Close the database connection
        connection.close()
        #self.rows = []
        self.initui()


    def add_production(self):
        # Get the value from the text box
        myproduction = self.prodtext_box.text()

        # Add production to the SQL table
        self.add_to_database(myproduction)

    def add_to_database(self, myproduction):
        # Function to add data to SQL table
        self.sqlins(myproduction)


    def browse_fountain_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'Fountain files (*.fountain);;Final Draft files (*.fdx)')
        if filename:
            extension = filename[0].split(".")[-1]
            if extension == "fountain": 
                self.fountain_show()
            else:
                self.fdx_show()
            self.fountain_edit.setText(filename[0])
            msgstr = ''
            if len(filename[0]) >0:
                msgstr = filename[0] + " Loaded!!!"
            else:
                msgstr = "Nothing Loaded!!!"
            self.status_bar1.showMessage(msgstr)

    def generate_shotlists(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))

        fountainfile = self.fountain_edit.text()

        # Check if the input file exists
        if not os.path.exists(fountainfile):
            self.status_bar2.showMessage("file does not exist")
            return
        
        shotsdeffile = self.shot_def_edit.text()

        # Check if the input file exists
        if not os.path.exists(shotsdeffile):
            self.status_bar2.showMessage("shot definition file does not exist")
            return

        foldername = QFileDialog.getExistingDirectory(self, 'Open Folder', current_dir)
        if foldername:

            extension = fountainfile.split(".")[-1]

            if extension == "fountain":
            
                aubshot = Aubrushli()

                aubshot.generateallshotlists(fountainfile, shotsdeffile, foldername)

            else:
                fdx = fdx2aub()
                fdx.fdx2dbaub(fountainfile, shotsdeffile, foldername )

            self.save_folder_edit.setText(foldername)
            
            self.status_bar2.showMessage("SHOTLISTS SAVED IN " +  foldername)
  

    def browse_shot_def(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'CSV files (*.csv)')
        if filename:
            self.shot_def_edit.setText(filename[0])
            self.status_bar2.showMessage("LOADED " +  filename[0])

    def Save_big_CSV(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV of Fountain document", current_dir, "Text Files (*.csv)", options=options)
        
                # Get the input file name
        input_file_name = self.fountain_edit.text()

        # Check if the input file exists
        if not os.path.exists(input_file_name):
            self.status_bar1.showMessage("fountain file does not exist")
            return
        

        extension = input_file_name.split(".")[-1]
        
        themessage = ''
        if extension == "fountain":
            
            aubshot = Aubrushli()

            aubshot.createbigcsv(input_file_name, file_name)
            themessage = "Saved at " + file_name

        else:
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                connection = sqlite3.connect(current_dir + "/aubrushli.db")
                connection.execute('PRAGMA synchronous = NORMAL')
                connection.execute('PRAGMA journal_mode = WAL')
                connection.execute('PRAGMA cache_size = -8192')
                connection.commit()
                cursor = connection.cursor()
                sql = 'SELECT max(ScreenplayID) FROM screenplay_document where path =?'
                params = (input_file_name,)  # create a tuple of parameters
                cursor.execute(sql, params)  # pass the tuple to cursor.execute()
                screenplayid = cursor.fetchone()[0]  # fetch the results
                connection.commit()
                connection.close()
                if screenplayid is not None:
                    fdx = fdx2aub()
                    fdx.createbigcsv(file_name, screenplayid)
                    themessage = "Saved at " + file_name
                else:
                    themessage = "Sorry you need to create shotlists first for final draft"
        


        self.big_CSV_edit.setText(file_name)
        self.status_bar1.showMessage(themessage)

    def Save_cast_list(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file_name = self.fountain_edit.text()

            # Check if the input file exists
        if not os.path.exists(input_file_name):
            self.status_bar3.showMessage("Input file does not exist")
            return

        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Cast List", current_dir, "Text Files (*.csv)", options=options)
        
        extension = input_file_name.split(".")[-1]
        
        themessage = ''
        if extension == "fountain":
            
                aubshot = Aubrushli()

                aubshot.create_cast_list(input_file_name, file_name)
                themessage = "Cast list saved to " + file_name

        else:
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                connection = sqlite3.connect(current_dir + "/aubrushli.db")
                connection.execute('PRAGMA synchronous = NORMAL')
                connection.execute('PRAGMA journal_mode = WAL')
                connection.execute('PRAGMA cache_size = -8192')
                connection.commit()
                cursor = connection.cursor()
                sql = 'SELECT max(ScreenplayID) FROM screenplay_document where path =?'
                params = (input_file_name,)  # create a tuple of parameters
                cursor.execute(sql, params)  # pass the tuple to cursor.execute()
                screenplayid = cursor.fetchone()[0]  # fetch the results
                connection.commit()
                connection.close()
                if screenplayid is not None:
                    fdx = fdx2aub()
                    fdx.create_cast_list(file_name, screenplayid)
                    themessage = "Cast list saved to " + file_name
                else:
                    themessage = "Sorry you need to create shotlists first for final draft castlists"

        self.cast_list_edit.setText(file_name)
        # # Show a message that the cast list has been created
        self.status_bar3.showMessage(themessage)

    def on_breakdown_summary_browse_clicked(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'Fountain files (*.fountain)')
        if filename:
            self.breakdown_summary_edit.setText(filename[0])
            self.status_bar4.showMessage(filename[0] + " loaded")

    def on_breakdown_summary_save_clicked(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = QFileDialog.getOpenFileName(self, 'Open File', current_dir, 'Fountain files (*.fountain)')
        if filename:
            self.OG_shot_list_browse_edit.setText(filename[0])
            self.status_bar5.showMessage(filename[0] + " loaded")

    def createlegacyshotlist(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
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
    
    def sqlsel(self):
        sb = sqlboiler()
        productions = sb.getallproduction()
        for i, row in productions.iterrows():
            radio_button = QRadioButton(f"Production: {row['ProductionName']}")
            radio_button.toggled.connect(self.radio_clicked)
            self.col1layout.addWidget(radio_button)
            self.rows.append((i + 1, row, radio_button))
    
    def radio_clicked(self):
        self.fountain_edit.show()
        self.fountain_label.show()
        self.fountain_browse.show()

    def fountain_show(self):
        self.tabs.setTabVisible(1,True)
        self.tabs.setTabVisible(2,True) 
        self.tabs.setTabVisible(3,True) 
        self.tabs.setTabVisible(4,True)
        self.big_CSV_edit.show()
        self.big_CSV_label.show()
        self.big_CSV_browse.show()

    def fdx_show(self):
        self.tabs.setTabVisible(1,True)
        self.tabs.setTabVisible(2,True) 
        self.big_CSV_edit.show()
        self.big_CSV_label.show()
        self.big_CSV_browse.show()
    
    def endis(self):
        #print("check")
        self.tabs.setTabVisible(1,False)
        self.tabs.setTabVisible(2,False) 
        self.tabs.setTabVisible(3,False) 
        self.tabs.setTabVisible(4,False)
        self.fountain_edit.hide()
        self.fountain_label.hide()
        self.fountain_browse.hide()
        self.big_CSV_edit.hide()
        self.big_CSV_label.hide()
        self.big_CSV_browse.hide()
        #self.tabs.widget(1).setVisible(False)

      


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('aubrushli2.ico'))
window = MainWindow()
window.show()
sys.exit(app.exec_())

