import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import networkx as nx

# Données de produits
products = [
    {"id": "Fer", "group": "métaux", "value": 100},
    {"id": "Or", "group": "métaux", "value": 70},
    {"id": "cuivre", "group": "métaux", "value": 80},
    {"id": "T-Shirts", "group": "Textiles", "value": 20},
    {"id": "chaussures", "group": "Textiles", "value": 40},
    {"id": "chapeaux ", "group": "Textiles", "value": 30},
    {"id": "montres", "group": "accessoires", "value": 50},
    {"id": "sacs", "group": "accessoires", "value": 60},
]

# Arêtes entre produits
edges = [
    ("Fer", "Or"),
    ("Fer", "cuivre"),
    ("T-Shirts", "chaussures"),
    ("T-Shirts", "chapeaux "),
    ("chapeaux ", "chaussures"),
    ("chaussures", "sacs"),
    ("montres", "Or"),
    ("montres", "sacs"),
    ("Fer", "montres"),
]

# Création du graphe
G = nx.Graph()
for product in products:
    G.add_node(product["id"], group=product["group"], value=product["value"])
G.add_edges_from(edges)

# Positions
pos = nx.spring_layout(G, seed=42)

# Infos nœuds
node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
color_map = {"métaux": "purple", "Textiles": "red", "accessoires": "blue"}

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)
    node_color.append(color_map.get(G.nodes[node]["group"], "grey"))
    node_size.append(G.nodes[node]["value"])

# Trace des nœuds
node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    hoverinfo="text",
    marker=dict(showscale=False, color=node_color, size=node_size, line_width=2),
)

# App Dash
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Product space"),
        dcc.Graph(
            id="product-space",
            figure=go.Figure(
                data=[node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode="closest",
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                ),
            ),
        ),
    ]
)


@app.callback(Output("product-space", "figure"), Input("product-space", "hoverData"))
def update_graph(hoverData):
    if hoverData is None:
        return go.Figure(
            data=[node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
            ),
        )

    # Récupérer le nœud survolé
    node_id = hoverData["points"][0]["text"]

    # Arêtes liées à ce nœud
    filtered_edges = [e for e in G.edges() if node_id in e]

    # Générer uniquement les segments des arêtes concernées
    edge_x, edge_y = [], []
    for edge in filtered_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    return go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
        ),
    )


if __name__ == "__main__":
    app.run(debug=True)
