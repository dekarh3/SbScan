from window import Ui_Form
from datetime import datetime
from mysql.connector import MySQLConnection, Error
from libScan import read_config
from PyQt5.QtCore import QDate, QDateTime, QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from libScan import read_config


class MainWindowSlots(Ui_Form):   # Определяем функции, которые будем вызывать в слотах

    def setupUi(self, form):
        Ui_Form.setupUi(self,form)
        dbconfig = read_config(section='mysql')
        self.dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
        self.read_cursor = self.dbconn.cursor()
        self.write_cursor = self.dbconn.cursor()
        self.histories = {}
        self.descriptions = {}
        self.okwed_lists = []
        self.tableFirms_inns = []
        self.GISids = []
        self.GISaddreses = []
        self.GISabouts = []
        self.setup_tableFIOmain()
        self.innFIO = self.tableFIOmain.model().index(0, 0).data()
        self.last_innFIO = self.tableFIOmain.model().index(0, 0).data()
        self.setup_tableFirms()
        self.inn = self.tableFirms_inns[0]
        self.last_inn = self.tableFirms_inns[0]
        return

    def setup_tableFIOmain(self):
        self.read_cursor.execute('SELECT f.inn_fio, f.family, f.`name`, f.surname, FORMAT((select sum(q.summ) '
                            'FROM main2fio AS q WHERE f.inn_fio = q.fio_inn_fio),0),'
                            'FORMAT((select sum(q.cost) FROM main2fio AS q WHERE f.inn_fio = q.fio_inn_fio),0), '
                            'f.history FROM fio AS f WHERE ROUND(f.inn_fio/10000000000)=30 '
                            'AND (select sum(q.summ) FROM main2fio AS q WHERE f.inn_fio = q.fio_inn_fio)>10000000 '
                            'ORDER BY (select sum(q.summ) FROM main2fio AS q WHERE f.inn_fio = q.fio_inn_fio) DESC;')
        rows = self.read_cursor.fetchall()
        self.tableFIOmain.setColumnCount(6)             # Устанавливаем кол-во колонок
        self.tableFIOmain.setRowCount(len(rows))        # Кол-во строк из таблицы
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if j == len(row) - 1:
                    self.histories[row[0]] = cell
                else:
                    self.tableFIOmain.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableFIOmain.setHorizontalHeaderLabels(["ИНН", "Фамилия", "Имя", "Отчество", "Прибыль", "Стоимость"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.tableFIOmain.horizontalHeaderItem(0).setToolTip("ИНН")
        self.tableFIOmain.horizontalHeaderItem(1).setToolTip("Фамилия")
        self.tableFIOmain.horizontalHeaderItem(2).setToolTip("Имя")
        self.tableFIOmain.horizontalHeaderItem(3).setToolTip("Отчество")
        self.tableFIOmain.horizontalHeaderItem(4).setToolTip("Прибыль")
        self.tableFIOmain.horizontalHeaderItem(5).setToolTip("Стоимость")

        # Устанавливаем выравнивание на заголовки
        self.tableFIOmain.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.tableFIOmain.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.tableFIOmain.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        self.tableFIOmain.horizontalHeaderItem(3).setTextAlignment(Qt.AlignCenter)
        self.tableFIOmain.horizontalHeaderItem(4).setTextAlignment(Qt.AlignCenter)
        self.tableFIOmain.horizontalHeaderItem(5).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFIOmain.resizeColumnsToContents()
        return

    def click_tableFIOmain(self, index):
        self.innFIO = self.tableFIOmain.model().index(index.row(), 0).data()
        self.updateHistory()
        self.inn = self.tableFirms_inns[0]
        self.updateDescription()
        self.setup_tableFirms()
        self.click_tableFirms()
        self.click_table2GIS()
        g = 0

        #        self.label_4.setText('Сумма должна быть больше 0')
        #        return None

        return None

    def updateHistory(self):
        current = self.textHistory.toPlainText()
        if self.histories[int(self.last_innFIO)] == None:
            past = ''
        else:
            past = self.histories[int(self.last_innFIO)]
        if current != past:
            self.write_cursor.execute('UPDATE fio SET history = %s WHERE inn_fio = %s', (current, self.last_innFIO))
            self.dbconn.commit()
            self.histories[int(self.last_innFIO)] = current
        self.last_innFIO = self.innFIO
        self.textHistory.setText(self.histories[int(self.innFIO)])

    def setup_tableFirms(self):
        self.read_cursor.execute("SELECT IF(LEFT(UCASE(m.firm_full_name),8) = 'ОБЩЕСТВО', "
                "REPLACE(SUBSTR(UCASE(m.firm_full_name),42),'\"',' '), UCASE(m.firm_full_name)) AS `OOO`,"
                " m.predstav, m.address, m.phone_1, m.phone_2, m.phone_3, m.phone_4, m.phone_5, FORMAT(q.summ,0),"
                "FORMAT(q.cost,0), m.inn, m.act_list, m.description "
                "FROM main2fio AS q LEFT JOIN main AS m ON m.inn = q.main_inn WHERE q.fio_inn_fio = %s", (self.innFIO,))
        rows = self.read_cursor.fetchall()
        self.tableFirms.setColumnCount(10)               # Устанавливаем кол-во колонок
        self.tableFirms.setRowCount(len(rows))          # Кол-во строк из таблицы
        self.okwed_lists = []
        self.tableFirms_inns = []
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if j == len(row) - 3:
                    self.tableFirms_inns.append(cell)
                if j == len(row) - 2:
                    self.okwed_lists.append(str(cell))
                elif j == len(row) - 1:
                    self.descriptions[self.tableFirms_inns[i]] = cell
                else:
                    if cell == None:
                        self.tableFirms.setItem(i, j, QTableWidgetItem(''))
                    else:
                        self.tableFirms.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableFirms.setHorizontalHeaderLabels(['ООО', 'Представитель', 'Адрес', '', '', '',
                                                     '', '', 'Сумма', 'Стоимость'])

        # Устанавливаем выравнивание на заголовки
        for i in range(8):
            self.tableFirms.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFirms.resizeColumnsToContents()

        return

    def updateDescription(self):
        current = self.textDescription.toPlainText()
        if self.descriptions[int(self.last_inn)] == None:
            past = ''
        else:
            past = self.descriptions[int(self.last_inn)]
        if current != past:
            self.write_cursor.execute('UPDATE main SET description = %s WHERE inn = %s', (current, self.last_inn))
            self.dbconn.commit()
            self.descriptions[int(self.last_inn)] = current
        self.last_inn = self.inn
        self.textDescription.setText(self.descriptions[int(self.inn)])


    def click_tableFirms(self, index=None):
        if index == None:
            index = self.tableFirms.model().index(0, 0)
        self.setup_tableOKWED(self.okwed_lists[index.row()])
        self.setup_table2GIS(self.tableFirms_inns[index.row()])
        self.click_table2GIS()
        self.setup_tableFIO(self.tableFirms_inns[index.row()])
        self.updateHistory()
        self.inn = self.tableFirms_inns[index.row()]
        self.updateDescription()
        g = 0

    def setup_tableOKWED(self, okwed_list):
        okwed_list_with_or = ''
        okwed_list_t = ()
        for i, okwed in enumerate(okwed_list.strip().split(' ')):
            okwed_list_t += (okwed, )
            if i == len(okwed_list.strip().split()) - 1:
                okwed_list_with_or += ' okwed = %s'
            else:
                okwed_list_with_or += ' okwed = %s OR '
        self.read_cursor.execute("SELECT  okwed, about FROM okwed WHERE" + okwed_list_with_or, okwed_list_t)
        rows = self.read_cursor.fetchall()
        self.tableOKWED.setColumnCount(2)  # Устанавливаем кол-во колонок
        self.tableOKWED.setRowCount(len(rows))  # Кол-во строк из таблицы
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.tableOKWED.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableOKWED.setHorizontalHeaderLabels(['Код', 'Значение'])

        # Устанавливаем выравнивание на заголовки
        for i in range(2):
            self.tableOKWED.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableOKWED.resizeColumnsToContents()

        return

    def setup_table2GIS(self, inn):
        self.tableFirm2gis.setColumnCount(0)
        self.tableFirm2gis.setRowCount(0)
        self.read_cursor.execute("SELECT g.word, t.full_name, t.id, t.address, t.opisan FROM main2gis AS g "
                                 "LEFT JOIN two_gis AS t ON g.id_from_gis=t.id "
                                 "LEFT JOIN main AS m ON g.main_inn=m.inn WHERE m.inn = %s", (inn,))
        rows = self.read_cursor.fetchall()
        self.tableFirm2gis.setColumnCount(2)               # Устанавливаем кол-во колонок
        self.tableFirm2gis.setRowCount(len(rows))          # Кол-во строк из таблицы
        self.GISids = []
        self.GISabouts = []
        self.GISaddreses = []
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if j == len(row) - 3:
                    self.GISids.append(str(cell))
                if j == len(row) - 2:
                    self.GISaddreses.append(str(cell))
                elif j == len(row) - 1:
                    self.GISabouts.append(str(cell))
                else:
                    self.tableFirm2gis.setItem(i, j, QTableWidgetItem(str(cell)))


        # Устанавливаем заголовки таблицы
        self.tableFirm2gis.setHorizontalHeaderLabels(['Слово', 'Компания'])

        # Устанавливаем выравнивание на заголовки
        for i in range(2):
            self.tableFirm2gis.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFirm2gis.resizeColumnsToContents()

        return

    def click_table2GIS(self, index=None):
        if index == None:
            index = self.tableFirm2gis.model().index(0, 0)
        self.setup_tableContacts2gis(index.row())
#        self.updateHistory()
#        self.updateDescription()


    def setup_tableContacts2gis(self, row_number):
        self.label_desc.clear()
        self.tableContacts2gis.setColumnCount(0)
        self.tableContacts2gis.setRowCount(0)
        if len(self.GISids) > 0:
            self.read_cursor.execute('SELECT `type`, contact FROM contacts WHERE id_from_gis = %s',
                                     (int(self.GISids[row_number]),))
            rows = self.read_cursor.fetchall()
            self.tableContacts2gis.setColumnCount(2)             # Устанавливаем кол-во колонок
            self.tableContacts2gis.setRowCount(len(rows))        # Кол-во строк из таблицы
            for i, row in enumerate(rows):
                for j, cell in enumerate(row):
                    self.tableContacts2gis.setItem(i, j, QTableWidgetItem(str(cell)))

            # Устанавливаем заголовки таблицы
            self.tableContacts2gis.setHorizontalHeaderLabels(["Тип", "Контакт"])

            # Устанавливаем выравнивание на заголовки
            self.tableContacts2gis.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
            self.tableContacts2gis.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)

            # делаем ресайз колонок по содержимому
            self.tableContacts2gis.resizeColumnsToContents()
            next_string = False
            addr = ''
            for i, char in enumerate(self.GISaddreses[row_number]):
                if i % 40 == 0 and i != 0:
                    next_string = True
                if next_string and char == ' ':
                    addr += char + '<br />'
                    next_string = False
                else:
                    addr += char
            self.label_desc.setText('<b>' + addr + '</b> <br />' + self.GISabouts[row_number])
        return

    def setup_tableFIO(self, inn):
        self.tableFIO.setColumnCount(0)
        self.tableFIO.setRowCount(0)
        self.read_cursor.execute('SELECT family, `name`, surname FROM main2fio AS q LEFT JOIN fio AS f '
                                 'ON q.fio_inn_fio = f.inn_fio WHERE q.main_inn = %s ORDER BY family', (inn,))
        rows = self.read_cursor.fetchall()
        self.tableFIO.setColumnCount(3)             # Устанавливаем кол-во колонок
        self.tableFIO.setRowCount(len(rows))        # Кол-во строк из таблицы
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.tableFIO.setItem(i, j, QTableWidgetItem(str(cell)))

        # Устанавливаем заголовки таблицы
        self.tableFIO.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество"])

        # Устанавливаем выравнивание на заголовки
        self.tableFIO.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.tableFIO.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)

        # делаем ресайз колонок по содержимому
        self.tableFIO.resizeColumnsToContents()

        return


