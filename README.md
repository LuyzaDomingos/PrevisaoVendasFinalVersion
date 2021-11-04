# PrevisaoVendas
Aplicação de Previsão de Vendas para o Armazém Paraíba: [Previsão de Vendas](https://armazem-develop.herokuapp.com/).

## Conteúdo
[Motivação do Projeto](TDB)<br>
[Funcionalidades](TDB) <br>
[Previsão por Produtos](TDB) <br>
[Previsão por Categoria](TDB) <br>
[Painel de Vendas](TDB) <br>

## Motivação do Projeto
O projeto de Previsão de Vendas busca auxiliar a equipe de estoque do Armazém Paraíba a tomar decisões sobre compra de produtos.

## Funcionalidades
O projeto Previsão de Vendas é uma aplicação web, podendo ser acessado por meio de um navegador web (e.g. Mozilla Firefox, Google Chrome). A aplicação consiste em três funcionalidades principais: Previsão por Produtos, Previsão por Categoria, e Painel de Vendas. A página inicial (imagem abaixo) da aplicação permite que o usuário selecione uma das funcionalidades, redirecionando-o para a respectiva página.

<p align = "center"><img src="https://lh3.googleusercontent.com/D0COPB5qGIPV_0OWyZsV91wqRlgDJBRhQVkSIrczL6SG15puaQzIlrcTNUe63OoGPhDQvvC1M1vOfbw8YhAkZZBW9wSWqWQZHk2kZ07y0WXA4VWzU9vfwTZPsrtIEAF3ki4kFwNi2yaHTwN63gOyPxsa2oV2Fls-F8U6o9atZg9hp79QbCOzuLSMIxdXI9WeLou2jISJLujMvK24j8ghPMODmpGZae-h1n0hUq7zIiBQqeaaLZ0oy7I7hLwGrka6_SLs_4_M__WQC-8BYM5KsTIC8Dl3dAtT5UHToEKaTLERZRYaHT8b_5uOwNuy7kMVR1ytpEXKk2z30gjtlPStrlHDbAjwflmvAHoLqKRiKWzCGUEbCJ7qmNZnLMBLi1WgEYodLS46thWrhU6laYwtrffnTkYc9dN6OTdZSa-k2c8J5o0fSKNSOqJ--2DN9SWfWt6oSpiljkq_jfJf0Wam49AfRR2ay_vV_Sd1hWAaaZrnEEYs-wiWa7HxvJ1U5AzLk9-r3OfP8ZeoO1ZOrhDOlQDbljM-4oYOY5-dELw6jqik_pzX-XgAaHtKrHVr47Vl5bP5foQ2oRkfRfsIIaIXkXJSNJiNq1Iqb-d4Iao5VNAWHIBrNQFUCtdpV0_79VPuHewrlRrWLZeUTA8ASNe94kSoMAQ2NnnhfpZ3wwAwIlhTtpGXN9-5xYFd3jpzRggsnj6wxAcVhgCX1ftHi-94HDw=w2246-h940-no?authuser=1"></p>

### Previsão por Produtos
A página de Previsão por Produtos, possui duas opções de visualização: **Vendas** e **Estoque**. Para ambos os casos é fornecida ao usuário uma barra que permite fazer a seleção de qual produto os gráficos devem ser visualizados, além de poder selecionar uma faixa de datas e também se o gráfico deve ser apresentado com o volume de vendas/estoque de um dia, semana, ou mês.

<p align = "center"><img src="https://lh3.googleusercontent.com/EbfAMXGYA9F6fUOOkRRWDCDnyIGv-1VToQp5TjM_dwTShiUw-oJY6G3zYzg6VGwUGBP7Jgr-mTys7ewG4Z08UKcG5vIB7vxK43UoDbkncohYX-rJKcmLF09lycRZfArng-xi4GyjXc5TnvKbV7FqV7Egkg5uOZArLdsAGBRh2i-y8z6HnXPfWgtQXZSJmxLTwOtFa2pZkg0FyE1TuYYG49PWQNFC7LZZLMKNLroBRRhUwDXjq8cQQdluF3t5YyHzIxD8dNLSeRWsuYl2rudvfwhba0sBVqKGQpDDniSl2KBJz5XqemVzP_L5xUoaMk9JQELBE8C8aAzv2XpOU6oAnv2GrdypD5-gdmtAa_lJDAwhDUsiEzRvy_ZuoR8jfwMlWURQx5qIVAic77hlk9GUNXVpn1OMxtM8DAudMwSpF8C5Nzs-Br5whFv7NZdffpQ0R4ZgyMIfNV1AROKUw_OC1V7bPGG533evRp7w7RqtwILlGAAEA4AW0YSRr_QbdIgWssI6tDBnEkkM3MUYQs76cC6oM8ODtquuPdl8WbUFc9mAwygS3AQlFSo_faZoKfKv4ZGGWZK7bB2J55PPPmUHXqzNR-2h__YiO47x5e7s9Ntuj8qeA1TLx01pm29rseqMXBL15yRXCt-FnLWOYhDDw6t9RDRfv3ZPKvH4D176bd-3jJWse6AU38A2yAbXxg1paZEIywAL3AtrqtdiR5JEsRI=w2648-h282-no?authuser=1"></p>

A parte de visualição de Vendas apresenta um par de gráficos, o primeiro ilustra as vendas acumuladas desde o início do período selecionado (linha azul, eixo esquerdo) e as vendas no período (linha verde, eixo direito), isto é, as vendas que ocorreram em um passo da frequência selecionada (por exemplo, se a frequência selecionada for a diária, será exibida a quantidade vendida do produto em um dia).

<p align = "center"><img src="https://lh3.googleusercontent.com/lTHBgLPxxmrD2zHNWoYArnXFeEA63Kum5otQfxCoVRxskABAXXCfcm6U-0xbbEKGu9FXUEY2MitxToDve1ZLScxyeRUHaL8D1lsi-KbsPc7CCiWxIezATw0NJxFKXWIkHsNnjAcNt4Nyhfj5rtoaDbpMuLj0EJ-xlGb-led0py-yZZuqXXrAvEvol5uyA_HWSrhO_c18ytSVept2oP_PMOdKE1P8xo4seEk3jtFR7jQU8_-ouc587oXn3XiH4_065bVnVjwdFoO9gxk4Hwg-kRzoDbPB-sM9xnMP_50A1SR9xjn-j3WdWpjqblxXVpt8wSZvYZwT2aToGoEAzIa9rnKJ4nHQUITAVL31NhNlAwDdqdpTVybu8nDUEJG81kkT5T0PQzj8YEj2y1OiIg4os7qMSDoqRSwUFeXQ_wToGtJA86nycmJ1ce0SNiIpNeju1QCVu5jHWI9XLWiwI7Tj38vRiEFCBXJb0mui-lC9fOfQ4ZSwPOVQumXbZqoU5G-I8pWTSLLG2eXEdWFiod_33puGGSLKBvTjVZfzbGS733GQWYE6Vf3_CNCVE2826OWef4GLBWMt4aHB58_aliYv666b2doWKaMaTY9bMs65OjcvnrMmZG4pRvXLypqQQEsOiRek9IL-v4OdFx1-ZK3A23284MRZCoJgwMv4PLwgvlx0KJpw5z3KBkzfsSXAQY58RJ0q7ekbjh7FDFAWLbMj9uo=w2880-h750-no?authuser=1"></p>

O segundo gráfico mostra a previsão das vendas do produto durante os próximos 365 dias, há uma linha cinza escuro que divide a série temporal em duas: passado e futuro, a porção futura da série é apresentada com uma linha vermelha, que permite visualizar o quanto do produto será vendido em um dia/semana/mês (a depender da frequência) futuro. Junto á linha, a uma faixa apresentada na cor vermelho claro que indica o intervalo de confiança de 95% da previsão.

<p align = "center"><img src="https://lh3.googleusercontent.com/N2Ivqm75v6NL1cO0yZg9RXUkmlhY58oscxSwP0I2bE1b1uRttJZQKJrlWpHkpkPFRKcb0JHHgLAX7az7L2QSRLNGzWWEs4T1CfZ9hSniNJqXjQgi945pZwkp1XXiaOg3jxPSWif3I92PYVXMcQhK0ZQlLFbtVM9GF6xlkzk-iR-5efrSVwDVY_6d8xPrqlh8tioWfS4R1EiHmhzqZAYkXhG8v1QLckCEzDmCuf9ghH0aDnN90S6XdXG3_vsq6MjSoqtRnlU9LHfSgLfxNsQEIP9kNQpQ8CsEUYrirUOu4tNAeE7fKLg5X9nYSShJFuQt8LE-45y0ZgMPMKYgcygR18ON8KlNXEoSboxVNDtq8VfgKWafObIq3B_Dp1sT50mjhs3lmxxEQygzF7O0XF6yFACZUXmXnga7Bo6NgfZ1DBS79XA1YmUzHr0fVIuy_j8mH2QIX_kyzzHgOOYpfsBvtqc8V0DdnouBMswGt9N-fpBk3bfPGNUG848D4bmCim__waPQgOp94bGPTgO1CddpPRKZ9Dl7NGIwDr1RXbMcvVbzpmCUwWXVh10kL2WtwAmp-4xsOwfqT3lSd0CVa12g3YXv3UARCc5KjWAayMLPVJuHTqCel9md7O6Casgbvcq1dlrBI8rM9Piq6Uiq0J7z_VzonOZZzXNHgl0tEMHlx7aRB8Xo2ai0w6rmYZ0p7a8Qe7GeKATW-EMtRwcHZk-dLf0=w2880-h750-no?authuser=1"></p>

### Previsão por Categoria

### Painel de Vendas
