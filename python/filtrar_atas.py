# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 22:33:21 2016

@author: lucas_000
"""

import os
import re
from txt_to_html import arquivos

diretorio = "E:/Dropbox/voto_aberto/atas_limpas"

def filtro_inicio_arquivo(diretorio, arquivos, inicio):
    """
    Retorna todos os arquivos de uma lista de arquivos
    cujo nome comece com o início.
    """
    filtrados = {}
    diretorio_atual = os.getcwd()
    os.chdir(diretorio)
    for arquivo in arquivos:
        if arquivo.startswith(inicio):
            with open(arquivo, 'r') as f:
                texto = f.read()
            nome = os.path.splitext(arquivo)[0]
            filtrados[nome] = texto
    os.chdir(diretorio_atual)
    return filtrados

def filtro_string(atas, regex):
    return {nome: atas[nome] for nome in atas
            if re.findall(regex, atas[nome])}

arquivos_txt = arquivos(diretorio, 'txt')
#atas_votos = filtro_string(diretorio, arquivos_txt, r'vota[ram|ção]')
atas_2016 = filtro_inicio_arquivo(diretorio, arquivos_txt, '2015')
votos_2016 = filtro_string(atas_2016, r'vota[ram|ção]')

# próximo passo: filtrar por ano (4 primeiros dígitos do nome do arquivo)

