from urllib.request import urlopen
from bs4 import BeautifulSoup

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
    # refazer abaixo usando contents!
    posicao = int(str(bilionario.find('span', class_='posicao')).split('>')[1].strip())
    nome = str(bilionario.find('h3')).split('>')[3].split('<')[0].strip()
  
  return (posicao, nome)
  
  
  




# salvando esse conteudo em arquivos


if __name__ == '__main__':
  lista_htmls = obter_htmls()
  teste = extrair_dados(lista_htmls[0])
  print(teste[0], teste[1])
  
  
  
  
  
  
  
  

