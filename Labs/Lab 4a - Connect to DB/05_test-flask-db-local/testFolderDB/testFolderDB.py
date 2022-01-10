from flask import Flask
app = Flask(__name__)

@app.route('/')

def hello():
    import mysql.connector
    from mysql.connector import Error
    ''' Connect to MySQL database '''
    try:
        conn = mysql.connector.connect(host='localhost',
                                       port='8889',
                                       database='company',
                                       user='bri4nnguy3n',
                                       password='26049569')
        if conn.is_connected():
            cursor = conn.cursor()
        else:
            return('problem')
        cursor.execute("SELECT * FROM user")
        
        row = cursor.fetchone()
        returnString=str(row)
        
 
     
        while row is not None:
            print(row)
            returnString+="<br/>" + str(row)
            row = cursor.fetchone()
        return(returnString)
    
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
    return('after finally')
