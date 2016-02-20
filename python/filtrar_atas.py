# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 22:33:21 2016

@author: lucas_000
"""

import itertools
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

def pegar_votantes(votos):
    sessoes_com_voto = [re.findall(r'(?:votou|votaram) (.*?) o[s]? (?:Senhor|Senhores) (?:Vereador|Vereadores) (.*?) \((.*?)\)', 
                        votos_2015[ata]) 
               for ata in sorted(list(votos))]
    votantes = []
    for sessao in sessoes_com_voto:
        for voto in sessao:
            if ',' in voto[1]:
                votantes.append(re.findall(r'(\b.*?),', voto[1]) + re.findall(' e (.*)$', voto[1]))
            elif ' e ' in voto[1]:
                votantes.append(voto[1].split(' e '))
            else:
                votantes.append(voto[1])
    return votantes

arquivos_txt = arquivos(diretorio, 'txt')
atas_2015 = filtro_inicio_arquivo(diretorio, arquivos_txt, '2015')
votos_2015 = filtro_string(atas_2015, r'votaram|votação')

#voto_regex = re.compile(r"""(?:votou|votaram) 
#                          (.*?) # matéria do voto
#                          o[s]? #
#                          (?:Senhor|Senhores) #
#                          (?:Vereador|Vereadores) #
#                          (.*?) # vereadores votantes 
#                          \(#
#                          (.*?)# número de votantes
#                          \)""", re.X)
#votaram2 = [re.findall(voto_regex, votos_2015[ata])
#           for ata in sorted(list(votos_2015))]

votantes_por_voto = pegar_votantes(votos_2015)
vereadores = set(itertools.chain(*votantes_por_voto))

