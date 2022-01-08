# -- coding:UTF-8 --
import pymysql
import datetime
from pymysql.converters import escape_string
import re
import sys

import constant_value

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='wechat',
    charset='utf8mb4',
    port=3306)

cursor = conn.cursor()
count_sql = "select max(msgid) msgid from wechat.message;"
cursor.execute(count_sql)
count = cursor.fetchone()
print(count[0])

for row in range(0, count[0]):
    qry_sql = "SELECT type, isSend, createTime, talker, content FROM wechat.message WHERE msgId = {0}".format(row)
    n = cursor.execute(qry_sql)
    if n > 0:
        row_data = cursor.fetchone()
        if row_data is not None and row_data[3] == 'wxid_fbthette9f7211':
            if row_data[1] == 0:
                send_user = constant_value.b
            else:
                send_user = constant_value.j

            if row_data[0] == 1 and isinstance(row_data[4], str):
                    try:
                        insert_sql = "INSERT INTO wechat.LOG(USER,DATETIME,CONTENT,type) VALUES ('{0}','{1}' ,'{2}', '{3}')".format(
                            send_user, datetime.datetime.fromtimestamp(row_data[2] / 1000),
                            escape_string(row_data[4]), 1)
                        cursor.execute(insert_sql)
                        # print(insert_sql)
                    except AssertionError:
                        print(row, row_data[0], row_data[1], row_data[2], row_data[3], row_data[4])
            else:
                try:
                    insert_sql = "INSERT INTO wechat.LOG(USER,DATETIME,type) VALUES ('{0}','{1}' ,'{2}')".format(
                        send_user, datetime.datetime.fromtimestamp(row_data[2] / 1000), row_data[0])
                    cursor.execute(insert_sql)
                    # print(insert_sql)
                except AssertionError:
                    print(row, row_data[0], row_data[1], row_data[2], row_data[3])


conn.commit()
cursor.close()
conn.close()
