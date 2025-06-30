import dash
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import networkx as nx

# Exemple de structure de données (à adapter avec tes vrais exports)
products = [
    {"id": "Fer", "group": "métaux", "value": 100},   # ici on donne les données des cercles, leur groupe, avec la taille des cercles 
    {"id": "Or", "group": "métaux", "value": 70},
    {"id": "cuivre", "group": "métaux", "value": 80},
    {"id": "T-Shirts", "group": "Textiles", "value": 20},
    {"id": "chaussures", "group": "Textiles", "value": 40}
]

# Simuler des liens entre produits similaires (dans la vraie vie, tu utilises une matrice de proximité)
edges = [
    ("Fer", "Or"),                   # ici on donne tous les liens entre les cercles 
    ("Fer", "cuivre"),
    ("T-Shirts", "chaussures"),
]

# Création du graphe avec networkx
G = nx.Graph()
for product in products:
    G.add_node(product["id"], group=product["group"], value=product["value"])

G.add_edges_from(edges)

# Calculer positions (comme dans un "product space")
pos = nx.spring_layout(G, seed=42)

# Générer les coordonnées et infos pour chaque nœud
node_x = []
node_y = []
node_text = []
node_color = []
node_size = []

color_map = {
    "métaux": "purple",             #pour la mise en couleur 
    "Textiles": "red"
}

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)
    group = G.nodes[node]['group']
    node_color.append(color_map.get(group, 'grey'))
    node_size.append(G.nodes[node]['value'])

# Créer les arêtes
edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

# Traces Plotly
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color=node_color,
        size=node_size,
        line_width=2
    )
)

# App Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Product space"),
    dcc.Graph(
        id='product-space',
        figure=go.Figure(data=[edge_trace, node_trace],
                         layout=go.Layout(
                             showlegend=False,
                             hovermode='closest',
                             margin=dict(b=20,l=5,r=5,t=40),
                             xaxis=dict(showgrid=False, zeroline=False),
                             yaxis=dict(showgrid=False, zeroline=False)
                         )
        )
    )
])

if __name__ == '__main__':
    app.run(debug=True)
