# tti.5-visual

# P28 : Etudier la complexité de la recherche scientifique

L'objectif de notre projet est de fournir une interface interractive permettant de visualiser graphiquement les liens entre les thèmes importants de la recherche scientifique sur l'électrification des transports. Nous nous inspirons donc d'un graphique d'Harvard : https://atlas.hks.harvard.edu/explore/productspace?exporter=country-250 

Il permet de visualiser des cluster sémantiques de mots et les liens entre les idées co-occurentes. Nous disposons donc d'un fichier csv contenant les titres de nombreux articles scientifiques sur l'électrification et d'un notebook fournis pas notre encadrant. Le notebook nous donne quelques graphiques intermédiaires pour tracer les liens entre 50 idées. Ils ne sont cependant pas interactifs. On utilise également 50 idées les plus importantes déjà extraites par une IA. 

Nous avons donc séparé les membres du groupe sur différents objectifs afin de reprendre et de nous approprier complètement le sujet.

L'interface graphique la plus aboutie basée sur des données que nous avons nous-mêmes générées se trouve dans Projet_final.ipynb. 
Différentes représentations tests des données sur les topics se trouvent dans Optim50.ipynb.

# Héloïse : Chercher à extraire les idées importantes des articles sans faire appel à une IA.

Je me suis principalement concentrée sur la sélection des mots clés sans faire appel à une IA. Pour cela, on utilise de nouveaux modules tokenize et stopwords qui permettent de diviser les mots d'un texte dans uune liste python puis de supprimer les mots non importants comme "the", "in"... Pour cela, il faut bien mettre en minuscule l'ensemble des mots en amont. Mon but est d'extraire uniquement les mots clés en lien avec le sujet des textes présentant chaque article dans le fichier csv. Il me faut ensuite enlever de la liste de mots la ponctuation et je fais le choix discutable certes, d'enlever les verbes conjugués (termiant par -ED). A ce stade, il me restait beaucoup de mots comptés deux fois, avec le singulier et le pluriel. Avec le module WordNetLemmatizer, je choisis uniquement les singuliers. J'enlève aussi les mots de moins de 3 lettres en supposant qu'ils ne sont pas porteurs d'informations car ce sont des mots de liaisons, ainsi que les valeurs numériques. J'ai ainsi une focntion mots_cles qui me permet de réduire drastiquement le nombre initial de mots pour un seul article. 

J'utilise cette fonction pour avoir une liste de liste contenant les mots clés de chaque article du fichier data. Un des problèmes est que certains mots apparaissent très souvent sans être des mots-clés comme " therefore"... D'autres mots ont été considéré comme mots-clés par ma première fonction tout en apparaissant très peu dans l'ensemble des articles. Je crée donc une focntion qui compte le nombre d'appartition de chaque mots. Sur près de 600 000 mots, si le mot apparaît moins de 500 fois, je le supprime. C'est un paramètre que j'ai choisi de manière subjective et qui pourrait être révisé. Je réduis ainsi à environ 200 le nombre de mots-clés. 

Les mots-clés sont essentiellement des mots en lien avec le sujet mais il y a encore quelques mots qui ne nous donnent pas d'infrmations supplémentaires : "aim", "study"... Je décide donc de donner ma liste de mots à chatGPT pour qu'il me choisisse uniquement les mots en lien avec le thème de l'électrification des transports. Il me réduis ma liste à 100 mots. 

L'étape suivante est de calculer le rayon de cercle de mots en focntion de leur importance dans la recherche scientifique, comme sur le graphique d'Harvard. Je choisi des rayons entre 10 et 100 en me basant sur la fréquence d'appartion du mot. 

Je renvoie ensuite ue matrice de co-occurence entre les 100 mots-clés que l'on a trouvé. Elle contient le nombre d'apparition dans un même titre de deux mots. Si a et b apparaissent dans de nombreux titres ensemble, je considère qu'ils ont un lien fort. Je rend la matrice en DataFrame pour l'afficher plus lisiblement. Je fixe le seuil de 1000 titres où deux mots apparaisent ensemble pour qu'ils aient un lien. Je rend donc une liste de tuples avec les différents liens qu'il nous faudra ensuite tracer sur notre graphique interactif. 

Tentative ratée : utiliser un LLM pour avoir une IA en requête sur mon notebook pour l'interroger d'une autre manière pour la sélection des mots clés sans faire appel en dehors du notebook à ChatGPT qu'en au sens des mots. 

Comme cette méthode ne marchait pas, j'ai fait quelques recherches supplémentaires et j'ai trouvé un module sklearn.cluster de KMeans qui permet de faire des clusters sémantiques. C'est exactement ce dont j'avais besoin. Donc je donne ma liste de mots-clés à ce module qui me renvoie un dictionnaire avec des clusters par sens des mots. 

Viens maintenant la partie Dash. Après avoir pris connaissance du module, j'ai essayé de tracer les mots en bulles avec le rayon que j'avais déterminé percédemment et les liens entre les mots avec des arrêtes. C'est ainsi un graphe non orienté que nous obtenons. Je coloris aussi les clusters de mots avec des couleurs différentes pour réperer les relation directes entre les mots. 

