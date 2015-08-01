# PCE - Plataforma Contratación del Estado

Extracción de datos de https://contrataciondelestado.es/

En fase MUY INICIAL
Solo obtiene los datos basicos del contrato.

##Programa principal
se ejecuta:

   python  pce_Principal.py  driverType(1=Firefox, online / 2=phantomjs) ministry(6..20) fini(dd-mm-aaaa) ffin (dd-mm-aaaa)')
   
   p.ej: 
   
   pce_Principal.py  2 6 01-01-2015 31-01-2015  
   
   Obtendría los contratos del MAGRAMA publicados en enero de 2015. y lo haría con el driver de phantomjs (en fondo)
   
   Necesita las siguientes librerías:
   *   **BeautifulSoup** (http://www.crummy.com/software/BeautifulSoup/)
   *   **Selenium** (http://docs.seleniumhq.org/)
   *  phantomjs  (http://phantomjs.org/) -- Solamente si se utiliza el driver 2
   *  peewee (https://pypi.python.org/pypi/peewee) -- 
   

##clase Contratos() en pce_extrae_contratos
Al instanciar esta clase ( con los mismos parámetros que el programa principal) en Contratos.expedientes[]  quedan las líneas de expedientes tal y como están en la página web
   
