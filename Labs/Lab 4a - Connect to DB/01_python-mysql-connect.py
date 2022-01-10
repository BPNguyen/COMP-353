import mysql.connector
from mysql.connector import Error
 
 
def connect():
    """ Connect to MySQL database """
    try:
        print ('inside')
        conn = mysql.connector.connect(host='localhost',
                                       port='8889',
                                       database='company',
                                       user='bri4nnguy3n',
                                       password='26049569')
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print('*************',e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    connect()
