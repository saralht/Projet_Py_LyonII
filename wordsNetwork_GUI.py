"""
Created on Fri Dec 11 08:16:56 2020

@author: HP LEHTIHET
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wordsNetwork_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from codeProjetv2 import Corpus
from codeProjetv2 import Creation_corpus
from codeProjetv2 import Document
import webbrowser
import urllib.request





chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'



# quand j'instatncie la classe corpus elle se cree a chaque fois que la ftn btnSearch est lancer:
    # tester le singleton 
# je dois faire un teste si le corpus est vide alors le creer sinon pass 
# je pense qu'il se cree a chaque fois que j'appuie sur la recherche 
# tester en le vidant 


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# instaciation des classes
c = Creation_corpus(metaclass=Singleton)



class Ui_WordsNetwork(object):
    def exit_cleaning(self):
        #res.clear()
        self.exitButton.clicked.connect(WordsNetwork.close)
        #urllib.request.urlretrieve("file:///C:/Users/HP/Desktop/MasterLyon2/Programmation%20Avanc%C3%A9/graph.html", "Image.jpg")
    
    # fonction qui renvois le dictionnaire des doc ou apparait le mot chercher 
    # en faisons appelle a la fonction docIncludingW de la classe creation_corpus
    def btnSearch(self):
        # recuperer le nom entre dans l'interface
        word = self.searchEdit.text()
        global crp
        crp =c.create()
        print("crp\n",crp)
        # je dois vider ce dict car il prend le resultat de lancienne recherche 
        global res 
        res = crp.docsIncludingW(word)
        print(res)
        return res
    
    # convertir le dictionnaire precedent en liste pour l'afficher dans le combobox
    def convertDict2List(self):
        res = self.btnSearch()
        # mettre les titres dans une liste pour les afficher dans le combobox
        global l
        l = []
        for key in res:
            l.append(res[key])
        return l
    
    # fonction de remplissage du combobox
    def remplissage_combobox(self):
        lst = self.convertDict2List()
        # on a choisie de selectionner que les 10 premiers elements pour l'afficher dans le combox
        # covid par exemple aparait dans 101 doccumentss
        self.docBox.clear()
        self.docBox.addItems(lst[0:9])
        
   
    # retourne la clé du document selectionnée 
    # cette clé se trouve dans docIncludingW
    # on a fait ça prsk combox contient une liste et non pas un dict
    def docSelected(self):
        # recuperer la valeur choisir du combobox
        itemSelected= self.docBox.currentText()
        # recuperer son key depuis le dictionnaire 
        for key in res:
            if res[key] == itemSelected:
                return key 
            
            
    # fonction qui permet d'afficher le grphe 
    def graph(self):
        cle = self.docSelected()
        doc = crp.get_coll() 
        #doc[cle].get_doc()
        doc[cle].get_text()    # renvoie le texte du doc choisie dans le combobox
        docc = doc[cle]
        # faire appelle a la fonction draw_graph de la classe Document
        docc.draw_graph()
        # faire appelle a la fonction qui dessine le graphe
        webbrowser.get(chrome_path).open("./graph.html")
         
       
    
        
    def setupUi(self, WordsNetwork):
        WordsNetwork.setObjectName("WordsNetwork")
        WordsNetwork.setEnabled(True)
        WordsNetwork.setFixedSize(628, 428)
       
        self.centralwidget = QtWidgets.QWidget(WordsNetwork)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 631, 441))
        self.frame.setStyleSheet("background-color: #cfdac8;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.title = QtWidgets.QLabel(self.frame)
        self.title.setGeometry(QtCore.QRect(140, 20, 341, 41))
        font = QtGui.QFont()
        font.setFamily("News701 BT")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("color: #7C9473;")
        self.title.setObjectName("title")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(220, 60, 181, 20))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#456268;")
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(80, 240, 481, 81))
        self.textEdit.setStyleSheet("color: #456268;")
        self.textEdit.setObjectName("textEdit")
        self.searchButton = QtWidgets.QPushButton(self.frame)
        
        
        self.searchButton.setGeometry(QtCore.QRect(280, 160, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("QPushButton{\n"
                                        "    background-color:#e8eae6;\n"
                                        "    border-radius: 12px;\n"
                                        "    color:#456268;\n"
                                        "    opacity: 0.9;\n"
                                        "}")
        self.searchButton.setObjectName("searchButton")
        #Fonction du boutton search
        self.searchButton.clicked.connect(self.remplissage_combobox)
        self.showGraphButton = QtWidgets.QPushButton(self.frame)
        self.showGraphButton.setGeometry(QtCore.QRect(170, 330, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.showGraphButton.setFont(font)
        self.showGraphButton.setStyleSheet("QPushButton{\n"
                                           "    background-color:#e8eae6;\n"
                                           "    border-radius: 12px;\n"
                                           "    color:#456268;\n"
                                           "    opacity: 0.9;\n"
                                           "}")
        self.showGraphButton.setObjectName("showGraphButton")
        # bouton qui ouvre le graphe
        self.showGraphButton.clicked.connect(self.graph)
        self.searchEdit = QtWidgets.QLineEdit(self.frame)
        self.searchEdit.setGeometry(QtCore.QRect(110, 120, 411, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.searchEdit.setFont(font)
        self.searchEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.searchEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.searchEdit.setStyleSheet("color: #456268;\n"
                                      "background-color: #e8eae6;\n"
                                      "border-radius:10px;")
        self.searchEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.searchEdit.setObjectName("searchEdit")
        self.docBox = QtWidgets.QComboBox(self.frame)
        self.docBox.setGeometry(QtCore.QRect(110, 200, 401, 22))
        self.docBox.setStyleSheet("background-color: #e8eae6;")
        self.docBox.setObjectName("docBox")
        self.exitButton = QtWidgets.QPushButton(self.frame)
        self.exitButton.setGeometry(QtCore.QRect(360, 330, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("QPushButton{\n"
                                      "    background-color:#e8eae6;\n"
                                      "    border-radius: 12px;\n"
                                      "    color:#456268;\n"
                                      "    opacity: 0.9;\n"
                                      "}")
        self.exitButton.setObjectName("exitButton")
        # exit button
        #self.exit.clicked.connect(WordsNetwork.close)
        self.exitButton.clicked.connect(self.exit_cleaning)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(250, 80, 118, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        WordsNetwork.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(WordsNetwork)
        self.statusbar.setObjectName("statusbar")
        WordsNetwork.setStatusBar(self.statusbar)

        self.retranslateUi(WordsNetwork)
        QtCore.QMetaObject.connectSlotsByName(WordsNetwork)

    def retranslateUi(self, WordsNetwork):
        _translate = QtCore.QCoreApplication.translate
        WordsNetwork.setWindowTitle(_translate("WordsNetwork", "WORDS NETWORK"))
        self.title.setText(_translate("WordsNetwork", "<strong>WORDS </strong>Network"))
        self.label.setText(_translate("WordsNetwork", "Université de Lyon II"))
        self.textEdit.setHtml(_translate("WordsNetwork", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.searchButton.setText(_translate("WordsNetwork", "Search"))
        self.showGraphButton.setText(_translate("WordsNetwork", "Show Graph"))
        self.searchEdit.setText(_translate("WordsNetwork", " entrer the word you search.."))
        self.exitButton.setText(_translate("WordsNetwork", "EXIT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WordsNetwork = QtWidgets.QMainWindow()
    ui = Ui_WordsNetwork()
    ui.setupUi(WordsNetwork)
    WordsNetwork.show()
    sys.exit(app.exec_())
  
