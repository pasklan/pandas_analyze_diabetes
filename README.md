# Análise de Dados de Pacientes com Diabetes

Este projeto realiza a análise de um conjunto de dados de pacientes idosos com diabetes, utilizando Python e pandas. O objetivo é facilitar a leitura, tratamento e análise dos dados coletados em um arquivo CSV.

## Estrutura dos Dados

O arquivo `data/dados.csv` contém informações como idade, sexo, escolaridade, ocupação, renda, adesão ao tratamento, entre outros. Os valores das colunas são codificados numericamente (ex: 1 = Sim, 2 = Não).

## Como usar

1. **Instale as dependências**  
   Execute no terminal:
   ```bash
   pip install pandas
   ```

2. **Execute o script de leitura**  
   ```bash
   python read_csv.py
   ```

3. **Edite o script conforme necessário**  
   O script lê o arquivo CSV, trata os dados e pode ser adaptado para análises específicas.

## Observações

- Os nomes das colunas podem conter espaços e caracteres especiais. Recomenda-se normalizá-los para facilitar o uso no pandas.
- Os valores das colunas são códigos numéricos. Consulte o dicionário de dados para interpretar corretamente cada coluna.
- Para mapear códigos para textos (ex: 1 = "Sim", 2 = "Não"), utilize o método `map()` do pandas.

## Exemplo de leitura e mapeamento

```python
import pandas as pd

df = pd.read_csv('data/dados.csv', encoding='utf-8')

# Normalizando nomes das colunas
df.columns = [col.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('?', '').replace('-', '_') for col in df.columns]

# Mapeando valores de exemplo
df['Sexo'] = df['Sexo'].map({1: 'Masculino', 2: 'Feminino'})
df['Adesao_terapeutica'] = df['Adesão_terapeutica'].map({1: 'Sim', 2: 'Não'})
```

## Licença

Este projeto é apenas para fins acadêmicos e de