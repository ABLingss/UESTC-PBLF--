import sys
import csv
import ctypes
from datetime import datetime, timedelta
from collections import defaultdict

import pygame
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from ctypes import POINTER, c_ubyte, cast, c_char_p, c_int
import sqlite3

from PyQt5.QtWidgets import QTableWidgetItem

from login import Ui_MainWindow as LoginUi, Ui_MainWindow
from main import Ui_MainInterface as MainUi
from flight_recommendation import Ui_FlightRecommendationWindow
from flight_details import Ui_FlightDetailsWindow
from sort_flights import Ui_FlightSortWindow
from comment import Ui_CommentAddWindow
from commentmanagement import Ui_CommentManagementWindow
from order_management import Ui_OrderManagementWindow
from order_details import Ui_OrderDetailsWindow
from main_manager import Ui_MainInterface as MainManagerUi
from manager import Ui_AdminDashboardWindow as AdminUi
from profile import Ui_ProfileManagementWindow as ProfilemanagerControl
from Profile_manager import Ui_ProfileManagementWindow as ProfileManagerUi
from query_flights import Ui_FlightSearchWindow as QueryFlightSearchWindow
from scroll_of_about import ScrollingTextWindow
from Order_manager import Ui_OrderEditWindow as OrderEditWindow
from flight_manager import Ui_admin_privileges as FlightsManagerWindow
from smallgames import SmallGamesWindow

from PyQt5 import QtWidgets
from eluosi import EluosiWindow
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
FlightDetails = ctypes.CDLL('./flightDetails.dll')

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
        self.db = sql_connection()

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

            # 从数据库获取该用户名的存储密码
            conn = self.db._get_connection('passenger')
            cursor = conn.cursor()

            cursor.execute("SELECT password, phone, id_card, mail FROM passenger WHERE name = ?", (name,))
            row = cursor.fetchone()  # 获取查询结果
            conn.close()

            if row:
                stored_hash_password = row[0]  # 获取数据库中的密码哈希值
                if hash_password == stored_hash_password:
                    # 传递用户信息到 ProfileManagerUI
                    phone = row[1]
                    id_card = row[2]
                    mail = row[3]
                    # 在这里打开 MainInterface，并将用户信息传递给它
                    self.main_window = MainInterface(name, phone, id_card, mail)
                    self.main_window.show()
                    self.close()
                else:
                    self.log_wrong.setText("用户名/密码错误")
                    self.log_wrong.setStyleSheet("color: red")
                    self.QTimer.singleShot(2000, self.make_log_wrong_close)
            else:
                self.log_wrong.setText("用户名/密码错误")
                self.log_wrong.setStyleSheet("color: red")
                self.QTimer.singleShot(2000, self.make_log_wrong_close)

    def register(self):
        # 获取用户输入的注册信息
        name = self.usernameRegister.text()
        password = self.passwordRegister.text()
        phone = self.phoneRegister.text()
        id_card = self.lineEdit_2.text()
        mail = self.emailRegister.text()

        if name == '':
            self.r_no_name.setText(" 用户名不能为空")
            self.r_no_name.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_name_close)
        elif password == '':
            self.r_no_password.setText(" 密码不能为空")
            self.r_no_password.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_password_close)
        elif phone == '':
            self.no_available_phone.setText(" 手机号不能为空")
            self.no_available_phone.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_phone_close)
        elif id_card == '':
            self.no_available_ID.setText(" 身份证号不能为空")
            self.no_available_ID.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_id_close)
        elif mail == '':
            self.no_avaliable_email.setText(" 邮箱不能为空")
            self.no_avaliable_email.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_email_close)
        else:
            # 使用数据库检查是否已存在
            if self.db.check_passenger_exists(name=name):
                self.r_no_name.setText("用户名已存在")
                self.r_no_name.setStyleSheet("color: red")
                self.QTimer.singleShot(2000, self.make_name_close)
                return  # 如果用户名已存在，直接退出

            # 加密密码
            data = str(password).encode('utf-8')

            # 创建一个 ctypes 数组来存储数据
            data_array = (ctypes.c_ubyte * len(data))(*data)

            # 创建一个上下文 ctx 用于 SHA256
            ctx = SHA256_CTX()  # 创建一个 SHA256_CTX 结构体实例
            RSA_dll.sha256_init(ctypes.byref(ctx))  # 初始化 SHA256

            # 更新 SHA256 上下文
            RSA_dll.sha256_update(ctypes.byref(ctx), cast(data_array, POINTER(ctypes.c_ubyte)), len(data))

            # 获取最终的 hash 输出
            hash_output = (ctypes.c_ubyte * 32)()  # SHA256 output is 32 bytes
            RSA_dll.sha256_final(ctypes.byref(ctx), hash_output)

            # 转换为十六进制字符串
            hash_password = ''.join(f'{byte:02x}' for byte in hash_output)

            # 调用 C 语言的 regis 函数进行注册
            result = passenger_lib.regis(name.encode('utf-8'), hash_password.encode('utf-8'), phone.encode('utf-8'),
                                         id_card.encode('utf-8'), mail.encode('utf-8'))

            result_str = result.decode('utf-8')

            if name == 'admin':
                self.no_avaliable_email.setText(" 禁止注册管理员账号")
                self.no_avaliable_email.setStyleSheet("color: red")
                self.QTimer.singleShot(2000, self.make_email_close)

            # 根据返回结果判断是否注册成功
            if result_str == 'yes':
                self.db.insert_passenger(name, hash_password, phone, id_card, mail)
                self.main_window = MainInterface(name, phone, id_card, mail)
                self.main_window.show()
                self.close()
            else:
                if result_str == 'name used':
                    self.r_no_name.setText("用户名已存在")
                    self.r_no_name.setStyleSheet("color: red")
                    self.QTimer.singleShot(2000, self.make_name_close)
                elif result_str == 'phone used':
                    self.no_available_phone.setText(" 手机号已存在")
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

    def make_log_wrong_close(self):
        self.log_wrong.setText(" ")

    def _handle_existing_user(self, name, phone, id_card, mail):
        if self.db.check_passenger_exists(name=name):
            self.r_no_name.setText("用户名已存在")
            self.r_no_name.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_name_close)
        elif self.db.check_passenger_exists(phone=phone):
            self.no_available_phone.setText(" 手机号已存在")
            self.no_available_phone.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_phone_close)
        elif self.db.check_passenger_exists(id_card=id_card):
            self.no_available_ID.setText(" 身份证号已存在")
            self.no_available_ID.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_id_close)
        elif self.db.check_passenger_exists(mail=mail):
            self.no_avaliable_email.setText("邮箱已存在")
            self.no_avaliable_email.setStyleSheet("color: red")
            self.QTimer.singleShot(2000, self.make_email_close)


    def cancel(self):
        self.close()


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
    def __init__(self, name, phone, id_card, mail):
        super().__init__()
        self.setupUi(self)

        self.name = name
        self.phone = phone
        self.id_card = id_card
        self.mail = mail

        # 按钮与函数连接
        self.flightRecommendationButton.clicked.connect(self.open_flight_recommendation)
        self.flightSearchButton.clicked.connect(self.open_flight_search)
        self.flightSortButton.clicked.connect(self.open_flight_sort)
        self.profileManagementButton.clicked.connect(self.open_profile_management)
        self.logout.clicked.connect(self.logout_user)
        self.about.clicked.connect(self.aboutus)
        self.commentManagementButton.clicked.connect(self.comment_management)
        self.games.clicked.connect(self.open_small_games_window)

    def open_flight_recommendation(self):
        self.flight_recommendation_window = FlightRecommendationWindow(self.name)
        self.flight_recommendation_window.show()

    def open_flight_search(self):
        self.flight_search_window = FlightSearchWindow(self.name)
        self.flight_search_window.show()

    def open_flight_sort(self):
        self.flight_sort_window = FlightSortWindow(self.name)
        self.flight_sort_window.show()


    def open_profile_management(self):
        self.profile_management_window = ProfileManagementWindow(self.name, self.phone, self.id_card, self.mail)
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
        self.comment_management_window = commentManagementWindow(self.name)
        self.comment_management_window.show()

    def open_small_games_window(self):
        # 创建并显示 SmallGamesWindow 窗口
        self.small_games_window = SmallGamesWindow()
        self.small_games_window.show()  # 显示 SmallGamesWindow 窗口

