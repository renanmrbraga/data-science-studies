import pandas as pd
import seaborn as sns
import plotly.io as pio
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import cufflinks as cf
import plotly.graph_objects as go
import plotly.express as px

# Carregar base de vendas
vendas = pd.read_excel(r"D:\Documents\Meus Documentos\Cursos\Escola DNC\Cientista de Dados\Matéria 4 - Análise de Regressão em Python\Prática\Materiais\varejo.xlsx")

# Substituir valores inconsistentes na coluna 'idcanalvenda'
vendas['idcanalvenda'] = vendas['idcanalvenda'].str.replace('APP', 'Aplicativo')

# Corrigir espaços na coluna 'Nome_Departamento'
vendas['Nome_Departamento'] = vendas['Nome_Departamento'].str.replace(' ', '_')

# Tratar valores nulos na coluna 'estado'
vendas['estado'] = vendas['estado'].fillna('MS')

# Tratar valores nulos na coluna 'Preço'
media_preco = vendas['Preço'].mean()
vendas['Preço'] = vendas['Preço'].fillna(media_preco)

# Filtrar registros onde o preço está correto
vendas_correto = vendas.query('Preço < Preço_com_frete').copy()

# Criar nova coluna 'mes' a partir da data
vendas_correto['mes'] = vendas_correto['Data'].dt.month

# Carregar base de clientes
try:
    cliente = pd.read_excel(r"D:\Documents\Meus Documentos\Cursos\Escola DNC\Cientista de Dados\Matéria 4 - Análise de Regressão em Python\Prática\Materiais\cliente_varejo.xlsx")
    cliente = cliente.astype({'renda': 'float'})
    # Juntar as bases
    vendas_cliente = vendas_correto.merge(cliente, how='left', on='cliente_Log')
except FileNotFoundError:
    print("Arquivo de clientes não encontrado.")

# Criar agregações para gráficos
agg_idcanal_renda = round(vendas_cliente.groupby('idcanalvenda')['renda'].agg('mean').sort_values(ascending=False).reset_index(), 2)
agg_idade_bandeira = round(vendas_cliente.groupby('bandeira')['idade'].agg('mean').sort_values(ascending=False).reset_index(), 2)
agg_dept_preco = round(vendas_correto.groupby('Nome_Departamento')['Preço_com_frete'].agg('mean').sort_values(ascending=False).reset_index(), 2)
venda_por_data = vendas_correto.groupby('Data').idcompra.nunique().reset_index()

# Criar um dashboard com subplots matplotlib
#fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Gráfico 1 - Idade Média por Bandeira
#axes[0, 0].bar(agg_idade_bandeira['bandeira'], agg_idade_bandeira['idade'], color='green')
#axes[0, 0].set_ylabel('Média de Idade')
#axes[0, 0].set_title('Idade Média por Bandeira')
#axes[0, 0].tick_params(axis='x', rotation=45)

# Gráfico 2 - Renda Média por Canal de Venda
#axes[0, 1].bar(agg_idcanal_renda['idcanalvenda'], agg_idcanal_renda['renda'], color='blue')
#axes[0, 1].set_ylabel('Renda Média')
#axes[0, 1].set_title('Renda Média por Canal de Venda')
#axes[0, 1].tick_params(axis='x', rotation=45)

# Gráfico 3 - Evolução das Vendas ao Longo do Tempo
#axes[1, 0].plot(venda_por_data.index, venda_por_data.values, color='red', linewidth=2)
#axes[1, 0].set_xlabel('Data da Venda')
#axes[1, 0].set_ylabel('Quantidade de Vendas')
#axes[1, 0].set_title('Quantidade de Vendas por Data')
#axes[1, 0].tick_params(axis='x', rotation=45)

# Gráfico 4 - Preço Médio por Departamento
#axes[1, 1].bar(agg_dept_preco['Nome_Departamento'], agg_dept_preco['Preço_com_frete'], color='purple')
#axes[1, 1].set_ylabel('Preço Médio')
#axes[1, 1].set_title('Preço Médio por Departamento')
#axes[1, 1].tick_params(axis='x', rotation=90)

# Ajustar layout para evitar sobreposição
#plt.tight_layout()
#plt.show()

# Gráfico 1 com plotly
fig1 = px.bar(agg_idade_bandeira, x='bandeira', y='idade')
pio.show(fig1) # Exibir o gráfico diretamente no VSCode

# Gráfico 2 com plotly
fig2 = px.line(venda_por_data, x='Data', y='idcompra')
pio.show(fig2) # Exibir o gráfico diretamente no VSCode