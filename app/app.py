import json
import dash
from dash import Dash, dcc, html, Input, Output, callback, State, ALL
from dash.exceptions import PreventUpdate
import requests

with open("data/AllPredictionsSorted.json", 'r',errors="ignore") as f:
    file = json.load(f)

# Recherche une carte par son numéro identifiant dans le fichier et renvoie l'uuid de ladite carte
def rechercheParId(input):
    for card_id in file:
        if card_id == input:
            return [f"{file[card_id]['uuid']}"]
    else:
        return [f'Carte(s) non trouvée(s)']

# Recherche une carte par son uuid dans le fichier et renvoie l'uuid de ladite carte
def rechercheParUuid(input):
    for card_id in file:
        if "uuid" in file[card_id]:
            if file[card_id]["uuid"] == input:
                return [f"{file[card_id]['uuid']}"]
    else:
        return [f'Carte non trouvée.']

# Recherche les cartes portant le nom en entrée dans le fichier et renvoie l'uuid de ladite carte
def rechercheParNom(input):
    found_ids=[]
    for card_id in file:
        if "name" in file[card_id]:
            if file[card_id]["name"] == input:
                found_ids.append(f"{file[card_id]['uuid']}")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

# Recherche les cartes appartenant au set dont le code est en entrée dans le fichier et renvoie l'uuid de ladite carte
def rechercheParSetCode(input):
    found_ids=[]
    for card_id in file:
        if "setCode" in file[card_id]:
            if file[card_id]["setCode"] == input:
                found_ids.append(f"{file[card_id]['uuid']}")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

# Recherche les cartes dessinées par l'artiste dans le fichier et renvoie l'uuid de ladite carte
def rechercheParArtiste(input):
    found_ids = []
    for card_id in file:
        if "artist" in file[card_id]:
            if file[card_id]["artist"] == input:
                found_ids.append(f"{file[card_id]['uuid']}")
    if found_ids:
        return found_ids
    else:
        return [f'Carte(s) non trouvée(s)']

app = Dash(__name__, suppress_callback_exceptions=True)

# Layout de l'application
app.layout = html.Div([
    dcc.Store(id='app-state', data='results'),
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
                    dcc.Input(id='input',
                              type='text',
                              placeholder="Recherche..."),
                    dcc.Dropdown(['','... par id','... par uuid','... par nom','... par code de set','... par artiste'],
                                 '',
                                 id='parametres-dropdown',
                                 searchable=False),
                    html.Div(id='resultatRecherche'),
                ]
            ),
            html.Div(
                className="resultats",
                id='bloc-resultats'
            ),
            html.Button("Retour", id="retour-btn", style={'display': 'none'})
        ]
    )
])

# Permet d'effectuer la recherche d'une carte selon les paramètres sélectionnés
# Construit aussi l'affichage
def afficheResultats(input, parametres_dropdown):
    match parametres_dropdown:
        case '... par id':
            resultats = rechercheParId(input)
        case '... par uiid':
            resultats = rechercheParUuid(input)
        case '... par nom':
            resultats = rechercheParNom(input)
        case '... par code de set':
            resultats = rechercheParSetCode(input)
        case '... par artiste':
            resultats = rechercheParArtiste(input)
        case _:
            resultats = []

    blocs = []
    for i, uuid in enumerate(resultats):
        details_carte = None
        for card_id in file:
            if "uuid" in file[card_id] and file[card_id]["uuid"] == uuid:
                details_carte = file[card_id]
                break
        
        if details_carte:
            texteDesc = f"{details_carte['name']} ({details_carte['setCode']})"
        else:
            texteDesc = "Carte non trouvée"
        # On construit un bloc contenant l'uuid qui n'apparaîtra pas (pour qu'il soit utilisé dans la recherche des détails)
        # et le nom avec entre parenthèses le code du set de la carte qui eux seront affichés
        bloc = html.Div(
            children=[
                texteDesc,
                html.Div(uuid, style={'display': 'none'}, className="hidden-uuid"),
            ],
            id={'type': 'result-item', 'index': i},
            className="column",
            style={'cursor': 'pointer'}
        )
        blocs.append(bloc)

    return html.Div(className="row", children=blocs)

# Après avoir reçu le nom et le code du set d'une carte, renvoie l'image de la carte associée
def get_image(name, set_code):
        url = f"https://api.scryfall.com/cards/named?exact={name}&set={set_code}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "image_uris" in data and "normal" in data["image_uris"]:
                return data["image_uris"]["normal"]
            else:
                print(f"Aucune image trouvée pour {name} ({set_code})")
                return None
        else:
            print(f"Erreur lors de la requête pour {name} ({set_code}): {response.status_code}")
            return None

