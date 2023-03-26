# import base64
import re
from Crypto.Cipher import AES
from binascii import (b2a_hex, a2b_hex)
import json
import datetime
from json import JSONEncoder
# from django.core import serializers
from django.db import connection

AES_LENGTH = 16


class AEScoder():

    def __init__(self):
        key = "0123456789123456"
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        a = b2a_hex(self.ciphertext)
        b = str(a, 'utf-8')
        return b

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        # return plain_text.rstrip('\0')
        a = bytes.decode(plain_text).rstrip('\0')
        return a


class mysql():
    def dict_proc_all(sql, params):
        cursor = connection.cursor()
        cursor.callproc(sql, params)
        mydata = cursor.fetchall()
        cursor.close()
        data = myjson.dict_json(mydata)
        return data

    def dict_proc_one(sql, params):
        cursor = connection.cursor()
        cursor.callproc(sql, params)
        mydata = cursor.fetchone()
        cursor.close()
        data = myjson.dict_json(mydata)
        return data


class myjson():
    def dict_json(mydata):
        datas = [entry for entry in mydata]
        datas = list(datas)
        data = json.dumps(datas, ensure_ascii=False)
        return data


def mytupleToDic(mytuple):
    dic = {}
    for i in mytuple:
        dic[int(i[0])] = i[1]
    return dic


class mychoices():
    pass


# Override the default method
class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class IDCardChecker:

    def __init__(self, card_num):
        self.card_num = card_num

    def is_valid(self):
        regex = r"^[1-9]\d{5}(19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
        if not re.match(regex, self.card_num):
            return False
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        sum_num = 0
        for i in range(17):
            sum_num += int(self.card_num[i]) * weight[i]
        check_num = check_code[sum_num % 11]
        if check_num == self.card_num[-1]:
            return True
        else:
            return False

    def get_gender(self):
        gender_num = int(self.card_num[-2])
        if gender_num % 2 == 0:
            return '女'
        else:
            return '男'

    def get_age(self):
        year = int(self.card_num[7:10])
        month = int(self.card_num[11:12])
        age = 1 - year
        if month >= 8:
            age += 1
        return age

    def get_birthday(self):
        return self.card_num[6:14]

    def get_province(self):
        province_code = {11: '北京', 12: '天津', 13: '河北', 14: '山西', 15: '内蒙古',
                         21: '辽宁', 22: '吉林', 23: '黑龙江', 31: '上海', 32: '江苏',
                         33: '浙江', 34: '安徽', 35: '福建', 36: '江西', 37: '山东',
                         41: '河南', 42: '湖北', 43: '湖南', 44: '广东', 45: '广西',
                         46: '海南', 50: '重庆', 51: '四川', 52: '贵州', 53: '云南',
                         54: '西藏', 61: '陕西', 62: '甘肃', 63: '青海', 64: '宁夏',
                         65: '新疆', 71: '台湾', 81: '香港', 82: '澳门', 91: '国外'}
        if self.is_valid():
            return province_code[int(self.card_num[:2])]
        else:
            return '不是中国公民身份证号码'

    def get_region(self):
        return self


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
    except (TypeError, ValueError):
        pass

    return False
