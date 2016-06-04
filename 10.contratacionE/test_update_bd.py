import sys
import datetime 
import traceback
import pymysql

    
def main():
    
    conn = pymysql.connect(host='localhost', port=3306, user='pce', passwd='pce', db='pce')

    cur = conn.cursor()
    
    cur.execute('SELECT * FROM pce_cargas WHERE num_exp = 1')
    resultado = cur.fetchall()
    
    for row in resultado:
        print("Year=%s, min=%s, numexp=%d" % (row[0], row[1],row[2]))
        ini = datetime.date(int(row[0]), 1, 1).strftime("%d-%m-%Y")
        fin = datetime.date(int(row[0]), 12, 31).strftime("%d-%m-%Y")

        print(ini,fin)
        
        sql_stm = "UPDATE pce_cargas set num_exp = %s WHERE year=%s and id_min=%s"
        cur.execute(sql_stm, (2,row[0],row[1]))
        conn.commit()

        
        
        
    conn.close()

if __name__ == "__main__":
    sys.exit(main())