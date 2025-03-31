CREATE TABLE IF NOT EXISTS despesas_operadoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operadora VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    valor DECIMAL(15, 2) NOT NULL,
    data DATE NOT NULL
);