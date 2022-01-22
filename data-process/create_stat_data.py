import pymysql
import yaml
import json

config_file = open("config.yaml", 'r', encoding='utf-8')
cfg = yaml.load(config_file.read(), Loader=yaml.FullLoader)
host = cfg.get('database').get('host')
user = cfg.get('database').get('user')
pwd = str(cfg.get('database').get('password'))
db = cfg.get('database').get('db')
charset = cfg.get('database').get('charset')
port = cfg.get('database').get('port')

conn = pymysql.connect(
    host=host,
    user=user,
    password=pwd,
    db=db,
    charset=charset,
    port=port)

cursor = conn.cursor()

data_json = {}
data = json.loads(json.dumps(data_json))

# 总条数
count_sql = "select count(*) from log;"
cursor.execute(count_sql)
count = cursor.fetchone()
data['count'] = count[0]

# 图片数目
count_img_sql = "select count(*) from log where type = 3;"
cursor.execute(count_img_sql)
count_img = cursor.fetchone()
data['imgCount'] = count_img[0]

# 语音数目
count_voice_sql = 'select count(*) from log where type = 34;'
cursor.execute(count_voice_sql)
count_voice = cursor.fetchone()
data['voiceCount'] = count_voice[0]

# 词汇数目
love_word = ['爱你', '想你', '晚安']
love_word_data = {}
for word in love_word:
    love_word_sql = "select count(*) from log where content like '%{0}%'".format(word)
    cursor.execute(love_word_sql)
    count_love_word = cursor.fetchone()
    love_word_data[word] = count_love_word[0]
data['loveWord'] = love_word_data

# 最长消息
count_longest_msg = "select content, datetime from log where length(content) = (select max(length(content)) from log);"
cursor.execute(count_longest_msg)
longest_msg = cursor.fetchone()
longest_msg_data = {'content': longest_msg[0], 'time': str(longest_msg[1])}
data['longMsg'] = longest_msg_data

# 最晚消息
count_latest_msg = "select content, user, datetime, DATE_FORMAT(datetime, '%l') as h from log " \
                   "where DATE_FORMAT(datetime, '%H') <= 5 and type = 1 " \
                   "order by DATE_FORMAT(datetime, '%H%i%s') desc;"
cursor.execute(count_latest_msg)
latest_msg = cursor.fetchone()
latest_msg_data = {'content': latest_msg[0], 'user': latest_msg[1], 'time': str(latest_msg[2]), 'hour': latest_msg[3]}
data['latestMsg'] = latest_msg_data

# 最多词汇
# 需要经过分词之后才能得到


# 月消息统计
month_data_arr = []
count_month_data_sql = "select count(id), date_format(datetime,'%c') as m from log group by m;"
cursor.execute(count_month_data_sql)
month_datas = cursor.fetchall()
for month_data in month_datas:
    month_data_arr.append([int(month_data[1]), int(month_data[0])])
data['monthGroup'] = month_data_arr


# 日常消息统计
hour_data_arr = []
count_hour_data_sql = "select count(id), CAST(date_format(datetime,'%k') as  UNSIGNED ) as h from log " \
                      "group by h order by h;"
cursor.execute(count_hour_data_sql)
hour_datas = cursor.fetchall()
for hour_data in hour_datas:
    hour_data_arr.append([int(hour_data[1]), int(hour_data[0])])
data['hourGroup'] = hour_data_arr


with open('data.json', 'w+', encoding='utf-8') as dj:
    dj.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')))






















