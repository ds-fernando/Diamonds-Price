#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def rangointercuartil(df):
    numeric_df = df.select_dtypes(include=['number'])
    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)
    IQR = Q3 - Q1

def limites(df):
    numeric_df = df.select_dtypes(include=['number']).dropna()
    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior = Q1 - (1.5 * IQR)
    limite_superior = Q3 + (1.5 * IQR)
    
    return limite_inferior, limite_superior

def detectar_outliers(df, columna):
    # Asegurar que la columna es numérica
    if df[columna].dtype not in ['float64', 'int64']:
        raise ValueError(f"La columna '{columna}' no es numérica.")
    
    # Obtener los límites inferior y superior
    limite_inferior, limite_superior = limites(df[[columna]])

    # Encontrar los outliers
    outliers = df[(df[columna] < limite_inferior[columna]) | (df[columna] > limite_superior[columna])]
    return outliers



# In[ ]:


def calcular_cuantiles(df):

    cuantiles = df.quantile(q=[0.75, 0.50, 0.25], numeric_only=True)
    cuantiles = cuantiles.transpose().rename_axis('Variable').reset_index()

    cuantiles['IQR'] = cuantiles[0.75] - cuantiles[0.25]

    cuantiles['Limite inferior'] = cuantiles[0.25] - 1.5 * cuantiles['IQR']
    cuantiles['Limite superior'] = cuantiles[0.75] + 1.5 * cuantiles['IQR']

    return cuantiles


# In[ ]:


# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()


# https://www.kaggle.com/code/sparky42/starter-california-housing-prices-371617f9-6?scriptVersionId=18714461&cellId=9
