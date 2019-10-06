# 爬取网站
from fake_useragent import UserAgent
url = "https://www.lagou.com/jobs/"

# 设置虚拟ua
ua = UserAgent()

# 浏览器信息

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": ua.random,
}

# 构造体，需要时启用
params = {
    # 必选项，选择项为default和new
    "px": "default",    # 默认结果或者最新结果

    # 可选项，选择项全职和实习
    "gx": "实习",   # 工作性质，是否为全职工作

    # "city": "北京",  # 所在城市
    # "district": "徐汇区",     # 招聘所在市区

    # 可选项，应届毕业生，3年及以下，3-5年，5-10年，10年以上，不要求
    # "gj": "",  # 工作经验

    # 可选项，未融资，天使轮，A轮，B轮，C轮，D轮及以上，上市公司，不需要融资
    # "jd": "天使轮",  # 融资阶段

    # 可选项，少于15人，15-50人，50-150人，150-500人，500-2000人，2000人以上
    # "gm": "少于15人",  # 公司规模

    # 如果不进行筛选默认注释，选项有2k以下，2k到5k,5k到10k，10k到15k，15k到25k，25k到50k，50k以上
    # "yx": "2k以下",   # 月薪

    # 可选项，学历要求，分为大专，本科，硕士，博士，不要求
    "xl": "本科",   # 学历要求

    #  可选项，选项包括移动互联网，电商，金融，企业服务，教育，文娱|内容，游戏，消费生活，硬件
    # "hy": "移动互联网",  # 行业领域

    # 必选项
    "isSchoolJob": "1",  # 是否为实习生工作
}


# 爬取页数
pages = 3

# 关键词
keyword = "数据分析"

# 1 MySQL 2 MongoDB
database = 3

# 启用MySQL config
mysql_config = {
    "host": "127.0.0.1",    # 连接主机
    "port": 3306,   # 连接端口
    "user": "root",  # 用户名
    "password": "",  # 密码
    "db": "",  # 连接数据库
    "table": "",  # 连接表格
}

# 启用MongoDB config
db_config = {
    "host": "127.0.0.1",    # 连接主机
    "port": "27017",    # 连接端口
    "user": "root",     # 用户名
    "db": "",   # 数据库
    "table": "",    # 表格
}

# 启用保存为csv
localpath = "jobs.csv"