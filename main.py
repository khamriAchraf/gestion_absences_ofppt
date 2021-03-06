import csv
import os
import sqlite3
import sys
import webbrowser
from datetime import date,datetime
from PyQt5.QtGui import QStandardItemModel, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QLineEdit, QPushButton, QDialog, \
    QFileDialog, QMainWindow
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from pyqt5_plugins.examplebutton import QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QCoreApplication, QUrl
from fpdf import FPDF



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('ofppt.db')
        self.cur = self.connection.cursor()
        self.dir=""
        self.res=""
        self.setWindowIcon(QIcon('logo.ico'))
        self.w = None  # No external window yet.
        self.ww = None  # No external window yet.
        self.www = None  # No external window yet.
        self.wwww = None  # No external window yet.
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 330)
        self.tableWidget.setColumnWidth(2, 330)
        self.tableWidget.setColumnWidth(3, 150)
        self.state()
        self.loadData()
        # get id of selected row
        self.supprimer.clicked.connect(lambda: self.suppr(self.tableWidget.selectedItems()[0].text()))
        self.tableWidget.selectionModel().selectionChanged.connect(lambda :self.state())
        self.addOne.clicked.connect(lambda : self.addOneH(self.tableWidget.selectedItems()[0].text()))
        self.addTwo.clicked.connect(lambda: self.addTwoH(self.tableWidget.selectedItems()[0].text()))
        self.minusOne.clicked.connect(lambda: self.minusOneH(self.tableWidget.selectedItems()[0].text()))
        self.minusTwo.clicked.connect(lambda: self.minusTwoH(self.tableWidget.selectedItems()[0].text()))
        self.pdf.clicked.connect(lambda: self.creerPdf())
        self.searchBar.textChanged.connect(self.search)
        self.cb.currentIndexChanged.connect(self.loadData)
        self.max.valueChanged.connect(self.loadData)
        self.min.valueChanged.connect(self.loadData)
        self.limit.stateChanged.connect(self.activateFilter)
        self.matching_items=[]
        self.i=-1
        self.next.clicked.connect(self.nextItem)
        self.previous.clicked.connect(self.previousItem)
        self.action.triggered.connect(self.importerCSV)
        self.me.clicked.connect(lambda : webbrowser.open('https://khamri-achraf.web.app/'))

    def importerCSV(self):
        try:
            file_filter = 'Fichier .csv (*.csv)'
            response = QFileDialog.getOpenFileName(
                parent=self,
                caption='Choisir un fichier csv',
                directory=os.getcwd(),
                filter=file_filter,
            )
            STATEMENT = "DELETE FROM ofppt;"
            myApp.cur.execute(STATEMENT)
            myApp.connection.commit()
            with open(response[0], 'r', encoding="utf8") as fin:
                dr = csv.DictReader(fin)  # comma is default delimiter
                to_db = [(i['nom'], i['cin'], i['filiere'], i['absence']) for i in dr]
                self.cur.executemany("INSERT INTO ofppt (nom, cin,filiere,absence) VALUES (?, ?, ?, ?);", to_db)
                self.connection.commit()
            myApp.loadData()
        except:
            pass

    def activateFilter(self):
        try:
            if self.limit.isChecked():
                self.label_3.setEnabled(True)
                self.label_4.setEnabled(True)
                self.min.setEnabled(True)
                self.max.setEnabled(True)
            else :
                self.label_3.setEnabled(False)
                self.label_4.setEnabled(False)
                self.min.setEnabled(False)
                self.max.setEnabled(False)
                self.loadData()
        except:
            pass


    def creerPdf(self):
        try:
            response = QFileDialog.getExistingDirectory(
                self,
                caption='Select a folder'
            )
            self.resp=response
            today = str(date.today().year)+str(date.today().month)+str(date.today().day)+'_'+str(datetime.now().hour)+str(datetime.now().minute)+str(datetime.now().second)
            item = self.tableWidget.selectedItems()
            pdf = PDF()
            pdf.add_page()
            pdf.set_title("Informations de l'??tudiant")
            pdf.set_font('Arial', '', 16)
            pdf.print_line('Nom & Pr??nom : ', item[1].text())
            pdf.print_line('CIN : ', item[0].text())
            pdf.print_line("Absence : ", item[3].text(),' s??ances.')
            dir=response+'/'+item[1].text()+'_'+today+'.pdf'
            self.dir=dir
            pdf.output(dir, 'F')
            self.show_new_windowwww()
        except:
            pass
    def commit(self):
        self.connection.commit()

    def minusOneH(self,cin):
        try:
            if not int(self.tableWidget.selectedItems()[3].text()) < 1:
                STATEMENT = "UPDATE ofppt SET absence = absence - 1 WHERE cin='" + cin+"'"
                self.cur.execute(STATEMENT)
                self.connection.commit()
                self.searchBar.setText("")
                self.loadData()
                self.state()
            else:
                pass
        except:
            pass
    def minusTwoH(self,cin):
        try:
            if not int(self.tableWidget.selectedItems()[3].text()) < 1:
                STATEMENT = "UPDATE ofppt SET absence = absence - 2 WHERE cin='" + cin + "'"
                self.cur.execute(STATEMENT)
                self.connection.commit()
                self.searchBar.setText("")
                self.loadData()
                self.state()
            else:
                pass
        except:
            pass

    def addOneH(self,cin):
        try:
            STATEMENT = "UPDATE ofppt SET absence = absence + 1 WHERE cin='" + cin + "'"
            self.cur.execute(STATEMENT)
            self.connection.commit()
            self.searchBar.setText("")
            self.loadData()
            self.state()
        except:
            pass

    def addTwoH(self,cin):
        try:
            STATEMENT = "UPDATE ofppt SET absence = absence + 2 WHERE cin='" + cin + "'"
            self.cur.execute(STATEMENT)
            self.connection.commit()
            self.searchBar.setText("")
            self.loadData()
            self.state()
        except:
            pass

    def suppr(self, rowNumber):
        try:
            if self.tableWidget.selectedItems() == []:
                pass
            else:
                STATEMENT = "DELETE FROM ofppt WHERE cin='" + self.tableWidget.selectedItems()[0].text() + "';"
                self.cur.execute(STATEMENT)
                self.connection.commit()
                self.loadData()
        except:
            pass

    def state(self):
        try:
            if self.searchBar.text()=="":
                self.next.setEnabled(False)
                self.previous.setEnabled(False)
            else:
                self.next.setEnabled(True)
                self.previous.setEnabled(True)
            if self.tableWidget.selectedItems() == []:
                self.supprimer.setEnabled(False)
                self.addOne.setEnabled(False)
                self.addTwo.setEnabled(False)
                self.minusOne.setEnabled(False)
                self.minusTwo.setEnabled(False)
                self.pdf.setEnabled(False)
                self.edit.setEnabled(False)
            else:
                self.supprimer.setEnabled(True)
                self.addOne.setEnabled(True)
                self.addTwo.setEnabled(True)
                self.pdf.setEnabled(True)
                self.edit.setEnabled(True)
                if self.tableWidget.selectedItems()[3].text() == '0':
                    self.minusOne.setEnabled(False)
                    self.minusTwo.setEnabled(False)
                elif self.tableWidget.selectedItems()[3].text() == '1':
                    self.minusTwo.setEnabled(False)
                    self.minusOne.setEnabled(True)
                else:
                    self.minusOne.setEnabled(True)
                    self.minusTwo.setEnabled(True)
        except:
            pass

    def search(self, keyword):
        self.state()
        try:
            # Clear current selection.
            self.tableWidget.setCurrentItem(None)

            if not keyword:
                # Empty string, don't search.
                return
            self.matching_items = self.tableWidget.findItems(keyword, Qt.MatchContains)
            if self.i < len(self.matching_items) - 1:
                self.i += 1
            else:
                self.i = 0
            if self.matching_items:
                # We have found something.
                item = self.matching_items[self.i]  # Take the first.
                self.tableWidget.setCurrentItem(item)
        except:
            pass

    def nextItem(self,keyword):
        try:
            if self.i<len(self.matching_items)-1:
                self.i+=1
            else:
                self.i=0
            self.tableWidget.setCurrentItem(self.matching_items[self.i])
        except:
            pass
    def previousItem(self,keyword):
        try:
            if self.i==0:
                self.i=len(self.matching_items)
            else:
                self.i-=1
            self.tableWidget.setCurrentItem(self.matching_items[self.i])
        except:
            pass

    def loadData(self):
        try:
            if True:
                if self.cb.currentText() == "Tout":
                    SQL_STATEMENT = "SELECT cin,nom,filiere,absence FROM ofppt ORDER BY filiere,nom "
                    if self.max.isEnabled():
                        SQL_STATEMENT = "SELECT cin,nom,filiere,absence FROM ofppt WHERE absence >="+ str(self.min.value())+" AND absence <= "+str(self.max.value())+"  ORDER BY filiere,nom "
                else:
                    SQL_STATEMENT = "SELECT cin,nom,filiere,absence FROM ofppt WHERE filiere='" + self.cb.currentText() + "' ORDER BY filiere,nom"
                    if self.max.isEnabled():
                        SQL_STATEMENT = "SELECT cin,nom,filiere,absence FROM ofppt WHERE filiere='" + self.cb.currentText() + "' and absence >="+ str(self.min.value())+" AND absence <= "+str(self.max.value())+ " ORDER BY filiere,nom"
                self.cur.execute(SQL_STATEMENT)
                results = self.cur.fetchall()
                self.tableWidget.setRowCount(len(results))
                tablerow = 0
                for row in results:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem((row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    if row[3]>19:
                        for j in range(0,4):
                            self.tableWidget.item(tablerow, j).setBackground(QColor(255, 114, 111))
                    tablerow+=1
            self.state()
            self.ajouterEt.clicked.connect(self.show_new_window)
            self.toutSupp.clicked.connect(self.show_new_windoww)
            self.edit.clicked.connect(self.show_new_windowww)
            self.tableWidget.cellDoubleClicked.connect(self.show_new_windowww)
        except:
            pass

    def show_new_window(self, checked):
        try:
            if self.w is None:
                self.w = Ajouter()
            self.w.show()
            self.w.result.setText("")
            self.w.cin.setText("")
            self.w.nom.setText("")
        except:
            pass

    def show_new_windoww(self, checked):
        try:
            if self.ww is None:
                self.ww = Confirmer()
            self.ww.show()
        except:
            pass

    def show_new_windowwww(self):
        if self.wwww is None:
            self.wwww = Dialogue()
        self.wwww.label.setText("PDF cr???? avec succ??s dans "+myApp.dir)
        self.wwww.show()


    def show_new_windowww(self, checked):
        try:
            if self.www is None:
                self.www = Modifier()
            self.www.cin.setText(myApp.tableWidget.selectedItems()[0].text())
            self.www.nom.setText(myApp.tableWidget.selectedItems()[1].text())
            self.www.spinBox.setValue(int(myApp.tableWidget.selectedItems()[3].text()))
            self.www.cb.setCurrentText(myApp.tableWidget.selectedItems()[2].text())
            self.www.result.setText('')
            self.www.old_cin=self.www.cin.text()
            self.www.show()
        except:
            pass

class Ajouter(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ajouter.ui', self)
        self.nom.textChanged.connect(self.okayBtnState)
        self.cin.textChanged.connect(self.okayBtnState)
        self.end.clicked.connect(self.closeWindow)
        self.ok.clicked.connect(self.ajouterEtudiant)


    def closeWindow(self):
        try:
            self.close()
            self.result.setText("")
        except:
            pass

    def okayBtnState(self):
        try:
            if self.nom.text() != "" and self.cin.text() != "":
                self.ok.setEnabled(True)
            else :
                self.ok.setEnabled(False)
        except:
            pass
    def ajouterEtudiant(self):
        v=0
        if v==0:
            STATEMENT = "INSERT INTO ofppt(cin,nom,filiere,absence) VALUES ('"+self.cin.text()+"','"+self.nom.text()+"','"+self.cb.currentText()+"',0)"
            myApp.cur.execute(STATEMENT)
            myApp.connection.commit()
            myApp.loadData()
            self.result.setText("Etudiant ajout?? !")

        else:
            self.result.setText("Etudiant existe d??j?? !")


class Modifier(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('modifier.ui', self)
        self.end.clicked.connect(self.closeWindow)
        self.ok.clicked.connect(self.modifierEtudiant)
        self.old_cin=''

    def closeWindow(self):
        self.close()



    def modifierEtudiant(self):
        try:
            v=0
            if v == 0:
                STATEMENT = "UPDATE ofppt SET cin='"+self.cin.text()+"',nom='"+self.nom.text()+"',filiere='"+self.cb.currentText()+"',absence="+str(self.spinBox.value())+" WHERE cin='"+self.old_cin+"'"

                myApp.cur.execute(STATEMENT)
                myApp.connection.commit()

                myApp.loadData()
                self.close()

            else:
                self.result.setText("Erreur: CIN existe d??j?? !")
        except:
            pass

class Confirmer(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('confirmer.ui', self)
        self.end.clicked.connect(self.close)
        self.effacer.clicked.connect(self.toutEffacer)

    def toutEffacer(self):
        try:
            STATEMENT = "DELETE FROM ofppt;"
            myApp.cur.execute(STATEMENT)
            myApp.connection.commit()
            myApp.loadData()
            self.close()
        except:
            pass

class Dialogue(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('dialog.ui', self)
        self.ok.clicked.connect(self.close)
        self.open.clicked.connect(self.ouvrirFicher)
        self.explorer.clicked.connect(self.ouvrirDossier)

    def ouvrirFicher(self):
        try:
            os.startfile(myApp.dir)
            self.close()
        except:
            pass
    def ouvrirDossier(self):
        try:
            explorer_dir=""
            for i in myApp.dir:

                if i=="/":
                    explorer_dir+='\\'
                else:
                    explorer_dir += i
            os.system("explorer.exe /select, \""+explorer_dir+"\"")
            self.close()
        except:
            pass

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        self.set_y(0)
        # Calculate width of title and position

        self.image("logo.jpg", x=None, y=None, w=0, h=0, type='', link='')
        w = self.get_string_width("bilan d'absence") + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_text_color(0,0,0)
        self.set_fill_color(255,255,255)
        # Thickness of frame (1 mm)
        # Title
        self.cell(w, 9, "Bilan d'absence", 0, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, str(datetime.now()), 0, 0, 'C')

    def info_line(self, label,value,extra=''):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(255, 255, 255)
        # Title
        self.cell(0, 6,label+value+extra , 0, 1, 'L', 1)
        # Line break
        self.ln(4)


    def print_line(self, label, value,extra=''):
        self.info_line(label, value,extra)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = MyApp()
    myApp.setFixedSize(1300, 743)
    myApp.setWindowIcon(QIcon('logo.ico'))
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        myApp.connection.close()
