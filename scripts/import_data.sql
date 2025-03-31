LOAD DATA INFILE '/var/lib/mysql-files/Teste_Bruno.csv'
INTO TABLE despesas_operadoras
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(operadora, categoria, valor, data);