/* CREATE DATABASE loja1 ; */ 

CREATE TABLE produtos (
  id_produto int NOT NULL AUTO_INCREMENT,
  nome varchar(100) NOT NULL,
  categoria varchar(50) NOT NULL,
  preco decimal(10,2) NOT NULL,
  PRIMARY KEY (id_produto)
) ;

CREATE TABLE vendas (
  id_venda int NOT NULL AUTO_INCREMENT,
  id_produto int DEFAULT NULL,
  quantidade int NOT NULL,
  data_venda date NOT NULL,
  PRIMARY KEY (id_venda),
  KEY id_produto (id_produto),
  CONSTRAINT vendas_ibfk_1 FOREIGN KEY (id_produto) REFERENCES produtos (id_produto)
);
