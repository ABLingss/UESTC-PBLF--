import sys
import ctypes
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from ctypes import POINTER, c_ubyte, cast, c_char_p, c_int

from PyQt5.QtWidgets import QTableWidgetItem

from login import Ui_MainWindow as LoginUi
from main import Ui_MainInterface as MainUi
from flight_recommendation import Ui_FlightRecommendationWindow
from flight_details import Ui_FlightDetailsWindow
from sort_flights import Ui_FlightSortWindow
from comment import Ui_CommentManagementWindow
from order_management import Ui_OrderManagementWindow
from order_details import Ui_OrderDetailsWindow
from main_manager import Ui_MainInterface as MainManagerUi
from manager import Ui_AdminDashboardWindow as AdminUi
from profile import Ui_ProfileManagementWindow
from Profile_manager import Ui_ProfileManagementWindow as ProfileManagerUi
from query_flights import Ui_FlightSearchWindow as QueryFlightSearchWindow
from scroll_of_about import ScrollingTextWindow
from Order_manager import Ui_OrderEditWindow as OrderEditWindow
from flight_manager import Ui_admin_privileges as FlightsManagerWindow
import CrawlerFlightsAdvancedAdvanced
# 爬虫实时更新

admin_hash_password = '17be601bf8b908059f8d63bc0231baf9f27ce43be277061169e19c58d00609ab'
# 密码：NaiLongDaWang520

# 加载dll
passenger_lib = ctypes.CDLL('./passenger.dll')
RSA_dll = ctypes.CDLL('./RSA.dll')
insert_and_delete_flights_dll = ctypes.CDLL('./insert_and_delete.dll')
flight_lib = ctypes.CDLL('./search_flights.dll')
flight_management = ctypes.CDLL('./orderchange.dll')
manager_lib = ctypes.CDLL('./manager.dll')
manager_order_lib = ctypes.CDLL('./manager_order.dll')
manager_order_delete = ctypes.CDLL('./manager_order_delete.dll')

# 结构体
class Flight(ctypes.Structure):
    _fields_ = [
        ("flight_id", ctypes.c_char * 200),
        ("departure_time", ctypes.c_char * 200),
        ("arrival_time", ctypes.c_char * 200),
        ("start", ctypes.c_char * 200),
        ("destination", ctypes.c_char * 200),
        ("company", ctypes.c_char * 200),
        ("price", ctypes.c_int),
        ("total_seats", ctypes.c_int),
        ("seat_number", ctypes.c_int),
        ("next", ctypes.POINTER(ctypes.POINTER('Flight')))  # 递归引用，表示指向同类型结构体的指针
    ]
class Order(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 20),  # char name[20]
        ("flight", ctypes.POINTER(Flight))  # struct flight* flight (pointer to Flight)
    ]
class Passenger(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char_p),
        ("password", ctypes.c_char_p),
        ("phone", ctypes.c_char_p),
        ("id", ctypes.c_char_p),
        ("mail", ctypes.c_char_p),
        ("next", ctypes.POINTER(ctypes.POINTER('Passenger'))
        )
    ]
# 存储c结构体
class SHA256_CTX(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_ubyte * 64),
        ("datalen", ctypes.c_uint),
        ("bitlen", ctypes.c_ulonglong),
        ("state", ctypes.c_uint * 8)
    ]

#注册
passenger_lib.regis.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
passenger_lib.regis.restype = ctypes.c_char_p

#登录
passenger_lib.login.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
passenger_lib.login.restype = ctypes.c_char_p

#改变个人信息
passenger_lib.change.argtypes = [ctypes.c_int, ctypes.c_char_p]
passenger_lib.change.restype = ctypes.c_int

# hash加密算法
RSA_dll.sha256_init.argtypes = [ctypes.POINTER(SHA256_CTX)]
RSA_dll.sha256_update.argtypes = [ctypes.POINTER(SHA256_CTX), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t]
RSA_dll.sha256_final.argtypes = [ctypes.POINTER(SHA256_CTX), ctypes.POINTER(ctypes.c_ubyte * 32)]  # SHA256_BLOCK_SIZE

