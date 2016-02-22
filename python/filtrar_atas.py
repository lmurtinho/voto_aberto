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

def filtro_regex(dicionario, regex):
    """
    Retorna todos os elementos no dicionário
    que contenham a regex.
    """
    return {nome: dicionario[nome] 
            for nome in dicionario
            if re.findall(regex, dicionario[nome])}

def pegar_votantes(atas):
    """
    O argumento é um dicionário de strings em que cada string é uma ata.
    O retorno é uma lista com os votantes para cada voto registrado
    em cada ata.
    """
    # retira todos os votos em todas as atas
    todos_os_votos = [{'data': ata,
                       'votos': re.findall(r'(?:votou|votaram) (.*?) [oa][s]? (?:senhor[a]?|senhor[ea]s) (?:vereador[a]?|vereador[ea]s) ([^;\.\(\d]+[^\W\d_])', 
                      atas[ata])}
                      for ata in sorted(list(atas))]
    votantes = []
    for sessao in todos_os_votos:
        for votacao in sessao['votos']:
            # mais de dois votantes: último separado por ' e ', 
            # demais por vírgula
            voto = {'data': sessao['data']}            
            if ',' in votacao[1]:
                voto['voto'] = re.findall(r'(\b.*?),', votacao[1]) + re.findall(' e (.*)$', votacao[1])
            # dois votantes separados por ' e '
            elif ' e ' in votacao[1]:
                voto['voto'] = votacao[1].split(' e ')
            # um votante
            else:
                voto['voto'] = votacao[1]
            votantes.append(voto)
    return votantes

arquivos_txt = arquivos(diretorio, 'txt')
atas_2015 = filtro_inicio_arquivo(diretorio, arquivos_txt, '2015')
votos_2015 = filtro_regex(atas_2015, r'votaram|votação')
votantes_por_voto = pegar_votantes(votos_2015)

vereadores = []
for voto in votantes_por_voto:
    if type(voto['voto']) == str:
        vereadores.append(voto['voto'])
    else:
        vereadores.extend(list(voto['voto']))
vereadores = set(vereadores)

#vereadores = set([vereador for vereador in 
#              itertools.chain(*[voto['voto'] for voto in votantes_por_voto])
#              if len(vereador)>2])
erros = [{'data': voto['data'], 
          'erros': [string for string in voto['voto'] if len(string)<3]} 
          for voto in votantes_por_voto]
erros = [erro for erro in erros if erro['erros']]