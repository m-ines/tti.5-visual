from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40]
fig = go.Figure(
    data=[
        go.Scatter(
            x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            y=[11, 12, 10, 11, 12, 11, 12, 13, 12, 11],
            mode="markers",
            marker=dict(
                size=size,
                sizemode="area",
                sizeref=2.0 * max(size) / (40.0**2),
                sizemin=4,
                color=[120, 125, 130, 135, 140, 145, 145, 140, 135, 130],
                opacity=[1, 0.8, 0.6, 0.4, 1, 0.8, 0.6, 0.4, 1, 0.8],
                showscale=True,
            ),
        )
    ]
)

app = Dash(__name__)


@app.callback(
    Output("dash_ewen", "figure"),
    Input("dash_ewen", "value"),
)
def update_figure(value):
    # Placeholder function, update as needed
    return fig


app.layout = html.Div([dcc.Graph(id="dash_ewen", figure=fig)])

if __name__ == "__main__":
    app.run(debug=True)