# 插入航班
insert_and_delete_flights_dll.insert.restype = ctypes.c_int
insert_and_delete_flights_dll.insert.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_char_p, ctypes.c_int, ctypes.c_int
]

# 删除航班
insert_and_delete_flights_dll.delete.argtypes = [c_char_p, c_char_p]  # delete 函数有两个字符串参数
insert_and_delete_flights_dll.delete.restype = c_int

# 搜索航班
flight_lib.search_direct.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
flight_lib.search_direct.restype = None

flight_lib.search_transfer.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
flight_lib.search_transfer.restype = None

# 订单修改
flight_management.order_change.argtypes = [c_char_p, c_char_p, c_int, c_int]
flight_management.order_change.restype = c_int

flight_management.print.argtypes = [c_int]
flight_management.print.restype = None

class LoginWindow(QtWidgets.QMainWindow, LoginUi, QTimer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)
        self.cancelButton.clicked.connect(self.cancel)
        self.registerButton.clicked.connect(self.register)
        self.QTimer = QTimer()

    def login(self):
        name = self.usernameLogin.text()
        password = self.passwordLogin.text()

        if name == '' or password == '':
            self.log_wrong.setText("用户名/密码不能为空")
            self.log_wrong.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_log_wrong_close)
        else:
            # 加密密码
            data = str(password).encode('utf-8')
            # print(data)

            # 创建一个 ctypes 数组来存储数据
            data_array = (ctypes.c_ubyte * len(data))(*data)
            # print(data_array)

            # 创建一个上下文 ctx 用于 SHA256
            ctx = SHA256_CTX()  # 创建一个 SHA256_CTX 结构体实例
            RSA_dll.sha256_init(ctypes.byref(ctx))  # 初始化 SHA256
            # print(RSA_dll.sha256_init(ctx))


            # 更新 SHA256 上下文
            RSA_dll.sha256_update(ctypes.byref(ctx), cast(data_array, POINTER(ctypes.c_ubyte)), len(data))

            # 获取最终的 hash 输出
            hash_output = (ctypes.c_ubyte * 32)()  # SHA256 output is 32 bytes
            RSA_dll.sha256_final(ctypes.byref(ctx), hash_output)

            # 转换为十六进制字符串
            hash_password = ''.join(f'{byte:02x}' for byte in hash_output)


            # 管理员登录
            if name == 'admin' and hash_password == admin_hash_password:
                self.main_manager_window = MainManagerWindow()
                self.main_manager_window.show()
                self.close()

            # 调用 C 语言的 login 函数进行登录验证
            result = passenger_lib.login(name.encode('utf-8'), hash_password.encode('utf-8'))
            result_str = result.decode('utf-8')
            # 根据返回结果判断是否登录成功
            if result_str == 'yes':
                self.main_window = MainInterface()
                self.main_window.show()
                self.close()
            else:
                self.log_wrong.setText("用户名/密码错误")
                self.log_wrong.setStyleSheet("color: red")
                self.QTimer.singleShot(2000, self.make_log_wrong_close)

    def make_log_wrong_close(self):
        self.log_wrong.setText(" ")



    def cancel(self):
        self.close()

    def register(self):
        # 获取用户输入的注册信息
        name = self.usernameRegister.text()
        password = self.passwordRegister.text()
        phone = self.phoneRegister.text()
        id = self.lineEdit_2.text()
        mail = self.emailRegister.text()

        if name == '' :
            self.r_no_name.setText(" 用户名不能为空")
            self.r_no_name.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_name_close)
        elif password == '' :
            self.r_no_password.setText(" 密码不能为空")
            self.r_no_password.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_password_close)
        elif phone == '':
            self.no_available_phone.setText(" 手机号不能为空")
            self.no_available_phone.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_phone_close)
        elif id == '':
            self.no_available_ID.setText(" 身份证号不能为空")
            self.no_available_ID.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_id_close)
        elif mail == '':
            self.no_avaliable_email.setText(" 邮箱不能为空")
            self.no_avaliable_email.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_email_close)
        else:
            # 加密密码
            data = str(password).encode('utf-8')
            # print(data)

            # 创建一个 ctypes 数组来存储数据
            data_array = (ctypes.c_ubyte * len(data))(*data)
            # print(data_array)

            # 创建一个上下文 ctx 用于 SHA256
            ctx = SHA256_CTX()  # 创建一个 SHA256_CTX 结构体实例
            RSA_dll.sha256_init(ctypes.byref(ctx))  # 初始化 SHA256
            # print(RSA_dll.sha256_init(ctx))


            # 更新 SHA256 上下文
            RSA_dll.sha256_update(ctypes.byref(ctx), cast(data_array, POINTER(ctypes.c_ubyte)), len(data))

            # 获取最终的 hash 输出
            hash_output = (ctypes.c_ubyte * 32)()  # SHA256 output is 32 bytes
            RSA_dll.sha256_final(ctypes.byref(ctx), hash_output)

            # 转换为十六进制字符串
            hash_password = ''.join(f'{byte:02x}' for byte in hash_output)

            # 调用 C 语言的 regis 函数进行注册
            result = passenger_lib.regis(name.encode('utf-8'), hash_password.encode('utf-8'), phone.encode('utf-8'),
                                         id.encode('utf-8'), mail.encode('utf-8'))

            # 解码字节串为字符串
            result_str = result.decode('utf-8')

            if name == 'admin':
                self.no_avaliable_email.setText(" 禁止注册管理员账号")
                self.no_avaliable_email.setStyleSheet("color: red")
                self.QTimer.singleShot(2000, self.make_email_close)
            # 根据返回结果判断是否注册成功
            if result_str == 'yes':
                self.main_window = MainInterface()
                self.main_window.show()
                self.close()
            else:
                if result_str == 'name used':
                    self.r_no_name.setText("用户名已存在")
                    self.r_no_name.setStyleSheet("color: red")
                    self.QTimer.singleShot(2000, self.make_name_close)
                elif phone == '':
                    self.no_available_phone.setText(" 手机号不能为空")
                    self.no_available_phone.setStyleSheet("color: red")
                    self.QTimer.singleShot(2000, self.make_phone_close)
                elif result_str == 'id used':
                    self.no_available_ID.setText(" 身份证号已存在")
                    self.no_available_ID.setStyleSheet("color: red")
                    self.QTimer.singleShot(2000, self.make_id_close)
                elif result_str == 'mail used':
                    self.no_avaliable_email.setText("邮箱已存在")
                    self.no_avaliable_email.setStyleSheet("color: red")
                    self.QTimer.singleShot(2000, self.make_email_close)

    def make_name_close(self):
        self.r_no_name.setText(" ")
    def make_password_close(self):
        self.r_no_password.setText(" ")
    def make_phone_close(self):
        self.no_available_phone.setText(" ")
    def make_id_close(self):
        self.no_available_ID.setText(" ")
    def make_email_close(self):
        self.no_avaliable_email.setText(" ")

