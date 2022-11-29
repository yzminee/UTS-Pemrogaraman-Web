import mysql.connector


def get_mysql_connection():
    return mysql.connector.connect(user='root', host='localhost', port=3306, password='', database='sekolah_2')
