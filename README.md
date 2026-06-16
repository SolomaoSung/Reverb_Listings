Projeto de Engenharia de Dados – Análise de Listings do Reverb

Objetivo

Construir um pipeline de dados para coletar informações de anúncios da plataforma Reverb, armazenar os dados localmente e realizar transformações para análise e geração de insights.

Arquitetura

O projeto segue as seguintes etapas:

Extração de dados da API do Reverb.
Armazenamento dos dados em DuckDB
Transformação, tratamento e enriquecimento dos dados.
Criação de tabelas analíticas e novas features para consumo analítico.
Fluxo de Dados

API Reverb → Python (Extração) → DuckDB (Camadas Bronze, Silver e Gold) → Dashboard Power BI para Análise 

Tecnologias Utilizadas
Python
Pandas
Requests
ArgParse
SQL 
DuckDB
Git
GitHub
Conda
Power BI
Fonte de Dados

API oficial do Reverb:

https://api.reverb.com/api/listings


Funcionalidades
Coleta de dados via API REST.
Armazenamento dos dados brutos no DuckDB
Organização dos dados em arquitetura de camadas (Bronze, Silver e Gold).
Transformações SQL 
Criação de tabelas analíticas para exploração e análise de dados no Power BI.
