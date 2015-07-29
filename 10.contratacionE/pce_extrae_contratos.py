# coding=utf-8

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


#Clase que devuelve los contratos de n ministerio entre unas fechas usando el dirver que se indique 
class Contratos():

    driver = webdriver()
    def __init__(self, driverType=1, ministry=17, fIni='01-01-2015',ffin='30-06-2015'):
        if driverType==1:
            self.driver  = webdriver.Firefox()
        else:   
            self.driver = webdriver.PhantomJS("/home/jmartinpit/phantomjs/bin/phantomjs")
            driver.set_window_size(1120, 550)

    def extraeContratos(table):
        f = open('tablaContratos.txt', 'a')
        for row in table.findAll("tr"):
          f.write(row.encode("UTF-8")+ "\n")
        f.close()
        