class MainInterface(QtWidgets.QMainWindow, MainUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 按钮与函数连接
        self.flightRecommendationButton.clicked.connect(self.open_flight_recommendation)
        self.flightSearchButton.clicked.connect(self.open_flight_search)
        self.flightSortButton.clicked.connect(self.open_flight_sort)
        self.profileManagementButton.clicked.connect(self.open_profile_management)
        self.logout.clicked.connect(self.logout_user)
        self.about.clicked.connect(self.aboutus)
        self.commentManagementButton.clicked.connect(self.comment_management)
        self.games.clicked.connect(self.open_games)

    def open_flight_recommendation(self):
        self.flight_recommendation_window = FlightRecommendationWindow()
        self.flight_recommendation_window.show()

    def open_flight_search(self):
        self.flight_search_window = FlightSearchWindow()
        self.flight_search_window.show()

    def open_flight_sort(self):
        self.flight_sort_window = FlightSortWindow()
        self.flight_sort_window.show()


    def open_profile_management(self):
        self.profile_management_window = ProfileManagementWindow()
        self.profile_management_window.show()
    #     这么写的原因是，因为这个类继承自两个父类，所以需要用super()函数来调用父类的方法。
    #     这样可以保证每个类都能调用父类的方法，而不会因为类名冲突而导致调用错误的方法。

    def logout_user(self):
        self.close()
        # 退出登录
        self.back_to_login = LoginWindow()
        self.back_to_login.show()

    def aboutus(self):
        # 打开关于我们的窗口 我们采用了一个滚动条进行简单表示，后期可以整花活
        self.about_window = AboutWindow()
        self.about_window.show()

    def comment_management(self):
        # 打开评论管理窗口
        self.comment_management_window = commentManagementWindow()
        self.comment_management_window.show()

    def open_games(self):
        # 打开航班详情窗口
        self.games_window = GamesWindow()
        self.games_window.show()

# class GamesWindow(QtWidgets.QMainWindow,):
# TODO 杨潇实现 俄罗斯方块的界面

class FlightRecommendationWindow(QtWidgets.QMainWindow, Ui_FlightRecommendationWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.findFlightsButton.clicked.connect(self.find_flights)

    def find_flights(self):
        # 假设这里是查找航班的逻辑
        print("查找航班按钮被点击")
        # 显示航班推荐结果
        self.resultsTextBrowser.setText("推荐航班：\n航班1\n航班2\n航班3")

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime

class FlightSortWindow(QtWidgets.QMainWindow, Ui_FlightSortWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化航班数据
        self.flights = [
            {'flight_number': 'CA123', 'departure_city': '北京', 'destination': '上海', 'departure_time': '2024-12-22 14:00', 'available_seats': 20, 'price': 500},
            {'flight_number': 'AA456', 'departure_city': '北京', 'destination': '广州', 'departure_time': '2024-12-22 09:00', 'available_seats': 50, 'price': 300},
            {'flight_number': 'UA789', 'departure_city': '上海', 'destination': '东京', 'departure_time': '2024-12-22 17:30', 'available_seats': 10, 'price': 800},
        ]

        # 连接排序按钮点击事件
        self.sortButton.clicked.connect(self.sort_flights)
        self.backToMainButton.clicked.connect(self.back_to_main)

    def sort_flights(self):
        # 获取排序条件（价格：0，时间：1）
        sort_criteria = self.sortCriteriaComboBox.currentIndex()

        # 根据不同的排序条件进行排序
        if sort_criteria == 0:  # 按价格排序
            self.flights.sort(key=lambda flight: flight['price'])
        elif sort_criteria == 1:  # 按时间排序
            self.flights.sort(key=lambda flight: datetime.strptime(flight['departure_time'], '%Y-%m-%d %H:%M'))

        # 更新表格显示排序后的航班数据
        self.update_flight_table()

    def back_to_main(self):
        self.close()

    def update_flight_table(self):
        # 清空现有表格内容
        self.sortedFlightTable.setRowCount(0)

        # 填充表格数据
        for flight in self.flights:
            row_position = self.sortedFlightTable.rowCount()
            self.sortedFlightTable.insertRow(row_position)
            self.sortedFlightTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight['flight_number']))
            self.sortedFlightTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight['departure_city']))
            self.sortedFlightTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight['destination']))
            self.sortedFlightTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight['departure_time']))
            self.sortedFlightTable.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(flight['available_seats'])))

