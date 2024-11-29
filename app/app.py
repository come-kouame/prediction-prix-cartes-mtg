from dash import Dash, dcc, html, Input, Output, callback, State, ALL
from dash.exceptions import PreventUpdate
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
        className="main",
        children=[
            html.Div(
                className="colonne-recherche colle",
                children=[
                    "Recherche",
                    dcc.Input(id='input', type='text', placeholder="Id de la carte"),
                    dcc.Dropdown(['','Recherche par id','Recherche par nom','Recherche par artiste'],'Recherche par id',id='parametres-dropdown',searchable=False),
                    html.Div(id='resultatRecherche'),
                ]
            ),
            html.Div(
                className="resultats",
                id='bloc-resultats'
            )
        ]
    )
])

def rechercheParId(input):
    for set_id in file["data"]:                                         
        if "cards" in file["data"][set_id]:
            for card in file["data"][set_id]["cards"]:
                if card["uuid"] == input:
                    return [f'{card["name"]}']
            else:
                continue
    else:
        return [f'Carte non trouvée.']

def rechercheParNom(input):
    found_ids=[]
    for set_id in file["data"]:                                     
        if "cards" in file["data"][set_id]:                         # Vérification si le set contient des cartes
            for card in file["data"][set_id]["cards"]:              # Parcours de chaque carte dans le set
                if "name" in card and card["name"] == input:                      # Accéder à la carte courante
                    found_ids.append(card["uuid"])
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

def rechercheParArtiste(input):
    found_ids=[]
    for set_id in file["data"]:
        if "cards" in file["data"][set_id]:
            for card in file["data"][set_id]["cards"]:
                if "artist" in card and card["artist"] == input:
                    found_ids.append(card["uuid"])
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

@callback(
    Output(component_id='bloc-resultats', component_property='children'),
    Input(component_id='input', component_property='value'),
    Input(component_id='parametres-dropdown', component_property='value')
)
def afficheResultats(input, parametres_dropdown):
    match parametres_dropdown:
        case 'Recherche par id':
            resultats = rechercheParId(input)
        case 'Recherche par nom':
            resultats = rechercheParNom(input)
        case 'Recherche par artiste':
            resultats = rechercheParArtiste(input)
        case _:
            resultats = []
    bloc_resultats = [
        html.Div(
            className="row",
            children=[
                html.Div(
                    f"{resultat}",
                    id={'type': 'result-item', 'index': i},
                    className="column",
                    style={'cursor':'pointer'}
                )
                for i,resultat in enumerate(resultats)
            ]
        )
    ]
    return bloc_resultats

@callback(
    Output('bloc-resultats', 'children'),  # Met à jour l'affichage des résultats ou des détails
    Input({'type': 'result-item', 'index': ALL}, 'n_clicks'),  # Capture tous les clics
    State({'type': 'result-item', 'index': ALL}, 'children')  # Capture le texte des résultats
)
def afficherDetailsCarte(n_clicks, result_texts):
    if not n_clicks or all(nc is None for nc in n_clicks):
        raise PreventUpdate

    # Trouve l'index du premier clic
    clicked_index = n_clicks.index(1)  # Identifie l'élément cliqué
    resultat = result_texts[clicked_index]  # Texte du résultat cliqué

    # Ici vous pouvez générer un affichage détaillé de la carte
    infos_carte = {
        'Nom': resultat,
        'Prix': '10€',
        'Extension': 'Magic Set',
        'Artiste': 'John Doe'
    }

    # Retourne les détails de la carte
    return html.Div(
        className="details-carte",
        children=[
            html.H2(f"Détails de la carte : {infos_carte['Nom']}"),
            html.P(f"Prix : {infos_carte['Prix']}"),
            html.P(f"Extension : {infos_carte['Extension']}"),
            html.P(f"Artiste : {infos_carte['Artiste']}"),
            html.Button("Retour", id="retour-btn", className="retour-btn")
        ]
    )


if __name__ == '__main__':
    app.run(debug=True)

