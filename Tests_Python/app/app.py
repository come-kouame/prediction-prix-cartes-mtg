from dash import Dash, dcc, html, Input, Output, callback
import json

with open("data/AllPrintings.json", 'r',errors="ignore") as f:
    file = json.load(f)

app = Dash()

app.layout = html.Div([
    html.Div(
        className="header",
        children=[
            html.Div('Prédiction de prix de cartes Magic The Gathering', className="titre-header")
        ]
    ),
    html.Div(
        className="cherche",
        children=[
            "Rentrez l'id de la carte : ",
            html.Br(),
            dcc.Input(id='input-id', type='text', placeholder="Id de la carte"),
            html.Br(),
            html.Div(id='nomCarte'),
        ]
    )
])

@callback(
    Output(component_id='nomCarte', component_property='children'),
    Input(component_id='input-id', component_property='value')
)
def afficheCarte(id_input):
    for set_id in file["data"]:                                         
        if "cards" in file["data"][set_id]:                             # Vérification si le set contient des cartes
            for card in file["data"][set_id]["cards"]:                  # Parcours de chaque carte dans le set
                if card["uuid"] == id_input:                            # Accéder à la carte courante
                    return f'{card["name"]}'                            # Affiche le nom de la carte correspondante
            else:
                continue                                                # Continue si aucune carte ne correspond dans ce set
    else:
        return f'Carte non trouvée.'




if __name__ == '__main__':
    app.run(debug=True)