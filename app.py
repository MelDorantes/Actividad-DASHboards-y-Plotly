import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('marketing_campaign.csv')

# Variable de Edad
df['Age'] = 2025 - df['Year_Birth']

# Gasto total
df['Total_Spending'] = df[[
    'MntWines','MntFruits','MntMeatProducts',
    'MntFishProducts','MntSweetProducts','MntGoldProds'
    ]].sum(axis=1)

# Esquemas de color
color_schemes = {
    'monocromatico': ['#264653', '#2A9D8F', '#E9C46A'],
    'complementario': ['#1D3557', '#E63946'],
    'triadico': ['#457B9D', '#E9C46A', '#F4A261']
    }

# 10 FUNCIONES DE GRÁFICOS

def graph_age_distribution():
    return px.histogram(
        df, x = 'Age', nbins=40,
        color_discrete_sequence = color_schemes['monocromatico'],
        marginal = 'rug',
        title = 'Distribución de la Edad de los Clientes'
        )


def graph_income_education():
    return px.box(
        df, x = 'Education', y = 'Income', color = 'Education',
        color_discrete_sequence = color_schemes['complementario'],
        title = 'Distribución de Ingresos por Nivel Educativo'
        )


def graph_age_income():
    return px.scatter(
        df, x = 'Age', y = 'Income', color = 'Age',
        color_continuous_scale = color_schemes['triadico'],
        hover_data = ['Marital_Status', 'Education'],
        title = 'Relación entre Edad e Ingresos'
        )


def graph_total_spending():
    return px.histogram(
        df, x = 'Total_Spending', nbins = 50,
        color_discrete_sequence = color_schemes['monocromatico'],
        title = 'Distribución del Gasto Total por Cliente'
        )


def graph_category_spending():
    category_means = df[[
        'MntWines','MntFruits','MntMeatProducts',
        'MntFishProducts','MntSweetProducts','MntGoldProds'
        ]].mean().reset_index()
    category_means.columns = ['Category', 'Mean_Spend']

    return px.bar(
        category_means,
        x = 'Category', y = 'Mean_Spend', color = 'Category',
        color_discrete_sequence = color_schemes['complementario'],
        title = 'Gasto Promedio por Categoría'
        )


def graph_campaign_acceptance():
    campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3',
                     'AcceptedCmp4', 'AcceptedCmp5']
    acceptance = df[campaign_cols].sum().reset_index()
    acceptance.columns = ['Campaign', 'Accepted']

    return px.pie(
        acceptance, names = 'Campaign', values = 'Accepted',
        color_discrete_sequence = color_schemes['triadico'],
        title = 'Aceptación por Campaña de Marketing'
        )


def graph_correlation_heatmap():
    cols = [
        'MntWines','MntFruits','MntMeatProducts',
        'MntFishProducts','MntSweetProducts','MntGoldProds'
        ]

    corr = df[cols].corr()

    fig = ff.create_annotated_heatmap(
        z = corr.values,              # convertir a matriz numpy
        x = corr.columns.tolist(),    # convertir a lista normal
        y = corr.index.tolist(),      # convertir a lista normal
        colorscale = 'bluyl',
        showscale = True
        )

    fig.update_layout(
        title = 'Mapa de Correlación de Gastos por Categoría',
        xaxis = dict(title = 'Categorías'),
        yaxis = dict(title = 'Categorías')
        )

    return fig


def graph_purchase_channels():
    purchase_types = df[[
        'NumWebPurchases','NumCatalogPurchases','NumStorePurchases'
        ]].mean()

    return px.bar(
        x = purchase_types.index,
        y = purchase_types.values,
        color = purchase_types.index,
        color_discrete_sequence = color_schemes["complementario"],
        title = "Promedio de Compras por Canal"
        )


def graph_marital_spending():
    return px.box(
        df, x = 'Marital_Status', y = 'Total_Spending', color = 'Marital_Status',
        color_discrete_sequence = color_schemes['triadico'],
        title = 'Gasto Total según Estado Civil'
        )


def graph_complain_spending():
    return px.scatter(
        df, x = 'Complain', y = 'Total_Spending', color = 'Complain',
        color_discrete_sequence = color_schemes['complementario'],
        title = 'Impacto de las Quejas en el Gasto'
    )



descriptions = {
    'Gráfico 1: Edad': 'La base de clientes se concentra entre los 30 y 60 años.',
    'Gráfico 2: Ingreso vs Educación': 'A mayor educación, mayores ingresos promedio.',
    'Gráfico 3: Edad vs Ingreso': 'Los ingresos muestran alta variabilidad a partir de los 35 años.',
    'Gráfico 4: Gasto Total': 'La mayoría de los clientes pertenece a un segmento de gasto medio.',
    'Gráfico 5: Categorías de Compra': 'El vino domina el gasto promedio del cliente.',
    'Gráfico 6: Aceptación de Campañas': 'Las campañas muestran baja efectividad general.',
    'Gráfico 7: Correlación de Gastos': 'El vino y la carne presentan correlación moderada.',
    'Gráfico 8: Canales de Compra': 'Las compras en tienda son el principal canal.',
    'Gráfico 9: Estado Civil y Gasto': 'Las personas casadas gastan ligeramente más.',
    'Gráfico 10: Quejas y Gasto': 'Los clientes con quejas tienden a gastar menos.'
    }

graphs = {
    'Gráfico 1: Edad': graph_age_distribution,
    'Gráfico 2: Ingreso vs Educación': graph_income_education,
    'Gráfico 3: Edad vs Ingreso': graph_age_income,
    'Gráfico 4: Gasto Total': graph_total_spending,
    'Gráfico 5: Categorías de Compra': graph_category_spending,
    'Gráfico 6: Aceptación de Campañas': graph_campaign_acceptance,
    'Gráfico 7: Correlación de Gastos': graph_correlation_heatmap,
    'Gráfico 8: Canales de Compra': graph_purchase_channels,
    'Gráfico 9: Estado Civil y Gasto': graph_marital_spending,
    'Gráfico 10: Quejas y Gasto': graph_complain_spending
    }


app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dashboard de Marketing Campaign', style = {'text-align': 'center'}),
    
    dcc.Dropdown(
        id = 'graph_selector',
        options = [{'label': k, 'value': k} for k in graphs.keys()],
        value = 'Gráfico 1: Edad',
        clearable = False
        ),
        
        dcc.Graph(id = 'main_graph'),
        
        html.Div(id = 'description', style = {'margin-top': '20px', 'font-size': '18px'})
        ])


@app.callback(
    Output('main_graph', 'figure'),
    Output('description', 'children'),
    Input('graph_selector', 'value')
)
def update_dashboard(selected_graph):
    fig = graphs[selected_graph]()
    desc = descriptions[selected_graph]
    return fig, desc


if __name__ == "__main__":
    app.run(debug=True)