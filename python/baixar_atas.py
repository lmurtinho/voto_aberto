# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:10:49 2016

@author: lucas_000
"""

from bs4 import BeautifulSoup

nomes_meses = ["Janeiro", "Fevereiro", "Março", "Abril", 
               "Maio", "Junho", "Julho", "Agosto",
               "Setembro", "Outubro", "Novembro", "Dezembro"]

def ler_links(site, ano=None):
    