import os
import cv2
import time
import ntpath
import pyAesCrypt
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget, QMessageBox
from PIL import Image
from Database import Database

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(640, 480)
        LoginWindow.setMinimumSize(QtCore.QSize(640, 480))
        LoginWindow.setMaximumSize(QtCore.QSize(640, 480))
        LoginWindow.setBaseSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 80, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnLogin = QtWidgets.QPushButton(self.centralwidget)
        self.btnLogin.setGeometry(QtCore.QRect(240, 190, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnLogin.setFont(font)
        self.btnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnLogin.setObjectName("btnLogin")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 240, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lblRegister = QtWidgets.QLabel(self.centralwidget)
        self.lblRegister.setGeometry(QtCore.QRect(360, 240, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.lblRegister.setFont(font)
        self.lblRegister.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lblRegister.setStyleSheet("border-bottom-width: 1px;\n"
"border-bottom-style: solid;\n"
"border-radius: 0px;")
        self.lblRegister.setObjectName("lblRegister")
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

        #################################################################

        self.lblRegister.mousePressEvent = self.openRegister
        self.btnLogin.clicked.connect(self.loginWithFace)


    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Secure PDF - Login"))
        self.label.setText(_translate("LoginWindow", "Secure PDF"))
        self.btnLogin.setText(_translate("LoginWindow", "Login With Face"))
        self.label_4.setText(_translate("LoginWindow", "Don\'t have an account?"))
        self.lblRegister.setText(_translate("LoginWindow", "Register here"))

    def openRegister(self, event):
        LoginWindow.hide()
        RegisterWindow.show()

    def createDir(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def recognizeFace(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.createDir("trainer/")
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX

        video_capture = cv2.VideoCapture(0)
        acc = 0
        Id = 0
        while True:
            _, image_frame = video_capture.read()
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2,5)

            for(x,y,w,h) in faces:
                cv2.rectangle(image_frame, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
                Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                acc = round(100-confidence, 2)

                cv2.rectangle(image_frame, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                cv2.putText(image_frame, str("Recognizing face..."), (x,y-40), font, 1, 
                    (255,255,255), 3)

            cv2.imshow("Recognizing Face. Please Wait ...", image_frame)

            if acc > 50:
                db.setUserId(Id)
                print(db.getUserId())
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def openMainMenu(self):
        MainWindow.show()
        LoginWindow.hide()

    def loginWithFace(self):
        msg = QMessageBox()
        try:
            _recognizeFace = self.recognizeFace()
        except Exception as e:
            errorDetail = str(e)
            msg.setWindowTitle("Error!")
            msg.setText("No face has registered yet!")
            msg.setInformativeText("See error log below")
            msg.setDetailedText(errorDetail)
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            if db.getUserId() > 0:
                msg.setWindowTitle("Login Success!")
                msg.setText("Welcome "+db.getNameFromId()+"!")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)

                self.openMainMenu()
            else:
                print(db.getUserId())

        x = msg.exec_()
                

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(640, 480)
        RegisterWindow.setMinimumSize(QtCore.QSize(640, 480))
        RegisterWindow.setMaximumSize(QtCore.QSize(640, 480))
        RegisterWindow.setBaseSize(QtCore.QSize(640, 320))
        font = QtGui.QFont()
        font.setFamily("Arial")
        RegisterWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 80, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 170, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.txtUsername = QtWidgets.QLineEdit(self.centralwidget)
        self.txtUsername.setGeometry(QtCore.QRect(200, 190, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.txtUsername.setFont(font)
        self.txtUsername.setFrame(True)
        self.txtUsername.setObjectName("txtUsername")
        self.btnRegister = QtWidgets.QPushButton(self.centralwidget)
        self.btnRegister.setGeometry(QtCore.QRect(250, 250, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.lblBack = QtWidgets.QLabel(self.centralwidget)
        self.lblBack.setGeometry(QtCore.QRect(280, 290, 101, 21))
        self.lblBack.setFont(font)
        self.lblBack.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lblBack.setStyleSheet("border-bottom-width: 1px;\n"
"border-bottom-style: solid;\n"
"border-radius: 0px;")
        self.lblBack.setObjectName("lblBack")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnRegister.setFont(font)
        self.btnRegister.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnRegister.setObjectName("btnRegister")
        RegisterWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RegisterWindow)
        self.statusbar.setObjectName("statusbar")
        RegisterWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)

        ###################################################

        self.btnRegister.clicked.connect(self.registerData)
        self.lblBack.mousePressEvent = self.openLogin

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "Secure PDf - Register"))
        self.label.setText(_translate("RegisterWindow", "Secure PDF"))
        self.label_2.setText(_translate("RegisterWindow", "Full Name"))
        self.btnRegister.setText(_translate("RegisterWindow", "Register Face"))
        self.lblBack.setText(_translate("RegisterWindow", "Back to Login"))

    def openLogin(self, event):
        RegisterWindow.hide()
        LoginWindow.show()      

    def createDir(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def getImagesAndLabels(self, path):
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples, ids

    def trainDataset(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces,ids = self.getImagesAndLabels('dataset')
        recognizer.train(faces, np.array(ids))   

        self.createDir('trainer/')
        recognizer.save('trainer/trainer.yml')
        print("Train completed")

    def createFaceDataset(self):
        nama = self.txtUsername.text()
        filename = nama.replace(" ", "")
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        face_id = db.getMaxId()+1
        count = 0
        
        self.createDir("dataset/")
        video_capture = cv2.VideoCapture(0)

        while True:
            _, image_frame = video_capture.read()
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1
                cv2.imwrite("dataset/" + filename + "." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow("Getting face. Please Wait ...", image_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif count == 300:
                self.trainDataset()             
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def registerData(self):
        user_id = db.getMaxId()+1
        nama = self.txtUsername.text()

        msg = QMessageBox()
        if nama == "":
            msg.setWindowTitle("Warning!")
            msg.setText("Please enter name!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            try:
                _createFaceDataset = self.createFaceDataset()
            except Exception as e:
                msg.setWindowTitle("Failed!")
                msg.setText("Fail getting face!")
                msg.setInformativeText("See error log below")
                msg.setDetailedText(e)
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
            else:
                msg.setWindowTitle("Success!")
                msg.setText("Successfully Registered!")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                db.insertUser(user_id, nama, nama)
                self.txtUsername.setText("")
                RegisterWindow.hide()
                LoginWindow.show()
        x = msg.exec_()

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        MainWindow.setBaseSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 30, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(50, 80, 541, 321))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.encTab = QtWidgets.QWidget()
        self.encTab.setObjectName("encTab")
        self.btnBrowseEnc = QtWidgets.QPushButton(self.encTab)
        self.btnBrowseEnc.setGeometry(QtCore.QRect(90, 100, 111, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnBrowseEnc.setFont(font)
        self.btnBrowseEnc.setObjectName("btnBrowseEnc")
        self.txtFileEnc = QtWidgets.QLineEdit(self.encTab)
        self.txtFileEnc.setEnabled(True)
        self.txtFileEnc.setGeometry(QtCore.QRect(200, 100, 251, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtFileEnc.setFont(font)
        self.txtFileEnc.setText("")
        self.txtFileEnc.setReadOnly(True)
        self.txtFileEnc.setObjectName("txtFileEnc")
        self.btnEncrypt = QtWidgets.QPushButton(self.encTab)
        self.btnEncrypt.setGeometry(QtCore.QRect(210, 160, 111, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnEncrypt.setFont(font)
        self.btnEncrypt.setObjectName("btnEncrypt")
        self.tabWidget.addTab(self.encTab, "")
        self.decTab = QtWidgets.QWidget()
        self.decTab.setObjectName("decTab")
        self.btnDecrypt = QtWidgets.QPushButton(self.decTab)
        self.btnDecrypt.setGeometry(QtCore.QRect(210, 160, 111, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnDecrypt.setFont(font)
        self.btnDecrypt.setObjectName("btnDecrypt")
        self.txtFileDec = QtWidgets.QLineEdit(self.decTab)
        self.txtFileDec.setEnabled(True)
        self.txtFileDec.setGeometry(QtCore.QRect(200, 100, 251, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtFileDec.setFont(font)
        self.txtFileDec.setText("")
        self.txtFileDec.setReadOnly(True)
        self.txtFileDec.setObjectName("txtFileDec")
        self.btnBrowseDec = QtWidgets.QPushButton(self.decTab)
        self.btnBrowseDec.setGeometry(QtCore.QRect(90, 100, 111, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnBrowseDec.setFont(font)
        self.btnBrowseDec.setObjectName("btnBrowseDec")
        self.tabWidget.addTab(self.decTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ########################################################

        self.btnBrowseEnc.clicked.connect(self.browseFileEnc)
        self.btnEncrypt.clicked.connect(self.encryptFile)

        self.btnBrowseDec.clicked.connect(self.browseFileDec)
        self.btnDecrypt.clicked.connect(self.decryptFile)

        self.actionAbout.triggered.connect(self.openAbout)
        self.actionExit.triggered.connect(self.closeProgram)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Secure PDF - Encrypt/Decrypt"))
        self.label.setText(_translate("MainWindow", "Secure PDF"))
        self.btnBrowseEnc.setText(_translate("MainWindow", "Browse"))
        self.txtFileEnc.setPlaceholderText(_translate("MainWindow", "Choose a file..."))
        self.btnEncrypt.setText(_translate("MainWindow", "Encrypt File"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.encTab), _translate("MainWindow", "Encrypt"))
        self.btnDecrypt.setText(_translate("MainWindow", "Decrypt File"))
        self.txtFileDec.setPlaceholderText(_translate("MainWindow", "Choose a file..."))
        self.btnBrowseDec.setText(_translate("MainWindow", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.decTab), _translate("MainWindow", "Decrypt"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def openAbout(self):
        AboutWindow.show()

    def closeProgram(self):
        sys.exit()

    def browseFileEnc(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse a file ...", "","PDF Files (*.pdf)", options=options)
        if fileName:
            self.txtFileEnc.setText(fileName)

    def browseFileDec(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse a file ...", "","All Files (*);;PDF Files (*.pdf)", options=options)
        if fileName:
            self.txtFileDec.setText(fileName)

    def encryptFile(self):
        bufferSize = 64 * 1024
        password = db.getKeyFromId()
        msg = QMessageBox()
        fileLocation = self.txtFileEnc.text()
        if (fileLocation == ""):
            msg.setWindowTitle("Warning!")
            msg.setText("No file selected!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            try:
                encryptFile = pyAesCrypt.encryptFile(fileLocation, 
                    fileLocation + ".enc", password, bufferSize)  
            except Exception as e:
                msg.setWindowTitle("Failed!")
                msg.setText("Encryption failed!")
                msg.setInformativeText("See error log below")
                msg.setDetailedText(e)
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
            else:
                msg.setWindowTitle("Success!")
                msg.setText("Encryption Success!")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                if os.path.exists(fileLocation):
                    os.remove(fileLocation)
                else:
                    print("The file does not exist")
                self.txtFileEnc.setText("")
        x = msg.exec_()

    def decryptFile(self):
        bufferSize = 64 * 1024
        password = db.getKeyFromId()
        msg = QMessageBox()
        fileLocation = self.txtFileDec.text()
        if (fileLocation == ""):
            msg.setWindowTitle("Warning!")
            msg.setText("No file selected!")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            try:
                newFile = ntpath.basename(fileLocation)
                decryptFile = pyAesCrypt.decryptFile(fileLocation, 
                    newFile[0:-4], password, bufferSize)  
            except ValueError as e:
                msg.setWindowTitle("Failed!")
                msg.setText("Decryption failed!")
                msg.setInformativeText("See error log below")
                msg.setDetailedText(str(e))
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
            else:
                msg.setWindowTitle("Success!")
                msg.setText("Decryption Success!")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                if os.path.exists(fileLocation):
                    os.remove(fileLocation)
                else:
                    print("The file does not exist")
                self.txtFileDec.setText("")
        x = msg.exec_()

class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.resize(240, 320)
        AboutWindow.setMinimumSize(QtCore.QSize(240, 320))
        AboutWindow.setMaximumSize(QtCore.QSize(240, 320))
        AboutWindow.setBaseSize(QtCore.QSize(240, 320))
        font = QtGui.QFont()
        font.setFamily("Arial")
        AboutWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(AboutWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 221, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        AboutWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AboutWindow)
        self.statusbar.setObjectName("statusbar")
        AboutWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AboutWindow)
        QtCore.QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        _translate = QtCore.QCoreApplication.translate
        AboutWindow.setWindowTitle(_translate("AboutWindow", "About App"))
        self.label.setText(_translate("AboutWindow", "Secure PDF"))
        self.label_2.setText(_translate("AboutWindow", "Choose a PDF Document before encrypt and decrypt."))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    db = Database()
    db.createTable()

    LoginWindow = QtWidgets.QMainWindow()
    loginUI = Ui_LoginWindow()
    loginUI.setupUi(LoginWindow)

    RegisterWindow = QtWidgets.QMainWindow()
    registerUI = Ui_RegisterWindow()
    registerUI.setupUi(RegisterWindow)

    MainWindow = QtWidgets.QMainWindow()
    mainUI = Ui_MainWindow()
    mainUI.setupUi(MainWindow)

    AboutWindow = QtWidgets.QMainWindow()
    aboutUI = Ui_AboutWindow()
    aboutUI.setupUi(AboutWindow)

    LoginWindow.show()
    sys.exit(app.exec_())

