import sys
from PyQt5 import QtWidgets
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


class LoginWindow(QtWidgets.QMainWindow, LoginUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)
        self.cancelButton.clicked.connect(self.cancel)
        self.registerButton.clicked.connect(self.register)

    def login(self):
        # 假设登录验证通过
        print("登录成功")

        self.main_window = MainInterface()
        self.main_window.show()
        self.close()

        # # 实现判断是不是管理员的函数ismin（）
        # if self.is_admin():
        # self.main_manager_window = MainManagerWindow()
        # self.main_manager_window.show()
        # self.close()
        # else:
        #     self.main_window = MainInterface()
        #     self.main_window.show()
        #     self.close()

    def cancel(self):
        self.close()

    def register(self):
    # 这里写注册的逻辑
        print("注册成功")
        self.main_window = MainInterface()
        self.main_window.show()
        self.close()

class MainInterface(QtWidgets.QMainWindow, MainUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        # 按钮与函数连接
        self.flightRecommendationButton.clicked.connect(self.open_flight_recommendation)
        self.flightSearchButton.clicked.connect(self.open_flight_search)
        self.flightSortButton.clicked.connect(self.open_flight_sort)
        self.orderManagementButton.clicked.connect(self.open_order_management)
        self.profileManagementButton.clicked.connect(self.open_profile_management)
        self.logout.clicked.connect(self.logout_user)
        self.about.clicked.connect(self.aboutus)
        self.commentManagementButton.clicked.connect(self.comment_management)
        self.flightDetailsButton.clicked.connect(self.open_flight_details)

    def open_flight_recommendation(self):
        self.flight_recommendation_window = FlightRecommendationWindow()
        self.flight_recommendation_window.show()

    def open_flight_search(self):
        self.flight_search_window = FlightSearchWindow()
        self.flight_search_window.show()

    def open_flight_sort(self):
        self.flight_sort_window = FlightSortWindow()
        self.flight_sort_window.show()

    def open_order_management(self):
        self.order_management_window = OrderManagementWindow()
        self.order_management_window.show()

    def open_profile_management(self):
        self.profile_management_window = ProfileManagementWindow()
        self.profile_management_window.show()
    #     这么写的原因是，因为这个类继承自两个父类，所以需要用super()函数来调用父类的方法。
    #     这样可以保证每个类都能调用父类的方法，而不会因为类名冲突而导致调用错误的方法。

    def logout_user(self):
        # 退出登录
        self.close()

    def aboutus(self):
        # 打开关于我们的窗口 我们采用了一个滚动条进行简单表示，后期可以整花活
        self.about_window = AboutWindow()
        self.about_window.show()

    def comment_management(self):
        # 打开评论管理窗口
        self.comment_management_window = commentManagementWindow()
        self.comment_management_window.show()

    def open_flight_details(self):
        # 打开航班详情窗口
        self.flight_details_window = FlightDetailsWindow()
        self.flight_details_window.show()


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


class FlightSearchWindow(QtWidgets.QMainWindow, QueryFlightSearchWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search_flights)
        self.backToMainButton.clicked.connect(self.back_to_main)

    def search_flights(self):
        # 这里应该是搜索航班的逻辑
        print("搜索航班按钮被点击")
        # 假设搜索结果如下
        self.resultsTextBrowser.setText("搜索结果：\n航班A\n航班B\n航班C")

    def back_to_main(self):
        self.close()

class FlightSortWindow(QtWidgets.QMainWindow, Ui_FlightSortWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sortButton.clicked.connect(self.sort_flights)
        self.backToMainButton.clicked.connect(self.back_to_main)

    def sort_flights(self):
        # 排序航班的逻辑，假设按价格排序
        print("排序航班按钮被点击")
        self.resultsTextBrowser.setText("排序后的航班：\n航班1（价格：1000元）\n航班2（价格：1200元）")

    def back_to_main(self):
        self.close()

class OrderManagementWindow(QtWidgets.QMainWindow, Ui_OrderManagementWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.createOrderButton.clicked.connect(self.create_order)
        self.cancelOrderButton.clicked.connect(self.cancel_order)
        self.backToMainButton.clicked.connect(self.back_to_main)

    def create_order(self):
        # 创建订单的逻辑
        print("创建订单按钮被点击")
        self.orderStatusLabel.setText("订单已创建")

    def cancel_order(self):
        # 取消订单的逻辑
        print("取消订单按钮被点击")
        self.orderStatusLabel.setText("订单已取消")

    def back_to_main(self):
        self.close()

class ProfileManagementWindow(QtWidgets.QMainWindow, Ui_ProfileManagementWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.saveButton.clicked.connect(self.save_profile)
        self.backButton.clicked.connect(self.back_to_main)

    def save_profile(self):
        # 更新用户个人资料的逻辑
        print("更新个人资料按钮被点击")
        self.statusLabel.setText("个人资料更新成功")

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

class AdminWindow(QtWidgets.QMainWindow, AdminUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.editOrderButton.clicked.connect(self.edit_order)
        self.editUserButton.clicked.connect(self.edit_user)
        self.backToPreviousButton.clicked.connect(self.back_to_main)
    def edit_order(self):
        self.OrderEditWindow = OrderEditUI()
        self.OrderEditWindow.show()

    def edit_user(self):
        # 修改用户的逻辑
        self.ProfileManagementWindow = ProfileManagerUI()
        self.ProfileManagementWindow.show()

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
        self.flightRecommendationButton.clicked.connect(self.open_flight_recommendation)
        self.flightSearchButton.clicked.connect(self.open_flight_search)
        self.flightSortButton.clicked.connect(self.open_flight_sort)
        self.orderManagementButton.clicked.connect(self.open_order_management)
        self.profileManagementButton.clicked.connect(self.open_profile_management)
        self.pushButton.clicked.connect(self.logout_user)
        self.pushButton_2.clicked.connect(self.aboutus)
        self.commentManagementButton.clicked.connect(self.comment_management)
        self.flightDetailsButton.clicked.connect(self.open_flight_details)
        self.pushButton_3.clicked.connect(self.open_admin_dashboard)

    def open_admin_dashboard(self):
        self.admin_dashboard_window = AdminWindow()
        self.admin_dashboard_window.show()
    def open_flight_recommendation(self):
        self.flight_recommendation_window = FlightRecommendationWindow()
        self.flight_recommendation_window.show()
    def open_flight_search(self):
        self.flight_search_window = FlightSearchWindow()
        self.flight_search_window.show()
    def open_flight_sort(self):
        self.flight_sort_window = FlightSortWindow()
        self.flight_sort_window.show()
    def open_order_management(self):
        self.order_management_window = OrderManagementWindow()
        self.order_management_window.show()
    def open_profile_management(self):
        self.profile_management_window = ProfileManagementWindow()
        self.profile_management_window.show()
    #     这么写的原因是，因为这个类继承自两个父类，所以需要用super()函数来调用父类的方法。
    #     这样可以保证每个类都能调用父类的方法，而不会因为类名冲突而导致调用错误的方法。
    def logout_user(self):
        # 退出登录
        self.close()
    def aboutus(self):
        # 打开关于我们的窗口 我们采用了一个滚动条进行简单表示，后期可以整花活
        self.about_window = AboutWindow()
        self.about_window.show()
    def comment_management(self):
        # 打开评论管理窗口
        self.comment_management_window = commentManagementWindow()
        self.comment_management_window.show()
    def open_flight_details(self):
        # 打开航班详情窗口
        self.flight_details_window = FlightDetailsWindow()
        self.flight_details_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

