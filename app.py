import os
import requests
from bs4 import BeautifulSoup
import zipfile
import logging
import PyPDF2
import pandas as pd
import re

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def baixar_pdfs(url, pasta_destino):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Código de status HTTP: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        pdf_links = [link['href'] for link in links if 'Anexo_I' in link['href'] or 'Anexo_II' in link['href']]

        if not pdf_links:
            logging.warning("Nenhum PDF encontrado.")
            return []

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        arquivos_baixados = []
        for pdf_link in pdf_links:
            if not pdf_link.startswith('http'):
                pdf_link = 'https://www.gov.br' + pdf_link
            
            nome_arquivo = os.path.join(pasta_destino, os.path.basename(pdf_link))
            try:
                pdf_response = requests.get(pdf_link)
                pdf_response.raise_for_status()
                with open(nome_arquivo, 'wb') as f:
                    f.write(pdf_response.content)
                arquivos_baixados.append(nome_arquivo)
                logging.info(f"Baixado: {nome_arquivo}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro ao baixar {pdf_link}: {e}")
        
        return arquivos_baixados
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a página: {e}")
        return []

def compactar_arquivos(arquivos, nome_zip):
    try:
        with zipfile.ZipFile(nome_zip, 'w') as zipf:
            for arquivo in arquivos:
                zipf.write(arquivo, os.path.basename(arquivo))
                logging.info(f"Arquivo adicionado ao ZIP: {arquivo}")
        logging.info(f"Todos os arquivos foram compactados em: {nome_zip}")
    except Exception as e:
        logging.error(f"Erro ao compactar arquivos: {e}")

def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ''
        for pagina in leitor.pages:
            texto += pagina.extract_text()
    return texto

def processar_texto_para_tabela(texto):
    linhas = texto.split('\n')
    dados = []
    for linha in linhas:
        if re.match(r'\d+', linha):
            colunas = [coluna.strip() for coluna in linha.split()]
            dados.append(colunas)
    if dados:
        return pd.DataFrame(dados)
    else:
        logging.warning("Nenhum dado válido encontrado no PDF.")
        return pd.DataFrame()

def substituir_abreviacoes(df):
    if 'OD' in df.columns:
        df['OD'] = df['OD'].replace({'OD': 'Odontológico'})
    if 'AMB' in df.columns:
        df['AMB'] = df['AMB'].replace({'AMB': 'Ambulatorial'})
    return df

def transformar_dados():
    caminho_pdf = 'pdfs_baixados/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'
    texto = extrair_texto_pdf(caminho_pdf)
    df = processar_texto_para_tabela(texto)
    df = substituir_abreviacoes(df)
    arquivo_csv = 'Teste_Bruno.csv'
    df.to_csv(arquivo_csv, index=False)
    logging.info(f"Arquivo CSV salvo em: {arquivo_csv}")

def baixar_arquivos(urls_anos, pasta_destino):
    try:
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        arquivos_baixados = []
        for url_ano in urls_anos:
            response_ano = requests.get(url_ano)
            if response_ano.status_code == 404:
                logging.error(f"Página não encontrada: {url_ano}")
                continue
            response_ano.raise_for_status()
            soup_ano = BeautifulSoup(response_ano.text, 'html.parser')
            links_ano = soup_ano.find_all('a', href=True)
            
            # Filtra os links que são diretórios de mês
            meses = [link['href'].rstrip('/') for link in links_ano if link['href'].endswith('/')]
            
            for mes in meses:
                url_mes = f"{url_ano.rstrip('/')}"
                response_mes = requests.get(url_mes)
                response_mes.raise_for_status()
                soup_mes = BeautifulSoup(response_mes.text, 'html.parser')
                links_mes = soup_mes.find_all('a', href=True)
                
                # Filtra os arquivos CSV ou ZIP
                arquivos = [link['href'] for link in links_mes if link['href'].endswith('.csv') or link['href'].endswith('.zip')]
                
                for arquivo in arquivos:
                    url_arquivo = f"{url_mes.rstrip('/')}/{arquivo.lstrip('/')}"
                    nome_arquivo = os.path.join(pasta_destino, os.path.basename(arquivo))
                    try:
                        arquivo_response = requests.get(url_arquivo)
                        arquivo_response.raise_for_status()
                        with open(nome_arquivo, 'wb') as f:
                            f.write(arquivo_response.content)
                        arquivos_baixados.append(nome_arquivo)
                        logging.info(f"Baixado: {nome_arquivo}")
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Erro ao baixar {url_arquivo}: {e}")
        
        return arquivos_baixados
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a página: {e}")
        return []

def main():
    url_rol = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    pasta_destino_rol = 'pdfs_baixados'
    arquivos_baixados_rol = baixar_pdfs(url_rol, pasta_destino_rol)
    
    if arquivos_baixados_rol:
        compactar_arquivos(arquivos_baixados_rol, 'arquivos_baixados.zip')
        transformar_dados()
    
    urls_anos = [
        'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023',
        'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024'
    ]
    pasta_destino_demonstracoes = 'demonstracoes_contabeis'
    baixar_arquivos(urls_anos, pasta_destino_demonstracoes)
    
if __name__ == '__main__':
    main()