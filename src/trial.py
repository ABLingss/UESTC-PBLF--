import ctypes
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

# 加载 DLL
insert_and_delete_flights_dll = ctypes.CDLL('./insert_and_delete.dll')

# 定义 insert 函数的参数类型和返回类型
insert_and_delete_flights_dll.insert.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int
]
insert_and_delete_flights_dll.insert.restype = ctypes.c_int

# 定义 delete 函数的参数类型和返回类型
insert_and_delete_flights_dll.delete.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
insert_and_delete_flights_dll.delete.restype = ctypes.c_int

class FlightsManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.back_to_main)
        self.pushButton.clicked.connect(self.insert_flight)
        self.pushButton_2.clicked.connect(self.delete_flight)
        self.update_table()

    def back_to_main(self):
        self.close()

    def insert_flight(self):
        # 获取用户输入的数据
        flight_id = self.lineEdit.text()
        departure_time = self.lineEdit_2.text()
        arrival_time = self.lineEdit_3.text()
        start = self.lineEdit_4.text()
        destination = self.lineEdit_5.text()
        company = self.lineEdit_6.text()

        # 获取价格和座位数
        try:
            price = int(self.lineEdit_7.text())  # 假设有一个价格输入框
            total_seats = int(self.lineEdit_8.text())  # 假设有一个座位输入框
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "输入错误", "价格和座位数应为整数!")
            return

        # 调用 C 函数来插入航班数据
        result = insert_and_delete_flights_dll.insert(
            flight_id.encode('utf-8'),
            departure_time.encode('utf-8'),
            arrival_time.encode('utf-8'),
            start.encode('utf-8'),
            destination.encode('utf-8'),
            company.encode('utf-8'),
            price,
            total_seats
        )

        if result == 1:
            QtWidgets.QMessageBox.information(self, "插入成功", "航班插入成功!")
        else:
            QtWidgets.QMessageBox.warning(self, "插入失败", "航班插入失败，请检查输入数据!")

        self.update_table()  # 插入航班后更新表格

    def delete_flight(self):
        # 获取用户输入的航班ID和出发时间
        flight_id = self.lineEdit_2.text()  # 这里假设您用 `lineEdit_2` 输入航班ID
        departure_time = self.lineEdit_3.text()  # 这里假设您用 `lineEdit_3` 输入出发时间

        if not flight_id or not departure_time:
            QtWidgets.QMessageBox.warning(self, "输入错误", "请填写完整的航班ID和出发时间!")
            return

        # 调用 C 函数来删除航班数据
        result = insert_and_delete_flights_dll.delete(
            departure_time.encode('utf-8'),
            flight_id.encode('utf-8')
        )

        if result == 1:
            QtWidgets.QMessageBox.information(self, "删除成功", "航班删除成功!")
        else:
            QtWidgets.QMessageBox.warning(self, "删除失败", "航班删除失败，请检查输入数据!")

        self.update_table()  # 删除航班后更新表格

    def update_table(self):
        # 更新表格的逻辑
        self.searchreasult.clearContents()  # 清空表格内容
        self.searchreasult.setRowCount(0)  # 重置行数

        # 遍历链表，显示航班信息
        temp = insert_and_delete_flights_dll.head
        while temp:
            row_position = self.searchreasult.rowCount()
            self.searchreasult.insertRow(row_position)

            # 将航班数据填充到表格
            self.searchreasult.setItem(row_position, 0, QTableWidgetItem(temp.flight_id.decode('utf-8')))
            self.searchreasult.setItem(row_position, 1, QTableWidgetItem(temp.departure_time.decode('utf-8')))
            self.searchreasult.setItem(row_position, 2, QTableWidgetItem(temp.arrival_time.decode('utf-8')))
            self.searchreasult.setItem(row_position, 3, QTableWidgetItem(str(temp.price)))
            self.searchreasult.setItem(row_position, 4, QTableWidgetItem(str(temp.total_seats)))

            temp = temp.next

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FlightsManagerWindow()
    window.show()
    sys.exit(app.exec_())

