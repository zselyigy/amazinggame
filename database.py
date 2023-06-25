import mysql.connector
from mysql.connector import Error

def dbconnect():
    try:
        connection = mysql.connector.connect(host='sql210.infinityfree.com ',
                                            database='if0_34493097_hiscores',
                                            user='if0_34493097',
                                            password='ztQiUZJ8S1r')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #         print("MySQL connection is closed")
