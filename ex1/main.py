from fastapi import FastAPI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

#API
app = FastAPI()


#CSV com os países e seus respectivos códigos
paises = pd.read_csv('C:/Users/cedua/OneDrive/Área de Trabalho/Desenvolvimento/Avaliacao_CD_I/ex1/paises.csv', sep=';')
#Usaremos apenas 143 países, conforme descrito no exercício
paises = paises[:143]

#Estrutura escolhida (visualizar o caderno dev.ipynb)
dict_comex = {}

anos = [a for a in range(2019,2025)] #2019 - 2024
meses = [m for m in range(1,13)] #mes1 ate mes12

#Criando a estrutura citada em dev.ipynb
def criar_dados_comex():
    '''
    CRIANDO UM DICIONÁRIO QUE ARMAZENARÁ DIVERSOS DATASETS (1 PARA CADA PAIS)
    CADA DATASET TERÁ A COLUNA DE IMPORTAÇÃO E EXPORTAÇÃO DE CADA UM DOS OUTROS PAÍSES
    OU SEJA, O DATASET DO PAIS 'AFG' NAO TERÁ A COLUNA DE IMPORTACAO E EXPORTACAO PARA 'AFG'
    '''
    lista_paises = paises['COD'].to_list()
    lista_paises.remove(pais)

    colunas_imp = [f'{p}_IMP' for p in lista_paises]
    colunas_exp = [f'{p}_EXP' for p in lista_paises]

    colunas = sorted(colunas_imp+colunas_exp)
    valores = [np.random.randint(1000, 99001, 284)] # gerando valores

    return pd.DataFrame(valores, columns=colunas)
#Visualize a estrutura em dev.ipynb
for ano in anos:
    dict_comex[ano] = {}
    for mes in meses:
        dict_comex[ano][mes] = {}
        for pais in list(paises['COD']):
            dict_comex[ano][mes][pais] = criar_dados_comex()

# ==================================================================================== #

@app.get('/IMP-EXP-entre-{pais_origem}-{pais_destino}-{ano}')
async def IMP_EXP(pais_origem: str, pais_destino: str, ano: int):
    '''
    Quantidade de importação e exportação entre dois países em determinado ano.
    '''
    assert pais_origem != pais_destino 

    total_exp = []
    total_imp = []
    for m in meses:
        soma_exp = int(dict_comex[2020][m]['AFG'].filter(like='CHN').iloc[0][0])
        total_exp.append(soma_exp)

        soma_imp = int(dict_comex[2020][m]['AFG'].filter(like='CHN').iloc[0][1])
        total_imp.append(soma_imp)

    return f'Em {ano} {pais_origem} importou {sum(total_imp)} de {pais_destino} // Em {ano} {pais_origem} exportou {sum(total_exp)} para {pais_destino}'



@app.get('/comex-{pais}-vs-mundo-por-{ano}')
async def comex_pais_mundo_ano(pais: str, ano: int):
    '''
    Quantidade que o país importou/exportou do/para o mundo em determinado ano.
    '''

    total_imp = []
    total_exp = []
    for m in meses:
        soma_imp = np.array([sum(dict_comex[ano][m][pais].filter(like='IMP').sum())])
        for soma in soma_imp:
            total_imp.append(soma)
        
        soma_exp = np.array([sum(dict_comex[ano][m][pais].filter(like='EXP').sum())])
        for soma in soma_exp:
            total_exp.append(soma)

    return f'Quantidade que o mundo importou do {pais} em {ano}: {int(sum(total_imp))} // Quantidade que o mundo exportou para {pais} em {ano}: {int(sum(total_exp))}'


@app.get('/final_report_{pais_origem}-{pais_destino}-{ano}')
async def final_report_ano(pais_origem: str, pais_destino: str, ano: int):
    '''
    Retorna o report final do ano. Caso o ano não esteja completo, retorna até o último mês disponível.
    '''
    assert pais_origem != pais_destino
    
    total_exp = []
    total_imp = []

    for m in range(1, len(dict_comex[ano])+1): #percorrendo sobre a quantidade de meses no ano mencionado
        soma_exp = int(dict_comex[ano][m][pais_origem].filter(like=pais_destino).iloc[0][0])
        total_exp.append(soma_exp)

        soma_imp = int(dict_comex[ano][m][pais_origem].filter(like=pais_destino).iloc[0][1])
        total_imp.append(soma_imp)

    plt.plot(range(1, len(dict_comex[ano])+1), total_exp)
    plt.plot(range(1, len(dict_comex[ano])+1), total_imp)
    plt.legend(['Total Exportações', 'Total Importações'])
    plt.title(f'Exportações/Importações entre {pais_origem} e {pais_destino}')
    plt.xlabel('Mês')
    plt.xticks(range(1, len(dict_comex[ano])+1))
    return plt.show()