# 这个是旧版的游戏界面实现 已经废弃
# class GamesWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("游戏窗口")
#         self.setGeometry(100, 100, 800, 600)
#
#         self.open_button = QtWidgets.QPushButton("打开俄罗斯方块", self)
#         self.open_button.clicked.connect(self.open_eluosi_window)
#
#     def open_eluosi_window(self):
#         # 创建并显示 EluosiWindow
#         self.eluosi_window = EluosiWindow()
#         self.eluosi_window.show()  # 显示俄罗斯方块窗口

# 把所有的c结构体和py字典变成数据库
class sql_connection:
    def __init__(self):
        # 定义不同数据类型对应的数据库文件
        self.db_files = {
            'flight': '../data/flights.db',
            'order': '../data/orders.db',
            'passenger': '../data/passengers.db',
            'comments': '../data/comments.db'
        }

    def _get_connection(self, db_type):
        """
        根据数据类型返回对应的数据库连接
        """
        try:
            if db_type not in self.db_files:
                raise ValueError(f"Unknown db type: {db_type}")

            db_file = self.db_files[db_type]
            connection = sqlite3.connect(db_file)
            return connection
        except sqlite3.Error as e:
            print(f"Error while connecting to {db_type}: {e}")
            raise  # 抛出异常或者可以返回 None

    def delete_flight(self, flight_id):
        conn = None
        try:
            conn = self._get_connection('flight')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Flight WHERE flight_id = ?", (flight_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def insert_comment(self, comments):
        # 获取连接到 comments.db
        conn = None
        try:
            conn = self._get_connection('comments')
            cursor = conn.cursor()

            # 假设 comments 是一个包含 name, company, 和 comment 的元组
            cursor.execute('''
                INSERT INTO comment (name, company, comment) VALUES (?, ?, ?)
            ''', comments)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def insert_flight(self, flight_id, departure_time, arrival_time, start, destination, company, price, total_seats,
                      seat_number):
        """
        插入航班数据
        """
        conn = None
        try:
            conn = self._get_connection('flight')
            cursor = conn.cursor()

            # 插入 Flight 数据
            cursor.execute(''' 
                INSERT INTO Flight (flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    # 此方法有未知bug 要插评论请直接复制下面注释中的代码到具体位置
    def insert_order(self, name, flight_id, departure_time, arrival_time, start, destination, company, price,
                     total_seats, seat_number):
        """
        插入订单数据
        """
        conn = None
        try:
            conn = self._get_connection('order')
            cursor = conn.cursor()

            # 插入 Order 数据
            cursor.execute('''
                INSERT INTO Order (name, flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, flight_id, departure_time, arrival_time, start, destination, company, price, total_seats,
                  seat_number))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    #                 try:
    #                     orders_connection = sqlite3.connect('../data/orders.db')  # 连接到 orders.db 数据库
    #                     orders_cursor = orders_connection.cursor()
    #
    #                     # 执行插入操作
    #                     orders_cursor.execute('''
    #                         INSERT INTO `Order` (name, flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number)
    #                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #                     ''', (self.name, self.flight_id, formatted_departure_time, formatted_arrival_time, start,
    #                           destination, company, price, total_seats, seat_number))
    #                     orders_connection.commit()
    def insert_passenger(self, name, password, phone, id, mail):
        # 获取连接到 passengers.db
        conn = None
        try:
            conn = self._get_connection('passenger')
            cursor = conn.cursor()

            # 插入 Passenger 数据
            cursor.execute('''
                INSERT INTO Passenger (name, password, phone, id_card, mail) VALUES (?, ?, ?, ?, ?)
            ''', (name, password, phone, id, mail))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def update_passenger(self, name, password, phone, id_card, mail):
        conn = None

        try:
            # 加密密码（仅当密码不为空时）
            hash_password = None
            if password:
                import hashlib
                hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # 动态生成更新 SQL 语句
            update_fields = []
            params = []

            if phone:
                update_fields.append("phone = ?")
                params.append(phone)
            if id_card:
                update_fields.append("id_card = ?")
                params.append(id_card)
            if mail:
                update_fields.append("mail = ?")
                params.append(mail)
            if hash_password:
                update_fields.append("password = ?")
                params.append(hash_password)

            if not update_fields:
                print("No fields to update.")
                return  # 如果没有字段需要更新，直接返回

            params.append(name)
            update_query = f"UPDATE Passenger SET {', '.join(update_fields)} WHERE name = ?"

            conn = self._get_connection('passenger')
            cursor = conn.cursor()
            cursor.execute(update_query, params)
            conn.commit()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def insert_comment(self, comments):
        # 获取连接到 comments.db
        conn = None
        try:
            conn = self._get_connection('comments')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO comment (name, company, comment) VALUES (?, ?, ?)
            ''', comments)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def check_passenger_exists(self, name=None):
        conn = None
        try:
            conn = self._get_connection('passenger')
            cursor = conn.cursor()

            # 检查是否传入了用户名，并构建查询语句
            if name:
                query = "SELECT * FROM Passenger WHERE name = ?"
                cursor.execute(query, (name,))
                result = cursor.fetchone()

                # 如果返回结果不为空，说明用户名已经存在
                return result is not None
            else:
                return False  # 如果没有提供用户名，直接返回 False

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False  # 出现错误时返回 False
        finally:
            if conn:
                conn.close()  # 关闭数据库连接

    def get_all_flights(self):
        conn = None
        try:
            conn = self._get_connection('flight')
            cursor = conn.cursor()

            # 查询所有航班数据
            cursor.execute('''SELECT flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number, connection FROM Flight''')
            flights = cursor.fetchall()

            return flights
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_flight_details(self, flight_id):
        """获取指定航班的详细信息"""
        conn = None
        try:
            conn = self._get_connection('flight')
            cursor = conn.cursor()

            cursor.execute("""
                SELECT flight_id, company, departure_time, arrival_time, price, start, destination, total_seats, seat_number, connection
                FROM Flight WHERE flight_id = ?
            """, (flight_id,))

            flight_details = cursor.fetchone()

            # 返回获取到的详细信息（包括航班号、航空公司、出发时间、到达时间、票价、出发城市、目的地等）
            if flight_details:
                return {
                    'flight_id': flight_details[0],
                    'company': flight_details[1],
                    'departure_time': flight_details[2],
                    'arrival_time': flight_details[3],
                    'price': flight_details[4],
                    'start': flight_details[5],
                    'destination': flight_details[6],
                    'total_seats': flight_details[7],
                    'seat_number': flight_details[8],
                    'connection': flight_details[9]
                }
            else:
                return None  # 如果没有找到该航班，则返回 None

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_all_passengers(self):
        """
        获取所有乘客信息。
        返回一个包含所有乘客资料的列表，每个元素是字典。
        """
        conn = None
        try:
            conn = self._get_connection('passenger')
            cursor = conn.cursor()
            cursor.execute("SELECT name, phone, id_card, mail FROM Passenger")
            results = cursor.fetchall()

            # 将查询结果转换为字典列表
            passengers = []
            for row in results:
                passengers.append({
                    'name': row[0],
                    'phone': row[1],
                    'id_card': row[2],
                    'mail': row[3]
                })

            return passengers
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def delete_passenger(self, username):
        """
        根据用户名删除乘客信息。
        """
        conn = None
        try:
            conn = self._get_connection('passenger')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Passenger WHERE name = ?", (username,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()


# 先通过系统时间判断现在是淡季还是旺季 寒暑假是旺季其他是淡季 旺季把目的地是旅游城市的航班优先 淡季把目的地不是旅游城市的航班优先
# 优先选择当前航班多的航空公司（证明这个航空公司受欢迎）
# 先同时进行直达和中转的查找
# 比较直达和中转的总价，如果中转的总价比直达的总价低，且中转的时间比直达的时间长的比例小于20%，优先推荐中转的
# 在table列出按这个规则排序的航班
class FlightRecommendationWindow(QtWidgets.QMainWindow, Ui_FlightRecommendationWindow):
    def __init__(self, name=None):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.db_connection = sql_connection()  # 创建数据库连接实例
        self.findFlightsButton.clicked.connect(self.find_flights)
        self.populate_airports()
        self.backToMainButton.clicked.connect(self.back_to_main)

        self.flightsTableWidgetDir.itemDoubleClicked.connect(self.open_flight_details)
        self.flightsTableWidgetCon.itemDoubleClicked.connect(self.open_flight_details1)

    def open_flight_details(self, item):
        # 获取当前双击的行号
        row = item.row()

        # 获取该行的航班数据
        flight_id = self.flightsTableWidgetDir.item(row, 0).text()  # 获取第一列（航班号）的文本

        # 创建航班详情页窗口并传递数据，包括name
        self.flight_details_window = FlightDetailsWindow(flight_id, self.name)
        self.flight_details_window.show()

    def open_flight_details1(self, item):
        # 获取当前双击的行号
        row = item.row()
        # 获取该行的航班数据
        flight_id = self.flightsTableWidgetCon.item(row, 0).text()  # 获取第一列（航班号）的文本
        # 创建航班详情页窗口并传递数据，包括name
        self.flight_details_window = FlightDetailsWindow(flight_id, self.name)
        self.flight_details_window.show()

    def get_all_flights(self):
        """
        获取所有航班数据
        """
        return self.db_connection.get_all_flights()

    def filter_seasonal_flights(self, flights, is_peak_season):
        """
        根据旺季/淡季筛选航班
        """
        tourist_cities = ['江北国际机场', '首都国际机场', '浦东国际机场', '虹桥国际机场', '萧山国际机场', '三清山机场',
                          '双流国际机场', '天府国际机场', '两江国际机场', '咸阳国际机场', '红原机场']

        # 判断当前时间是否为旺季（旺季为寒暑假月份）
        if is_peak_season:
            # 旺季优先显示旅游城市，其他城市也会显示，但旅游城市排前
            flights.sort(key=lambda x: x[4] in tourist_cities, reverse=True)
        else:
            # 淡季优先显示非旅游城市，其他城市也会显示，但非旅游城市排前
            flights.sort(key=lambda x: x[4] not in tourist_cities, reverse=True)

        return flights

    def rank_by_airline_popularity(self, flights):
        """
        按照航空公司受欢迎度进行排序
        """
        airline_counts = defaultdict(int)
        for flight in flights:
            airline_counts[flight[5]] += 1

        # 根据航空公司航班数量进行排序
        flights.sort(key=lambda x: airline_counts[x[1]], reverse=True)  # 根据航空公司排序
        return flights

    def compare_direct_and_connecting(self, flights):
        """
        比较直达与中转航班的价格和时长
        """

        def time_difference(departure_time, arrival_time):
            """
            计算时长差，假设时间格式为 'HH:MM'
            """
            # 如果时间是无效的（None 或空字符串），返回默认值（0）
            if not departure_time or not arrival_time or departure_time == '-' or arrival_time == '-':
                return 0  # 返回 0 分钟作为默认值

            try:
                # 如果时间是字符串或数字，先确保它们是有效的
                departure_time_str = str(departure_time).strip()
                arrival_time_str = str(arrival_time).strip()

                # 填充时间并转换为 datetime 对象
                departure = datetime.strptime(departure_time_str.zfill(4), "%H%M")
                arrival = datetime.strptime(arrival_time_str.zfill(4), "%H%M")

                # 如果到达时间在出发时间之前，说明跨过了午夜，增加一天
                if arrival < departure:
                    arrival += timedelta(days=1)

                # 计算时长差（单位：分钟）
                time_diff = (arrival - departure).total_seconds() / 60
                return time_diff
            except (ValueError, TypeError):
                # 如果转换失败（如无效时间格式），返回默认值
                return 0

        direct_flights = []
        connecting_flights = []

        for f in flights:
            connection = f[8]  # 连接字段（中转站）

            if connection is None or connection == "NULL":  # 直达航班
                direct_flights.append(f)
            else:  # 中转航班
                connecting_flights.append(f)

        # 排序直达航班和中转航班
        direct_flights.sort(key=lambda x: x[5])  # 根据票价排序
        connecting_flights.sort(key=lambda x: time_difference(x[6], x[7]))  # 根据时长排序

        # 合并直达航班和中转航班
        final_flights = []

        for flight in connecting_flights:
            # 获取中转站
            connection = flight[8]  # 连接字段，中转站
            total_price = flight[5]  # 中转航班的单一票价
            total_duration = time_difference(flight[6], flight[7])  # 假设航班的时间差

            final_flights.append({
                'segments': [flight[1], connection, flight[2]],  # 出发地 -> 中转地 -> 目的地
                'total_price': total_price,
                'total_duration': total_duration
            })

        return direct_flights + final_flights

    def recommend_flights(self):
        """
        推荐航班
        """
        # 获取所有航班数据
        flights = self.get_all_flights()

        # 获取当前月份并判断是否为旺季（假设旺季为寒暑假月份）
        current_month = datetime.now().month
        is_peak_season = current_month in [1, 2, 6, 7, 8, 12]

        # 根据季节筛选航班
        seasonal_flights = self.filter_seasonal_flights(flights, is_peak_season)

        # 排序：首先根据航空公司受欢迎度排序
        sorted_by_airline = self.rank_by_airline_popularity(seasonal_flights)

        # 比较直达与中转航班，选择性价比更高的航班
        final_recommended_flights = self.compare_direct_and_connecting(sorted_by_airline)

        return final_recommended_flights

    def populate_airports(self):
        """
        填充出发地和目的地下拉框 清空table
        """
        conn = None
        try:
            conn = self.db_connection._get_connection('flight')
            cursor = conn.cursor()

            # 查询所有机场名称
            cursor.execute('SELECT DISTINCT start FROM Flight')  # 获取所有航班的出发地
            start_airports = cursor.fetchall()

            cursor.execute('SELECT DISTINCT destination FROM Flight')  # 获取所有航班的目的地
            destination_airports = cursor.fetchall()

            # 合并并去重出发地和目的地的机场列表
            airports = set(
                [airport[0] for airport in start_airports] + [airport[0] for airport in destination_airports])

            # 将机场名称添加到下拉框中
            self.departureComboBox.clear()  # 清空现有的选项
            self.destinationComboBox.clear()

            # 填充出发地和目的地下拉框
            self.departureComboBox.addItems(sorted(airports))  # 使用 sorted 进行字母排序
            self.destinationComboBox.addItems(sorted(airports))

        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
        finally:
            # 确保连接关闭
            self.flightsTableWidgetDir.setRowCount(0)
            self.flightsTableWidgetCon.setRowCount(0)
            if conn:
                conn.close()

    def find_flights(self):
        def time_difference(departure_time, arrival_time):
            """
            计算时长差，假设时间格式为 'HH:MM'
            """
            # 如果时间是无效的（None 或空字符串），返回默认值（0）
            if not departure_time or not arrival_time or departure_time == '-' or arrival_time == '-':
                return 0  # 返回 0 分钟作为默认值

            try:
                # 如果时间是字符串或数字，先确保它们是有效的
                departure_time_str = str(departure_time).strip()
                arrival_time_str = str(arrival_time).strip()

                # 填充时间并转换为 datetime 对象
                departure = datetime.strptime(departure_time_str.zfill(4), "%H%M")
                arrival = datetime.strptime(arrival_time_str.zfill(4), "%H%M")

                # 如果到达时间在出发时间之前，说明跨过了午夜，增加一天
                if arrival < departure:
                    arrival += timedelta(days=1)

                # 计算时长差（单位：分钟）
                time_diff = (arrival - departure).total_seconds() / 60
                return time_diff
            except (ValueError, TypeError):
                # 如果转换失败（如无效时间格式），返回默认值
                return 0

        # 获取推荐航班列表
        recommended_flights = self.recommend_flights()

        if recommended_flights:
            # 清空现有表格内容
            self.flightsTableWidgetDir.setRowCount(0)
            self.flightsTableWidgetCon.setRowCount(0)

            # 初始化直达航班表头
            self.flightsTableWidgetDir.setColumnCount(5)
            self.flightsTableWidgetDir.setHorizontalHeaderLabels([
                '航班号', '出发时间', '到达时间', '票价', '航司'
            ])

            # 初始化中转航班表头
            self.flightsTableWidgetCon.setColumnCount(6)
            self.flightsTableWidgetCon.setHorizontalHeaderLabels([
                '航班号', '出发地', '中转地', '目的地', '出发时间', '总票价'
            ])

            # 直达航班排序（按票价）
            direct_flights = sorted(
                [f for f in recommended_flights if len(f) > 8 and (f[8] is None or f[8] == 'NULL')],
                key=lambda x: float(x[6] or 0)  # 使用索引访问价格
            )

            # 中转航班排序（按时长）
            connecting_flights = sorted(
                [f for f in recommended_flights if len(f) > 8 and f[8] is not None and f[8] != 'NULL'],
                key=lambda x: time_difference(x[6], x[7])  # 使用索引访问时间字段
            )

            # 填充直达航班数据到表格
            for flight in direct_flights:
                row_position = self.flightsTableWidgetDir.rowCount()
                self.flightsTableWidgetDir.insertRow(row_position)
                self.flightsTableWidgetDir.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight[0]))  # 航班号
                self.flightsTableWidgetDir.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight[1]))  # 出发地
                self.flightsTableWidgetDir.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight[2]))  # 目的地
                self.flightsTableWidgetDir.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(flight[6])))  # 出发时间
                self.flightsTableWidgetDir.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(flight[5])))  # 票价

            # 填充中转航班数据到表格
            for flight in connecting_flights:
                row_position = self.flightsTableWidgetCon.rowCount()
                self.flightsTableWidgetCon.insertRow(row_position)

                # 中转航班的两段信息：出发地 -> 中转地 -> 目的地
                self.flightsTableWidgetCon.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight[0]))  # 航班号
                self.flightsTableWidgetCon.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight[1]))  # 出发地
                self.flightsTableWidgetCon.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight[8]))  # 中转地
                self.flightsTableWidgetCon.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight[2]))  # 目的地
                self.flightsTableWidgetCon.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(flight[6])))  # 出发时间
                self.flightsTableWidgetCon.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(flight[5])))  # 总票价

    def back_to_main(self):
        self.close()

    def make_log_wrong_close(self):
        self.statuslabel.setText("")

class FlightSortWindow(QtWidgets.QMainWindow, Ui_FlightSortWindow):
    def __init__(self, name=None):
        super().__init__()
        self.setupUi(self)

        self.name = name

        # 创建数据库连接对象
        self.db_connection = sql_connection()

        # 初始化航班数据
        self.flights = self.db_connection.get_all_flights()

        # 连接排序按钮点击事件
        self.sortButton.clicked.connect(self.sort_flights)
        self.backToMainButton.clicked.connect(self.back_to_main)

        self.sortedFlightTable.setColumnCount(6)
        self.sortedFlightTable.setHorizontalHeaderLabels(['航班号', '出发城市', '目的地', '出发时间', '座位总数', '价格'])

        # 连接双击表格事件
        self.sortedFlightTable.itemDoubleClicked.connect(self.open_flight_details)

    def sort_flights(self):
        # 获取排序条件（价格：0，时间：1）
        sort_criteria = self.sortCriteriaComboBox.currentIndex()

        # 根据不同的排序条件进行排序
        if sort_criteria == 0:  # 按价格排序
            self.flights.sort(key=lambda flight: float(flight[6]) if flight[6] else 0.0)  # flight[6] 是价格
        elif sort_criteria == 1:  # 按时间排序
            # 将 `hh:mm` 格式转换为 `datetime` 对象进行排序
            self.flights.sort(key=lambda flight: datetime.strptime(flight[1], '%H:%M'))  # flight[1] 是出发时间

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

            # 使用 flight 数据填充表格
            self.sortedFlightTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight[0]))  # flight_id
            self.sortedFlightTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight[3]))
            self.sortedFlightTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight[4]))
            self.sortedFlightTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight[1]))
            self.sortedFlightTable.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(flight[7])))
            self.sortedFlightTable.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(flight[6])))

    def open_flight_details(self, item):
        # 获取当前双击的行号
        row = item.row()

        # 获取该行的航班数据
        flight_id = self.sortedFlightTable.item(row, 0).text()  # 获取第一列（航班号）的文本

        # 创建航班详情页窗口并传递数据，包括name
        self.flight_details_window = FlightDetailsWindow(flight_id, self.name)
        self.flight_details_window.show()

class FlightSearchWindow(QtWidgets.QMainWindow, QueryFlightSearchWindow):
    def __init__(self, name=None):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.searchButtonDir.clicked.connect(self.search_flights_Dir)
        self.backToMainButton.clicked.connect(self.back_to_main)
        self.searchButtonTran.clicked.connect(self.search_flights_Tran)

        self.sql_conn = sql_connection()
        self.populate_airports()
        self.flightTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.flightTable.itemDoubleClicked.connect(self.open_flight_details)

    def open_flight_details(self, item):
        # 获取当前双击的行号
        row = item.row()

        # 获取表格中所有列的标题（列名）
        column_headers = [self.flightTable.horizontalHeaderItem(i).text() for i in
                          range(self.flightTable.columnCount())]

        try:
            # 查找 '航班号2' 在列标题中的索引
            flight_id_column_index = column_headers.index('航班号2')  # 假设表格的列标题为 '航班号2'
        except ValueError:
            # 如果找不到 '航班号2' 列标题，则默认使用第一列（索引 0）
            flight_id_column_index = 0

        # 获取该行的航班号（根据列索引）
        flight_id = self.flightTable.item(row, flight_id_column_index).text()

        # 创建航班详情页窗口并传递数据，包括 flight_id 和 name
        self.flight_details_window = FlightDetailsWindow(flight_id, self.name)
        self.flight_details_window.show()

    def populate_airports(self):

        # 获取连接
        conn = None
        try:
            conn = self.sql_conn._get_connection('flight')
            cursor = conn.cursor()

            # 查询所有机场名称
            cursor.execute('SELECT DISTINCT start FROM Flight')  # 获取所有航班的出发地
            start_airports = cursor.fetchall()

            cursor.execute('SELECT DISTINCT destination FROM Flight')  # 获取所有航班的目的地
            destination_airports = cursor.fetchall()

            # 合并并去重出发地和目的地的机场列表
            airports = set(
                [airport[0] for airport in start_airports] + [airport[0] for airport in destination_airports])

            # 将机场名称添加到下拉框中
            self.startbox.clear()  # 清空现有的选项
            self.destinationbox.clear()

            # 填充出发地和目的地下拉框
            self.startbox.addItems(sorted(airports))  # 使用 sorted 进行字母排序
            self.destinationbox.addItems(sorted(airports))

        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
        finally:
            # 确保连接关闭
            if conn:
                conn.close()

    def search_flights_Dir(self):
        start = self.startbox.currentText()  # 获取出发地
        destination = self.destinationbox.currentText()  # 获取目的地

        # 查询直达航班信息（模糊搜索）
        conn = self.sql_conn._get_connection('flight')
        try:
            cursor = conn.cursor()
            query = '''
                SELECT flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number
                FROM Flight
                WHERE start LIKE ? AND destination LIKE ?
            '''
            cursor.execute(query, (f"%{start}%", f"%{destination}%"))
            flights = cursor.fetchall()

            # 清空现有表格内容
            self.flightTable.setRowCount(0)

            # 更新表格列数和列头名称
            self.flightTable.setColumnCount(9)
            self.flightTable.setHorizontalHeaderLabels([
                '航班号', '出发时间', '到达时间', '出发地', '目的地', '航空公司', '票价', '总座位数', '剩余座位数'
            ])

            # 根据查询结果判断状态
            if flights:
                # 填充表格
                for flight in flights:
                    row_position = self.flightTable.rowCount()
                    self.flightTable.insertRow(row_position)

                    # 填充每一列数据
                    self.flightTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight[0]))  # 航班号
                    self.flightTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight[1]))  # 出发时间
                    self.flightTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight[2]))  # 到达时间
                    self.flightTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight[3]))  # 出发地
                    self.flightTable.setItem(row_position, 4, QtWidgets.QTableWidgetItem(flight[4]))  # 目的地
                    self.flightTable.setItem(row_position, 5, QtWidgets.QTableWidgetItem(flight[5]))  # 航空公司
                    self.flightTable.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(flight[6])))  # 票价
                    self.flightTable.setItem(row_position, 7, QtWidgets.QTableWidgetItem(str(flight[7])))  # 总座位数
                    self.flightTable.setItem(row_position, 8, QtWidgets.QTableWidgetItem(str(flight[8])))  # 剩余座位数


                self.statuslabel.setText("查询成功！")
                self.statuslabel.setStyleSheet("color: red")
            else:
                # 如果没有查询到数据
                self.statuslabel.setText("未查询到数据！")
                self.statuslabel.setStyleSheet("color: red")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.statuslabel.setText(f"数据库错误: {e}")
            self.statuslabel.setStyleSheet("color: red")
        finally:
            if conn:
                conn.close()

    def search_flights_Tran(self):
        start = self.startbox.currentText()  # 获取出发地
        destination = self.destinationbox.currentText()  # 获取目的地

        # 查询中转航班信息（模糊搜索）
        conn = self.sql_conn._get_connection('flight')
        try:
            cursor = conn.cursor()
            query = '''
                SELECT f1.flight_id, f1.departure_time, f1.arrival_time, f1.start, f1.destination, f1.company, f1.price, f1.total_seats, f1.seat_number,
                       f2.flight_id, f2.departure_time, f2.arrival_time, f2.start, f2.destination, f2.company, f2.price, f2.total_seats, f2.seat_number
                FROM Flight f1
                JOIN Flight f2 ON f1.destination = f2.start
                WHERE f1.start LIKE ? AND f2.destination LIKE ?
            '''
            cursor.execute(query, (f"%{start}%", f"%{destination}%"))
            flights = cursor.fetchall()

            # 清空现有表格内容
            self.flightTable.setRowCount(0)

            # 更新表格列数和列头名称
            self.flightTable.setColumnCount(18)
            self.flightTable.setHorizontalHeaderLabels([
                '总价', '出发时间1', '到达时间1', '出发地1', '目的地1', '航空公司1', '票价1', '总座位数1',
                '剩余座位数1', '航班号2', '出发时间2', '到达时间2', '出发地2', '目的地2', '航空公司2', '票价2',
                '总座位数2', '剩余座位数2'
            ])

            # 根据查询结果判断状态
            if flights:
                # 填充表格
                for flight in flights:
                    row_position = self.flightTable.rowCount()
                    self.flightTable.insertRow(row_position)

                    # 计算总价（两个航班的票价之和）
                    total_price = flight[6] + flight[15]

                    # 填充总价
                    self.flightTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(total_price)))  # 总价

                    # 填充第1段航班信息
                    self.flightTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight[1]))  # 第1段出发时间
                    self.flightTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight[2]))  # 第1段到达时间
                    self.flightTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight[3]))  # 第1段出发地
                    self.flightTable.setItem(row_position, 4, QtWidgets.QTableWidgetItem(flight[4]))  # 第1段目的地
                    self.flightTable.setItem(row_position, 5, QtWidgets.QTableWidgetItem(flight[5]))  # 第1段航空公司
                    self.flightTable.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(flight[6])))  # 第1段票价
                    self.flightTable.setItem(row_position, 7, QtWidgets.QTableWidgetItem(str(flight[7])))  # 第1段总座位数
                    self.flightTable.setItem(row_position, 8, QtWidgets.QTableWidgetItem(str(flight[8])))  # 第1段剩余座位数

                    # 填充第2段航班信息
                    self.flightTable.setItem(row_position, 9, QtWidgets.QTableWidgetItem(flight[9]))  # 第2段航班号
                    self.flightTable.setItem(row_position, 10, QtWidgets.QTableWidgetItem(flight[10]))  # 第2段出发时间
                    self.flightTable.setItem(row_position, 11, QtWidgets.QTableWidgetItem(flight[11]))  # 第2段到达时间
                    self.flightTable.setItem(row_position, 12, QtWidgets.QTableWidgetItem(flight[12]))  # 第2段出发地
                    self.flightTable.setItem(row_position, 13, QtWidgets.QTableWidgetItem(flight[13]))  # 第2段目的地
                    self.flightTable.setItem(row_position, 14, QtWidgets.QTableWidgetItem(flight[14]))  # 第2段航空公司
                    self.flightTable.setItem(row_position, 15, QtWidgets.QTableWidgetItem(str(flight[15])))  # 第2段票价
                    self.flightTable.setItem(row_position, 16, QtWidgets.QTableWidgetItem(str(flight[16])))  # 第2段总座位数
                    self.flightTable.setItem(row_position, 17, QtWidgets.QTableWidgetItem(str(flight[17])))  # 第2段剩余座位数

                self.statuslabel.setText("查询成功！")
                self.statuslabel.setStyleSheet("color: red")
            else:
                # 如果没有查询到数据
                self.statuslabel.setText("未查询到数据！")
                self.statuslabel.setStyleSheet("color: red")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.statuslabel.setText(f"数据库错误: {e}")
            self.statuslabel.setStyleSheet("color: red")
        finally:
            if conn:
                conn.close()

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

class ProfileManagementWindow(QtWidgets.QMainWindow, ProfileManagerUi):
    def __init__(self, name, phone, id_card, mail):
        super().__init__()
        self.setupUi(self)

        # 显示用户个人信息
        self.currentUsernameLabel.setText(f"用户名：{name}")
        self.currentPhoneLabel.setText(f"手机号：{phone}")
        self.label.setText(f"身份证号：{id_card}")
        self.currentEmailLabel.setText(f"邮箱：{mail}")

        # 保存这些信息，方便在后续更新时使用
        self.name = name
        self.phone = phone
        self.id_card = id_card
        self.mail = mail

        self.backButton.clicked.connect(self.back_to_main)
        self.saveButton.clicked.connect(self.save_user)

        # 创建数据库连接实例
        self.db_connection = sql_connection()

    def back_to_main(self):
        self.close()

    def save_user(self):
        # 获取用户修改后的信息（如果留空，则表示不修改）
        updated_name = self.usernameLineEdit.text()
        updated_phone = self.phoneLineEdit.text()
        updated_id_card = self.IDLineEdit.text()
        updated_mail = self.emailLineEdit.text()
        updated_password = self.passwordLineEdit.text()

        # 动态检测哪些字段需要更新
        fields_to_update = {
            "name": updated_name if updated_name else None,  # 如果为空，跳过更新
            "phone": updated_phone if updated_phone else None,
            "id_card": updated_id_card if updated_id_card else None,
            "mail": updated_mail if updated_mail else None,
            "password": updated_password if updated_password else None
        }

        # 调用数据库更新方法，仅传递需要更新的字段
        self.db_connection.update_passenger(
            name=self.name,  # 使用当前用户名作为条件
            password=fields_to_update["password"],
            phone=fields_to_update["phone"],
            id_card=fields_to_update["id_card"],
            mail=fields_to_update["mail"]
        )

        # 更新界面显示
        if updated_name:
            self.currentUsernameLabel.setText(f"用户名：{updated_name}")
            self.name = updated_name  # 更新类属性
        if updated_phone:
            self.currentPhoneLabel.setText(f"手机号：{updated_phone}")
            self.phone = updated_phone
        if updated_id_card:
            self.label.setText(f"身份证号：{updated_id_card}")
            self.id_card = updated_id_card
        if updated_mail:
            self.currentEmailLabel.setText(f"邮箱：{updated_mail}")
            self.mail = updated_mail
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

    def closeEvent(self, event):
        # 在 AboutWindow 关闭时，也调用 ScrollingTextWindow 的 closeEvent 来停止音乐
        self.scroll_window.closeEvent(event)
        event.accept()



class commentManagementWindow(QtWidgets.QMainWindow, Ui_CommentManagementWindow):
    def __init__(self,name=None):
        super().__init__()
        self.setupUi(self)
        self.AddCommentButton.clicked.connect(self.add_comment)
        self.backToMainButton.clicked.connect(self.back_to_main)

        self.db = sql_connection()
        self.name = name  # 保存传递的用户名

        # 加载评论数据
        self.load_comments()

    def load_comments(self):
        # 从数据库获取评论数据
        conn = self.db._get_connection('comments')
        cursor = conn.cursor()
        cursor.execute("SELECT name, company, comment FROM comment")
        comments = cursor.fetchall()

        # 清空现有数据
        self.commenttable.setRowCount(0)  # 清空表格行
        self.commenttable.setColumnCount(3)  # 设置列数为3列
        self.commenttable.setHorizontalHeaderLabels(["用户名", "航司", "评论"])  # 设置列标题

        # 填充数据到表格
        self.commenttable.setRowCount(len(comments))  # 设置行数
        for row, comment in enumerate(comments):
            self.commenttable.setItem(row, 0, QtWidgets.QTableWidgetItem(comment[0]))  # 用户名
            self.commenttable.setItem(row, 1, QtWidgets.QTableWidgetItem(comment[1]))  # 航司
            self.commenttable.setItem(row, 2, QtWidgets.QTableWidgetItem(comment[2]))  # 评论内容

        # 设置表格为只读
        self.commenttable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # 设置表格不可选择
        self.commenttable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        conn.close()

    def add_comment(self):
        self.comment_add_window = commentAddWindow(self.db, self.name, parent=self)
        self.comment_add_window.show()

    def back_to_main(self):
        self.close()


class commentAddWindow(QtWidgets.QMainWindow, Ui_CommentAddWindow):
    def __init__(self, db, name, parent=None):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.name = name
        self.parent = parent  # 保存对父窗口的引用
        self.submitCommentButton.clicked.connect(self.create_comment)
        self.backToMainButton.clicked.connect(self.back_to_main)

        # 初始化航空公司选择框
        self.load_airlines()


    def load_airlines(self):
        # 从 company.csv 获取航空公司列表
        with open('company.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            airlines = [row[0] for row in csvreader if row]  # 读取每行的第一列（航空公司名称）
        # 将航空公司添加到 comboBox
        for airline in airlines:
            self.comboBox.addItem(airline)

    def create_comment(self):
        # 获取评论内容,选中的航空公司和用户名
        comment_content = self.commentTextEdit.toPlainText()
        airline = self.comboBox.currentText()
        user_name = self.name

        if not comment_content.strip():
            self.statuslabel.setText("评论内容不能为空！")
            self.statuslabel.setStyleSheet("color: red;")
            return

        # 将评论内容和航空公司插入数据库
        try:
            # 传入的元组格式为 (name, company, comment)
            self.db.insert_comment((user_name, airline, comment_content))
            self.statuslabel.setText("评论已提交成功！")
        except Exception as e:
            self.statuslabel.setText(f"提交失败: {e}")
            self.statuslabel.setStyleSheet("color: red;")

    def back_to_main(self):
        # 调用父窗口的 load_comments 方法刷新评论
        if self.parent:
            self.parent.load_comments()  # 刷新父窗口的数据

        self.close()


class FlightDetailsWindow(QtWidgets.QMainWindow, Ui_FlightDetailsWindow):
    def __init__(self, flight_id=None, name=None):
        super().__init__()
        self.setupUi(self)
        self.flight_id = flight_id  # 接收传递的 flight_id
        self.name = name
        self.backToPreviousButton.clicked.connect(self.back_to_previous)
        self.pushButton.clicked.connect(self.order)

        # 初始化数据库连接
        self.db = sql_connection()

        if self.flight_id:
            self.display_flight_details()

    def back_to_previous(self):
        self.close()

    def order(self):
        self.order_details_window = OrderDetailsWindow(self.flight_id, self.name)
        self.order_details_window.show()

    def display_flight_details(self):
        # 通过 flight_id 查询航班信息
        try:
            # 通过 db_connection 获取航班详情
            flight_details = self.db.get_flight_details(self.flight_id)

            if flight_details:
                # 使用返回的详细信息更新 UI
                self.id.setText(f"航班号: {flight_details['flight_id']}")
                self.company.setText(f"航空公司: {flight_details['company']}")
                self.depaturetime.setText(f"出发时间: {flight_details['departure_time']}")
                self.arrivaltime.setText(f"到达时间: {flight_details['arrival_time']}")
                self.price.setText(f"票价: {flight_details['price']}元")
                # self.start.setText(f"出发城市: {flight_details['start']}")
                # self.destination.setText(f"目的地: {flight_details['destination']}")
                # self.total_seats.setText(f"座位总数: {flight_details['total_seats']}")
                # self.seat_number.setText(f"剩余座位: {flight_details['seat_number']}")
                # self.connection.setText(f"航班连接: {flight_details['connection']}")
            else:
                self.id.setText("航班号: 未找到")
                self.company.setText("航空公司: 未找到")
                self.depaturetime.setText("出发时间: 未找到")
                self.arrivaltime.setText("到达时间: 未找到")
                self.price.setText("票价: 未找到")
                # self.start.setText("出发城市: 未找到")
                # self.destination.setText("目的地: 未找到")
                # self.total_seats.setText("座位总数: 未找到")
                # self.seat_number.setText("剩余座位: 未找到")
                # self.connection.setText("航班连接: 未找到")

        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            # 在 UI 中显示错误信息
            self.id.setText("航班号: 错误")
            self.company.setText("航空公司: 错误")
            self.depaturetime.setText("出发时间: 错误")
            self.arrivaltime.setText("到达时间: 错误")
            self.price.setText("票价: 错误")
            # self.start.setText("出发城市: 错误")
            # self.destination.setText("目的地: 错误")
            # self.total_seats.setText("座位总数: 错误")
            # self.seat_number.setText("剩余座位: 错误")
            # self.connection.setText("航班连接: 错误")

    # def format_time(self, datetime_str):
    #     """将数据库中的 DATETIME 字符串格式化为更友好的显示格式"""
    #     try:
    #         if datetime_str:
    #             return datetime_str.split()[1]  # 提取时间部分（例如：'15:30:00'）
    #         return ""
    #     except Exception as e:
    #         return "格式化错误"


class OrderDetailsWindow(QtWidgets.QMainWindow, Ui_OrderDetailsWindow):
    def __init__(self, flight_id=None, name=None):
        super().__init__()
        self.setupUi(self)
        self.flight_id = flight_id  # 接收传递的 flight_id
        self.name = name  # 接收传递的 name
        self.backToPreviousButton.clicked.connect(self.back_to_main)
        self.pushButton.clicked.connect(self.order)

        # 初始化数据库连接
        self.db = sql_connection()

        if self.flight_id:
            self.load_flight_details()

    def back_to_main(self):
        self.close()

    def order(self):
        # 通过 flight_id 从数据库获取航班信息（仍然从 flights.db 获取航班信息）
        connection = sqlite3.connect('../data/flights.db')  # 连接 flights.db 获取航班信息
        cursor = connection.cursor()

        cursor.execute(
            "SELECT departure_time, arrival_time, start, destination, company, price, total_seats, seat_number FROM Flight WHERE flight_id = ?",
            (self.flight_id,))
        flight_details = cursor.fetchone()

        if flight_details:
            departure_time, arrival_time, start, destination, company, price, total_seats, seat_number = flight_details

            # 处理 total_seats 格式，确保它是一个有效的整数
            if isinstance(total_seats, str) and total_seats.strip('%').isdigit():
                total_seats = int(total_seats.strip('%'))  # 如果是百分比格式，去掉百分号并转换为整数
            else:
                total_seats = 0  # 如果无法转换为整数，默认设置为 0

            seat_number = seat_number if seat_number is not None else 0  # 如果 seat_number 是 None，设置为 0

            # 获取当前日期
            current_date = datetime.now().strftime('%Y-%m-%d')  # 获取当前日期，格式为 'YYYY-MM-DD'

            # 格式化时间字段为标准的 DATETIME 格式
            try:
                # 如果 departure_time 和 arrival_time 仅为小时和分钟，如 '12:40'，则为它们添加当前日期
                formatted_departure_time = f"{current_date} {departure_time}:00"  # 如 '2024-12-25 12:40:00'
                formatted_arrival_time = f"{current_date} {arrival_time}:00"
            except Exception as e:
                print(f"Error formatting time: {e}")
                QtWidgets.QMessageBox.warning(self, "错误", f"时间格式化失败：{e}", QtWidgets.QMessageBox.Ok)
                return  # 退出函数，不继续执行插入操作

            if formatted_departure_time and formatted_arrival_time:
                # 连接到 orders.db 插入数据
                try:
                    orders_connection = sqlite3.connect('../data/orders.db')  # 连接到 orders.db 数据库
                    orders_cursor = orders_connection.cursor()

                    # 执行插入操作
                    orders_cursor.execute('''
                        INSERT INTO `Order` (name, flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (self.name, self.flight_id, formatted_departure_time, formatted_arrival_time, start,
                          destination, company, price, total_seats, seat_number))
                    orders_connection.commit()

                    # 提示用户订单已成功创建
                    QtWidgets.QMessageBox.information(self, "订单创建", "订单已成功创建！", QtWidgets.QMessageBox.Ok)
                    self.statusLabel.setText("订单状态: 已支付")
                    self.close()
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                    QtWidgets.QMessageBox.warning(self, "错误", f"数据库操作失败：{e}", QtWidgets.QMessageBox.Ok)
                finally:
                    orders_connection.close()  # 确保连接关闭


            else:
                QtWidgets.QMessageBox.warning(self, "错误", "时间格式错误，无法创建订单！", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "未找到航班信息！", QtWidgets.QMessageBox.Ok)

        connection.close()  # 关闭 flights.db 的连接

    def load_flight_details(self):
        # 使用 sql_connection 获取航班信息
        flight_details = self.db.get_flight_details(self.flight_id)

        if flight_details:
            company = flight_details['company']
            departure_time = flight_details['departure_time']
            arrival_time = flight_details['arrival_time']
            start = flight_details['start']
            destination = flight_details['destination']
            price = flight_details['price']

            # 更新界面上的标签内容
            self.orderDetailsLabel.setText("订单详情")
            self.usernameLabel.setText(f"用户名: {self.name}")  # 显示用户名
            self.companyLabel.setText(f"航司: {company}")
            self.flightNumberLabel.setText(f"航班号: {self.flight_id}")
            self.departureLabel.setText(f"出发地: {start}")
            self.destinationLabel.setText(f"目的地: {destination}")
            self.priceLabel.setText(f"价格: ¥{price}")
            self.statusLabel.setText("订单状态: 待支付")
        else:
            # 如果没有找到航班信息，显示默认信息
            self.orderDetailsLabel.setText("订单详情")
            self.usernameLabel.setText("用户名: 未找到")
            self.flightNumberLabel.setText("航班号: 未找到")
            self.departureLabel.setText("出发地: 未找到")
            self.destinationLabel.setText("目的地: 未找到")
            self.priceLabel.setText("价格: 未找到")
            self.statusLabel.setText("订单状态: 未找到")


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


