# Seazone API

## Descrição
Projeto desenvolvido para o [desafio técnico da Seazone](descricao_projeto.pdf). Você pode visualizar o Diagrama Entidade-Relacionamento (DER) [aqui](der.png). 
A API desenvolvida é capaz de realizar as seguintes operações:

### Imóveis
#### - Criação de imóveis
#### - Listagem de imóveis (com filtros)
#### - Busca de imóveis por ID
#### - Deleção lógica de imóveis
#### - Update de imóveis (parcial ou completo)

### Anúncios
#### - Criação de anúncios
#### - Listagem de anúncios (com filtros)
#### - Busca de anúncios por ID
#### - Update de anúncios (parcial ou completo)

### Reservas
#### - Criação de reservas
#### - Listagem de reservas (com filtros)
#### - Busca de reservas por ID
#### - Deleção lógica de reservas


## Configuração do projeto

### Tecnologias
- Python 3.9
- Django 4.2.5 e Django REST Framework 3.14.0
- Banco de dados PostgreSQL 16.0
- Swagger
- Docker (opcional)

### Passos para execução

1. Clone o repositório.

2. Crie um ambiente virtual:
> python -m venv venv

3. Entre no ambiente (Windows):
> venv\Scripts\activate

4. Instale as dependências do projeto:
> pip install -r requirements.txt

5. Configure o banco de dados do projeto:  

* Nessa etapa, vá até a [raiz do projeto Django](seazone) e localize o arquivo [local_settings_sample.py](seazone/local_settings_sample.py). Utilize-o como base para configurar seu banco PostgreSQL ou verifique as outras opções disponíveis na [documentação do Django](https://docs.djangoproject.com/en/4.2/ref/databases/).
* ATENÇÃO: caso opte por algum outro banco de dados, talvez seja necessário realizar a instalação de outros pacotes.
* Crie um arquivo local_settings.py seguindo o exemplo. Você pode passar a SECRET_KEY do projeto tanto no arquivo local_settings.py quanto nas variáveis de ambiente. Você pode checar o exemplo de arquivo de variáveis de ambiente [aqui](.env_exemplo).

Com o banco configurado, aplique as migrações do projeto:
> python manage.py migrate

Para iniciar o projeto, utilize o seguinte comando:
> python manage.py runserver

A documentação gerada via [Swagger](https://swagger.io/) está disponível em:
> http://localhost:8000

### Dados de teste
É possível carregar dados de teste para alimentar o banco de dados com fixtures .json. Para isso, um comando que importa os dados de teste foi criado. Para executá-lo, utilize:
> python manage.py importar_dados_teste

### Docker
O projeto inclui um docker-compose.yml, tornando mais prática a inicialização do banco de dados. Para rodar via Docker, utilize:
> docker-compose up -d

Certifique-se de que o arquivo .env esteja configurado corretamente antes de iniciar o container, pois ele informará ao docker-compose as variáveis a serem utilizadas.

### Testes
São feitos testes unitários utilizando a biblioteca de testes do Django REST Framework. Cada entidade tem seus respectivos testes:

#### Imóveis
* Teste de criação
* Teste de listagem
* Teste de busca por ID
* Teste de update
* Teste de deleção


#### Anúncios
* Teste de criação
* Teste de listagem (com filtros)
* Teste de busca por ID
* Teste de update
* Teste para saber se o método de deleção está como não permitido


#### Reservas
* Teste de criação
* Teste de listagem
* Teste de busca por ID
* Teste de deleção
* Teste do intervalo de datas (check-in e check-out)
* Teste para saber se o método de update está como não permitido

Para executar os testes de forma individual (Imóveis, Anúncios ou Reservas), basta utilizar o seguinte comando:
> python manage.py test <nome_do_app>

Exemplo:
> python manage.py test imoveis

Para executar todos os testes, utilize:
> python manage.py test


### Sugestões de melhorias para implementações futuras
* Implementar autenticação com token JWT.
* Implementar Celery e Redis para:
  - Enviar e-mails de confirmação/cancelamento das entidades. EX: confirmação de reserva.
  - Atualizar automaticamente o status das entidades. EX: reserva com status "ativo" que já passou da data de check-out.
  - Permitir planejar a ativação de um imóvel em data futura. EX: um imóvel que será ativado em 01/01/2025.