class FlightSearchWindow(QtWidgets.QMainWindow, QueryFlightSearchWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButtonDir.clicked.connect(self.search_flights_Dir)
        self.backToMainButton.clicked.connect(self.back_to_main)
        self.searchButtonTran.clicked.connect(self.search_flights_Tran)

    def search_flights_Dir(self):
        # TODO 写好数据内容后回来改
        # 获取用户输入的出发地、目的地和时间
        start = self.lineEdit.text()  # 获取出发地
        destination = self.lineEdit_2.text()  # 获取目的地

        # 调用 C 函数查找直达航班
        self.flight_lib.search_direct(start.encode('utf-8'), destination.encode('utf-8'))

        # 获取查询结果
        result = ctypes.create_string_buffer(1024)  # 缓冲区接收 C 函数返回的字符串
        self.flight_lib.get_direct_flights(result)

        # 清空现有表格内容
        self.flightTable.setRowCount(0)

        # 解析查询结果并填充表格
        flight_data = result.value.decode('utf-8').split('\n')
        for i in range(0, len(flight_data), 4):
            if i + 3 < len(flight_data):
                row_position = self.flightTable.rowCount()
                self.flightTable.insertRow(row_position)
                self.flightTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight_data[i]))  # 航班号
                self.flightTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight_data[i + 1]))  # 出发地
                self.flightTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight_data[i + 2]))  # 目的地
                self.flightTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight_data[i + 3]))  # 出发时间

    def search_flights_Tran(self):

        # 获取用户输入的出发地和目的地
        start = self.lineEdit.text()  # 获取出发地
        destination = self.lineEdit_2.text()  # 获取目的地

        # 调用 C 函数查找中转航班
        self.flight_lib.search_transfer(start.encode('utf-8'), destination.encode('utf-8'))

        # 获取查询结果
        result = ctypes.create_string_buffer(1024)  # 缓冲区接收 C 函数返回的字符串
        self.flight_lib.get_transfer_flights(result)

        # 清空现有表格内容
        self.flightTable.setRowCount(0)

        # 解析查询结果并填充表格
        flight_data = result.value.decode('utf-8').split('\n')
        for i in range(0, len(flight_data), 4):
            if i + 3 < len(flight_data):
                row_position = self.flightTable.rowCount()
                self.flightTable.insertRow(row_position)
                self.flightTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight_data[i]))  # 航班号
                self.flightTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight_data[i + 1]))  # 出发地
                self.flightTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight_data[i + 2]))  # 目的地
                self.flightTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight_data[i + 3]))  # 出发时间

    def back_to_main(self):
        self.close()

