/* pratica */
INSERT INTO vendas (id_produto, quantidade, data_venda)
VALUES (NULL, 5, '2024-01-10');



SELECT v.id_venda, p.nome, v.quantidade, v.data_venda
FROM vendas v
LEFT JOIN produtos p ON v.id_produto = p.id_produto;

select * from produtos; com a tabela vazia aqui reforça o erro!!!
select * from vendas;

UPDATE vendas
SET id_produto = 1
WHERE id_produto IS NULL;


DELETE FROM vendas
WHERE id_produto IS NULL;

ALTER TABLE vendas
MODIFY id_produto INT NOT NULL;


INSERT INTO produtos (nome, categoria, preco)
VALUES ('Mouse Gamer', 'Periféricos', 120.00);

INSERT INTO vendas (id_produto, quantidade, data_venda)
VALUES (1, 3, '2024-01-15');
