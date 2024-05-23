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
        self.grammar_general = r"""
                    ORDER: {<d.*><nc.*>?<aq.*>}
                            {<d.*><nc.*>}
                            {<Z><nc.*>}
                            """
        self.grammar_specific = r"""
                    FOOD: {<nc.*>}
                    QUANTITY: {<dn.*>}
                          {<di.*>}
                          {<Z>}
                        """

        self.setStyleSheet("background-color: white;")

        self.regex_method_1 = None
        self.uni_method_1 = None
        self.naive_method_1 = None

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
        self.label_method = QLabel("Escoge un método de clasificación:     ")
        self.label_write = QLabel("Escribe aquí lo que quieras pedir: ")
        self.label_result = QLabel("Has pedido...")
        self.label_chunks = QLabel()

        #LINEDIT
        self.line_food = QLineEdit("")

        # BUTTONS
        self.button_delete = QPushButton("Repetir")
        self.button_delete.setStyleSheet("background-color: #CCDDFF; border-style: outset; border-color: #6EB5FF;"
                                         " border-radius: 5px; border-width: 2px")
        self.button_order = QPushButton("¡Pedir!")
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

    def create_actions(self):
        self.button_order.clicked.connect(self.order)
        self.button_delete.clicked.connect(self.delete)

    def order(self):
        self.button_order.setEnabled(False)
        self.line_food.setEnabled(False)
        if self.line_food.text() != "":
            sentence = self.line_food.text()
            try:
                if self.button_regex.isChecked():
                    if self.regex_method_1 is None:
                        self.init_regex()
                    # Obtenemos el chunk de la petición
                    sentence_parsed = self.regex_method_1.regex_parse(sentence)
                    order = self.get_order_words(sentence_parsed)
                    # Lo parseamos otra vez para diferenciar entre comida y cantidad
                    result = self.regex_method_2.regex_parse(order)
                    self.show_result(result)
                elif self.button_unigram.isChecked():
                    if self.uni_method_1 is None:
                        self.init_uni()
                    # Obtenemos el chunk de la petición
                    sentence_parsed = self.uni_method_1.parse(sentence)
                    order = self.get_order_words(sentence_parsed)
                    # Lo parseamos otra vez para diferenciar entre comida y cantidad
                    result = self.uni_method_2.parse(order)
                    self.show_result(result)
                elif self.button_naive.isChecked():
                    if self.naive_method_1 is None:
                        self.init_naive()
                    # Obtenemos el chunk de la petición
                    sentence_parsed = self.naive_method_1.parse(sentence)
                    order = self.get_order_words(sentence_parsed)
                    # Lo parseamos otra vez para diferenciar entre comida y cantidad
                    result = self.naive_method_2.parse(order)
                    self.show_result(result)
                else:
                    self.show_dialog_2()
            except:
                self.show_dialog_3()
                self.delete()
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
        self.regex_method_1 = RegexParser(self.grammar_general)
        self.regex_method_2 = RegexParser(self.grammar_specific)

    def init_uni(self):
        self.uni_method_1 = MyUnigramChunker(self.grammar_general, 1)
        self.uni_method_2 = MyUnigramChunker(self.grammar_specific, 2)

    def init_naive(self):
        self.naive_method_1 = NaiveBayesChunker(self.grammar_general, 1)
        self.naive_method_2 = NaiveBayesChunker(self.grammar_specific, 2)

    def get_order_words(self, parsed):
        for n in parsed:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'ORDER':
                    order = ' '.join([str(n.leaves()[0][0]), str(n.leaves()[1][0])])
        return order

    def show_result(self, parsed_order):
        print("Result...")
        result = str
        quantity = None
        for n in parsed_order:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == 'FOOD':
                    print(n)
                    food = "FOOD: " + str(n.leaves()[0][0])
                    result = food + "\n"
                elif n.label() == 'QUANTITY':
                    quantity = "QUANTITY: " + str(n.leaves()[0][0])
        if food is not None:
            if quantity is None:
                quantity = "1"
            result = result + str(quantity)
            self.label_chunks.setText(result)
        else:
            self.label_chunks.setText("No se ha podido identificar, prueba otro método")

    def show_dialog_1(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Tienes que pedir algo")
        msg.setWindowTitle("Error")
        msg.exec_()
        self.button_order.setEnabled(True)

    def show_dialog_2(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Tienes que elegir un método")
        msg.setWindowTitle("Error")
        msg.exec_()
        self.button_order.setEnabled(True)

    def show_dialog_3(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("El método no ha funcionado")
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