class ProfileManagementWindow(QtWidgets.QMainWindow, ProfileManagerUi):
    def __init__(self, name, phone, id_card, mail):
        super().__init__()
        self.setupUi(self)
        self.db = sql_connection()

        # 显示用户个人信息
        self.currentUsernameLabel.setText(f"用户名：{name}")
        self.currentPhoneLabel.setText(f"手机号：{phone}")
        self.label.setText(f"身份证号：{id_card}")
        self.currentEmailLabel.setText(f"邮箱：{mail}")

        # 保存这些信息，方便在后续更新时使用
        self.name = name
        self.phone = phone
        self.id_card = id_card
        self.mail = mail

        self.backButton.clicked.connect(self.back_to_main)
        self.saveButton.clicked.connect(self.save_user)

    def back_to_main(self):
        self.close()

    def save_user(self):
        # 获取用户修改后的信息（如果留空，则表示不修改）
        updated_name = self.usernameLineEdit.text()
        updated_phone = self.phoneLineEdit.text()
        updated_id_card = self.IDLineEdit.text()
        updated_mail = self.emailLineEdit.text()
        updated_password = self.passwordLineEdit.text()

        # 动态检测哪些字段需要更新
        fields_to_update = {
            "name": updated_name if updated_name else None,  # 如果为空，跳过更新
            "phone": updated_phone if updated_phone else None,
            "id_card": updated_id_card if updated_id_card else None,
            "mail": updated_mail if updated_mail else None,
            "password": updated_password if updated_password else None
        }

        # 调用数据库更新方法，仅传递需要更新的字段
        self.db.update_passenger(
            name=self.name,  # 使用当前用户名作为条件
            password=fields_to_update["password"],
            phone=fields_to_update["phone"],
            id_card=fields_to_update["id_card"],
            mail=fields_to_update["mail"]
        )

        # 更新界面显示
        if updated_name:
            self.currentUsernameLabel.setText(f"用户名：{updated_name}")
            self.name = updated_name  # 更新类属性
        if updated_phone:
            self.currentPhoneLabel.setText(f"手机号：{updated_phone}")
            self.phone = updated_phone
        if updated_id_card:
            self.label.setText(f"身份证号：{updated_id_card}")
            self.id_card = updated_id_card
        if updated_mail:
            self.currentEmailLabel.setText(f"邮箱：{updated_mail}")
            self.mail = updated_mail
        self.label_3.setText("修改成功！")
        self.label_3.setStyleSheet("color: red;")


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
        self.profile_management_window = ProfileManagerWindow()
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

        # 设置表格的列名
        self.searchreasult.setHorizontalHeaderLabels([
            "航班号", "起飞时间", "到达时间", "起点", "终点", "航空公司", "票价", "总座位数", "座位号", "连接"
        ])

        self.searchreasult.resizeColumnsToContents()

        # 启用多选模式
        self.searchreasult.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # 连接按钮事件
        self.pushButton_3.clicked.connect(self.back_to_main)
        self.pushButton.clicked.connect(self.insert_flight)
        self.pushButton_2.clicked.connect(self.delete_flight)
        self.pushButton_4.clicked.connect(self.update_table)

        # 初始化数据库连接
        self.db = sql_connection()

        # 初始化航班数据存储
        self.flights_data = []

        # 更新航班表格
        self.update_table()

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

        # 将新航班添加到数据库
        self.db.insert_flight(flight_id, departure_time, arrival_time, start_point, destination, airline, price=0,
                              total_seats=0, seat_number="")

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
        selected_rows = self.searchreasult.selectedIndexes()

        if selected_rows:
            # 获取所有选中的航班号
            flight_ids_to_delete = []
            for index in selected_rows:
                row = index.row()
                flight_id = self.searchreasult.item(row, 0).text()  # 获取航班号
                if flight_id not in flight_ids_to_delete:
                    flight_ids_to_delete.append(flight_id)

            # 提示用户确认删除
            reply = QtWidgets.QMessageBox.question(self, '删除航班',
                                                   f"你确定要删除这些航班吗？\n{' '.join(flight_ids_to_delete)}",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                # 删除选中的航班
                for flight_id in flight_ids_to_delete:
                    self.db.delete_flight(flight_id)  # 使用数据库删除航班

                # 更新表格显示
                self.update_table()
        else:
            QtWidgets.QMessageBox.warning(self, '错误', "请选择一个或多个航班进行删除")

    def update_table(self):
        """更新表格中的数据"""
        # 清空现有的表格内容
        self.searchreasult.setRowCount(0)

        # 从数据库获取所有航班数据
        flights_info = self.db.get_all_flights()

        # 如果航班数据存在，填充表格
        for flight in flights_info:
            row_position = self.searchreasult.rowCount()
            self.searchreasult.insertRow(row_position)

            # 按照正确的顺序填充数据
            self.searchreasult.setItem(row_position, 0, QtWidgets.QTableWidgetItem(flight[0]))  # flight_id
            self.searchreasult.setItem(row_position, 1, QtWidgets.QTableWidgetItem(flight[1]))  # departure_time
            self.searchreasult.setItem(row_position, 2, QtWidgets.QTableWidgetItem(flight[2]))  # arrival_time
            self.searchreasult.setItem(row_position, 3, QtWidgets.QTableWidgetItem(flight[3]))  # start
            self.searchreasult.setItem(row_position, 4, QtWidgets.QTableWidgetItem(flight[4]))  # destination
            self.searchreasult.setItem(row_position, 5, QtWidgets.QTableWidgetItem(flight[5]))  # company
            self.searchreasult.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(flight[6])))  # price
            self.searchreasult.setItem(row_position, 7, QtWidgets.QTableWidgetItem(str(flight[7])))  # total_seats
            self.searchreasult.setItem(row_position, 8, QtWidgets.QTableWidgetItem(flight[8]))  # seat_number
            self.searchreasult.setItem(row_position, 9, QtWidgets.QTableWidgetItem(flight[9]))  # connection

        # 刷新表格
        self.searchreasult.resizeColumnsToContents()


