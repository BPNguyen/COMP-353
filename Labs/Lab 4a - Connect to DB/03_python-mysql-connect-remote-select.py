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
            #cursor = conn.cursor()
            cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course")
 
        row = cursor.fetchone()
 
        while row is not None:
            print(row)
            #print(row[1])
            print(row['courseName'])
            row = cursor.fetchone()
 
    
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    connect()
