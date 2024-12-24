import pandas as pd
import sqlite3
import random


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

    def insert_flight_with_price(self, flight_csv_file, price_csv_file):
        """
        将航班数据和价格数据直接加到 flights.db 的 Flight 表中
        :param flight_csv_file: 包含航班基本信息的 CSV 文件路径
        :param price_csv_file: 包含价格的 CSV 文件路径（没有与航班 ID 关联）
        """
        conn = None
        try:
            # 读取航班基本信息和价格信息的 CSV 文件
            flight_df = pd.read_csv(flight_csv_file)
            price_df = pd.read_csv(price_csv_file)

            # 如果 price 列未包含数据，随机生成价格（如果需要）
            if 'price' not in price_df.columns:
                price_df['price'] = [random.uniform(200, 1500) for _ in range(len(price_df))]

            # 确保 price 列的数量与航班数据的行数一致，直接把价格添加到航班数据中
            if len(price_df) < len(flight_df):
                # 如果价格数量不足，用随机生成的价格填充
                price_df = price_df.append(
                    pd.DataFrame({'price': [random.uniform(200, 1500)] * (len(flight_df) - len(price_df))}),
                    ignore_index=True)

            # 将价格列直接添加到航班数据中
            flight_df['price'] = price_df['price']

            # 获取连接到 flights.db
            conn = self._get_connection('flight')
            cursor = conn.cursor()

            # 确保表格存在，并检查是否包含 connection 列
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS Flight (
                    flight_id TEXT PRIMARY KEY,
                    departure_time TEXT,
                    arrival_time TEXT,
                    start TEXT,
                    destination TEXT,
                    company TEXT,
                    price REAL,
                    total_seats INTEGER,
                    seat_number TEXT,
                    connection TEXT
                )
            ''')

            # 检查是否已经存在 connection 列
            cursor.execute("PRAGMA table_info(Flight);")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            if 'connection' not in column_names:
                cursor.execute("ALTER TABLE Flight ADD COLUMN connection TEXT;")

            # 插入数据：将航班数据插入，并直接附加价格数据
            for index, row in flight_df.iterrows():
                cursor.execute(''' 
                    INSERT OR REPLACE INTO Flight 
                    (flight_id, departure_time, arrival_time, start, destination, company, price, total_seats, seat_number, connection) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['flight_id'], row['departure_time'], row['arrival_time'], row['start'], row['destination'],
                    row['company'], row['price'], row['total_seats'], row['seat_number'], row['connection']
                ))

            # 提交事务
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except pd.errors.EmptyDataError as e:
            print(f"CSV error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            if conn:
                conn.close()


# 使用示例
sql_conn = sql_connection()
flight_csv_file = '全国主要机场航班数据.csv'  # 包含航班基本信息的 CSV 文件路径
price_csv_file = 'price.csv'  # 包含价格的 CSV 文件路径
sql_conn.insert_flight_with_price(flight_csv_file, price_csv_file)