# Récupère le ou les derniers prix d'une carte selon le type de carte
def extraireDernierPrix(prices):
    prix_textes = []
    if not prices:
        return ["Prix non disponible"]
    # date jusqu'à laquelle les données sont non prédites ; dans notre cas c'est le 14 novembre 2024
    date_actuelle = "2024-11-14"  

    for card_type in prices:
        valeurs = prices[card_type]
        # on garde juste les dates qui ne sont pas le résultat de la prédiction
        dates_reelles = {date: prix for date, prix in valeurs.items() if date <= date_actuelle}
        if dates_reelles:
            derniere_date = sorted(dates_reelles.keys())[-1]  # Dernière date parmi celles réelles
            prix = dates_reelles[derniere_date]
            prix_textes.append(f"{card_type.capitalize()} : {prix}€ (le {derniere_date})")

    return prix_textes if prix_textes else ["Aucun prix disponible"]

# Créé un graphique du prix d'une carte en fonction de la date pour un type de carte
def generer_graphique(prices, version):
    dates = []
    prix = []
    
    for date, valeur in sorted(prices.items()):
        dates.append(date)
        prix.append(valeur)
    
    return dcc.Graph(
        figure={
            'data': [
                {'x': dates, 'y': prix, 'type': 'line', 'name': version}
            ],
            'layout': {
                'title': f"Évolution des prix ({version})",
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Prix'},
            }
        },
        style={'marginBottom': '20px'}
    )

# Le callback permet de récupérer les entrées et d'actualiser la page en fonction de ceux-ci
@app.callback(
    [Output('bloc-resultats', 'children'),
     Output('retour-btn', 'style')],
    [Input('input', 'value'),
     Input('parametres-dropdown', 'value'),
     Input({'type': 'result-item', 'index': ALL,}, 'n_clicks'),
     Input('retour-btn', 'n_clicks')],
    [State({'type': 'result-item', 'index': ALL}, 'children')]
)
def navigationEntreEtats(input_value, dropdown_value, result_clicks, retour_click, result_texts):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Si le bouton retour a été cliqué, on réaffiche les résultats et on le cache
    if 'retour-btn.n_clicks' in ctx.triggered_id:
        return afficheResultats(input_value, dropdown_value), {'display': 'none'}

    # Si on a cliqué sur un des résultats
    if result_clicks and any(result_clicks):
        clicked_index = None

        for i, nc in enumerate(result_clicks):
            if nc:
                clicked_index = i
                break
            
        if clicked_index is not None and clicked_index < len(result_texts):
            clicked_child = result_texts[clicked_index]
            uuid = None
            for child in clicked_child:
                if "props" in child and "className" in child["props"] and child["props"]["className"] == "hidden-uuid":
                    uuid = child["props"]["children"]
                    break

            if not uuid:
                raise PreventUpdate # Au cas où il y a un problème avec un des uuid
            
            details = None
            for card_id in file:
                if "uuid" in file[card_id] and file[card_id]["uuid"] == uuid:
                    details = file[card_id]
                    break
            if details:
                name = details["name"] if "name" in details else "Inconnu"
                set_name = details["setName"] if "setName" in details else "Inconnu"
                set_code = details["setCode"] if "setCode" in details else "Inconnu"
                artist = details["artist"] if "artist" in details else "Inconnu"
                rarity = details["rarity"] if "rarity" in details else "Inconnu"
                prices_textes = extraireDernierPrix(details["prices"]) if "prices" in details else ["Prix non disponible"]

                # On récupère l'image associée au nom et au code du set du résultat
                image_url = get_image(name, set_code)

                # On récupère le ou les graphiques associés aux prix du résultat 
                price_graphs = []
                if "prices" in details:
                    for version, data in details["prices"].items():
                        if data:  # Vérifie si les prix existent
                            price_graphs.append(generer_graphique(data, version))

                # On renvoie le bloc contenant les détails de la carte et on affiche le bouton retour
                return html.Div(className="details-carte", children=[
                    html.H2(f"Détails de la carte : {name}"),
                    html.Div(
                    children=[
                        html.Img(src=image_url, style={'width': '300px', 'display': 'block'}) 
                        ]
                    ),
                    html.P(f"Set : {set_name} ({set_code})"),
                    html.P(f"Artiste : {artist}"),
                    html.P(f"Rareté : {rarity}"),
                    html.Div([html.P(prix) for prix in prices_textes]),
                    html.Div(price_graphs)
                ]), {'display': 'block'}

    # Affichage par défaut
    return afficheResultats(input_value, dropdown_value), {'display': 'none'}

if __name__ == '__main__':
    app.run(debug=False)