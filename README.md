# lifprojet



# Objectifs

Le but de ce projet est d'analyser les variations de prix des cartes du jeu Magic The Gathering, célèbre jeu de cartes à jouer et collectionner.</br>
Nous avons utilisé l'algorithme de calcul Apriori afin d'établir une méthode pour prédire les prix des cartes selon les variations de prix des autres cartes de la base de donnée.</br>
Nous avons la possibilité de simuler un évenement (tournoi) -> cet évenement va augmenter le prix de certaines cartes qui sont beaucoup joués (cartes méta) ce qui va provoqué des variations de prix sur d'autres cartes associées.</br>
Nous avons également réalisé une application web permettant de visualisé la prédiction de prix des cartes Magic.

# Installation

( Optionnel )
Apres téléchargement vous pouvez remplacer les fichiers json dans data par les plus récents fournis par MTGJSON : https://mtgjson.com/downloads/all-files/ 
Exécuter simplement le fichier buildMTGFiles.py, il va merge les 2 fichiers afin de créer des fichiers moins lourds que nous utiliserons pour l'application et l'algorithme apriori

### dossier app
Exécutez le script app.py pour lancer le serveur. Voici le message obtenu dans le terminal :
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
Copiez l'adresse du serveur 'http://127.0.0.1:8050/' et collez la dans votre moteur de recherche pour utiliser l'application.
L'application s'utilise de la manière suivante
1. Saisissez à droite de la page le type de filtre que vous souhaitez (nom, artiste, id...)
2. Entrez ensuite un filtre dans la barre de texte pour trouver la carte souhaitée
3. Sélectionnez la carte souhaitée au centre de la page
4. Les informations concernant la carte s'affichent
### dossier data
Contient toutes les données utiles au projet :
| Nom du fichier        |      Description                 |
|:---------------------:|:--------------------------------:|
| AllPrintings.json     | Contient toutes les informations sur toutes les cartes (sauf le prix). Peut ête obtenu via MTGJson.com |

### dossier PricesDataSorter
Là où se trouve les fonctions de triage des donnée ainsi que l'algorithme Apriori
### dossier Test_Python
Tests réalisés sur la base que nous avons réaliser au début pour nous familiarisé avec (plusieurs ne donnerons rien car ils utilisent des fichiers json qui ne sont plus présent dans le projet)