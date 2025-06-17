import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact, ttest_ind
import statsmodels.api as sm
import os


# ======================================================
# Data Reading
# ======================================================


data_path = os.path.join('..', 'data', 'dados.csv')
df = pd.read_csv(data_path, encoding='utf-8', sep=',')

print("\n✔️Dados carregados.")
print(df.head())


# ======================================================
# Análise automática para todas as variáveis (exceto Idade e Tempo de estudo)
# ======================================================

output_results = []

excluded_columns = ['Idade', 'Tempo de estudo', 'Adesão terapeutica']

for column in df.columns:
    if column in excluded_columns:
        continue

    print(f"Analisando relação entre Adesão e {column}...")
    
    try:
        conting_table = pd.crosstab(df['Adesão terapeutica'], df[column])
        
        if conting_table.shape == (2, 2):
            # Fisher para tabelas 2x2
            odds_ratio, p_fisher = fisher_exact(conting_table)
            output_results.append({
                'Variável': column,
                'Teste': 'Fisher',
                'p-valor': p_fisher,
                'Detalhe': f'Odds Ratio: {odds_ratio:.4f}'
            })
            print(f'Fisher aplicado. p-valor: {p_fisher:.4f}, OR: {odds_ratio:.4f}')
        else:
            # Qui-Quadrado para tabelas maiores
            chi2, p_chi, dof, expected = chi2_contingency(conting_table)
            output_results.append({
                'Variável': column,
                'Teste': 'Qui-Quadrado',
                'p-valor': p_chi,
                'Detalhe': f'GL: {dof}'
            })
            print(f'Qui-Quadrado aplicado. p-valor: {p_chi:.4f}, GL: {dof}')

    except Exception as e:
        print(f"Erro na análise da variável '{column}': {e}") 
        
# ======================================================
# Test T: Idade x Adesão terapêutica
# ======================================================
print("\nTeste T para Idade entre os grupos de Adesão")
idade_aderiu =  df[df['Adesão terapeutica'] == 1]['Idade']
idade_nao_aderiu = df[df['Adesão terapeutica'] == 2]['Idade']

idade_aderiu = pd.to_numeric(idade_aderiu, errors='coerce')
idade_nao_aderiu = pd.to_numeric(idade_nao_aderiu, errors='coerce')

t_stat, p_ttest = ttest_ind(idade_aderiu.dropna(), idade_nao_aderiu.dropna(), nan_policy='omit')
output_results.append({
    'Variável': 'Idade',
    'Teste': 'T-Test',
    'p-valor': p_ttest,
    'Detalhe': ''
})
print(f'p-valor do T-test: {p_ttest:.4f}')        
        
# ======================================================
# Regressão Logística: Idade + Apoio Familiar explicando Adesão
# ======================================================
print("\nRegressão Logística: Idade + Apoio Familiar explicando Adesão")

df['adesao_bin'] = df['Adesão terapeutica'].map({1: 1, 2: 0})

column_familia = "Seus familiares te apoiam no tratamento?"
df['apoio_fam'] = df[column_familia].map({1: 1, 2: 0})

X = df[['Idade', 'apoio_fam']].apply(pd.to_numeric, errors='coerce')
X = sm.add_constant(X)
y = df['adesao_bin']

X = X.dropna()
y = y.loc[X.index]

model = sm.Logit(y, X).fit()
print(model.summary())    

os.makedirs('../output', exist_ok=True)

# Exportar tabela de p-valores
output_path = os.path.join('..', 'output', 'resultados.csv')
resultados_df = pd.DataFrame(output_results)
resultados_df.to_csv(output_path, index=False)
print(f'✔️Resultados exportados para {output_path}')

# Exportar sumário da regressão logística como TXT
summary_path = os.path.join('..', 'output', 'logit_summary.txt')
with open(summary_path, 'w') as f:
    f.write(model.summary().as_text())
print(f'✔️Sumário da regressão exportado para {summary_path}')