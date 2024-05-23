from NLP_method import*

import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QLabel,
                             QRadioButton, QLineEdit, QFrame, QMessageBox)
from PyQt5.QtGui import QColor, QPixmap, QPalette
from PyQt5.QtCore import Qt


class Waiter(QMainWindow):

    def __init__(self, parent=None):
        super(Waiter, self).__init__(parent=parent)
        self.initGUI()
        self.create_actions()
        self.grammar = r"""
                    FOOD: {<nc.*>}
                    QUANTITY: {<dn.*>}
                          {<di.*>}
                          {<Z>}
                        """

        self.setStyleSheet("background-color: white;")

        self.regex_method = None
        self.uni_method = None
        self.naive_method = None

    def initGUI(self):
        self.setWindowTitle("Waiter NLP")
        self.resize(300, 400)
        self.setCentralWidget(QWidget(self))
        wkdir = os.getcwd()
        img_dir = os.path.join(wkdir, "waiter_.jpg")

        #PALETTE
        pal = self.palette()
        pal.setColor(QPalette.WindowText, QColor("#6EB5FF"))

        # FRAMES
        self.frame_top = QFrame()
        self.frame_top.setLineWidth(1)
        self.frame_top.setFrameStyle(QFrame.Panel | QFrame.Panel)
        self.frame_top.setPalette(pal)
        self.frame_bot = QFrame()
        self.frame_bot.setLineWidth(1)
        self.frame_bot.setFrameStyle(QFrame.Panel | QFrame.Panel)
        self.frame_bot.setPalette(pal)

        # LAYOUTS
        self.layout_main = QVBoxLayout()
        self.layout_dialog = QVBoxLayout()
        self.layout_waiter = QVBoxLayout()
        self.layout_method = QHBoxLayout()
        self.layout_scenario = QHBoxLayout()


        #LABELS
        self.label_method = QLabel("Choose a classification method:     ")
        self.label_write = QLabel("Enter here what you want to order: ")
        self.label_result = QLabel("Your order is...")
        self.label_chunks = QLabel()

        #LINEDIT
        self.line_food = QLineEdit("")

        # BUTTONS
        self.button_delete = QPushButton("Try again")
        self.button_delete.setStyleSheet("background-color: #CCDDFF; border-style: outset; border-color: #6EB5FF;"
                                         " border-radius: 5px; border-width: 2px")
        self.button_order = QPushButton("Order!")
        self.button_order.setStyleSheet("background-color: #CCDDFF; border-style: outset; border-color: #6EB5FF;"
                                         " border-radius: 5px; border-width: 2px")
        self.button_delete.resize(15, 20)
        self.button_regex = QRadioButton("RegexParser")
        self.button_unigram = QRadioButton("UnigramChunker")
        self.button_naive = QRadioButton("NaiveBayesClassifier")

        labelImage = QLabel(self)
        pixmap = QPixmap(img_dir)
        labelImage.resize(300, 300)
        labelImage.setPixmap(pixmap.scaled(labelImage.size(), Qt.KeepAspectRatio))
        labelImage.setAlignment(Qt.AlignLeft)

        self.layout_method.addWidget(self.label_method)
        self.layout_method.addWidget(self.button_regex)
        self.layout_method.addWidget(self.button_unigram)
        self.layout_method.addWidget(self.button_naive)

        self.layout_waiter.addWidget(labelImage, alignment=Qt.AlignLeft)

        self.layout_dialog.addWidget(self.label_write)
        self.layout_dialog.addWidget(self.line_food)
        self.layout_dialog.addWidget(self.button_order)
        self.layout_dialog.addWidget(self.label_result)
        self.layout_dialog.addWidget(self.label_chunks)

        self.layout_scenario.addLayout(self.layout_waiter)
        self.layout_scenario.addLayout(self.layout_dialog)
        self.frame_bot.setLayout(self.layout_scenario)
        self.frame_top.setLayout(self.layout_method)
        self.layout_main.addWidget(self.frame_top)
        self.layout_main.addWidget(self.frame_bot)
        self.layout_main.addWidget(self.button_delete)
        self.centralWidget().setLayout(self.layout_main)

    # CONNECTIONS
    def create_actions(self):
        self.button_order.clicked.connect(self.order)
        self.button_delete.clicked.connect(self.delete)

    # MAIN METHOD
    def order(self):
        self.button_order.setEnabled(False)
        self.line_food.setEnabled(False)
        if self.line_food.text() != "":
            sentence = self.line_food.text()
            try:
                if self.button_regex.isChecked():
                    if self.regex_method is None:
                        self.init_regex()
                    parsed = self.regex_method.regex_parse(sentence)
                    self.show_result(parsed)
                elif self.button_unigram.isChecked():
                    if self.uni_method is None:
                        self.init_uni()
                    parsed = self.uni_method.parse(sentence)
                    self.show_result(parsed)
                elif self.button_naive.isChecked():
                    if self.naive_method is None:
                        self.init_naive()
                    parsed = self.naive_method.parse(sentence)
                    self.show_result(parsed)
                else:
                    self.show_dialog_2()
            except:
                self.show_dialog_3()
        else:
            self.show_dialog_1()

    def delete(self):
        self.label_chunks.clear()
        self.line_food.clear()
        if self.line_food.isEnabled():
            pass
        else:
            self.line_food.setEnabled(True)
        if self.button_order.isEnabled():
            pass
        else:
            self.button_order.setEnabled(True)

    def init_regex(self):
        self.regex_method = RegexParser(self.grammar)

    def init_uni(self):
        self.uni_method = MyUnigramChunker(self.grammar)

    def init_naive(self):
        self.naive_method = NaiveBayesChunker(self.grammar)

    def show_result(self, parsedSentence):
        print("Result...")
        result = str
        food = None
        quantity = None
        for n in parsedSentence:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'FOOD':
                    food = "FOOD: " + str(n.leaves()[0][0])
                    result = food + "\n"
                elif n.label() == 'QUANTITY':
                    quantity = "QUANTITY: " + str(n.leaves()[0][0])
        if food is not None:
            if quantity == None:
                quantity = "1"
            result = result + str(quantity)
            self.label_chunks.setText(result)
        else:
            self.label_chunks.setText("Unable to identify, try with other method")


    def show_dialog_1(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You need to order something")
        msg.setWindowTitle("Error")
        msg.exec_()
        self.button_order.setEnabled(True)

    def show_dialog_2(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You have to select a classification method")
        msg.setWindowTitle("Error")
        msg.exec_()
        self.button_order.setEnabled(True)

    def show_dialog_3(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Method failed")
        msg.setWindowTitle("Error")
        msg.exec_()
        self.button_order.setEnabled(True)


def main():
    app = QApplication( sys.argv )
    GUI = Waiter()
    GUI.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
