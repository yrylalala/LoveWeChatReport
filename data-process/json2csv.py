# -- coding:UTF-8 --
import csv
import json

with open('./result.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)

words = json_data['word']

with open("test.csv", "w", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)

    # 先写入columns_name
    # writer.writerow(["单词", "词频"])
    # 写入多行用writerows
    for word in words:
        # print(word["word"])
        # print(word["count"])
        writer.writerow([word["word"], str(word["count"])])
