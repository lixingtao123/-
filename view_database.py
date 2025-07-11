import sqlite3
import os

# 数据库路径
DB_PATH = 'data/stock_simulator.db'

# 检查数据库是否存在
if not os.path.exists(DB_PATH):
    print(f"错误: 数据库文件不存在 - {DB_PATH}")
    exit(1)

# 连接数据库
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
cursor = conn.cursor()

# 查看所有表
print("\n===== 数据库表 =====")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
for table in tables:
    print(f"- {table}")

# 查看用户表
print("\n===== 用户表 (users) =====")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print(f"总用户数: {len(users)}")
if users:
    # 打印表头
    print(f"{'用户名':<15} {'类型':<10} {'余额':<12} {'创建时间':<20}")
    print("-" * 60)
    # 打印数据
    for user in users:
        print(f"{user['username']:<15} {user['type']:<10} {user['balance']:<12.2f} {user['created_at']:<20}")

# 查看持仓表
print("\n===== 持仓表 (holdings) =====")
cursor.execute("SELECT * FROM holdings")
holdings = cursor.fetchall()
print(f"总持仓数: {len(holdings)}")
if holdings:
    # 打印表头
    print(f"{'用户名':<15} {'股票代码':<15} {'股票名称':<15} {'数量':<10} {'成本':<10}")
    print("-" * 70)
    # 打印数据
    for holding in holdings:
        print(f"{holding['username']:<15} {holding['stock_code']:<15} {holding['name']:<15} {holding['quantity']:<10} {holding['cost']:<10.2f}")

# 查看股票表
print("\n===== 股票表 (stocks) =====")
cursor.execute("SELECT * FROM stocks")
stocks = cursor.fetchall()
print(f"总股票数: {len(stocks)}")
if stocks:
    # 打印表头
    print(f"{'代码':<15} {'名称':<15} {'价格':<10} {'涨跌幅':<10}")
    print("-" * 60)
    # 打印前10条数据
    for i, stock in enumerate(stocks):
        if i >= 10:  # 只显示前10条
            print("... (更多)")
            break
        print(f"{stock['code']:<15} {stock['name']:<15} {stock['price']:<10.2f} {stock['change']:<10.2f}")

# 查看交易记录表
print("\n===== 交易记录表 (transactions) =====")
cursor.execute("SELECT COUNT(*) FROM transactions")
count = cursor.fetchone()[0]
print(f"总交易记录数: {count}")

if count > 0:
    # 打印表头
    print(f"{'用户名':<10} {'类型':<6} {'股票代码':<12} {'股票名称':<12} {'价格':<8} {'数量':<8} {'金额':<12} {'时间':<20}")
    print("-" * 90)
    
    # 打印最近10条交易记录
    cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 10")
    transactions = cursor.fetchall()
    for tx in transactions:
        print(f"{tx['username']:<10} {tx['type']:<6} {tx['stock_code']:<12} {tx['stock_name']:<12} {tx['price']:<8.2f} {tx['quantity']:<8} {tx['amount']:<12.2f} {tx['timestamp']:<20}")
    
    if count > 10:
        print("... (更多)")

# 关闭连接
conn.close()
print("\n数据库查询完成!") 