class OrderManagementWindow(QtWidgets.QMainWindow, Ui_OrderManagementWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cancelOrderButton.clicked.connect(self.cancel_order)
        self.backToMainButton.clicked.connect(self.back_to_main)

        # 示例航班数据（假设是列表形式，每个元素是一个包含订单信息的列表）
        self.flights_data = [
            ['ORD123', '张三', 'MU5001', '2024-12-22 10:00', '2024-12-22 12:00', '北京-上海', '东方航空', '1000', '座位1A'],
            ['ORD124', '李四', 'CZ5010', '2024-12-22 14:00', '2024-12-22 16:00', '上海-广州', '南方航空', '1200', '座位2B']
        ]

        self.update_table()

    def cancel_order(self):
        """取消选中的订单"""
        # 获取当前选中的行
        selected_row = self.orderTable.currentRow()

        if selected_row >= 0:
            # 删除选中行的数据
            del self.flights_data[selected_row]

            # 更新表格显示
            self.update_table()

    def update_table(self):
        """更新表格显示"""
        # 更新表格的行数
        self.orderTable.setRowCount(len(self.flights_data))

        # 将更新后的数据填充到表格中
        for row, flight in enumerate(self.flights_data):
            for col, info in enumerate(flight):
                self.orderTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(info)))

    def back_to_main(self):
        """返回主界面"""
        self.close()



