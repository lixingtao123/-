import os
import sqlite3
from datetime import datetime

class Database:
    """基于SQLite的数据库类，用于管理用户数据和股票数据"""
    
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.db_path = os.path.join(self.data_dir, "stock_simulator.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._initialize_tables()
        self._initialize_default_data()

    def _initialize_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                type TEXT,
                balance REAL,
                created_at TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS holdings (
                username TEXT,
                stock_code TEXT,
                quantity INTEGER,
                cost REAL,
                name TEXT,
                PRIMARY KEY (username, stock_code)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                code TEXT PRIMARY KEY,
                name TEXT,
                price REAL,
                change REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                type TEXT,
                stock_code TEXT,
                stock_name TEXT,
                price REAL,
                quantity INTEGER,
                amount REAL,
                timestamp TEXT
            )
        ''')
        cursor.execute("PRAGMA table_info(holdings)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'name' not in columns:
            cursor.execute('ALTER TABLE holdings ADD COLUMN name TEXT')
        self.conn.commit()

    def _initialize_default_data(self):
        """初始化默认数据（如果数据库为空）"""
        cursor = self.conn.cursor()
        
        # 检查users表是否为空
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        # 检查stocks表是否为空
        cursor.execute("SELECT COUNT(*) FROM stocks")
        stock_count = cursor.fetchone()[0]
        
        # 如果users表为空，添加默认用户
        if user_count == 0:
            default_users = [
                ("admin", "admin123", "admin", 1000000.0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                ("user", "user123", "user", 100000.0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            ]
            cursor.executemany(
                "INSERT INTO users (username, password, type, balance, created_at) VALUES (?, ?, ?, ?, ?)",
                default_users
            )
        
        # 如果stocks表为空，添加默认股票
        if stock_count == 0:
            default_stocks = [
                ("sh.000016", "上证50", 4.82, -2.23),
                ("sh.600000", "浦发银行", 12.35, -0.08),
                ("sh.600009", "上海机场", 32.78, 1.24),
                ("sh.600016", "民生银行", 4.73, 0.21),
                ("sh.600018", "上港集团", 5.8, 0.52),
                ("sh.600019", "宝钢股份", 6.7, 0.3),
                ("sh.600028", "中国石化", 5.87, 2.09),
                ("sh.600029", "南方航空", 6.04, 0.33),
                ("sh.600030", "中信证券", 26.38, 1.66),
                ("sh.600031", "三一重工", 17.91, -1.49),
                ("sh.600036", "招商银行", 45.31, 1.43),
                ("sh.600048", "保利发展", 8.16, 0.49),
                ("sh.600050", "中国联通", 5.31, 0.0),
                ("sh.600056", "中国医药", 10.59, -0.28),
                ("sh.600061", "国投资本", 7.23, 1.69),
                ("sh.600104", "上汽集团", 16.04, 2.89),
                ("sh.600115", "中国东航", 4.04, 0.25),
                ("sh.600196", "复星医药", 25.76, -0.77),
                ("sh.600276", "恒瑞医药", 54.71, -0.76),
                ("sh.600309", "万华化学", 55.02, 0.71),
                ("sh.600340", "华夏幸福", 2.27, 0.89),
                ("sh.600438", "通威股份", 16.14, 1.13),
                ("sh.600487", "亨通光电", 15.37, 0.92),
                ("sh.600519", "贵州茅台", 1480.0, 0.34),
                ("sh.600536", "中国软件", 44.79, -0.02),
                ("sh.600547", "山东黄金", 30.15, 0.84),
                ("sh.600570", "恒生电子", 26.42, 0.46),
                ("sh.600585", "海螺水泥", 22.76, 0.18),
                ("sh.600588", "用友网络", 13.52, -1.6),
                ("sh.600600", "青岛啤酒", 73.14, 0.15),
                ("sh.600606", "绿地控股", 1.69, 0.6),
                ("sh.600690", "海尔智家", 25.15, 1.09),
                ("sh.600703", "三安光电", 12.08, 0.92),
                ("sh.600745", "闻泰科技", 32.65, -0.06),
                ("sh.600809", "山西汾酒", 177.1, 0.16),
                ("sh.600837", "海通证券", 8.5, -0.2),
                ("sh.600875", "东方电气", 16.49, -0.54),
                ("sh.600887", "伊利股份", 28.44, -0.39),
                ("sh.600893", "航发动力", 35.9, 1.61),
                ("sh.600900", "长江电力", 30.18, 0.5),
                ("sh.600941", "中国移动", 113.36, 0.04),
                ("sh.601012", "隆基绿能", 14.72, 2.94),
                ("sh.601088", "中国神华", 39.7, 0.13),
                ("sh.601111", "中国国航", 8.04, -0.62),
                ("sh.601138", "工业富联", 20.4, 1.19),
                ("sh.601166", "兴业银行", 23.98, 0.71),
                ("sh.601211", "国泰君安", 18.63, 0.65),
                ("sh.601229", "上海银行", 10.67, 0.38),
                ("sh.601288", "农业银行", 5.62, 0.0),
                ("sh.601318", "中国平安", 54.46, 1.93),
                ("sh.601328", "交通银行", 7.71, 0.13),
                ("sh.601360", "三六零", 10.31, 0.0),
                ("sh.601390", "中国中铁", 5.57, 0.72),
                ("sh.601398", "工商银行", 7.12, 0.28),
                ("sh.601601", "中国太保", 35.66, 2.24),
                ("sh.601628", "中国人寿", 40.68, 3.09),
                ("sh.601633", "长城汽车", 22.27, 0.27),
                ("sh.601668", "中国建筑", 5.72, 0.88),
                ("sh.601688", "华泰证券", 17.14, 1.96),
                ("sh.601800", "中国交建", 8.93, 1.13),
                ("sh.601857", "中国石油", 8.85, 1.49),
                ("sh.601878", "浙商证券", 10.75, 1.32),
                ("sh.601888", "中国中免", 61.38, 0.36),
                ("sh.601899", "紫金矿业", 18.66, 2.13),
                ("sh.601919", "中远海控", 16.02, 0.19),
                ("sh.601939", "建设银行", 8.92, -0.56),
                ("sh.601985", "中国核电", 9.35, -0.11),
                ("sh.601988", "中国银行", 5.43, -0.37),
                ("sh.603259", "药明康德", 65.05, 0.23),
                ("sh.603288", "海天味业", 41.73, 0.02),
                ("sh.603501", "韦尔股份", 127.03, 0.25),
                ("sh.603599", "广汇汽车", 11.43, 0.97),
                ("sh.603799", "华友钴业", 34.99, 3.31),
                ("sh.603993", "洛阳钼业", 7.73, 3.07),
                ("sh.688036", "传音控股", 74.79, -0.68),
                ("sh.688111", "金山办公", 279.85, 0.21),
                ("sh.688981", "中芯国际", 82.91, 0.72),
                ("sz.000001", "平安银行", 11.85, 0.34),
                ("sz.000002", "万科A", 6.57, -0.45),
                ("sz.000063", "中兴通讯", 32.09, 0.19),
                ("sz.000088", "盐田港", 4.67, -0.21),
                ("sz.000100", "TCL科技", 4.31, 1.17),
                ("sz.000333", "美的集团", 75.49, 0.59),
                ("sz.000538", "云南白药", 56.99, 0.69),
                ("sz.000568", "泸州老窖", 115.18, -0.09),
                ("sz.000651", "格力电器", 44.77, 0.27),
                ("sz.000725", "京东方A", 3.93, 0.77),
                ("sz.000750", "国元证券", 3.9, 1.56),
                ("sz.000776", "广发证券", 16.89, 2.8),
                ("sz.000786", "北新建材", 28.38, 0.53),
                ("sz.000858", "五粮液", 124.7, 0.25),
                ("sz.002007", "华兰生物", 16.4, 0.68),
                ("sz.002027", "分众传媒", 7.26, 0.14),
                ("sz.002142", "宁波银行", 26.86, 0.98),
                ("sz.002230", "科大讯飞", 48.1, 0.21),
                ("sz.002352", "顺丰控股", 46.9, 0.99),
                ("sz.002371", "北方华创", 416.75, -0.06),
                ("sz.002415", "海康威视", 28.12, -0.04),
                ("sz.002460", "赣锋锂业", 31.88, 2.34),
                ("sz.002475", "立讯精密", 31.97, 0.6),
                ("sz.002594", "比亚迪", 361.99, 2.51),
                ("sz.002673", "西部证券", 7.63, 1.33),
                ("sz.002714", "牧原股份", 44.38, 4.79),
                ("sz.002821", "凯莱英", 92.2, -2.35),
                ("sz.300059", "东方财富", 21.49, 2.48),
                ("sz.300122", "智飞生物", 19.79, -0.5),
                ("sz.300124", "汇川技术", 63.69, 0.84),
                ("sz.300223", "北京君正", 65.02, 0.49),
                ("sz.300274", "阳光电源", 64.19, 0.06),
                ("sz.300308", "中际旭创", 107.98, 0.19),
                ("sz.300347", "泰格医药", 52.56, -0.77),
                ("sz.300750", "宁德时代", 250.5, 3.03),
                ("sz.300759", "康龙化成", 25.06, -0.52),
                ("sz.300760", "迈瑞医疗", 237.32, 0.67),
                ("sz.399001", "深证成指", 10246.02, 0.83),
                ("sz.399006", "创业板指", 2061.87, 1.21),
                ("sz.399673", "创业板50", 2029.1, 1.3),
                ("sz.399905", "中证500", 5792.95, 0.61)
            ]
            cursor.executemany(
                "INSERT INTO stocks (code, name, price, change) VALUES (?, ?, ?, ?)",
                default_stocks
            )
        
        self.conn.commit()

    # 用户相关
    def get_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = {}
        for row in cursor.fetchall():
            user_dict = dict(row)
            username = user_dict["username"]
            # 为每个用户添加holdings字段
            user_dict["holdings"] = self.get_holdings(username)
            users[username] = user_dict
        return users

    def get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        if not row:
            return None
            
        user_dict = dict(row)
        # 添加holdings字段
        user_dict["holdings"] = self.get_holdings(username)
        return user_dict

    def authenticate_user(self, username, password):
        user = self.get_user(username)
        if user and user.get("password") == password:
            return user
        return None

    def validate_user(self, username, password):
        user = self.authenticate_user(username, password)
        if user:
            user_with_username = user.copy()
            user_with_username["username"] = username
            return user_with_username
        return None

    def user_exists(self, username):
        return self.get_user(username) is not None

    def register_user(self, username, password, user_type="普通用户", initial_balance=100000.0):
        if user_type == "普通用户":
            user_type = "user"
        elif user_type == "管理员":
            user_type = "admin"
        if self.user_exists(username):
            return False
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password, type, balance, created_at) VALUES (?, ?, ?, ?, ?)",
                       (username, password, user_type, initial_balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        return True

    def add_user(self, username, password, user_type="user", initial_balance=100000.0):
        if self.user_exists(username):
            return False, "用户名已存在"
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password, type, balance, created_at) VALUES (?, ?, ?, ?, ?)",
                       (username, password, user_type, initial_balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        return True, "用户添加成功"

    def update_user(self, username, data):
        user = self.get_user(username)
        if not user:
            return False, "用户不存在"
        
        # 处理持仓数据 (如果有)
        if "holdings" in data:
            # 这里不处理holdings，因为holdings已经单独存储在holdings表中
            del data["holdings"]
            
        update_fields = []
        update_values = []
        for key, value in data.items():
            if key != "username" and key != "holdings":
                update_fields.append(f"{key}=?")
                update_values.append(value)
        
        if not update_fields:
            return False, "无可更新字段"
            
        update_values.append(username)
        sql = f"UPDATE users SET {', '.join(update_fields)} WHERE username=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, update_values)
        self.conn.commit()
        return True, "用户信息更新成功"

    def delete_user(self, username):
        if not self.user_exists(username):
            return False, "用户不存在"
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        cursor.execute("DELETE FROM holdings WHERE username=?", (username,))
        cursor.execute("DELETE FROM transactions WHERE username=?", (username,))
        self.conn.commit()
        return True, "用户删除成功"

    # 股票相关
    def get_stocks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM stocks")
        return {row["code"]: dict(row) for row in cursor.fetchall()}

    def get_stock(self, code):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM stocks WHERE code=?", (code,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_stock(self, code, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO stocks (code, name, price, change)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET name=excluded.name, price=excluded.price, change=excluded.change
        ''', (code, data.get("name", code), data.get("price", 0), data.get("change", 0)))
        self.conn.commit()
        return True, "股票信息更新成功"

    # 持仓相关
    def get_holdings(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM holdings WHERE username=?", (username,))
        holdings = {}
        for row in cursor.fetchall():
            stock_code = row["stock_code"]
            name = row["name"]
            if not name:
                stock = self.get_stock(stock_code)
                name = stock["name"] if stock else stock_code
                
            holdings[stock_code] = {
                "name": name,
                "quantity": row["quantity"],
                "cost": row["cost"]
            }
        return holdings

    def update_holding(self, username, stock_code, quantity, cost, name=None):
        cursor = self.conn.cursor()
        if name is None:
            stock = self.get_stock(stock_code)
            name = stock["name"] if stock else stock_code
        
        # 如果数量为0，删除持仓
        if quantity <= 0:
            self.delete_holding(username, stock_code)
            return
            
        cursor.execute('''
            INSERT INTO holdings (username, stock_code, quantity, cost, name)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(username, stock_code) DO UPDATE SET quantity=excluded.quantity, cost=excluded.cost, name=excluded.name
        ''', (username, stock_code, quantity, cost, name))
        self.conn.commit()

    def delete_holding(self, username, stock_code):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM holdings WHERE username=? AND stock_code=?", (username, stock_code))
        self.conn.commit()

    # 交易记录相关
    def record_transaction(self, username, transaction_type, stock_code, stock_name, price, quantity, amount):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (username, type, stock_code, stock_name, price, quantity, amount, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, transaction_type, stock_code, stock_name, price, quantity, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        return True, "交易记录保存成功"

    def get_user_transactions(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE username=? ORDER BY timestamp", (username,))
        return [dict(row) for row in cursor.fetchall()]

    # 交易执行
    def execute_trade(self, username, transaction_type, stock_code, quantity):
        user = self.get_user(username)
        stock = self.get_stock(stock_code)
        
        if not user:
            return False, "用户不存在"
        
        if not stock:
            return False, "股票不存在"
            
        price = stock["price"]
        amount = price * quantity
        holdings = self.get_holdings(username)
        
        if transaction_type == "buy":
            if user["balance"] < amount:
                return False, "余额不足"
                
            # 更新用户余额
            user_balance = user["balance"] - amount
            self.update_user(username, {"balance": user_balance})
            
            # 更新持仓
            if stock_code in holdings:
                old_quantity = holdings[stock_code]["quantity"]
                old_cost = holdings[stock_code]["cost"]
            else:
                old_quantity = 0
                old_cost = 0
                
            new_quantity = old_quantity + quantity
            new_cost = (old_cost * old_quantity + amount) / new_quantity if new_quantity > 0 else 0
            
            # 更新或添加持仓
            self.update_holding(username, stock_code, new_quantity, new_cost, stock["name"])
            
        elif transaction_type == "sell":
            if stock_code not in holdings or holdings[stock_code]["quantity"] < quantity:
                return False, "持仓不足"
                
            # 更新用户余额
            user_balance = user["balance"] + amount
            self.update_user(username, {"balance": user_balance})
            
            # 更新持仓
            new_quantity = holdings[stock_code]["quantity"] - quantity
            new_cost = holdings[stock_code]["cost"]  # 卖出不改变成本价
            
            # 如果持仓为0，删除该股票持仓
            if new_quantity <= 0:
                self.delete_holding(username, stock_code)
            else:
                self.update_holding(username, stock_code, new_quantity, new_cost, stock["name"])
        else:
            return False, "交易类型无效"
            
        # 记录交易
        self.record_transaction(username, transaction_type, stock_code, stock["name"], price, quantity, amount)
        return True, "交易成功"

# 创建数据库实例
db = Database() 
