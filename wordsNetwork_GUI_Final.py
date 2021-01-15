# -*- coding: utf-8 -*-
"""
                        **** PROJET PYTHON M1 INFORMATIQUE  ****
                                      (Sujet II)
                                  Interface Graphique
                                  
                                      Etudiantes:
                          Fatim-Zahra El Gaouzi, Sara Lehtihet
                                     
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from codeProjetFinal import Creation_corpus
import webbrowser
import os
from pyvis.network import Network
from codeProjetFinal import Singleton 

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

#mainDir = os.path.dirname(os.path.realpath(__file__))


# instaciation unique des classe qui cree le corpus ( en utilisant le singleton )
c = Creation_corpus(metaclass=Singleton)




######################################################################
#     Class Ui_WordsNetwork (interface Principale)
######################################################################  
   
class Ui_WordsNetwork(object):
       
    # fonction qui renvois le dictionnaire des doc ou apparait le mot chercher 
    # en faisant appel a la fonction docIncludingW de la class creation_corpus
    def btnSearch(self):
        # recuperer le nom entre dans l'interface
        word = self.searchEdit.text()
        global crp
        crp =c.create()
        global res 
        res = crp.docsIncludingW(word)
        return res
    
    # convertir le dictionnaire precedent en liste pour l'afficher dans le combobox
    def convertDict2List(self):
        res = self.btnSearch()
        global l
        l = []
        for key in res:
            l.append(res[key])
        return l
    
    # fonction de remplissage du combobox
    def remplissage_combobox(self):
        lst = self.convertDict2List()
        # on a choisie de selectionner que les 20 premiers elements pour l'afficher dans le combox
        # covid par exemple aparait dans 101 doccuments
        self.docBox.clear()
        self.docBox.addItems(lst[0:19])
        
   
    # retourne la clé (dans le corpus) du document selectionnée  pour recupérer le texte du document séléctionné
    # cette clé se trouve dans docIncludingW
    def docSelected(self):
        # recuperer la valeur choisie du combobox
        itemSelected= self.docBox.currentText()
        # recuperer son key depuis le dictionnaire 
        for key in res:
            if res[key] == itemSelected:
                return key 
            
            
    # fonction qui permet d'afficher le grphe 
    def graph(self):
        cle = self.docSelected()
        doc = crp.get_coll() 
        doc[cle].get_text()    # renvoie le texte du doc choisie dans le combobox
        docc = doc[cle]
        # faire appelle a la fonction draw_graph de la classe Document
        docc.draw_graph()
        # faire appelle a la fonction qui dessine le graphe
        webbrowser.get(chrome_path).open("./graph.html")
        #metode qui permet d'enregistrer le graphe
        got_net = Network(height="100%", width="100%", bgcolor="#0d335d", font_color="#2c3e50",heading="Graphe :")
        got_net.save_graph('./graph.html')
         
       
        """
           CODE POUR L INTERFACE GRAPHIQUE
        """
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
        #add some explication au texte edit
        #self.textEdit.setText(str("sara") + ": " + str("test") + "\n")
        
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
        self.exitButton.clicked.connect(WordsNetwork.close)
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
  