# Loïc : Analyser les méthodes de représentation des données en 2D

Je me suis pour ma part concentré sur les données envoyés pour essayer de les appréhender et de les représenter.

Après les avoir rendues utilisables, une question que nous nous sommes posés est comment présenter efficacement des données sur un plan 2D en considérant en entrée une matrice de distance entre paires de points (ou de proximité). 

J'ai tout d'abord essayé d'implémenter moi-même une solution à ce problème, qui correspond à minimiser la différence entre les distances théoriques de la matrices et celles représentées sur le plan. J'ai fini par abandonner cette idée, la fonction à minimiser ne présentant certains critères nécessaires au bon fonctionnement de la plupart des algo de minimisation- notamment la convexité. 

Je suis donc passé par l'utilisation de différentes libraires et algorithmes pré-implémentés de représentation en 2D depuis une matrice de distance. L'idée était de comparer les différences de ceux-ci et d'observer comment les clusters se formaient. C'est l'objet de Optim50. Je me rends compte que la méthode de Fruchterman-Reingold est la plus utilisée et celle qui semble la plus adaptée. Comme l'algorithme conçu pour les données personnalisées utilise également celui-ci, j'ai tenté d'adapter le code pour obtenir l'interface graphique associé aux topics. C'est ce que j'ai commencé à faire dans graph_topics. Je n'ai malheuresment pas eu le temps de finir, cela nécessitant un certain travail de déconstruire et réadapter le code fonctionnel à des données différentes. 
 
# Ewen : créer une interface graphique interactive 

Je me suis intéressé en grande majorité à la création et l'adaptation de l'interface graphique pour obtenir un graphe interactif proche de celui qui nous était demandé : un graphe type "Product Space" pour relier dans notre cas les sujets de recherche et non les produits fabriqués (cf https://atlas.hks.harvard.edu/explore/productspace?exporter=country-646&importer=group-1&year=2021 pour un exemple).

Les enjeux étaient surtout de bien comprendre le fonctionnement du module dash, nouveau pour nous et très utile pour permettre de donner la dimension interactive au graphe. 
Héloïse a elle aussi manipulé dash pour générer certains premiers graphes que j'ai pu reprendre avec toute la base de données de mots clés qu'elle a générée pour élaborer le graphe final. 

J'ai donc ajouter les noeuds et les arêtes, construits à partir des mots clés obtenus et de leurs liens, au graphe créé. Puis en utilisant dash, il a été possible de les représenter sur une interface qui tourne à la manière d'une app.
J'ai ensuite beaucoup travaillé pour améliorer l'interface graphique, d'abord en ajoutant du code et notamment une partie d'actualisation selon le noeud survolé pour permettre de n'afficher que les arêtes qui sont reliées au noeud survolé et ainsi alléger le graphe. J'ai également repris le travail d'Héloïse qui avait déjà permis d'attribuer des couleurs différentes aux clusters. 
Par la suite, il a été possible d'intégrer un bouton permettant de sélectionner un pays et un autre pour sélectionner une année (instructions ajoutées dans la partie layout de la partie dash/ app). 

Grâce au travail d'Ines pour obtenir un tri des mots clés en fonction des années, des pays mais aussi des pays et années en même temps, nous avons pu intégrer des instructions qui permettent de représenter en couleurs, selon
le cluster, les mots clés qui apparaissent dans la liste par pays et année pour le pays et l'année sélectionnés par l'utilisateur via les boutons, et en gris ceux qui n'apparaissaient pas, à la manière des graphes "Product space" exemples. 

Une des grandes difficultés était de gérer le zoom et le survol des points et l'intelligence artificielle a su suggéré les outils hoverData et relayoutData qui ont permis de gérer ce problème et améliorer nettement l'interactivité.
# Ines : Analyser la recherche par pays 

Pour exploiter le tri de mots clefs effectué par Héloïse et afin qu'Ewen puisse plot le graphique interactif, il faut faire un tri sur le dataframe pour spécifier les mots clés qui apparaissent par pays et/ou par année. 

Pour ce faire, keywords_per_country retourne une liste des mots clefs par pays, avec répétition, et les mots clés sont des mots composés (par exemple "electric vehicle" correspond au même mot clef).

De même, keywords_per_year retourne une liste des mots clefs par année, avec répétition, et les mots clés sont des mots composés (par exemple "electric vehicle" correspond au même mot clef).

Enfin, keywords_per_country_year retourne une liste des mots clefs pour une année et un pays, avec répétition, et les mots clés sont des mots composés (par exemple "electric vehicle" correspond au même mot clef).

Pour correspondre à la liste de mots clefs d'Heloïse, on utilise keywords_split, qui sépare les différentes composantes d'un mot clef : "electric vehicle" devient "electric" d'une part, et "vehicle" de l'autre

filtered_keywords filtre quels mots sont dans la liste de mots principaux d'Heloïse, pour ne retenir que les mots principaux

sans_doublons est assez explicite, elle enlève les doublons dans la liste de mots clefs

On compose toutes ces petites opérations en une grande fonction, country pour les pays, year pour les années, country_&_year pour l'intersection pays et année

Ewen dispose donc en fin de travail de ces trois fonctions pour faire le tri pour ses graphiques.




