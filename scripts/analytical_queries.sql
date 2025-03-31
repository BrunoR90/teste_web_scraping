-- 10 operadoras com maiores despesas no último trimestre
SELECT operadora, SUM(valor) AS total_despesas
FROM despesas_operadoras
WHERE categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND data >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
GROUP BY operadora
ORDER BY total_despesas DESC
LIMIT 10;

-- 10 operadoras com maiores despesas no último ano
SELECT operadora, SUM(valor) AS total_despesas
FROM despesas_operadoras
WHERE categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND data >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY operadora
ORDER BY total_despesas DESC
LIMIT 10;