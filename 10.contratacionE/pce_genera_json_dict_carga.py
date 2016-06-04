import sys
import ujson
import pymysql


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

cargas_file = "cargas.json"

    
def main():

    cargas={}
    conn = pymysql.connect(host='localhost', port=3306, user='pce', passwd='pce', db='pce')

    cur = conn.cursor()

    
    for year in range(2011,2016):

        for min in sorted(ministry.keys()):
            cargas[year,min]=0            
            cur.execute("INSERT INTO pce_cargas(year, id_min, num_exp) VALUES ("+str(year)+","+str(min)+",0)")
            conn.commit()

#    print(cargas)            

#    with open(cargas_file, 'w') as fp:
#        ujson.dump(cargas, fp)
    
    
if __name__ == "__main__":
    sys.exit(main())