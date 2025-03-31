# Teste Web Scraping

Este projeto tem como objetivo baixar, processar e analisar dados financeiros relacionados a operadoras de saúde no Brasil. A aplicação utiliza Python para web scraping e PostgreSQL para armazenamento e análise dos dados.

## Funcionalidades

1. **Baixar PDFs**: Baixa arquivos PDFs de procedimentos de saúde.
2. **Compactar Arquivos**: Compacta os arquivos baixados em um arquivo ZIP.
3. **Transformar Dados**: Extrai dados dos PDFs e os transforma em um arquivo CSV.
4. **Importar Dados**: Importa os dados CSV para um banco de dados PostgreSQL.
5. **Análise de Dados**: Executa queries analíticas para identificar as operadoras com maiores despesas.

## Como Executar

### Pré-requisitos

- Docker
- Docker Compose

Inicie o ambiente com Docker Compose:
docker-compose up -d

Verifique os logs para confirmar que os scripts foram executados:
docker logs postgres_db

Acesse o banco de dados:
docker exec -it postgres_db psql -U user -d operadoras_db

Execute queries analíticas:
SELECT * FROM despesas_operadoras LIMIT 10;

Como Testar
Testes Manuais
1. Verifique se os arquivos foram baixados:
Verifique a pasta pdfs_baixados para confirmar que os PDFs foram baixados.
Verifique o arquivo arquivos_baixados.zip para confirmar que os arquivos foram compactados.

2. Verifique se os dados foram transformados:
Verifique o arquivo Teste_Bruno.csv para confirmar que os dados foram extraídos e transformados corretamente.

3. Verifique se os dados foram importados:
Acesse o banco de dados e execute queries para verificar se os dados foram importados corretamente.

Testes Automatizados
1. Execute o script de teste:
python test_app.py

2. Verifique os logs para confirmar que todos os testes foram aprovados.
Estrutura do Projeto
app.py: Script principal para baixar, processar e transformar os dados.
docker-compose.yml: Configuração do ambiente Docker com PostgreSQL.
scripts/: Contém os scripts SQL para criação de tabelas, importação de dados e queries analíticas.