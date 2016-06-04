import sys
import datetime 
import traceback
import ujson
import pymysql

import pce_Principal

ministry={
                6: 'MAGRAMA',
                7: 'MAExCoop',
                8: 'MDEfensa',
                9: 'MINECO',
                10: 'MEDCD',
                11: 'MESS',
                12: 'MFOM',
                13: 'MINHAP',
                14: 'MINET',
                15: 'MINJUS',
                16: 'MINPRES',
                17: 'MSSSI',
                18: 'MinTraInm',
                19: 'MinInt',
                20: 'Presidencia Gobierno'
}

log_file = "cargaInicial.log"


def log2file(log_str):

    str2w = str(datetime.datetime.now()).split('.')[0] + " - " + log_str +"\n"
    f = open(log_file, 'a')
#    print(str2w,file=f)
    f.write(str2w)

    f.close()  
    
def main():
    
    conn = pymysql.connect(host='localhost', port=3306, user='pce', passwd='pce', db='pce')

    cur = conn.cursor()
    
    cur.execute('SELECT * FROM pce_cargas WHERE num_exp = 0')
    resultado = cur.fetchall()
    
    for row in resultado:
#        print("Year=%s, min=%s, numexp=%d" % (row[0], row[1],row[2]))
        ini = datetime.date(int(row[0]), 1, 1).strftime("%d-%m-%Y")
        fin = datetime.date(int(row[0]), 12, 31).strftime("%d-%m-%Y")

#        print(ini,fin)
        
        try:
            nreg=pce_Principal.main(2, row[1],ini,fin)
            if nreg == 0:
                nreg = 1
            log2file('Procesado '+row[0] + " - " +row[1]+" num.reg.:"+str(nreg))  
            sql_stm = "UPDATE pce_cargas set num_exp = %s WHERE year=%s and id_min=%s"
            cur.execute(sql_stm, (nreg,row[0],row[1]))

            conn.commit()
        except:
            var = traceback.format_exc()
            log2file("Error inesperado"+ var)
        
        
        
    conn.close()

if __name__ == "__main__":
    sys.exit(main())