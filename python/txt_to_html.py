# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:11:36 2016

@author: lucas_000
"""

from bs4 import BeautifulSoup
import re
import os

def arquivos(diretorio, extensao):
    """
    Retorna lista com nomes de todos os arquivos
    no diretorio com a extensão determinada.
    """
    return [arquivo for arquivo in os.listdir(diretorio)
            if os.path.splitext(arquivo)[1] == "." + extensao]

def txt_to_html(diretorio):
    """
    Transforma todos os arquivos txt do diretório
    em arquivos html.
    """
    arquivos_txt = arquivos(diretorio, "txt")
    diretorio_atual = os.getcwd()
    os.chdir(diretorio)
    for arquivo in arquivos_txt:
        os.rename(arquivo, os.path.splitext(arquivo)[0]+".html")
    os.chdir(diretorio_atual)

def sopa(diretorio):
    """
    Retorna dicionário com "sopas" (BeautifulSoup)
    de todos os arquivos html do diretório.
    """
    arquivos_html = arquivos(diretorio, "html")
    diretorio_atual = os.getcwd()
    os.chdir(diretorio)    
    sopas = {}
    for arquivo in arquivos_html:
        nome = os.path.splitext(arquivo)[0]        
        with open(arquivo, encoding="utf-8") as f:
            sopas[nome] = BeautifulSoup(f, 'lxml')
    os.chdir(diretorio_atual)
    return sopas

def texto(sopas):
    """
    Retorna o texto das sopas (BeautifulSoup)
    no dicionário sopas.
    """
    return {sopa: sopas[sopa].get_text().lower() for sopa in sopas}

def limpar_textos(textos):
    """
    Retira dos textos no dicionário "textos" todos os
    caracteres "estranhos" e pontos em Dr. ou S.O.S.
    """
    textos = {texto: re.sub(r'[^ .,;:\-\'\"\(\)\w]', r'', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'césar maia', r'cesar maia', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'dr\.', r'dr', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'drjoão', r'dr joão', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'ivanir de melo', 
                            r'ivanir de mello', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r's\.o\.s\.', 'sos', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r's\.o\.s', 'sos', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'brizola neto', 'brizola', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'marcelino dalmeida', 
                            'marcelino d\'almeida', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'aloísio', 'aloisio', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'átila a.', 'átila a', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r's. ferraz', 's ferraz', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'prof. célio', 'prof célio', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'prof. uoston', 'prof uoston', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'k. ribeiro', 'k ribeiro', textos[texto])
              for texto in textos} 
    textos = {texto: re.sub(r'zico trinta e quatro', 
                            'zico (trinta e quatro)', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'zico vinte e três', 
                            'zico (vinte e três)', textos[texto])
              for texto in textos}
    textos = {texto: re.sub(r'marcelino d\'almeida marcelo arar',
                            'marcelino d\'almeida, marcelo arar', 
                            textos[texto])
              for texto in textos}               
    return {texto: re.sub(r'  +', r' ', textos[texto])
            for texto in textos}

def salvar_texto(diretorio, textos, pasta):
    """
    Salva todos os textos no dicionário "textos" na pasta,
    dentro do diretório.
    """
    novo_diretorio = '/'.join([diretorio, pasta])
    if not os.path.exists(novo_diretorio):
        os.mkdir(novo_diretorio)    
    diretorio_atual = os.getcwd()
    os.chdir(novo_diretorio)
    
    for texto in textos:
        nome = texto + ".txt"
        if nome not in os.listdir(novo_diretorio):
            with open(nome, 'w') as f:
                f.write(textos[texto])
    os.chdir(diretorio_atual)

diretorio = "E:/Dropbox/voto_aberto"
pasta = "atas_limpas"

txt_to_html(diretorio)
sopas = sopa(diretorio)
atas = texto(sopas)
atas = limpar_textos(atas)
salvar_texto(diretorio, atas, pasta)