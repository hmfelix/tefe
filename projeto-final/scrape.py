from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def obter_htmls():
  # raiz dos enderecos a serem raspados
  raiz_endereco = 'https://forbes.com.br/listas/bilionarios-brasileiros-2025/pg/'
  
  # lista para estocar as paginas raspadas
  lista_htmls = []
  
  # obtendo o conteudo html puro de cada pagina
  for i in range(1,11):
    url = raiz_endereco + str(i) + '/'
    with urlopen(url) as resposta:
      html_puro = resposta.read().decode('utf-8')
      lista_htmls.append(html_puro)
  
  return lista_htmls
  
# funcao que extrai os dados de cada html
def extrair_dados(html):
  soup = BeautifulSoup(html)
  main_tag = soup.find('ol', class_='lista_bilionarios')
  lista_bilionarios = main_tag.find_all('li')
  lista_linhas = []
  for bilionario in lista_bilionarios:
    posicao = int(str(bilionario.find('span', class_='posicao').text).strip())
    nome = str(bilionario.find('h3').contents[2]).strip()
    # caso em que o campo idade nao existe:
    if 'Idade' not in bilionario.find('div', class_='info').text:
      idade = 0
    else:
      idade = bilionario.find('div', class_='info').contents[1].find('strong')
      idade = int(idade.text.strip().split(' ')[0])
    # caso em que não consta naturalidade:
    if bilionario.find('div', class_='info').contents[1].text == '\n':
      naturalidade == ''
    # caso em que não consta nem naturalidade nem idade:
    elif idade == 0:
      naturalidade = bilionario.find('div', class_='info').contents[1].find('strong').text.strip()
    else:
      naturalidade = bilionario.find('div', class_='info').contents[3].find('strong').text.strip()
    patrimonio = float(bilionario.find('span', class_='patrimonio').find('strong').text.split(' ')[1].replace(',', '.'))
    origem = bilionario.find('span', class_='origem-patrimonio').find('strong').text.strip()
    texto = bilionario.find('div', class_='texto')
    # caso em que não consta texto descritivo:
    if texto is None:
      texto = ''
    else:
      texto = texto.text.strip()
    linha = [posicao, nome, idade, naturalidade, patrimonio, origem, texto]
    lista_linhas.append(linha)
  resultado = pd.DataFrame(lista_linhas, columns=['Posição', 'Nome', 'Idade', 'Naturalidade', 'Patrimonio (R$ bi)', 'Origem', 'Texto'])
  return resultado
  
def consolidar_dados(lista_htmls):
  lista_dfs = []
  for html in lista_htmls:
    lista_dfs.append(extrair_dados(html))
  return pd.concat(lista_dfs, ignore_index=True)


if __name__ == '__main__':
  lista_htmls = obter_htmls()
  df_bilionarios = consolidar_dados(lista_htmls)
  df_bilionarios.to_csv('projeto-final/dados/bilionarios.csv', index=False)

