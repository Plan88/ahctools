from dash import Dash

from tools.ahc002.compornents import get_compornent

app = Dash(__name__)
app.layout = get_compornent

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port="8080")
