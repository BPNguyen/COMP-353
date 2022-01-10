from flask import Flask
app = Flask(__name__)

@app.route('/')

def hello():
    import mysql.connector
    from mysql.connector import Error
    ''' Connect to MySQL database '''
    try:
        conn = mysql.connector.connect(host='45.55.59.121',
                                       database='COMP453Remote',
                                       user='453RemoteUser',
                                       password='student453')
        if conn.is_connected():
            cursor = conn.cursor()
        else:
            return('problem')
        cursor.execute("SELECT * FROM user")
        
        row = cursor.fetchone()
        returnString=str(row)
        
 
     
        while row is not None:
            print(row)
            returnString+="<br/>" + str(row) + '<br/>' + str(row[2])
            row = cursor.fetchone()
        return(returnString)
    
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
    return('after finally')
