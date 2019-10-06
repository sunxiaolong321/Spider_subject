# 导入数据到mysql
def to_mysql(data):
    import pymysql
    from ..settings import mysql_config
    # 建立mysql连接
    connection = pymysql.connect(host=mysql_config["host"], port=mysql_config["port"],
                                 user=mysql_config["user"], password=mysql_config["password"],
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("连接mysql成功")

    cursor = connection.cursor()

    # 创建数据库，如果数据库不存在
    cursor.execute("show databases")

    db = mysql_config["db"].lower()

    # 判断表格是否存在
    flag = 0
    if db in [db["Database"] for db in cursor.fetchall()]:
        print("数据库已存在，切换到当前数据库")
        connection.select_db(mysql_config["db"])
        cursor.execute("show tables")
        for tables in cursor.fetchall():
            if mysql_config["table"] in [table for table in tables.values()]:
                print("表格已经存在")
                flag = 1
    else:
        print("数据库不存在，创建成功")
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % mysql_config["db"])
        connection.select_db(mysql_config["db"])
    create_sql = ""

    if flag == 0:
        insert_key = data[0]
        for key, value in insert_key.items():
            if isinstance(value, int):
                create_sql += "%s INT," % key
            elif isinstance(value, float):
                create_sql += "%s FLOAT," % key
            elif isinstance(value, str):
                create_sql += "%s VARCHAR(40)," % key
            elif isinstance(value, list):
                create_sql += "%s VARCHAR(40)," % key
            else:
                print(key, value)

        sql = "CREATE TABLE %s (%s)" % (mysql_config["table"], create_sql[:-1])
        # print(sql)
        cursor.execute(sql)
        print("创建表格成功")

    cols = ", ".join('`{}`'.format(k) for k in data[0].keys())
    val_cols = ", ".join('%({})s'.format(k) for k in data[0].keys())

    sql = "insert into {}(%s) values(%s)".format(mysql_config["table"])
    res_sql = sql % (cols, val_cols)

    for count in range(0, len(data)):
        for key, value in data[count].items():
            if isinstance(value, list):
                data[count][key] = ", ".join(value)

    # 设置中文编码方式，不然就出现
    # pymysql.err.DataError: (1406, "Data too long for column 'url' at row 1")
    try:
        print("正在插入数据")
        cursor.executemany(res_sql, data)
        connection.commit()
    except:
        print("发生错误，导入失败")
        connection.rollback()
    cursor.close()
    connection.close()


class to_mongo():

    def __init__(self):
        from ..settings import db_config
        self.host = db_config["host"]
        self.port = db_config["port"]
        self.db = db_config["db"]
        self.table = db_config["table"]

    def mongodb_connection(self):
        import pymongo
        print("正在连接mongodb数据库")
        myclient = pymongo.MongoClient(
            "mongodb://%s:%s/" % (self.host, self.port))
        self.myclient = myclient

    def save(self, data):
        print("连接成功")
        dblist = self.myclient.list_database_names()
        if self.db in dblist:
            print("数据库已存在！")
        else:
            print("数据库不存在，新建数据库")

        mydb = self.myclient[self.db]
        mycol = mydb[self.table]
        # 插入字典为列表包裹的字典类型数据
        x = mycol.insert_many(data)
        print("插入成功")

    # 选择数据库


def to_csv(data):
    import csv
    from settings import localpath
    with open(localpath, 'a+', encoding="utf8", newline="") as f:       # 采用b的方式处理可以省去很多问题

        with open(localpath, "r",encoding="utf8",newline="")as e:
            reader = csv.reader(e)
            if not [row for row in reader]:
                cw = csv.DictWriter(f, fieldnames=[title for title in data[0]])
                cw.writeheader()
            else:
                cw = csv.DictWriter(f, fieldnames=[title for title in data[0]])
        cw.writerows(data)
    print("保存本地成功")


def database_select(data):

    from settings import database

    from sys import exit
    if database == 1:
        to_mysql(data)
    elif database == 2:
        connection = to_mongo()
        connection.mongodb_connection()
        connection.save(data)
    elif database == 3:
        to_csv(data)
    else:
        print("选择错误，正在出程序")
        exit()
