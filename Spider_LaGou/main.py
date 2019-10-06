from settings import headers, keyword, pages, params, url
from src.gethtml import url_post
from src.parsedata import parse_data
from src.savedata import database_select


def main():
    for page in range(1, pages+1):
        data = url_post(url, page, headers, params, keyword)
        format_data = parse_data(data, url)
        database_select(format_data)
    print('全部操作成功')


if __name__ == "__main__":
    main()
