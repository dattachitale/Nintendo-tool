import sys
import re
import subprocess
from PySide2.QtCore import QThread
import os
import PySide2
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
from PySide2.QtGui import *
from datetime import date, time
import datetime
env = os.getenv("NINTENDO_SDK_ROOT")


#write a function to check connection at beggining
def run_cmd():
        check = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if check.wait()!= 0 or Connection_out.wait()!= 0:
            return True
        else:
            return False

'''********************** Main GUI Dialogue class **********************'''
class My_Main_Dialog(QtWidgets.QWidget):
    def __init__(self,title):
        super().__init__()
        self.setWindowTitle(title)
        #self.setMinimumHeight(400)
        #self.setMinimumWidth(532)
        self.setFixedSize(532,410)
        self.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.Main_Menu = QtWidgets.QMenuBar()
        self.File_Menu = self.Main_Menu.addMenu('&File')
        self.View_Menu = self.Main_Menu.addMenu('&View')
        self.Console_Menu = self.Main_Menu.addMenu('&Console')
        self.Help_Menu = self.Main_Menu.addMenu('&Help')
                            # File_Menu
        self.Set_name = self.File_Menu.addAction('Set your console &name')
        self.Set_name.setIcon(QIcon("./Images/fileMenu_setName.png"))
        self.File_Menu.addSeparator()
        # self.Exit_app.setIcon(QIcon("exit.png"))
        self.Set_name.triggered.connect(self.set_name)
        self.Swich_app = self.File_Menu.addAction('&Switch to Home Menu')
        self.Swich_app.setIcon(QIcon("./Images/fileMenu_home.png"))
        self.File_Menu.addSeparator()
        #self.Exit_app.setIcon(QIcon("exit.png"))
        self.Swich_app.triggered.connect(self.swich_app)
        self.Exit_app = self.File_Menu.addAction('&Exit')
        self.Exit_app.setIcon(QIcon("./Images/fileMenu_exit.png"))
        self.Exit_app.triggered.connect(self.exit_app)
                            #View_Menu
        self.Firmware = self.View_Menu.addAction("&Console Firmware Version")
        self.Firmware.setIcon(QIcon("./Images/viewManu_firmware.png"))
        self.View_Menu.addSeparator()
        self.Firmware.triggered.connect(self.firmware_info)
        self.App_List = self.View_Menu.addAction("&Installed App List")
        self.App_List.setIcon(QIcon("./Images/viewManu_appList.png"))
        self.View_Menu.addSeparator()
        self.App_List.triggered.connect(self.application_list)
        self.Console_List = self.View_Menu.addAction('&Registered Target List')
        self.Console_List.setIcon(QIcon("./Images/viewManu_consoleList.png"))
        self.View_Menu.addSeparator()
        self.Console_List.triggered.connect(self.console_list)
                            #Console_Menu
        self.Connect_Console = self.Console_Menu.addAction('&Connect')
        self.Connect_Console.setIcon(QIcon("./Images/consoleMenu_connect.png"))
        self.Console_Menu.addSeparator()
        self.Connect_Console.triggered.connect(self.connect_console)
        self.Disconnect_Console = self.Console_Menu.addAction('&Disconnect')
        self.Disconnect_Console.setIcon(QIcon("./Images/consoleMenu_disconnect.png"))
        self.Console_Menu.addSeparator()
        self.Disconnect_Console.triggered.connect(self.disconnect_console)
        self.Power_Off = self.Console_Menu.addAction('&Power off')
        self.Power_Off.setIcon(QIcon("./Images/consoleMenu_powerOff.png"))
        self.Console_Menu.addSeparator()
        self.Power_Off.triggered.connect(self.power_off)
        self.Reboot = self.Console_Menu.addAction('&Reboot')
        self.Reboot.setIcon(QIcon("./Images/consoleMenu_reboot.png"))
        self.Console_Menu.addSeparator()
        self.Reboot.triggered.connect(self.reboot)
                            #Help_Menu
        self.About = self.Help_Menu.addAction('&About')
        self.About.setIcon(QIcon("./Images/helpMenu_about.png"))
        self.Help_Menu.addSeparator()
        self.About.triggered.connect(self.about)
        self.Link_menu = self.Help_Menu.addMenu("&Links")
        self.Link_menu.setIcon(QIcon("./Images/helpMenu_link.png"))
        self.Home = QtWidgets.QAction("&Switch Home")
        self.Home.setIcon(QIcon("./Images/helpMenu_home.png"))
        self.Train_Doc = QtWidgets.QAction("&Training Documents")
        self.Train_Doc.setIcon(QIcon("./Images/helpMenu_Train_document.png"))
        self.NDI_Doc = QtWidgets.QAction("&NDI Documents")
        self.NDI_Doc.setIcon(QIcon("./Images/helpMenu_ndi_document.png"))
        self.Link_menu.addAction(self.Home)
        self.Link_menu.addSeparator()
        self.Document = self.Link_menu.addMenu("&Documents")
        self.Document.setIcon(QIcon("./Images/helpMenu_documents.png"))
        self.Home.triggered.connect(self.home_url)
        self.Document.addAction(self.Train_Doc)
        self.Document.addSeparator()
        self.Train_Doc.triggered.connect(self.training_doc_explorer)
        self.Document.addAction(self.NDI_Doc)
        self.NDI_Doc.triggered.connect(self.ndi_doc)

    def create_layout(self):
        self.Main_layout = QtWidgets.QVBoxLayout()
        self.Tab_Widget = QtWidgets.QTabWidget()
        self.Tab_Widget.addTab(Tab_Applications(), "Manage Applications")
        self.Tab_Widget.addTab(Tab_Media(), "Media and Attachments")
        self.Tab_Widget.addTab(Tab_User_accounts(), "Manage User Accounts")
        self.Tab_Widget.addTab(Tab_Save_Data(), "Manage Save Data")
        self.Main_layout.addWidget(self.Tab_Widget)
        self.setLayout(self.Main_layout)
        self.Main_layout.setMenuBar(self.Main_Menu)

    '''***************** File Menu Functions' Declaration *****************'''
    '''Set name to console'''
    def set_name(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=False)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=False)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to set console name</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            self.Set_name_input = QtWidgets.QInputDialog()
            text, ok = self.Set_name_input.getText(self, 'Console Name', 'Make sure console is connected first \n\nEnter name for your console :')
            self.Set_name_input.setOkButtonText("datta")
            if ok and text:
                comm = env + r'\Tools\CommandLineTools\ControlTarget.exe set-name ' + text
                subprocess.Popen(comm, shell=True)
                New_name = "<b>" + text + "</b>"
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Name set Information                                                                                                  ")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("Console Name has been set to: " +New_name)
                sms_box.setInformativeText("Please check <b>Target Name</b> column of Target Manager to reflect changes.")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()

    '''Switch boot menu to Home'''
    def swich_app(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to switch the initial boot menu as Home</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            self.sms_box = QtWidgets.QMessageBox()
            self.sms_box.setWindowTitle("Switch to Home Menu: ")
            self.sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            self.sms_box.setText('''<b>Are you sure you want to use this option? If you click Yes, console will restart.''')
            self.sms_box.setInformativeText('''Please use this option only once (after you initialize console) to set console's Initial Boot Menu to Home Menu.''')
            self.sms_box.setDetailedText('''This option is used when you want to set console's Initial Boot Menu as "HOME MENU" (Usally after initialization)''')
            self.sms_box.setStandardButtons(self.sms_box.Yes | self.sms_box.No)
            self.sms_box.setDefaultButton(self.sms_box.No)
            self.sms_box.setIcon(self.sms_box.Warning)
            self.press = self.sms_box.exec_()

            if self.press == self.sms_box.Yes:
                subprocess.Popen(env + r'\Tools\CommandLineTools\TargetShell.exe switch-menu --menu=homemenu --reset', shell=True)
            else:
                self.sms_box.close()

    '''Exit the application'''
    def exit_app(self):
        self.close()


    '''***************** View Menu Functions' Declaration *****************'''
    '''Firmware Information'''
    def firmware_info(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to show Firmware information</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            self.Console_Firmware = subprocess.check_output(env + r'\Tools\CommandLineTools\ControlTarget.exe firmware-version', shell=True)
            self.Firm_Result = self.Console_Firmware.decode("latin1", 'ignore').split('\n')
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Firmware Information")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText(self.Firm_Result[0])
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

    '''get application list'''
    def application_list(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to show Application list</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            self.Aplications = subprocess.check_output(env + r'\Tools\CommandLineTools\ControlTarget.exe list-application', shell=True)
            self.App_Result = self.Aplications.decode("latin1", 'ignore').split('\n')
            result = ""
            for i in range(2, len(self.App_Result) - 3):
                result = result + self.App_Result[i]
            #print(result)
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Application Information                                                                                    ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>Installed applications are:</b>")
            sms_box.setInformativeText(result)
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

    '''Get Console list'''
    def console_list(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to show Console list</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            self.Consoles = subprocess.check_output(env + r'\Tools\CommandLineTools\ControlTarget.exe list-target', shell=True)
            self.Console_Result = self.Consoles.decode("latin1", 'ignore').split('\t')
            result = ""
            for i in range(0, len(self.Console_Result) - 1):
                result = result + self.Console_Result[i]
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Console Information ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>Registered Consoles:</b> ")
            sms_box.setInformativeText(result)
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

    '''***************** Console Menu Functions' Declaration *****************'''
    '''Connect console'''
    def connect_console(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to connect</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("Switch console has been connected to Nintendo Target Manager")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
            #self.Connect_Console.setEnabled(False)
            #self.Disconnect_Console.setEnabled(True)

    '''Disconnect console'''
    def disconnect_console(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to disconnect</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe disconnect', shell=True)
            sms_box = QtWidgets.QMessageBox()
            #self.sms_box.setParent(self)
            sms_box.setWindowTitle("Disconnection Information")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("Switch kit has been disconnected from Nintendo Target Manager")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
            #self.Disconnect_Console.setEnabled(False)
            #self.Connect_Console.setEnabled(True)

    '''Turn off console'''
    def power_off(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to Power Off</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe power-off', shell=True)
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Power Off Information                                                   ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>Powering Off console...     Please sit tight.")
            sms_box.setInformativeText(" Press OK button to close this sms box")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

    '''Restart console'''
    def reboot(self):
        Alive_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe check-alive --any', shell=True)
        Connection_out = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
        if Alive_out.wait() != 0 or Connection_out.wait() != 0:
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found or Failed to Reboot</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe reset', shell=True)
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Reboot Information                                                   ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>Rebooting the console...         Please sit tight.")
            sms_box.setInformativeText(" Press OK button to close this message box")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

    '''***************** Help Menu Functions' Declaration *****************'''
    '''Developed by'''
    def about(self):
        self.sms_box = QtWidgets.QMessageBox()
        pixmap = QPixmap(r'C:\Users\dchitale\Desktop\download.png')
        self.sms_box.setWindowTitle("About Information ")
        self.sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
        self.sms_box.setText("<b>This app is developed by Datta")
        self.sms_box.setInformativeText("Switch Interface v1.0 <br> All rights reserved © 2021")
        self.sms_box.setIcon(self.sms_box.Information)
        self.sms_box.exec_()

    def home_url(self):
        QDesktopServices.openUrl(QtCore.QUrl('https://world.ubisoft.org/job/quality_control/nzone/nzone.html'))

    def training_doc_explorer(self):
        os.startfile(r'\\ubisoft.org\punstudio\QC\Public\Platform New\Console Docs\NINTENDO NX\Switch_Training')

    def ndi_doc(self):
        QDesktopServices.openUrl(QtCore.QUrl('file:///D:/NintendoSDK/NintendoSDK_10_4_0/NintendoSDK/Documents/Package/contents/title.html'))


'''********************** First tab "Tab_Media" class **********************'''
class Tab_Media(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
                            #Create Screenshot groupbox
        self.Media_screenshot_grp_box = QtWidgets.QGroupBox("Screenshot Section")
        self.Media_screenshot_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Media_screenshot_grp_box.setMaximumHeight(70)
        self.Media_screenshot_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            #Create Copy groupbox
        self.Media_copy_grp_box = QtWidgets.QGroupBox("Copy Album Section")
        self.Media_copy_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Media_copy_grp_box.setMaximumHeight(70)
        self.Media_copy_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            #Create Delete groupbox
        self.Media_delete_grp_box = QtWidgets.QGroupBox("Delete Album Section")
        self.Media_delete_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Media_delete_grp_box.setMaximumHeight(70)
        self.Media_delete_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            # SD card groupbox
        self.Media_sdcard_grp_box = QtWidgets.QGroupBox("SD-card Attachment Section")
        self.Media_sdcard_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Media_sdcard_grp_box.setMaximumHeight(90)
        self.Media_sdcard_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")

        '''*********************** create widgets for all four groupboxes ***********************'''
                    #create widgets for Screenshot groupbox
        self.Screenshot_lable = QtWidgets.QLabel("<b>Take a screenshot directly from here")
        self.Screenshot_button = QtWidgets.QPushButton(" Screenshot")
        self.Screenshot_button.setStyleSheet('font:bold')
        self.Screenshot_button.setIcon(QIcon("./Images/media_screenshot.png"))
        self.Screenshot_button.setMaximumWidth(100)
                    # add above widgets to screenshot_grp_box
        self.V_screenshot_grp_box = QtWidgets.QHBoxLayout()
        self.V_screenshot_grp_box.addWidget(self.Screenshot_lable)
        self.V_screenshot_grp_box.addWidget(self.Screenshot_button)
                    # set screenshot_grp_box's layout
        self.Media_screenshot_grp_box.setLayout(self.V_screenshot_grp_box)

                    #create widgets for Copy groupbox
        self.Copy_lable = QtWidgets.QLabel("<b>Copy all attachments from Switch console to PC")
        self.Copy_button = QtWidgets.QPushButton(" Copy Album")
        self.Copy_button.setStyleSheet('font:bold')
        self.Copy_button.setIcon(QIcon("./Images/media_copy.png"))
        self.Copy_button.setMaximumWidth(100)
                    # add above widgets to Copy_grp_box
        self.V_copy_grp_box = QtWidgets.QHBoxLayout()
        self.V_copy_grp_box.addWidget(self.Copy_lable)
        self.V_copy_grp_box.addWidget(self.Copy_button)
                    # set Copy_grp_box's layout
        self.Media_copy_grp_box.setLayout(self.V_copy_grp_box)

                    # create widgets for Delete groupbox
        self.Delete_lable = QtWidgets.QLabel("<b>Delete all attachments from Switch console")
        self.Delete_button = QtWidgets.QPushButton("Delete Album")
        self.Delete_button.setStyleSheet('font:bold')
        self.Delete_button.setIcon(QIcon("./Images/media_trash.png"))
        self.Delete_button.setMaximumWidth(100)
                    # add above widgets to Delete groupbox
        self.V_delete_grp_box = QtWidgets.QHBoxLayout()
        self.V_delete_grp_box.addWidget(self.Delete_lable)
        self.V_delete_grp_box.addWidget(self.Delete_button)
                    # set Delete_grp_box's layout
        self.Media_delete_grp_box.setLayout(self.V_delete_grp_box)

                        # create widgets for SD-card groupbox
        self.SDcard_copy_lable = QtWidgets.QLabel("<b>Copy all attachment from SD-Card to PC")
        self.SDcard_copy_button = QtWidgets.QPushButton("  Copy")
        self.SDcard_copy_button.setStyleSheet('font:bold')
        self.SDcard_copy_button.setIcon(QIcon("./Images/media_SD.png"))
        self.SDcard_copy_button.setMaximumWidth(75)

        self.SDcard_delete_lable = QtWidgets.QLabel("<b>Delete the attachment from SD-Card")
        self.SDcard_delete_button = QtWidgets.QPushButton("  Delete")
        self.SDcard_delete_button.setStyleSheet('font:bold')
        self.SDcard_delete_button.setIcon(QIcon("./Images/media_SD.png"))
        self.SDcard_delete_button.setMaximumWidth(75)
            # created two different Hbox (copy and delete SD) and one Vbox for group box
        self.V_Sdcard_grp_box = QtWidgets.QVBoxLayout()
        self.H_Sdcard_inside_grp_box = QtWidgets.QHBoxLayout()
        self.H2_Sdcard_inside_grp_box = QtWidgets.QHBoxLayout()
                # add above two different Hbox to Vbox
        self.V_Sdcard_grp_box.addLayout(self.H_Sdcard_inside_grp_box)
        self.V_Sdcard_grp_box.addLayout(self.H2_Sdcard_inside_grp_box)
                 # add all widgets to these to Vboxes
        self.H_Sdcard_inside_grp_box.addWidget(self.SDcard_copy_lable)
        self.H_Sdcard_inside_grp_box.addWidget(self.SDcard_copy_button)
        self.H2_Sdcard_inside_grp_box.addWidget(self.SDcard_delete_lable)
        self.H2_Sdcard_inside_grp_box.addWidget(self.SDcard_delete_button)
                 # set App's SD card groupbox's layout
        self.Media_sdcard_grp_box.setLayout(self.V_Sdcard_grp_box)
        '''************************** creating done here ******************************'''

        '''*********************** add all above to main layout ***********************'''
        self.Main_layout = QtWidgets.QVBoxLayout()
        #self.Main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.Main_layout.addWidget(self.Media_screenshot_grp_box)
        self.Main_layout.addWidget(self.Media_copy_grp_box)
        self.Main_layout.addWidget(self.Media_delete_grp_box)
        self.Main_layout.addWidget(self.Media_sdcard_grp_box)
        self.setLayout(self.Main_layout)

                            #Connections
        self.Screenshot_button.clicked.connect(self.take_screenshot)
        self.Delete_button.clicked.connect(self.delete_all_attachments)
        self.Copy_button.clicked.connect(self.copy_all_attachments)
        self.SDcard_copy_button.clicked.connect(self.copy_all_attachments_SDcard)
        self.SDcard_delete_button.clicked.connect(self.delete_all_attachments_SDcard)

    '''***************** Button Connections' Functions Declaration *****************'''
    def take_screenshot(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to take a Screenshot</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            if not os.path.exists(r'C:\Album'):
                os.makedirs(r'C:\Album')
            today_date = datetime.datetime.now().strftime("%d-%m-%y")       # create folder with today's date
            directory = r'C:/Album/' + today_date
            if not os.path.exists(directory):
                os.chdir(r'C:\Album')
                os.makedirs(today_date)
            reply = subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe take-screenshot --directory=' + directory, shell=True)
            reply.wait()
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Capture Information")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText('''Screenshot has been taken. Click OK to Open Folder''')
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
            os.startfile(directory)

    def delete_all_attachments(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to delete the Album</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            out = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album list --storage builtin',stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            for i in range(2):
                line = out.stdout.readline()
            if "Found 0 files" in line:                     # if system storage is empty
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Attachment information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("There are no Attachments to delete in the console")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Confirmation ")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("Are you sure you want to delete all attachments from console?")
                sms_box.setStandardButtons(sms_box.Yes | sms_box.No)
                sms_box.setIcon(sms_box.Warning)
                press = sms_box.exec_()
                if press == sms_box.Yes:
                    reply = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album clean --storage builtin',stdout=subprocess.PIPE, universal_newlines=True, shell=True)
                    reply.wait()
                    for i in range(3):
                        line = reply.stdout.readline()
                    if "Cleaning Album ... failed to complete" in line:        # if video is already open in console then can't delete
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Delete Attachment Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("Deleting Failed. This is because video file is open in console. \n\nPlease close the video file from the console")
                        sms_box.setIcon(sms_box.Warning)
                        sms_box.exec_()
                    else:
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Delete Attachment Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("All the attachments have been deleted. \n\nPlease refresh the console")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                else:
                    sms_box.close()

    def copy_all_attachments(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to copy all the attachments</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            out = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album list --storage builtin',stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            for i in range(2):
                line = out.stdout.readline()
                if "Found 0 files" in line:                     # if system storage is empty
                    sms_box = QtWidgets.QMessageBox()
                    sms_box.setWindowTitle("Attachment information")
                    sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                    sms_box.setText("There are no Attachments found in the console")
                    sms_box.setIcon(sms_box.Information)
                    sms_box.exec_()
                    break
            else:
                if not os.path.exists(r'C:\Album'):
                    os.makedirs(r'C:\Album')
                today_date = datetime.datetime.now().strftime("%d-%m-%y")       # create folder with today's date
                directory = r'C:/Album/' + today_date
                if not os.path.exists(directory):
                    os.chdir(r'C:\Album')
                    os.makedirs(today_date)
                reply = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album download --storage builtin --directory ' + directory, shell=True)
                reply.wait()
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Download Completion Information                                 ")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>Downloading Album completed.")
                sms_box.setInformativeText("Please click on <b>Open</b> button to open file path")
                sms_box.setIcon(sms_box.Information)
                sms_box.setStandardButtons(sms_box.Open)
                sms_box.exec_()
                os.startfile(directory)

    def copy_all_attachments_SDcard(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to copy all the attachments from SD Card</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

        else:
            installation_progress = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill '+ env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album list --sd', stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            for i in range(2):
                line = installation_progress.stdout.readline()
            if "Failed to mount target storage." in line:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("SD Card information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No SD card found. Please insert an SD card into console")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()

            else:
                if not os.path.exists(r'C:\AlbumSD'):
                    os.makedirs(r'C:\AlbumSD')
                today_date = datetime.datetime.now().strftime("%d-%m-%y")  # create folder with today's date
                directory = r'C:/AlbumSD/' + today_date
                if not os.path.exists(directory):
                    os.chdir(r'C:\AlbumSD')
                    os.makedirs(today_date)
                reply = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album download --storage sdcard --directory ' + directory, shell=True)
                reply.wait()
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Download Completion Information                                 ")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("Downloading SD Album completed.")
                sms_box.setInformativeText("Please click on <b>Open</b> button to open file path")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
                os.startfile(directory)

    def delete_all_attachments_SDcard(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to delete the Album from SD card</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            installation_progress = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album list --sd', stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            for i in range(2):
                line = installation_progress.stdout.readline()
            if "Failed to mount target storage." in line:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("SD Card information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No SD card found. Please insert an SD card into console")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()

            else:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Confirmation ")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("Are you sure you want to delete all attachments from SD card?")
                sms_box.setStandardButtons(sms_box.Yes | sms_box.No)
                sms_box.setIcon(sms_box.Warning)
                press = sms_box.exec_()
                if press == sms_box.Yes:
                    reply = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe --suppress-auto-kill '+ env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- album clean --sd', shell=True)
                    reply.wait()
                    sms_box = QtWidgets.QMessageBox()
                    sms_box.setWindowTitle("Delete information")
                    sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                    sms_box.setText("All the attachments have been deleted from SD card")
                    sms_box.setIcon(sms_box.Information)
                    sms_box.exec_()
                else:
                    sms_box.close()


'''***************** Second tab "Manage Applications" class *****************'''
class Tab_Applications(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
                    # Create App's 1st groupbox
        self.App_first_grp_box = QtWidgets.QGroupBox("Application Installer")
        self.App_first_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.App_first_grp_box.setMinimumHeight(90)
        self.App_first_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")

                    #Create App's second groupbox
        self.App_second_grp_box = QtWidgets.QGroupBox("Application Launcher")
        self.App_second_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.App_second_grp_box.setMinimumHeight(70)
        self.App_second_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")

                    #Create App's third groupbox
        self.App_third_grp_box = QtWidgets.QGroupBox("Application Terminator")
        self.App_third_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.App_third_grp_box.setMinimumHeight(70)
        self.App_third_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")

                    #Create App's fourth groupbox
        self.App_fourth_grp_box = QtWidgets.QGroupBox("Application Uninstaller")
        self.App_fourth_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.App_fourth_grp_box.setMinimumHeight(70)
        self.App_fourth_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")


        '''*********************** create widgets for all four groupboxes ***********************'''
                # create and add widgets for App's first groupbox
        self.Install_lable = QtWidgets.QLabel("<b>Install the selected Application on Switch console")
        self.Install_button = QtWidgets.QPushButton(" Install App")
        self.Progress_Bar = QtWidgets.QProgressBar()
        self.Progress_Bar_lable = QtWidgets.QLabel("<b>Progress :")
        self.Pbar_Cancel_button = QtWidgets.QPushButton("  Cancel")
        self.Pbar_Cancel_button.setEnabled(False)
        self.Progress_Bar_lable.setEnabled(False)
        self.Install_button.setIcon(QIcon("./Images/app_install.png"))
        self.Install_button.setStyleSheet('font:bold')
        self.Install_button.setMaximumWidth(100)
             # created two different Hbox (install and progress bar) and one Vbox for group box
        self.V_Install_grp_box = QtWidgets.QVBoxLayout()
        self.H_inside_grp_box = QtWidgets.QHBoxLayout()
        self.H2_inside_grp_box = QtWidgets.QHBoxLayout()
            # add above two different Hbox to Vbox
        self.V_Install_grp_box.addLayout(self.H_inside_grp_box)
        self.V_Install_grp_box.addLayout(self.H2_inside_grp_box)
            #add all widgets to these to Vboxes
        self.H_inside_grp_box.addWidget(self.Install_lable)
        self.H_inside_grp_box.addWidget(self.Install_button)
        self.H2_inside_grp_box.addWidget(self.Progress_Bar_lable)
        self.H2_inside_grp_box.addWidget(self.Progress_Bar)
        self.H2_inside_grp_box.addWidget(self.Pbar_Cancel_button)
            # set App's first groupbox's layout
        self.App_first_grp_box.setLayout(self.V_Install_grp_box)

                #create and add widgets for App's second groupbox
        self.Launch_lable = QtWidgets.QLabel("<b>Launch an installed Application on Switch console")
        self.Launch_button = QtWidgets.QPushButton(" Launch App")
        self.Launch_button.setIcon(QIcon("./Images/app_launch.png"))
        self.Launch_button.setStyleSheet('font:bold')
        #self.Screenshot_button.setIcon(QIcon("screenshot.png"))
        self.Launch_button.setMaximumWidth(100)
                # add above widgets to App's second_grp_box
        self.V_Launch_grp_box = QtWidgets.QHBoxLayout()
        self.V_Launch_grp_box.addWidget(self.Launch_lable)
        self.V_Launch_grp_box.addWidget(self.Launch_button)
                # set App's second_grp_box's layout
        self.App_second_grp_box.setLayout(self.V_Launch_grp_box)

                #create and add widgets for App's third groupbox
        self.Terminate_lable = QtWidgets.QLabel("<b>Terminate the running Application on Switch console")
        self.Terminate_button = QtWidgets.QPushButton("  Terminate")
        self.Terminate_button.setIcon(QIcon("./Images/app_terminate.png"))
        self.Terminate_button.setStyleSheet('font:bold')
        self.Terminate_button.setMaximumWidth(100)
                # add above widgets to App's third groupbox
        self.V_Terminate_grp_box = QtWidgets.QHBoxLayout()
        self.V_Terminate_grp_box.addWidget(self.Terminate_lable)
        self.V_Terminate_grp_box.addWidget(self.Terminate_button)
                # set App's third groupbox's layout
        self.App_third_grp_box.setLayout(self.V_Terminate_grp_box)

                # create and add widgets for App's fourth groupbox
        self.Uninstall_lable = QtWidgets.QLabel("<b>Uninstall the selected Application from Switch console")
        self.Uninstall_button = QtWidgets.QPushButton("  Uninstall")
        self.Uninstall_button.setIcon(QIcon("./Images/app_uninstall.png"))
        self.Uninstall_button.setStyleSheet('font:bold')
        self.Uninstall_button.setMaximumWidth(100)
                    # add above widgets to App's fourth  groupbox
        self.V_uninstall_grp_box = QtWidgets.QHBoxLayout()
        self.V_uninstall_grp_box.addWidget(self.Uninstall_lable)
        self.V_uninstall_grp_box.addWidget(self.Uninstall_button)
                    # set App's fourth  groupbox's layout
        self.App_fourth_grp_box.setLayout(self.V_uninstall_grp_box)
        '''************************** creating done here ******************************'''

        '''*********************** add all above to main layout ***********************'''
        self.Main_layout = QtWidgets.QVBoxLayout()
        self.Main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.Main_layout.addWidget(self.App_first_grp_box)
        self.Main_layout.addWidget(self.App_second_grp_box)
        self.Main_layout.addWidget(self.App_third_grp_box)
        self.Main_layout.addWidget(self.App_fourth_grp_box)
        self.setLayout(self.Main_layout)

                            #Connections
        self.Launch_button.clicked.connect(self.launch_app)
        self.Terminate_button.clicked.connect(self.terminate_app)
        self.Uninstall_button.clicked.connect(self.uninstall_app)
        self.Install_button.clicked.connect(self.install_app)


    '''***************** Button Connections' Functions Declaration *****************'''
    def launch_app(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to launch application</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            res = subprocess.check_output(env + r'\Tools\CommandLineTools\ControlTarget.exe list-application', shell=True)
            cmd_result = res.decode("latin1", 'ignore').split('\n')
            result = []
            for i in range(2, len(cmd_result)-3):
                result.append(cmd_result[i])
#Else populate list to QinputDialog and launch selected application
            self.input_dialogue = QtWidgets.QInputDialog()
            self.app_item, self.app_ok = self.input_dialogue.getItem(self, "Application Selection","<b>Select an Application/Game to launch:", result, 0,False)
            if self.app_ok and "DevMenu Application" in self.app_item:
                self.comm = env + r'\Tools\CommandLineTools\ControlTarget.exe launch-application ' + self.app_item
                subprocess.Popen(self.comm, shell=True)
            elif self.app_ok:
                comm = env + r'\Tools\CommandLineTools\ControlTarget.exe launch-application ' + self.app_item
                subprocess.Popen(comm, shell=True)
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Select an User Account")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>Select an User Account from console screen to start the game</b>")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                self.input_dialogue.close()

    def terminate_app(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to terminate application</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()

        else:
            subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe terminate', shell=True)

    def uninstall_app(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to uninstall application</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            res = subprocess.check_output(env + r'\Tools\CommandLineTools\ControlTarget.exe list-application', shell=True)
            cmd_result = res.decode("latin1", 'ignore').split('\n')
            result = []
            for i in range(2, len(cmd_result) - 3):
                if cmd_result[i] == '0x0100000000002065            1.0.0  DevMenu Application  \r':
                    continue
                result.append(cmd_result[i])
        #print(result)
# if the applications are not installed (exclude DevMenu - risk to uninstall it)- list is empty
            if len(result) == 0:
                self.sms_box = QtWidgets.QMessageBox()
                self.sms_box.setWindowTitle("App/Game Information")
                self.sms_box.setText("<b>No Games or Applications installed on the console")
                self.sms_box.setInformativeText("Please install a Game/Application on console first")
                self.sms_box.setIcon(self.sms_box.Information)
                self.sms_box.exec_()
#Else populate list to QinputDialog and uninstall selected applicaion
            else:
                self.input_dialogue = QtWidgets.QInputDialog()
                text, ok = self.input_dialogue.getItem(self, "Application Selection", "<b>Select an Application/Game to uninstall:",result, 0, False)
                if ok:
                    comm = env + r'\Tools\CommandLineTools\ControlTarget.exe uninstall-application ' + text
                    reply = subprocess.Popen(comm, shell=True)
                    if reply.wait()== 0:                        #wait for comm to excute (uninstall) and get reply from it and then convey user
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Uninstallation Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("Application has been uninstalled successfully")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                    else:
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Uninstallation Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("Something went wrong. Please try again")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                else:
                    self.input_dialogue.close()

    def install_app(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to install application</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            file_name = QtWidgets.QFileDialog.getOpenFileName(self,'Open nsp build file', r"C:\\", 'Nsp file(*.nsp)')
            #print(file_name)
            #print(type(file_name))
            destination_list = ["System Memory (NAND)", "SD Card", "Game Card"]     # create a list for destination where you want to install game
            if file_name ==('', ''):                                                # If user selects "Cancel" on QFileDialog then just do nothing
                pass
            else:
                #create input dialogue to ask the destination to install game
                input_dialogue = QtWidgets.QInputDialog()
                app_item, app_ok = input_dialogue.getItem(self, "Install Destination Selection","<b>Select a destination for Application/Game to install:",destination_list, 0, False)

               # if there is no SD card in the console
                if app_ok and app_item == "SD Card":
                    installation_progress = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- sdcard status',stdout=subprocess.PIPE, universal_newlines=True, shell=True)
                    line = installation_progress.stdout.readline()
                    if "Sdcard is not inserted." in line:
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("SD Card information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("No SD card. Please insert an SD Card and then install App/Game")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()

                    # if there is no Game card in the console
                elif app_ok and app_item == "Game Card":
                    installation_progress = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- gamecard status',stdout=subprocess.PIPE, universal_newlines=True, shell=True)
                    line = installation_progress.stdout.readline()
                    if "Not Inserted" in line:
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Game Card information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("No Game card. Please insert a Game Card and then install App/Game")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                elif app_ok:
                    # start thread
                    self.worker = Worker(file_name,app_item)
                    self.worker.start()
                    self.worker.thread_error.connect(self.error_thread)
                    self.worker.thread_finish.connect(self.finish_tread)
                    self.worker.thread_interrupt_error.connect(self.interrupt_thread)
                    self.Pbar_Cancel_button.clicked.connect(self.cancel_Pbar)
                    self.worker.process.connect(self.update_Pbar)
                else:
                    input_dialogue.close()

    def cancel_Pbar(self):
        self.worker.terminate()
        subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe disconnect', shell=True)
        self.Progress_Bar.reset()
        self.Pbar_Cancel_button.setEnabled(False)
        self.Progress_Bar_lable.setEnabled(False)

    def update_Pbar(self, val):
        self.Pbar_Cancel_button.setEnabled(True)
        self.Progress_Bar_lable.setEnabled(True)
        self.Progress_Bar.setValue(val)

    def error_thread(self, error):
        self.worker.terminate()
        sms_box = QtWidgets.QMessageBox()
        sms_box.setWindowTitle("Installation Error Information")
        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
        sms_box.setText("<b>Unexpected error. Please reboot the console or re-install the application</b>")
        sms_box.setInformativeText("This is because you interrupt installation or last installation was unsuccessful")
        sms_box.setIcon(sms_box.Information)
        sms_box.exec_()
        self.Progress_Bar.reset()
        self.Pbar_Cancel_button.setEnabled(False)
        self.Progress_Bar_lable.setEnabled(False)

    def interrupt_thread(self, interrupt_error):
        self.worker.terminate()
        sms_box = QtWidgets.QMessageBox()
        sms_box.setWindowTitle("Installation Error Information")
        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
        sms_box.setText("<b>Installation interrupted. Please re-install the application</b>")
        sms_box.setIcon(sms_box.Information)
        sms_box.exec_()
        self.Progress_Bar.reset()
        self.Pbar_Cancel_button.setEnabled(False)
        self.Progress_Bar_lable.setEnabled(False)

    def finish_tread(self, complete):
        sms_box = QtWidgets.QMessageBox()
        sms_box.setWindowTitle("Installation Successful Information")
        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
        sms_box.setText("Application installed successfully")
        sms_box.setIcon(sms_box.Information)
        sms_box.exec_()
        #self.Progress_Bar.reset()
        self.Progress_Bar.reset()
        self.Pbar_Cancel_button.setEnabled(False)
        self.Progress_Bar_lable.setEnabled(False)


'''********** Separate Worker class for installation thread in background *************'''
class Worker(QThread):
    process = QtCore.Signal(int)
    thread_finish = QtCore.Signal(str)
    thread_error = QtCore.Signal(str)
    thread_interrupt_error = QtCore.Signal(str)

    def __init__(self, file_name, app_item):
        super(Worker, self).__init__()
        self.file_name = file_name
        self.app_item = app_item
        print(file_name)
        print(app_item)

    def run(self):
        if self.app_item == "System Memory (NAND)":
            comm = env + r'\Tools\CommandLineTools\ControlTarget.exe install-application ' + self.file_name[0] + ' -- --force' + ' -s builtin'
        elif self.app_item == "SD Card":
            comm = env + r'\Tools\CommandLineTools\ControlTarget.exe install-application ' + self.file_name[0] + ' -- --force' + ' -s sdcard'
        elif self.app_item == "Game Card":
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- gamecard write ' + self.file_name[0]

        installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, stderr=True, shell=True)
        for i in range(2):
            line = installation_progress.stdout.readline()
            #print(line)
            if "Unexpected error" in line:
                self.thread_error.emit("error")
        while installation_progress.poll() is None:
            line = installation_progress.stdout.readline()
            #print(line)
            if "[SUCCESS]" in line:
                self.thread_finish.emit("successful")
                break
            elif "Failure" in line:  # or "Path"
                self.thread_interrupt_error.emit("interrupt_error")
                break
            else:
                value = line.split(' ')
                value.append(value)
                set_min = int(value[0])
                max_value = int(value[2])
                percentage = (set_min / max_value) * 100
                #print(percentage)
                set_value = percentage
                self.process.emit(set_value)
'''************************** Seperate Worker class done ******************************'''


'''***************** Third tab "User Accounts" class *****************'''
class Tab_User_accounts(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
                            #Create Create_User groupbox
        self.Create_User_grp_box = QtWidgets.QGroupBox("Create User Section")
        self.Create_User_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Create_User_grp_box.setMinimumHeight(75)
        self.Create_User_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            #Create Show_User groupbox
        self.Show_User_grp_box = QtWidgets.QGroupBox("Show User Section")
        self.Show_User_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Show_User_grp_box.setMinimumHeight(75)
        self.Show_User_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            # Create Delete_single_User groupbox
        self.Delete_Single_User_grp_box = QtWidgets.QGroupBox("Delete Single User Section")
        self.Delete_Single_User_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Delete_Single_User_grp_box.setMinimumHeight(75)
        self.Delete_Single_User_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            # Create Delete_User groupbox
        self.Delete_User_grp_box = QtWidgets.QGroupBox("Delete All User Section")
        self.Delete_User_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Delete_User_grp_box.setMinimumHeight(75)
        self.Delete_User_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")

        '''*********************** create widgets for all four groupboxes ***********************'''
                    # create and add widgets for first groupbox
        self.Create_user_lable = QtWidgets.QLabel("<b>Create a new User Account on Switch console")
        self.Create_user_button = QtWidgets.QPushButton(" Create User")
        self.Create_user_button.setIcon(QIcon("./Images/user_create.png"))
        self.Create_user_button.setStyleSheet('font:bold')
        self.Create_user_button.setMaximumWidth(100)
                    # created Hbox to in the Create_user_grp_box
        self.H_Create_user_grp_box = QtWidgets.QHBoxLayout()
                    # add all widgets to these to Hbox
        self.H_Create_user_grp_box.addWidget(self.Create_user_lable)
        self.H_Create_user_grp_box.addWidget(self.Create_user_button)
                    # set App's first groupbox's layout
        self.Create_User_grp_box.setLayout(self.H_Create_user_grp_box)

                    # create and add widgets for second groupbox
        self.Show_User_lable = QtWidgets.QLabel("<b>Show all User Accounts on Switch console")
        self.Show_User_button = QtWidgets.QPushButton(" Show Users")
        self.Show_User_button.setIcon(QIcon("./Images/user_show.png"))
        self.Show_User_button.setStyleSheet('font:bold')
        self.Show_User_button.setMaximumWidth(100)

                    # add above widgets to App's second_grp_box
        self.H_Show_User_grp_box = QtWidgets.QHBoxLayout()
        self.H_Show_User_grp_box.addWidget(self.Show_User_lable)
        self.H_Show_User_grp_box.addWidget(self.Show_User_button)
                    # set App's second_grp_box's layout
        self.Show_User_grp_box.setLayout(self.H_Show_User_grp_box)

                    # create and add widgets for third groupbox
        self.Delete_Single_User_lable = QtWidgets.QLabel("<b>Delete one User Account from Switch console")
        self.Delete_Single_User_button = QtWidgets.QPushButton("Delete Single")
        self.Delete_Single_User_button.setIcon(QIcon("./Images/user_delete.png"))
        self.Delete_Single_User_button.setStyleSheet('font:bold')
        self.Delete_Single_User_button.setMaximumWidth(100)
                    # add above widgets to App's third groupbox
        self.H_Delete_Single_User_grp_box = QtWidgets.QHBoxLayout()
        self.H_Delete_Single_User_grp_box.addWidget(self.Delete_Single_User_lable)
        self.H_Delete_Single_User_grp_box.addWidget(self.Delete_Single_User_button)
                    # set App's third groupbox's layout
        self.Delete_Single_User_grp_box.setLayout(self.H_Delete_Single_User_grp_box)

                    # create and add widgets for fourth groupbox
        self.Delete_User_lable = QtWidgets.QLabel("<b>Delete all User Accounts from Switch console")
        self.Delete_User_button = QtWidgets.QPushButton("  Delete All")
        self.Delete_User_button.setIcon(QIcon("./Images/user_delete_all.png"))
        self.Delete_User_button.setStyleSheet('font:bold')
        self.Delete_User_button.setMaximumWidth(100)
                    # add above widgets to App's fourth groupbox
        self.H_Delete_User_grp_box = QtWidgets.QHBoxLayout()
        self.H_Delete_User_grp_box.addWidget(self.Delete_User_lable)
        self.H_Delete_User_grp_box.addWidget(self.Delete_User_button)
                    # set App's third groupbox's layout
        self.Delete_User_grp_box.setLayout(self.H_Delete_User_grp_box)
        '''************************** creating done here ******************************'''

        '''*********************** add all above to main layout ***********************'''
        self.Main_layout = QtWidgets.QVBoxLayout()
        self.Main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.Main_layout.addWidget(self.Create_User_grp_box)
        self.Main_layout.addWidget(self.Show_User_grp_box)
        self.Main_layout.addWidget(self.Delete_Single_User_grp_box)
        self.Main_layout.addWidget(self.Delete_User_grp_box)
        self.setLayout(self.Main_layout)

                    #connections
        self.Create_user_button.clicked.connect(self.create_user)
        self.Show_User_button.clicked.connect(self.show_user)
        self.Delete_Single_User_button.clicked.connect(self.delete_single_user)
        self.Delete_User_button.clicked.connect(self.delete_all_user)

    '''***************** Button Connections' Functions Declaration *****************'''
    def create_user(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to create User Account</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account add'
            installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            for i in range(2):
                line = installation_progress.stdout.readline()
            if "[SUCCESS]" in line:
                user_output = subprocess.check_output(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list', shell=True)
                user_list = user_output.decode("latin1", 'ignore').split('\n')
                for i in range(0, len(user_list)-3):
                    #print(list((user_list[i], i+1)))               #print list of user as well as index of user
                    new_index_list = list((i+1, user_list[i]))      #store list of user as well as index of user in a variable
                #print(new_index_list)
                user_list_string = str(new_index_list)
                final_output = '   ' + user_list_string[1:2] + '                  ' + user_list_string[5:-4]  # truncate unwanted character ([ ] r)
                #get the last user to show in sms that this last use has been created
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("User Account Creation Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>Following User Account has been created successfully")
                sms_box.setInformativeText("Index                                      User ID \n\n" + final_output + "\n\nPlease refresh the console to see User Account.")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("User Account Creation Information                                                                                    ")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>User Account Creation failed                                                                                      ")
                sms_box.setInformativeText("This is because you have already created 8 User Accounts, which is max. Limit\nOr you have tried to create User Account while DevMenu/Game is running.\n\nPlease delete some User Accounts or close the game or restart the console.")
                sms_box.setIcon(sms_box.Warning)
                sms_box.exec_()

    def show_user(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to show User Accounts</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list'
            installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            line = installation_progress.stdout.readline()
            if "[SUCCESS]" in line:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("User Account Listing Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No User Accounts to show. Please create an User Account first")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                user_output = subprocess.check_output(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list', shell=True)
                user_list = user_output.decode("latin1", 'ignore').split('\n')
                new_index_list = []
                for i in range(0, len(user_list) - 3):
                    new_index_list.append(user_list[i])
                final_list = ""
                for index, value in enumerate(new_index_list):
                    final_list = final_list + '    ' + str(index+1) + '               ' + str(value) + '\n'
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("User Account Listing Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setMinimumHeight(900)
                sms_box.setText("<b> List of User Accounts present on the console")
                sms_box.setInformativeText("Index                                       User ID\n\n" + final_list)
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()

    def delete_single_user(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to delete User Account</b>")
            sms_box.setInformativeText(
                "Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list'
            installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            line = installation_progress.stdout.readline()
            if "[SUCCESS]" in line:  # if there are no User Accounts in console
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("User Account Delete Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No User Accounts to delete. Please create an User Account first")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                user_output = subprocess.check_output(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list', shell=True)
                user_list = user_output.decode("latin1", 'ignore').split('\n')
                new_index_list = []
                for i in range(0, len(user_list) - 3):               #ietrate till last-3 (unneccessary text)
                    new_index_list.append(user_list[i])
                all_index = []
                for index, val in enumerate(new_index_list):        #Get index as well as value
                    all_index.append(str(list((index+1, val))))
                            # remove all unnecessary characters from list
                removable = str.maketrans('', '', r'''[],'\\r"''')
                final_list = [s.translate(removable) for s in all_index]
                            # add some space between index and user account name to decode
                list_with_space = [x[0:2] + '         ' + x [2:] for x in final_list]
                single_input_dialogue = QtWidgets.QInputDialog()
                single_app_item, single_app_ok = single_input_dialogue.getItem(self, "User Account Selection","<b>Select an User Account with index to delete:",list_with_space, 0, False)
                if single_app_ok:
                    index_adder = int(single_app_item[0])-1     # NDI command's index starts from 0
                             #ask for confirmation
                    sms_box = QtWidgets.QMessageBox()
                    sms_box.setWindowTitle("Confirmation ")
                    sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                    sms_box.setText("Are you sure you want to delete    " + single_app_item + "  \nUser Account from console?")
                    sms_box.setInformativeText("Don't worry, the saves for this User Account will be still there in console")
                    sms_box.setStandardButtons(sms_box.Yes | sms_box.No)
                    sms_box.setIcon(sms_box.Warning)
                    press = sms_box.exec_()
                    if press == sms_box.Yes:
                        single_comm = env + r'\Tools\CommandLineTools\TargetShell.exe delete-account --index=' + str(index_adder) + ' --keep-savedata'
                        reply = subprocess.Popen(single_comm, shell=True)
                        if reply.wait() == 0:   #wait fot command to execute and return 0 for error free and then show successful sms to user
                            sms_box = QtWidgets.QMessageBox()
                            sms_box.setWindowTitle("Single User Account Delete Information")
                            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                            sms_box.setText(single_app_item + "     User Account has been deleted ")
                            sms_box.setInformativeText("Please refresh the console to reflect changes")
                            sms_box.setIcon(sms_box.Information)
                            sms_box.exec_()
                        else:                   #else something is wrong
                            sms_box = QtWidgets.QMessageBox()
                            sms_box.setWindowTitle("User Account Delete Information")
                            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                            sms_box.setText("Something went wrong. Please reconnect or restart console")
                            sms_box.setIcon(sms_box.Information)
                            sms_box.exec_()
                    else:
                        sms_box.close()
                else:
                    single_input_dialogue.close()

    def delete_all_user(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to delete all User Accounts</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list'
            installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            line = installation_progress.stdout.readline()
            if "[SUCCESS]" in line:   #if there are no User Accounts in console
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("User Account Delete Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No User Accounts to delete. Please create an User Account first")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Confirmation")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>Are you sure you want to delete All User Accounts from console?")
                sms_box.setInformativeText("Don't worry, the saves for the User Accounts will be still there in console")
                sms_box.setStandardButtons(sms_box.Yes | sms_box.No)
                sms_box.setIcon(sms_box.Warning)
                press = sms_box.exec_()
                if press == sms_box.Yes:
                    reply = subprocess.Popen(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account clear_all --keep_savedata', shell=True)
                    if reply.wait() == 0:   #wait fot command to execute and return 0 for error free and then show successful sms to user
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("User Account Delete Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("<b>All the User Accounts have been deleted")
                        sms_box.setInformativeText("Please refresh the console to reflect changes")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                    else:                   #else something is wrong
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("User Account Delete Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("Something went wrong. Please reconnect or restart console")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                else:
                    sms_box.close()


'''***************** Fourth tab "Save Data" class *****************'''
class Tab_Save_Data(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
                            #Create Create_User groupbox
        self.Import_Save_grp_box = QtWidgets.QGroupBox("Import Save Data Section")
        self.Import_Save_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Import_Save_grp_box.setMinimumHeight(75)
        self.Import_Save_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            #Create Show_User groupbox
        self.Export_Save_grp_box = QtWidgets.QGroupBox("Export Save Data Section")
        self.Export_Save_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Export_Save_grp_box.setMinimumHeight(75)
        self.Export_Save_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            # Create Delete_single_User groupbox
        self.Delete_byAppid_grp_box = QtWidgets.QGroupBox("Delete Save Data by App ID Section")
        self.Delete_byAppid_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Delete_byAppid_grp_box.setMinimumHeight(75)
        self.Delete_byAppid_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")
                            # Create Delete_User groupbox
        self.Delete_All_Save_grp_box = QtWidgets.QGroupBox("Delete All Save Data Section")
        self.Delete_All_Save_grp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.Delete_All_Save_grp_box.setMinimumHeight(75)
        self.Delete_All_Save_grp_box.setStyleSheet("QGroupBox{font:bold; color:rgb(0, 102, 102);border: 1px solid black}")

        '''*********************** create widgets for all four groupboxes ***********************'''
                    # create and add widgets for first groupbox
        self.Import_save_lable = QtWidgets.QLabel("<b>Import saves from PC to Switch console")
        self.Import_save_button = QtWidgets.QPushButton("Import Saves")
        self.Import_save_button.setIcon(QIcon("./Images/saves_import.png"))
        self.Import_save_button.setStyleSheet('font:bold')
        self.Import_save_button.setMaximumWidth(101)
                     # created Hbox to in the Create_user_grp_box
        self.H_Import_save_grp_box = QtWidgets.QHBoxLayout()
                    # add all widgets to these to Hbox
        self.H_Import_save_grp_box.addWidget(self.Import_save_lable)
        self.H_Import_save_grp_box.addWidget(self.Import_save_button)
                    # set App's first groupbox's layout
        self.Import_Save_grp_box.setLayout(self.H_Import_save_grp_box)

                    # create and add widgets for second groupbox
        self.Export_save_lable = QtWidgets.QLabel("<b>Export saves from Switch console to PC")
        self.Export_save_button = QtWidgets.QPushButton("Export Saves")
        self.Export_save_button.setIcon(QIcon("./Images/saves_export.png"))
        self.Export_save_button.setStyleSheet('font:bold')
        self.Export_save_button.setMaximumWidth(100)
                    # add above widgets to App's second_grp_box
        self.H_Export_save_grp_box = QtWidgets.QHBoxLayout()
        self.H_Export_save_grp_box.addWidget(self.Export_save_lable)
        self.H_Export_save_grp_box.addWidget(self.Export_save_button)
                    # set App's second_grp_box's layout
        self.Export_Save_grp_box.setLayout(self.H_Export_save_grp_box)

                    # create and add widgets for third groupbox
        self.Delete_byAppid_lable = QtWidgets.QLabel("<b>Delete Save Data by App/Game ID from Switch console")
        self.Delete_byAppid_button = QtWidgets.QPushButton("Delete by App")
        self.Delete_byAppid_button.setIcon(QIcon("./Images/saves_delete_by_app.png"))
        self.Delete_byAppid_button.setStyleSheet('font:bold')
        self.Delete_byAppid_button.setMaximumWidth(103)
                     # add above widgets to App's third groupbox
        self.H_Delete_byAppid_grp_box = QtWidgets.QHBoxLayout()
        self.H_Delete_byAppid_grp_box.addWidget(self.Delete_byAppid_lable)
        self.H_Delete_byAppid_grp_box.addWidget(self.Delete_byAppid_button)
                    # set App's third groupbox's layout
        self.Delete_byAppid_grp_box.setLayout(self.H_Delete_byAppid_grp_box)

                    # create and add widgets for fourth groupbox
        self.Delete_all_saves_lable = QtWidgets.QLabel("<b>Delete all Save Data from Switch console")
        self.Delete_all_saves_button = QtWidgets.QPushButton("Delete Saves")
        self.Delete_all_saves_button.setIcon(QIcon("./Images/saves_delete_all.png"))
        self.Delete_all_saves_button.setStyleSheet('font:bold')
        self.Delete_all_saves_button.setMaximumWidth(100)
                     # add above widgets to App's fourth groupbox
        self.H_Delete_all_saves_grp_box = QtWidgets.QHBoxLayout()
        self.H_Delete_all_saves_grp_box.addWidget(self.Delete_all_saves_lable)
        self.H_Delete_all_saves_grp_box.addWidget(self.Delete_all_saves_button)
                    # set App's fourth groupbox's layout
        self.Delete_All_Save_grp_box.setLayout(self.H_Delete_all_saves_grp_box)
        '''************************** creating done here ******************************'''

        '''*********************** add all above to main layout ***********************'''
        self.Main_layout = QtWidgets.QVBoxLayout()
        self.Main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.Main_layout.addWidget(self.Import_Save_grp_box)
        self.Main_layout.addWidget(self.Export_Save_grp_box)
        self.Main_layout.addWidget(self.Delete_byAppid_grp_box)
        self.Main_layout.addWidget(self.Delete_All_Save_grp_box)
        self.setLayout(self.Main_layout)

                            # connections
        self.Import_save_button.clicked.connect(self.import_save)
        self.Export_save_button.clicked.connect(self.export_save)
        self.Delete_byAppid_button.clicked.connect(self.Delete_byAppid)
        self.Delete_all_saves_button.clicked.connect(self.delete_all_saves)

    '''***************** Button Connections' Functions Declaration *****************'''
    def import_save(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to import Save Data</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            file_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open importable folder only', r"C:\\")
            if file_name == '':  # If user selects "Cancel" on QFileDialog then just do nothing
                pass
            else:
                        # Get the User Accounts now on which saves can be imported
                comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list'
                installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
                line = installation_progress.stdout.readline()
                if "[SUCCESS]" in line:  # if there are no User Accounts in console
                    sms_box = QtWidgets.QMessageBox()
                    sms_box.setWindowTitle("User Account Information")
                    sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                    sms_box.setText("No User Accounts on which saves will be imported. Please create an User Account first and then import saves")
                    sms_box.setIcon(sms_box.Information)
                    sms_box.exec_()
                else:
                    user_output = subprocess.check_output(env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- account list', shell=True)
                    user_list = user_output.decode("latin1", 'ignore').split('\n')
                    new_index_list = []
                    for i in range(0, len(user_list) - 3):  # ieterate till last-3 (unneccessary text)
                        new_index_list.append(user_list[i])
                    all_index = []
                    for index, val in enumerate(new_index_list):  # Get index as well as value
                        all_index.append(str(list((index + 1, val))))
                            # remove all unnecessary characters from list
                    removable = str.maketrans('', '', r'''[],'\\r"''')
                    final_list = [s.translate(removable) for s in all_index]
                            # add some space between index and user account name to decode
                    list_with_space = [x[0:2] + '         ' + x[2:] for x in final_list]
                            #show list of those user account which are present on console so that user will select it and import saves on that User Account
                    User_input_dialogue = QtWidgets.QInputDialog()
                    User_app_item, User_app_ok = User_input_dialogue.getItem(self, "User Account Selection","<b>Select an User Account on which saves will be imported:",list_with_space, 0, False)
                    if User_app_ok:
                        index_adder = int(User_app_item[0]) - 1  # NDI command's index starts from 0
                        User_comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- savedata import ' + '--input ' + file_name + ' --user-index ' + str(index_adder)
                        reply = subprocess.Popen(User_comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
                        check_line = reply.stdout.readline()
                        if " is a invalid format" in check_line:  # if user select wrong imported folder
                            sms_box = QtWidgets.QMessageBox()
                            sms_box.setWindowTitle("Import Saves Information")
                            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                            sms_box.setText("You have selected wrong or empty import folder. Select correct import folder")
                            sms_box.setInformativeText("E.g.  Select folder like: ' <b>20190204201418_0100978003488000<b> '")
                            sms_box.setIcon(sms_box.Information)
                            sms_box.exec_()
                        else:  # else import successful
                            sms_box = QtWidgets.QMessageBox()
                            sms_box.setWindowTitle("Import Saves Information")
                            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                            sms_box.setText("Saves has been imported successfully on User Account: \n\n" + User_app_item)
                            sms_box.setIcon(sms_box.Information)
                            sms_box.exec_()
                    else:
                        User_input_dialogue.close()

    def export_save(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to import Save Data</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- savedata list'
            installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            line = installation_progress.stdout.readline()
            if "[SUCCESS]" in line:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Save Data Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No Save Data found to Export. Please create Save Data first and then Export")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                export_output = subprocess.check_output(comm, shell=True)
                export_list = export_output.decode("latin1", 'ignore').split('\n')
                #print(export_list)
                final_export_list = []
                for i in range(0, len(export_list) - 3):  # ieterate till last-3 (unneccessary text)
                    final_export_list.append(export_list[i])
                #print(final_export_list)
                export_input_dialogue = QtWidgets.QInputDialog()
                export_item, export_ok = export_input_dialogue.getItem(self, "Save Data Selection", "<b>Select Save Data from the below list to Export :</b>",final_export_list, 0, False)
                if export_ok:
                    if not os.path.exists(r'C:\ExportSaves'):
                        os.makedirs(r'C:\ExportSaves')
                    export_comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- savedata export --savedata-id ' + export_item[13:31] + ' --output C:\ExportSaves'
                    reply = subprocess.Popen(export_comm, shell=True)
                    if reply.wait() == 0:
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Export Save Data Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("<b>Save Data has been exported successfully")
                        sms_box.setInformativeText("Please click on <b>Open</b> button to open file path")
                        sms_box.setIcon(sms_box.Information)
                        sms_box.setStandardButtons(sms_box.Open)
                        sms_box.exec_()
                        os.startfile(r'C:\ExportSaves')
                    #print(export_comm)
                else:
                    export_input_dialogue.close()

    def Delete_byAppid(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to delete Save Data by App/Game ID</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            res = subprocess.check_output(env + r'\Tools\CommandLineTools\ControlTarget.exe list-application', shell=True)
            cmd_result = res.decode("latin1", 'ignore').split('\n')
            result = []
            for i in range(2, len(cmd_result) - 3):
                if cmd_result[i] == '0x0100000000002065            1.0.0  DevMenu Application  \r':
                    continue
                result.append(cmd_result[i])
            #print(result)
            # if the applications are not installed - list is empty
            if len(result) == 0:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("App/Game Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>No Games or Applications installed on the console")
                sms_box.setInformativeText("Please install a Game/Application on console first")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
        # Else populate list to QinputDialog and ask user to select application
            else:
                input_dialogue = QtWidgets.QInputDialog()
                App_name, ok = input_dialogue.getItem(self, "Application Selection", "<b>Select a Game for which you want to delete Save Data:</b>\n",result, 0, False)
                if ok:
                    comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env +  r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- savedata delete --application-id ' + App_name[:19]
                    #print(comm)
                    reply = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
                    line = reply.stdout.readline()
                    #print(line)
                    if "Save data associated with application id " in line:  # if there is no save data for selected application
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Delete Saves Data Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText(line)
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                    else:  # else delete save data for selected application successful
                        sms_box = QtWidgets.QMessageBox()
                        sms_box.setWindowTitle("Delete Saves Data Information")
                        sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                        sms_box.setText("All the Save Data has been deleted successfully for following Game: \n\n" + App_name)
                        sms_box.setIcon(sms_box.Information)
                        sms_box.exec_()
                else:
                    input_dialogue.close()


    def delete_all_saves(self):
        run_cmd()
        if run_cmd():
            sms_box = QtWidgets.QMessageBox()
            sms_box.setWindowTitle("Connection Information                                                       ")
            sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
            sms_box.setText("<b>No Target found and Failed to delete all Save Data</b>")
            sms_box.setInformativeText("Please connect/reconnect console to PC using Type C cable or wake it up from sleep mode.")
            sms_box.setIcon(sms_box.Information)
            sms_box.exec_()
        else:
            comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- savedata list'
            installation_progress = subprocess.Popen(comm, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            line = installation_progress.stdout.readline()
            if "[SUCCESS]" in line:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Save Data Information")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("No Save Data found to delete. Please create Save Data first")
                sms_box.setIcon(sms_box.Information)
                sms_box.exec_()
            else:
                sms_box = QtWidgets.QMessageBox()
                sms_box.setWindowTitle("Delete Confirmation")
                sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                sms_box.setText("<b>Are you sure you want to delete All Save Data from console?")
                sms_box.setStandardButtons(sms_box.Yes | sms_box.No)
                sms_box.setIcon(sms_box.Warning)
                press = sms_box.exec_()
                if press == sms_box.Yes:
                    delete_comm = env + r'\Tools\CommandLineTools\RunOnTarget.exe ' + env + r'\TargetTools\NX-NXFP2-a64\DevMenuCommand\Release\DevMenuCommand.nsp -- savedata delete all'
                    reply = subprocess.Popen(delete_comm, shell=True)
                    reply.wait()
                    sms_box = QtWidgets.QMessageBox()
                    sms_box.setWindowTitle("Save Data Delete Information")
                    sms_box.setWindowIcon(QIcon("./Images/Main_Logo.ico"))
                    sms_box.setText("All the Save Data has been deleted successfully")
                    sms_box.setIcon(sms_box.Information)
                    sms_box.exec_()
                else:
                    sms_box.close()


def appExec():
    app = QtWidgets.QApplication(sys.argv)
    dialog = My_Main_Dialog('Switch Interface')
    dialog.show()
    subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe connect', shell=True)
    app.exec_()
    subprocess.Popen(env + r'\Tools\CommandLineTools\ControlTarget.exe disconnect', shell=True)


sys.exit(appExec())
