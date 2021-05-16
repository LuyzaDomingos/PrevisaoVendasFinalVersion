CREATE TABLE regiao(
    regiao_id serial,
    nome varchar(255) NOT NULL,
    PRIMARY KEY(regiao_id)
);

CREATE TABLE categoria (
    categoria_id serial,
    nome varchar(255) NOT NULL,
    PRIMARY KEY(categoria_id)

);

CREATE TABLE tempo(
    tempo_id serial,
    mes integer NOT NULL,
    ano integer NOT NULL,
    semestre integer NOT NULL,
    trimestre integer NOT NULL,
    PRIMARY KEY(tempo_id)
);

CREATE TABLE produto (
	produto_id serial,
	nome varchar(255) NOT NULL,
	valor float,
	fornecedor varchar(255),
	PRIMARY KEY (produto_id)
);

CREATE TABLE loja (
	loja_id serial,
	nome varchar(255) NOT NULL,
    sigla varchar(255) NOT NULL,
	PRIMARY KEY (loja_id)
);

CREATE TABLE venda_mensal(
    regiao_id integer NOT NULL,
    loja_id integer NOT NULL,
    categoria_id integer NOT NULL,
    produto_id integer NOT NULL,
    tempo_id integer NOT NULL,
    quantidade integer NOT NULL,
    quantidade_mes_anterior integer NOT NULL,
    valor float,
    estoque integer, 
    ruptura integer,
    PRIMARY KEY(regiao_id, loja_id, categoria_id, produto_id, tempo_id),
    FOREIGN KEY(regiao_id) REFERENCES regiao(regiao_id),
    FOREIGN KEY(loja_id) REFERENCES loja(loja_id),
    FOREIGN KEY(categoria_id) REFERENCES categoria(categoria_id),
    FOREIGN KEY(produto_id) REFERENCES produto(produto_id),
    FOREIGN KEY(tempo_id) REFERENCES tempo(tempo_id),

);