class ProfileManagementWindow(QtWidgets.QMainWindow, Ui_ProfileManagementWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 模拟一个用户信息字典
        self.user_info = {
            'username': 'TODO',
            'id_card': 'TODO',
            'email': 'TODO',
            'phone': 'TODO',
            'password': 'TODO'
        }

        self.update_profile()
        self.saveButton.clicked.connect(self.save_profile)
        self.backButton.clicked.connect(self.back_to_main)

    def save_profile(self):
        # 获取用户输入
        username = self.usernameLineEdit.text().strip()
        id_card = self.IDLineEdit.text().strip()
        email = self.emailLineEdit.text().strip()
        phone = self.phoneLineEdit.text().strip()
        password = self.passwordLineEdit.text().strip()

        # 更新字典中的信息
        if username:
            self.user_info['username'] = username
            self.currentUsernameLabel.setText(f"用户名：{username}")
        if id_card:
            self.user_info['id_card'] = id_card
            self.label.setText(f"身份证号：{id_card}")
        if email:
            self.user_info['email'] = email
            self.currentEmailLabel.setText(f"邮箱：{email}")
        if phone:
            self.user_info['phone'] = phone
            self.currentPhoneLabel.setText(f"手机号：{phone}")
        if password:
            self.user_info['password'] = password

        # 更新状态信息
        self.statusLabel.setText("个人资料更新成功")

    def update_profile(self):
        username = self.user_info['username']
        id_card = self.user_info['id_card']
        email = self.user_info['email']
        phone = self.user_info['phone']
        password = self.user_info['password']

        self.currentUsernameLabel.setText(f"用户名：{username}")
        self.label.setText(f"身份证号：{id_card}")
        self.currentEmailLabel.setText(f"邮箱：{email}")
        self.currentPhoneLabel.setText(f"手机号：{phone}")

    def back_to_main(self):
        self.close()

class AboutWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 ScrollingTextWindow 的实例
        self.scroll_window = ScrollingTextWindow()

        # 设置这个滚动文本窗口为 AboutWindow 的中央部件
        self.setCentralWidget(self.scroll_window)

        # 设置窗口标题
        self.setWindowTitle("关于我们")
        self.setGeometry(100, 100, 800, 600)

class commentManagementWindow(QtWidgets.QMainWindow, Ui_CommentManagementWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.submitCommentButton.clicked.connect(self.create_comment)
        self.backToMainButton.clicked.connect(self.back_to_main)

    def create_comment(self):
        # 创建评论的逻辑
        print("创建评论按钮被点击")
        self.commentStatusLabel.setText("评论已创建")

    def back_to_main(self):
        self.close()

class FlightDetailsWindow(QtWidgets.QMainWindow, Ui_FlightDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backToPreviousButton.clicked.connect(self.back_to_previous)
        self.pushButton.clicked.connect(self.order)
    def back_to_previous(self):
        self.close()

    def order(self):
        self.order_details_window = OrderDetailsWindow()
        self.order_details_window.show()

class OrderDetailsWindow(QtWidgets.QMainWindow, Ui_OrderDetailsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backToPreviousButton.clicked.connect(self.back_to_main)
    def back_to_main(self):
        self.close()

# class AdminWindow(QtWidgets.QMainWindow, AdminUi):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.editOrderButton.clicked.connect(self.edit_order)
#         self.editUserButton.clicked.connect(self.edit_user)
#         self.backToPreviousButton.clicked.connect(self.back_to_main)
#     def edit_order(self):
#         self.OrderEditWindow = OrderEditUI()
#         self.OrderEditWindow.show()
#
#     def edit_user(self):
#         # 修改用户的逻辑
#         self.ProfileManagementWindow = ProfileManagerUI()
#         self.ProfileManagementWindow.show()
#


    def back_to_main(self):
        self.close()

class ProfileManagerUI(QtWidgets.QMainWindow, ProfileManagerUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.back_to_main)
        self.saveButton.clicked.connect(self.save_user)

    def back_to_main(self):
        self.close()

    def save_user(self):
        print("已保存")
#         save的逻辑

class OrderEditUI(QtWidgets.QMainWindow, OrderEditWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.back_to_previous)
        self.saveOrderButton.clicked.connect(self.save_order)

    def back_to_previous(self):
        self.close()

    def save_order(self):
        print("已保存")
#         save的逻辑



class MainManagerWindow(QtWidgets.QMainWindow, MainManagerUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 按钮与函数连接
        self.orderchangebutton.clicked.connect(self.open_order_management)
        self.profileManagementButton.clicked.connect(self.open_profile_management)
        self.pushButton.clicked.connect(self.logout_user)
        self.InsertAndDeleteButton.clicked.connect(self.open_flights_manager)

    # def open_admin_dashboard(self):
    #     self.admin_dashboard_window = AdminWindow()
    #     self.admin_dashboard_window.show()
    # def open_flight_recommendation(self):
    #     self.flight_recommendation_window = FlightRecommendationWindow()
    #     self.flight_recommendation_window.show()
    # def open_flight_search(self):
    #     self.flight_search_window = FlightSearchWindow()
    #     self.flight_search_window.show()
    # def open_flight_sort(self):
    #     self.flight_sort_window = FlightSortWindow()
    #     self.flight_sort_window.show()
    # def open_order_management(self):
    #     self.order_management_window = OrderManagementWindow()
    #     self.order_management_window.show()
    def open_order_management(self):
        self.order_management_window = OrderManagementWindow()
        self.order_management_window.show()
    def open_flights_manager(self):
        self.flights_manager_window = FlightsManagerWindow()
        self.flights_manager_window.show()
    def open_profile_management(self):
        self.profile_management_window = ProfileManagementWindow()
        self.profile_management_window.show()
    #     这么写的原因是，因为这个类继承自两个父类，所以需要用super()函数来调用父类的方法。
    #     这样可以保证每个类都能调用父类的方法，而不会因为类名冲突而导致调用错误的方法。
    def logout_user(self):
        # 退出登录
        self.back_to_login = LoginWindow()
        self.back_to_login.show()
        self.close()
    # def aboutus(self):
    #     # 打开关于我们的窗口 我们采用了一个滚动条进行简单表示，后期可以整花活
    #     self.about_window = AboutWindow()
    #     self.about_window.show()
    # def comment_management(self):
    #     # 打开评论管理窗口
    #     self.comment_management_window = commentManagementWindow()
    #     self.comment_management_window.show()

    # def open_flights_manager(self):
    #     # 打开航班详情窗口
    #     self.flights_manager_window = FlightsManagerWindow()
    #     self.flights_manager_window.show()

class FlightsManagerWindow(QtWidgets.QMainWindow, FlightsManagerWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchreasult.resizeColumnsToContents()

        # 连接按钮事件
        self.pushButton_3.clicked.connect(self.back_to_main)
        self.pushButton.clicked.connect(self.insert_flight)
        self.pushButton_2.clicked.connect(self.delete_flight)
        self.pushButton_4.clicked.connect(self.update_table)

        # 初始化航班数据存储
        self.flights_data = []

    def back_to_main(self):
        """关闭当前窗口，返回到主窗口"""
        self.close()

    def insert_flight(self):
        """插入新航班信息"""
        flight_id = self.lineEdit.text()
        departure_time = self.lineEdit_2.text()
        start_point = self.lineEdit_4.text()
        arrival_time = self.lineEdit_3.text()
        airline = self.lineEdit_6.text()
        destination = self.lineEdit_5.text()

        # 航班信息存储在一个字典中 TODO 接入数据库
        new_flight = {
            "flight_id": flight_id,
            "departure_time": departure_time,
            "start_point": start_point,
            "arrival_time": arrival_time,
            "airline": airline,
            "destination": destination
        }

        # 将新航班添加到航班数据中
        self.flights_data.append(new_flight)

        # 清空输入框
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_4.clear()
        self.lineEdit_3.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

        # 更新表格显示
        self.update_table()

    def delete_flight(self):
        """删除选中的航班信息"""
        # 获取当前选中的行
        selected_row = self.searchreasult.currentRow()

        if selected_row >= 0:
            # 删除选中行的数据
            del self.flights_data[selected_row]

            # 更新表格显示
            self.update_table()

    def update_table(self):
        """更新表格中的数据"""
        # 清空现有的表格内容
        self.searchreasult.setRowCount(0)

        # 遍历航班数据，填充表格
        for flight in self.flights_data:
            row_position = self.searchreasult.rowCount()
            self.searchreasult.insertRow(row_position)
            self.searchreasult.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight["flight_id"]))
            self.searchreasult.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight["departure_time"]))
            self.searchreasult.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight["start_point"]))
            self.searchreasult.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight["arrival_time"]))
            self.searchreasult.setItem(row_position, 4, QtWidgets.QTableWidgetItem(flight["airline"]))

        # 刷新表格
        self.searchreasult.resizeColumnsToContents()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
