from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

df_final = pd.DataFrame()

for pagina in range(1,11):
    endereco_da_pagina = "https://www.transfermarkt.com.br/transfers/neuestetransfers/statistik/plus/ajax/yw1/plus/1/galerie/0/wettbewerb_id/alle/land_id//minMarktwert/0/maxMarktwert/200.000.000/yt0/Mostrar/page/" + str(pagina)

    objeto_response = requests.get(endereco_da_pagina, headers=headers)

    pagina_bs = BeautifulSoup(objeto_response.content, 'html.parser')


    nomes_jogadores = []

    tags_jogadores = pagina_bs.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})

    for i in range(0, len (tags_jogadores)):
        nomes_jogadores.append(str(tags_jogadores[i]).split(' class',1)[0].split('<img alt="',1) [1])

    nomes_jogadores = list(filter(None, nomes_jogadores))

    # ----------------------------------------------------------------------------------------------

    time_origem = []

    tags_origens = pagina_bs.find_all("td",{"class": None})

    for tag_origem in tags_origens:

        imagem_time = tag_origem.find("img", {"class": "tiny_wappen"}, {"title":True})

        if(imagem_time != None):
            time_origem.append(imagem_time['title'])
    aux = 0
    lista_time_origem = []

    for i ,jogador in enumerate(time_origem):
        if i == aux:
            aux = aux + 2
            lista_time_origem.append(jogador)


    time_destino = []

    tag_destinos = pagina_bs.find_all("td",{"class": None})

    for tag_destino in tag_destinos:

        imagem_time = tag_destino.find("img", {"class": "tiny_wappen"}, {"title":True})

        if(imagem_time != None):
            time_destino.append(imagem_time['title'])
    aux = 1
    lista_time_destino = []

    for i ,jogador in enumerate(time_destino):
        if i == aux:
            aux = aux + 2
            lista_time_destino.append(jogador)


    # ----------------------------------------------------------------------------------------------

    pais_jogadores = []

    tags_ligas = pagina_bs.find_all("td",{"class": None})
    

    for tag_liga in tags_ligas:
        
        imagem_pais = tag_liga.find("img", {"class": "flaggenrahmen"}, {"title":True})
        if(imagem_pais != None): 
            pais_jogadores.append(imagem_pais['title'])


    # ----------------------------------------------------------------------------------------------

    pais_jogadores = []

    tags_ligas = pagina_bs.find_all("td",{"class": "zentriert"})

    for tag_liga in tags_ligas:

        imagem_pais = tag_liga.find("img", {"class": "flaggenrahmen"}, {"title":True})

        if(imagem_pais != None):

            pais_jogadores.append(imagem_pais['title'])

    # ----------------------------------------------------------------------------------------------


    #-----------------------------------------------------------------------------------------------
    custos_jogadores = []
    custo_jogador = pagina_bs.find_all("td", {"class": "rechts"})

    for tag_custo in custo_jogador:
        texto_preco = tag_custo.text
        # O texto do preço contém caracteres que não precisamos como £ (euros) e m (milhão) então iremos retirá-los
        texto_preco = texto_preco.replace("€", "").replace(" mi. "," Milhoes").replace(" mil "," Mil").replace("?","Valor nao informado").replace("-","sem valor")
        # Converteremos agora o valor para uma variável numérica
        # preco_numerico = float(texto_preco)
        custos_jogadores.append(texto_preco)

        aux = 0
    lista_valor_mercado = []

    for i ,jogador in enumerate(custos_jogadores):
        if i == aux:
            aux = aux + 2
            lista_valor_mercado.append(jogador)
    #-------------------------------------------------------------------------------------------------
    quantia_paga = []
    # hauptlink
    quantia_jogador = pagina_bs.find_all("td", {"class": "rechts"})

    for tag_quantia in quantia_jogador:
        texto_preco = tag_quantia.text
        # O texto do preço contém caracteres que não precisamos como £ (euros) e m (milhão) então iremos retirá-los
        texto_preco = texto_preco.replace("€", "").replace(" mi. "," Milhoes").replace(" mil "," Mil").replace("?","Valor nao informado").replace("-","sem clube")
        # Converteremos agora o valor para uma variável numérica
        # preco_numerico = float(texto_preco)
        quantia_paga.append(texto_preco)

        aux = 1
    lista_valor_quantia = []

    for i ,jogador in enumerate(quantia_paga):
        if i == aux:
            aux = aux + 2
            lista_valor_quantia.append(jogador)
    #-------------------------------------------------------------------------------------------------


    # ----------------------------------------------------------------------------------------------

    idade_jogador = []

    idade = pagina_bs.find_all("td", class_ = "zentriert", text=re.compile("\d+"))


    for tag_idade in idade:
        texto_idade = tag_idade.text
        idade_jogador.append(texto_idade)
    aux = 0
    lista_idade = []

    for i ,jogador in enumerate(idade_jogador):
        if i == aux:
            aux = aux + 2
            lista_idade.append(jogador)

    # ----------------------------------------------------------------------------------------------

    data_trf = []

    data = pagina_bs.find_all("td", class_ = "zentriert", text=re.compile("\d+"))


    for tag_data in data:
        texto_data = tag_data.text
        data_trf.append(texto_data)
    aux = 1
    lista_data_trf = []

    for i ,jogador in enumerate(data_trf):
        if i == aux:
            aux = aux + 2
            lista_data_trf.append(jogador)

    # ----------------------------------------------------------------------------------------------
    
    df = pd.DataFrame({"Nome Jogador":nomes_jogadores,"Idade Jogador":lista_idade,"País de Origem":pais_jogadores,"Time antigo":lista_time_origem,"Novo Time":lista_time_destino,"Data de Tranferencia":lista_data_trf,"Valor de Mercado":lista_valor_mercado,"Valor da Tranferência":lista_valor_quantia})
    
    df_final = df_final.append(df)

df_final.to_csv(r"C:\Users\FilipeCarvalho\Desktop\webscraping\mydata.trmrkt_total.csv",index=False,encoding='utf-8')


