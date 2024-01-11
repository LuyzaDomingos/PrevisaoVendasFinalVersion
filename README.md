# PrevisaoVendas
Aplicação de Previsão de Vendas

## Motivação do Projeto
O projeto de Previsão de Vendas busca auxiliar a equipe de estoque do Armazém Paraíba a tomar decisões sobre compra de produtos.

## Funcionalidades
O projeto Previsão de Vendas é uma aplicação web, podendo ser acessado por meio de um navegador web (e.g. Mozilla Firefox, Google Chrome). A aplicação consiste em três funcionalidades principais: **Previsão por Produtos**, **Previsão por Categoria**, e **Painel de Vendas**. A página inicial (imagem abaixo) da aplicação permite que o usuário selecione uma das funcionalidades, redirecionando-o para a respectiva página.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 00 57" src="https://user-images.githubusercontent.com/17768174/140374910-beff0698-a19a-4a7e-b545-4660613721a0.png"></p>

### Previsão por Produtos
A página de Previsão por Produtos, possui duas opções de visualização: **Vendas** e **Estoque**. Para ambos os casos é fornecida ao usuário uma barra que permite fazer a seleção de qual produto os gráficos devem ser visualizados, além de poder selecionar uma faixa de datas e também se o gráfico deve ser apresentado com o volume de vendas/estoque de um dia, semana, ou mês.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 03 21" src="https://user-images.githubusercontent.com/17768174/140375312-d4186183-1b56-4709-b957-98262b5013e8.png"></p>

A parte de visualição de Vendas apresenta um par de gráficos, o primeiro ilustra as vendas acumuladas desde o início do período selecionado (linha azul, eixo esquerdo) e as vendas no período (linha verde, eixo direito), isto é, as vendas que ocorreram em um passo da frequência selecionada (por exemplo, se a frequência selecionada for a diária, será exibida a quantidade vendida do produto em um dia).

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 04 21" src="https://user-images.githubusercontent.com/17768174/140375588-fee6c41d-0c18-46c3-b7bb-f95b00de1970.png"></p>

O segundo gráfico mostra a previsão das vendas do produto durante os próximos 365 dias, há uma linha cinza escuro que divide a série temporal em duas: passado e futuro, a porção futura da série é apresentada com uma linha vermelha, que permite visualizar o quanto do produto será vendido em um dia/semana/mês (a depender da frequência) futuro. Junto á linha, a uma faixa apresentada na cor vermelho claro que indica o intervalo de confiança de 95% da previsão.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 04 33" src="https://user-images.githubusercontent.com/17768174/140375729-5c76409b-32ae-4d2a-a4ad-f71d64eb18f4.png"></p>

A visualização de Estoque também apresenta um par de gráficos, sendo que o primeiro mostra a série temporal do estoque do produto selecionado, junto a indicadores sobre o Giro e a Cobertura do produto.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 07 52" src="https://user-images.githubusercontent.com/17768174/140376061-8b7ad204-4866-4ce8-88d0-a6ca122e57ef.png"></p>

O segundo gráfico mostra as vendas do produto no período e quanto a organização deixou de vender por conta da falta do produto em estoque.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 08 34" src="https://user-images.githubusercontent.com/17768174/140376296-357edbde-0204-4df9-ab92-3d3c4390f2ef.png"></p>

### Previsão por Categoria
A página de Previsão por Categoria apresenta um resumo de indicadores das categorias, no caso, são apresentadas a **Venda Prevista** para o mês, além do **Estoque** atual e a **Cobertura**. Os dois primeiros indicadores são acompanhados de um delta que indica a variação do indicador, em %, em relação ao mês anterior (por exemplo, na imagem a venda prevista da primeira lionha está acompanhada de uma seta pra baixo e um -8% que indica uma projeção de queda de 8 nas vendas em relação ao mês anterior). A primeira linha apresenta a soma dos indicadores de Venda e Estoque para todas as categorias, enquanto que a Cobertura nesse caso é a mediana.
 
<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 18 45" src="https://user-images.githubusercontent.com/17768174/140377882-6130c5c8-e05c-44fd-8332-2246bb946c54.png"></p>

Ainda, é possível ordernar a lista segundo qualquer um dos indicadores, tanto de forma crescente ou decrescente. Adicionalmente, é possível baixar todos os dados dessa visão em formato .xslx (Microsoft Excel).

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 22 39" src="https://user-images.githubusercontent.com/17768174/140378618-e3b357f1-0ac1-4ffa-92f1-11ca58518aef.png"></p>

Cada categegoria nessa tela, possui dois botões que permitem respectivamente visualizar o relatório de vendas sobre a mesma **(WIP)**, ou visualizar o panorama da categoria (imagem abaixo). O panorama da categoria mostra a soma das séries temporais de todos os produtos pertencentes a ela, assim como os cinco produtos mais vendidos da categoria.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 29 37" src="https://user-images.githubusercontent.com/17768174/140379745-a612651b-ed90-4c46-af19-729390469024.png"></p>

### Painel de Vendas
O painel de vendas apresenta uma visão das vendas por região, loja, ou a organização como um todo. A tela principal da página mostra algumas informações sobre as vendas, como o gráfico de barras das vendas no mês, a quantidade vendida e a variação com o mês anterior, a quantidade que se deixou de vender por conta de ruptura de estoque e a variação desse indicador com o mês anterior, além dos cinco produtos mais vendidos e os cincos produtos que mais se perdeu vendas por ruptura de estoque.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 33 25" src="https://user-images.githubusercontent.com/17768174/140380355-e0e25c39-b57e-41e1-86e7-3bc4cd680625.png"></p>

É possível selecionar um mês e uma categoria para receber destaque na exibição dos dados e indicadores. No caso de selecionar a categoria **Geral**, considera-se como produtos as próprias categorias (e.g. Eletrodomésticos, Celular, entre outros).

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 34 11" src="https://user-images.githubusercontent.com/17768174/140380670-b1d97f58-2d9c-438d-b9ca-d02522190ed6.png"></p>

Selecionando as opções de **Região** ou **Lojas**, é exibida uma lista com a quantidade vendida no mês selecionado da categoria escolhida (e a variação com o mês anterior), além do valor das vendas e a variação **(indisponível)**.

<p align = "center"><img width="900" alt="Captura de Tela 2021-11-04 às 13 35 52" src="https://user-images.githubusercontent.com/17768174/140381102-b282b023-7a1b-4f18-8e56-8cf5ee8dfe2d.png"></p>

O botão amarelo permite que seja apresentado o Painel de Vendas personalizado para a Região/Loja selecionada


## Execução - Desenvolvimento

Para executar o projeto em modo de desenvolvimento é necessário:
- Ter instalado:  Python => 3.6, o pip e uma IDE(recomendamos o VS Code).
- Ter o Django instalado - [link](https://docs.djangoproject.com/en/3.2/topics/install/).
- Criar um ambiente virtual utilizando os seguintes comandos: $ python3 -m venv venv e $ source venv/bin/activate 
- Instalar as blibliotecas que se encontram no arquivo requirements.txt utilizando o comando : $ pip install -r requirements.txt
- Comando para executar o projeto: $ python3 index.py run

## Deploy

 - Para realizar o deploy é necessário possuir o arquivo de chave privada do PuTTY.
 - Clonar o projeto no servidor e rodar o comando na pasta do repositório: $ nohup python3 index.py run &
 - Acessar o endereço: http://184.72.194.142:8050/