class ProfileManagerWindow(QtWidgets.QMainWindow, ProfilemanagerControl):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backButton.clicked.connect(self.back_to_main)
        self.deleteButton.clicked.connect(self.delete_user)
        self.db = sql_connection()

        self.initialize_table()  # 初始化表格
        self.load()  # 加载用户信息

    def back_to_main(self):
        # 返回到主界面，关闭当前窗口
        self.close()

    def initialize_table(self):
        """
        初始化 QTableWidget 的列名。
        """
        # 设置表格列名
        column_headers = ['用户名', '手机号', '身份证号', '邮箱']
        self.tableWidget.setColumnCount(len(column_headers))  # 设置列数
        self.tableWidget.setHorizontalHeaderLabels(column_headers)  # 设置列标题

    def load(self):
        """
        加载所有用户信息。
        """
        # 获取所有用户信息
        users_info = self.db.get_all_passengers()

        # 清空表格数据
        self.tableWidget.setRowCount(0)  # 先清空所有行

        # 如果有用户信息，插入到表格中
        if users_info:
            for user in users_info:
                row_position = self.tableWidget.rowCount()  # 获取当前行数
                self.tableWidget.insertRow(row_position)  # 插入一行
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(user['name']))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(user['phone']))
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(user['id_card']))
                self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(user['mail']))

    def delete_user(self):
        """
        删除当前选中的用户信息。
        """
        selected_row = self.tableWidget.currentRow()  # 获取当前选中的行
        if selected_row >= 0:
            # 获取选中的用户名
            username = self.tableWidget.item(selected_row, 0).text()  # 使用用户名列 (第0列)

            # 提示用户确认删除
            reply = QtWidgets.QMessageBox.question(self, '删除用户',
                                                   f"你确定要删除用户 {username} 吗？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                # 删除当前用户
                self.db.delete_passenger(username)
                QtWidgets.QMessageBox.information(self, '成功', "用户已成功删除")
                self.load()  # 删除后重新加载用户列表
        else:
            QtWidgets.QMessageBox.warning(self, '错误', "请选择一个用户进行删除")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
