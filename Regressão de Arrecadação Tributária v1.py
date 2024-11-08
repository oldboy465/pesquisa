import easygui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, KFold, cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb

# Configurações de exibição
pd.set_option("display.float_format", "{:.3f}".format)
sns.set(style="whitegrid")

# Função para calcular as métricas
def avaliar_modelo(model, X, y):
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = cross_val_predict(model, X, y, cv=kf)
    
    metrics = {
        "RMSE": round(np.sqrt(mean_squared_error(y, y_pred)), 3),
        "MSE": round(mean_squared_error(y, y_pred), 3),
        "MAE": round(mean_absolute_error(y, y_pred), 3),
        "sMAPE": round(np.mean(2 * np.abs(y - y_pred) / (np.abs(y) + np.abs(y_pred))) * 100, 3),
        "R²": round(r2_score(y, y_pred), 3)
    }
    return metrics

# Lista de algoritmos
algoritmos = {
    "SVM": SVR(),
    "Random Forest": RandomForestRegressor(),
    "Decision Tree": DecisionTreeRegressor(),
    "Linear Regression": LinearRegression(),
    "Boosting": GradientBoostingRegressor(),
    "XGBoost": xgb.XGBRegressor()
}

# Seleção do arquivo
arquivo = easygui.fileopenbox(msg="Selecione o arquivo .xlsx com os dados", title="Seleção do Arquivo", filetypes=["*.xlsx"])
dados = pd.read_excel(arquivo)

# Listando variáveis e obtendo escolhas
print("Variáveis encontradas no arquivo:")
for i, col in enumerate(dados.columns):
    print(f"{i} - {col}")

# Seleção das variáveis dependente e independentes
var_dep = int(input("Digite o número da variável dependente: "))
vars_indep = list(map(int, input("Digite os números das variáveis independentes, separados por vírgula: ").split(",")))

X = dados.iloc[:, vars_indep]
y = dados.iloc[:, var_dep]

# Identificação das variáveis mais importantes
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X, y)
importancias = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)

# Gráfico de Importância das Variáveis
plt.figure(figsize=(10, 6))
sns.barplot(x=importancias, y=importancias.index, palette="viridis", orient='h')
plt.title("Importância das Variáveis (Random Forest)")
plt.xlabel("Importância")
plt.ylabel("Variáveis")
plt.show()

# Avaliação dos algoritmos
print("\nMétricas de avaliação para cada algoritmo:")
resultados = {}
for nome, algoritmo in algoritmos.items():
    print(f"\n{nome}")
    resultados[nome] = avaliar_modelo(algoritmo, X, y)

# Transformando os resultados em um DataFrame
tabela_resultados = pd.DataFrame(resultados).T
print(tabela_resultados)

# Gráficos de comparação das métricas
metrics = ["RMSE", "MSE", "MAE", "sMAPE", "R²"]
for metric in metrics:
    plt.figure(figsize=(10, 6))
    sns.barplot(x=tabela_resultados.index, y=tabela_resultados[metric], palette="viridis")
    plt.title(f"Comparação de {metric} entre Algoritmos")
    plt.xlabel("Algoritmo")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.show()
