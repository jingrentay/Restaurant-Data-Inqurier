import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone3App.ui"  # Enter file here

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Milestone2(QMainWindow):
    def __init__(self):
        super(Milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.statistics)
        # self.ui.bname.textChanged.connect(self.getBusinessNames)
        # self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='durian123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM businessTable ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if self.ui.stateList.currentIndex() >= 0:
            sql_str = "SELECT distinct city FROM businessTable WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, city, state FROM businessTable WHERE state ='" + state + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

    def cityChanged(self):
        self.ui.zipcodeList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.selectedItems()[0].text()

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            sql_str = "SELECT distinct zipcode FROM businessTable WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY zipcode;"
            # print(sql_str)

            try:
                results = self.executeQuery(sql_str)
                # print(results)
                for row in results:
                    item = str(row[0])
                    # print(item)
                    self.ui.zipcodeList.addItem(item)
            except:
                print("Query failed!")

    def zipcodeChanged(self):
        self.ui.categoryList.clear()
        self.ui.businessTable.clear()
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()

        if len(self.ui.zipcodeList.selectedItems()) > 0:
            sql_str = "SELECT distinct c_name FROM category, businessTable WHERE zipcode = '" + zipcode + "' AND category.business_id = businessTable.business_id GROUP BY c_name;"

            try:
                results = self.executeQuery(sql_str)
                #print(results)

                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed!")

            sql_str2 = "SELECT name, address, city, stars, reviewcount, reviewrating, numcheckins FROM businessTable WHERE zipcode = '" + zipcode + "' ORDER BY name"
            #print(sql_str2)

            try:
                results2 = self.executeQuery(sql_str2)
                #print(results2)

                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results2[0]))
                self.ui.businessTable.setRowCount(len(results2))
                #self.ui.businessTable.setHorizontalHeaderLabels(("Business_name", "Address", "City", "Stars", "ReviewCount", "ReviewRating", "Number of CheckIns"))
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 150)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 50)
                self.ui.businessTable.setColumnWidth(4, 50)
                self.ui.businessTable.setColumnWidth(5, 50)
                self.ui.businessTable.setColumnWidth(6, 50)

                current_row = 0

                for row in results2:
                    for col_count in range(0, len(results2[0])):
                        self.ui.businessTable.setItem(current_row, col_count, QTableWidgetItem(str(row[col_count])))

                    current_row += 1

            except:
                print("Query failed!")

    def statistics(self):
        self.ui.topCategory.clear()
        self.ui.numBusiness.clear()
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()

        if len(self.ui.zipcodeList.selectedItems()) > 0:
            sql_str = "SELECT COUNT(*) FROM businessTable WHERE zipcode = '" + zipcode + "'"

            sql_str2 = "SELECT COUNT (*) as num_business, category FROM businessTable, category WHERE zipcode = '" + zipcode + "' AND category.business_id = businessTable.business_id ORDER BY name"
            #print(sql_str2)

        try:
            results = self.executeQuery(sql_str)

            self.ui.numBusiness.addItem(str(results[0][0]))

        except:
            print("Query failed!")

        try:
            results2 = self.executeQuery(sql_str2)
            print(results2)

            style = "::section {""background-color: #f3f3f3; }"
            self.ui.topCategory.horizontalHeader().setStyleSheet(style)
            self.ui.topCategory.setColumnCount(len(results2[0]))
            self.ui.topCategory.setRowCount(len(results2))
            self.ui.topCategory.setHorizontalHeaderLabels(["# of Businesses", "Category"])
            self.ui.topCategory.resizeColumnsToContents()
            self.ui.topCategory.setColumnWidth(0, 150)
            self.ui.topCategory.setColumnWidth(1, 400)

            current_row = 0

            for row in results2:
                for col_count in range(0, len(results2[0])):
                    self.ui.topCategory.setItem(current_row, col_count, QTableWidgetItem(str(row[col_count])))

                current_row += 1

        except:
            print("Query failed2!")

    # def getBusinessNames(self):
    #     self.ui.businesses.clear()
    #     businessname = self.ui.bname.text()
    #     sql_str = "SELECT name FROM businessTable WHERE name LIKE '%" + businessname + "%' ORDER BY name;"
    #     try:
    #         results = self.executeQuery(sql_str)
    #         for row in results:
    #             self.ui.businesses.addItem(row[0])
    #     except:
    #         print("Query failed!")
    #
    # def displayBusinessCity(self):
    #     businessname = self.ui.businesses.selectedItems()[0].text()
    #     sql_str = "SELECT city FROM businessTable WHERE name = '" + businessname + "';"
    #     try:
    #         results = self.executeQuery(sql_str)
    #         self.ui.bcity.setText(results[0][0])
    #     except:
    #         print("Query failed!")
    #
    # def displayZipcodeCity(self):
    #     businesscity = self.ui.businesses.selectedItems()[0].text()
    #     sql_str = "SELECT zipcode FROM businessTable WHERE city = '" + businesscity + "';"
    #     try:
    #         results = self.executeQuery(sql_str)
    #         self.ui.bzipcode.setText(results[0][0])
    #     except:
    #         print("Query failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone2()
    window.show()
    sys.exit(app.exec_())
