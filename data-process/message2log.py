# -- coding:UTF-8 --
import pymysql
import datetime
from pymysql.converters import escape_string
import yaml

config_file = open("config.yaml", 'r', encoding='utf-8')
cfg = yaml.load(config_file.read(), Loader=yaml.FullLoader)
host = cfg.get('database').get('host')
user = cfg.get('database').get('user')
pwd = str(cfg.get('database').get('password'))
db = cfg.get('database').get('db')
charset = cfg.get('database').get('charset')
port = cfg.get('database').get('port')
talkerID = cfg.get('userinfo').get('talkerID')
sender_name = cfg.get('userinfo').get('sendername')
receiver_name = cfg.get('userinfo').get('receivername')

conn = pymysql.connect(
    host=host,
    user=user,
    password=pwd,
    db=db,
    charset=charset,
    port=port)

cursor = conn.cursor()
count_sql = "SELECT max(msgid) msgid FROM message;"
cursor.execute(count_sql)
count = cursor.fetchone()
print(count[0])

for row in range(0, count[0]):
    qry_sql = "SELECT type, isSend, createTime, talker, content FROM message WHERE msgId = {0}".format(row)
    n = cursor.execute(qry_sql)
    if n > 0:
        row_data = cursor.fetchone()
        if row_data is not None and row_data[3] == talkerID:
            if row_data[1] == 0:
                send_user = receiver_name
            else:
                send_user = sender_name

            if row_data[0] == 1 and isinstance(row_data[4], str):
                try:
                    insert_sql = "INSERT INTO log(user, datetime, content, type) " \
                                 "VALUES ('{0}', '{1}', '{2}', '{3}')".format(
                        send_user, datetime.datetime.fromtimestamp(row_data[2] / 1000),
                        escape_string(row_data[4]), 1)
                    cursor.execute(insert_sql)
                    # print(insert_sql)
                except AssertionError:
                    print(row, row_data[0], row_data[1], row_data[2], row_data[3], row_data[4])
            else:
                try:
                    insert_sql = "INSERT INTO log(user, datetime, type) VALUES ('{0}', '{1}', '{2}')".format(
                        send_user, datetime.datetime.fromtimestamp(row_data[2] / 1000), row_data[0])
                    cursor.execute(insert_sql)
                    # print(insert_sql)
                except AssertionError:
                    print(row, row_data[0], row_data[1], row_data[2], row_data[3])

conn.commit()
cursor.close()
conn.close()
