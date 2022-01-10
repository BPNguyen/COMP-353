import mysql.connector
from mysql.connector import Error
 
 
def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='45.55.59.121',
                                       database='COMP453Remote',
                                       user='453RemoteUser',
                                       password='student453')
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    connect()
