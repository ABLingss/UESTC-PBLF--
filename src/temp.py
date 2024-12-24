import sqlite3

def create_or_rebuild_order_table():
    try:
        # 连接到数据库
        connection = sqlite3.connect('../data/orders.db')
        cursor = connection.cursor()

        # 删除已经存在的 Order 表（如果有的话）
        cursor.execute('DROP TABLE IF EXISTS `Order`;')

        # 创建新的 Order 表，使用自动生成的 order_id 作为主键
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `Order` (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自动递增的主键
                name TEXT NOT NULL,  -- 用户名
                flight_id TEXT NOT NULL,  -- 航班 ID
                departure_time TEXT NOT NULL,  -- 出发时间
                arrival_time TEXT NOT NULL,  -- 到达时间
                start TEXT NOT NULL,  -- 出发地
                destination TEXT NOT NULL,  -- 目的地
                company TEXT NOT NULL,  -- 航空公司
                price REAL NOT NULL,  -- 价格
                total_seats INTEGER NOT NULL,  -- 总座位数
                seat_number INTEGER NOT NULL,  -- 座位号
                UNIQUE(name, flight_id)  -- 确保同一个用户对同一航班只能有一个订单
            );
        ''')

        # 提交事务
        connection.commit()

        # 完成后关闭连接
        connection.close()

        print("Order table created successfully with 'order_id' as primary key.")
    except sqlite3.Error as e:
        print(f"Error while creating or rebuilding table: {e}")

# 执行函数来创建或重建 Order 表
create_or_rebuild_order_table()
