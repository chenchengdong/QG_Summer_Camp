import pandas as pd
from pandas.io import sql
import json
import pymysql
from sqlalchemy import create_engine


def data_save():
    book_list = []
    with open('./data/BookInformation.json', 'r', encoding='utf-8') as f:
        for line in f:
            book = json.loads(s=line)
            book['review'] = str(book['review'])
            book['publishHouse'] = '未知'
            book['pointCount'] = 0
            book_list.append(book)
        book_df = pd.DataFrame(book_list)
        # bookDf = bookDf.applymap(str)
        book_df.to_csv('./data/BookInformation.csv', encoding='utf-8')
        try:
            conn = create_engine('mysql+pymysql://root:3751ueoxjwgixjw3913@39.98.41.126:3306/book_management', encoding='utf-8')
            pd.io.sql.to_sql(book_df, "library", conn, if_exists='append', index=True)
            print("成功写入数据库！")
        except Exception as e:
            print(e)


