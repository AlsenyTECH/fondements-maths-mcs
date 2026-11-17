# -*- coding: utf-8 -*-
"""Registre unique du site : niveaux, modules, nœuds.

Tout le site est engendré à partir de ce fichier : la carte des dépendances,
les sommaires de chaque page, les liens « prérequis » et « ouvre sur ».
Un nœud ajouté ici apparaît partout, sans toucher au HTML.

Champs d'un nœud
----------------
id       identifiant stable, sert d'ancre (#arith-euclide)
titre    intitulé affiché
duree    minutes de travail estimées
objectif une phrase : ce qu'on doit savoir faire en sortant
prereq   liste d'id de nœuds à maîtriser avant
l3       "oui"     déjà vu en licence, à réviser
         "partiel" entrevu en licence, approfondi en master
         "non"     nouveau en master
master   où la notion sert dans le Master MCS
"""


class Noeud:
    def __init__(self, id, titre, duree, objectif, prereq=(), l3="non", master=""):
        self.id = id
        self.titre = titre
        self.duree = duree
        self.objectif = objectif
        self.prereq = list(prereq)
        self.l3 = l3
        self.master = master
        self.corps = ""      # rempli par les fichiers de contenu
        self.video = None    # (fichier, legende, duree) ou None


class Module:
    def __init__(self, id, titre, resume, noeuds):
        self.id = id
        self.titre = titre
        self.resume = resume
        self.noeuds = noeuds


class Niveau:
    def __init__(self, num, titre, sous_titre, resume, modules):
        self.num = num
        self.titre = titre
        self.sous_titre = sous_titre
        self.resume = resume
        self.modules = modules

    @property
    def fichier(self):
        return "niveau-%d.html" % self.num

    @property
    def noeuds(self):
        return [n for m in self.modules for n in m.noeuds]


# ─────────────────────────────────────────────────────────────────────────────
# NIVEAU 0 — Langage et outils
# ─────────────────────────────────────────────────────────────────────────────

M_LANGAGE = Module("langage", "Langage et preuves",
    "Le vocabulaire commun à tous les cours du master, et les quatre façons de démontrer.",
    [
    Noeud("log-quantif", "Logique, quantificateurs, négation", 35,
        "Écrire et nier correctement un énoncé quantifié, et reconnaître ce qu'il faut prouver.",
        l3="oui",
        master="Tout énoncé de sécurité est un énoncé quantifié : « pour tout adversaire, "
               "il existe un simulateur tel que… ». Le nier correctement, c'est savoir ce qu'est une attaque."),
    Noeud("preuves", "Les quatre techniques de preuve", 40,
        "Choisir entre preuve directe, contraposée, absurde et récurrence, et rédiger proprement.",
        prereq=["log-quantif"], l3="oui",
        master="La preuve par réduction, centrale en cryptographie, est une contraposée déguisée : "
               "si quelqu'un casse le schéma, alors il résout le problème difficile."),
    Noeud("ensembles", "Ensembles, applications, cardinaux", 35,
        "Manipuler images, images réciproques, injections et surjections sans hésiter.",
        prereq=["log-quantif"], l3="oui",
        master="Un chiffrement est une application bijective à clé fixée ; une fonction de hachage "
               "est une surjection volontairement non inversible."),
    Noeud("quotients", "Relations d'équivalence et quotients", 45,
        "Construire un ensemble quotient et vérifier qu'une opération y passe au quotient.",
        prereq=["ensembles"], l3="partiel",
        master="C'est la construction qui donne ℤ/nℤ, les corps finis 𝔽p[X]/(P) et les courbes "
               "elliptiques. Si le quotient est flou, tout le master le sera."),
    Noeud("denombrement", "Dénombrement et probabilités discrètes", 40,
        "Compter, et majorer une probabilité par le lemme de l'union et le paradoxe des anniversaires.",
        prereq=["ensembles"], l3="partiel",
        master="Donne la taille de l'espace des clés, le coût d'une recherche exhaustive et "
               "l'attaque des anniversaires sur les fonctions de hachage."),
    ])

NIVEAU_0 = Niveau(0, "Langage et outils", "Le socle commun",
    "Rien d'ici n'est spécifique au master, et c'est exactement pour cela qu'on n'y revient jamais : "
    "tout le monde est censé le savoir. Un quotient mal compris au niveau 0 ressort en géométrie "
    "algébrique six mois plus tard.",
    [M_LANGAGE])


# ─────────────────────────────────────────────────────────────────────────────
# NIVEAU 1 — Arithmétique, groupes, algèbre linéaire
# ─────────────────────────────────────────────────────────────────────────────

M_ARITH = Module("arith", "Arithmétique de ℤ",
    "De la division euclidienne aux résidus quadratiques : le calcul qui fait tourner RSA.",
    [
    Noeud("arith-euclide", "Divisibilité, PGCD, algorithme d'Euclide", 40,
        "Calculer un PGCD à la main et savoir pourquoi l'algorithme termine.",
        prereq=["preuves"], l3="oui",
        master="Premier exemple d'algorithme dont on analyse le coût : c'est le point de départ "
               "du cours de complexité."),
    Noeud("arith-bezout", "Bézout et l'algorithme d'Euclide étendu", 45,
        "Trouver (u, v) tels que au + bv = pgcd(a, b), et en déduire un inverse modulaire.",
        prereq=["arith-euclide"], l3="oui",
        master="C'est l'opération qui calcule la clé privée RSA à partir de l'exposant public : d = e⁻¹ mod φ(n)."),
    Noeud("arith-congruences", "Congruences et l'anneau ℤ/nℤ", 45,
        "Calculer dans ℤ/nℤ et justifier que les opérations y sont bien définies.",
        prereq=["quotients", "arith-euclide"], l3="oui",
        master="L'arithmétique modulaire est le terrain de jeu de presque toute la cryptographie "
               "à clé publique."),
    Noeud("arith-chinois", "Le théorème chinois des restes", 45,
        "Résoudre un système de congruences et décomposer ℤ/nℤ en produit.",
        prereq=["arith-congruences"], l3="partiel",
        master="Accélère le déchiffrement RSA d'un facteur quatre, et c'est aussi la faille "
               "exploitée par certaines attaques par fautes."),
    Noeud("arith-euler", "(ℤ/nℤ)*, indicatrice d'Euler, Fermat", 50,
        "Calculer φ(n), appliquer les théorèmes de Fermat et d'Euler, faire une exponentiation rapide.",
        prereq=["arith-chinois"], l3="partiel",
        master="C'est le théorème qui fait fonctionner RSA : m^(ed) ≡ m (mod n)."),
    Noeud("arith-premiers", "Nombres premiers et tests de primalité", 50,
        "Tester la primalité par Fermat puis Miller-Rabin, et estimer le nombre de premiers.",
        prereq=["arith-euler"], l3="partiel",
        master="Générer une clé RSA ou un groupe pour Diffie-Hellman commence toujours par "
               "tirer un grand premier."),
    Noeud("arith-residus", "Résidus quadratiques, Legendre, Jacobi", 50,
        "Décider si a est un carré modulo p, et calculer un symbole de Jacobi efficacement.",
        prereq=["arith-premiers"], l3="non",
        master="Fonde le chiffrement de Rabin, le cryptosystème de Goldwasser-Micali et les "
               "tests de primalité de Solovay-Strassen."),
    ])

M_GROUPES = Module("grp", "Groupes",
    "La structure qui porte le logarithme discret, de ℤ/nℤ aux courbes elliptiques.",
    [
    Noeud("grp-base", "Groupes, sous-groupes, ordre d'un élément", 45,
        "Reconnaître un groupe, calculer l'ordre d'un élément, dresser une table.",
        prereq=["arith-congruences"], l3="oui",
        master="L'ordre d'un élément mesure la sécurité : un générateur d'ordre trop petit "
               "rend le logarithme discret facile."),
    Noeud("grp-lagrange", "Le théorème de Lagrange", 40,
        "Démontrer Lagrange par les classes, et en tirer Fermat et Euler.",
        prereq=["grp-base", "quotients"], l3="oui",
        master="Donne immédiatement les ordres possibles d'un sous-groupe, donc les paramètres "
               "sûrs d'un protocole."),
    Noeud("grp-cycliques", "Groupes cycliques et générateurs", 50,
        "Décrire tous les sous-groupes d'un groupe cyclique et trouver un générateur.",
        prereq=["grp-lagrange"], l3="partiel",
        master="Diffie-Hellman et ElGamal vivent dans un groupe cyclique ; choisir le générateur "
               "est une décision de sécurité."),
    Noeud("grp-morphismes", "Morphismes, sous-groupes distingués, quotients", 50,
        "Construire un groupe quotient et manipuler noyau et image.",
        prereq=["grp-cycliques"], l3="partiel",
        master="Le passage au quotient est la technique qui réduit un problème difficile "
               "en plusieurs problèmes faciles — c'est l'idée de Pohlig-Hellman."),
    Noeud("grp-isomorphismes", "Les théorèmes d'isomorphisme", 45,
        "Appliquer le premier théorème d'isomorphisme pour identifier un quotient.",
        prereq=["grp-morphismes"], l3="partiel",
        master="Sert à prouver que deux groupes apparemment différents portent le même "
               "problème de logarithme discret."),
    Noeud("grp-abeliens", "Structure des groupes abéliens finis", 50,
        "Décomposer un groupe abélien fini en produit de groupes cycliques.",
        prereq=["grp-isomorphismes", "arith-chinois"], l3="non",
        master="Dit exactement à quoi ressemble le groupe des points d'une courbe elliptique, "
               "et donc comment l'attaquer."),
    ])

M_LIN = Module("lin", "Algèbre linéaire",
    "Les espaces vectoriels relus sur un corps fini quelconque, pas seulement sur ℝ.",
    [
    Noeud("lin-ev", "Espaces vectoriels, bases, dimension", 45,
        "Travailler dans un espace vectoriel sur un corps fini et manipuler bases et dimension.",
        prereq=["ensembles"], l3="oui",
        master="Un code correcteur linéaire est exactement un sous-espace vectoriel de 𝔽qⁿ."),
    Noeud("lin-matrices", "Matrices, rang, pivot de Gauss", 45,
        "Mener un pivot de Gauss sur 𝔽q et en lire le rang et le noyau.",
        prereq=["lin-ev"], l3="oui",
        master="Le décodage par syndrome et la cryptanalyse linéaire sont des pivots de Gauss "
               "sur 𝔽2."),
    Noeud("lin-dualite", "Dualité et orthogonalité", 45,
        "Calculer un orthogonal et utiliser la formule des dimensions.",
        prereq=["lin-matrices"], l3="partiel",
        master="Le code dual et la matrice de contrôle de parité ne sont rien d'autre que "
               "l'orthogonal du code."),
    Noeud("lin-reduction", "Réduction, polynôme minimal", 50,
        "Trouver un polynôme annulateur et s'en servir pour calculer des puissances.",
        prereq=["lin-matrices"], l3="partiel",
        master="Les registres à décalage (LFSR) et les générateurs type XORshift s'analysent "
               "par leur polynôme caractéristique sur 𝔽2."),
    ])

M_PROBA = Module("proba", "Probabilités",
    "Le cadre mesuré des probabilités : ce qui donne un sens à « négligeable » et à « au hasard ».",
    [
    Noeud("proba-espaces", "Espaces probabilisés et tribus", 50,
        "Construire un espace probabilisé et utiliser la continuité monotone d'une probabilité.",
        prereq=["ensembles", "denombrement"], l3="partiel",
        master="Toute définition de sécurité commence par « soit (Ω, A, P) » : c'est le cadre "
               "où l'on parle de l'adversaire et de ses chances."),
    Noeud("proba-bayes", "Conditionnement et formule de Bayes", 45,
        "Calculer une probabilité conditionnelle et inverser un conditionnement par Bayes.",
        prereq=["proba-espaces"], l3="oui",
        master="Un détecteur d'intrusion fiable à 99 % peut se tromper la plupart du temps : "
               "Bayes l'explique, et les attaques bayésiennes l'exploitent."),
    Noeud("proba-va", "Variables aléatoires et lois", 50,
        "Déterminer la loi d'une variable aléatoire et la caractériser par sa fonction de répartition.",
        prereq=["proba-espaces"], l3="partiel",
        master="« Tirer une clé uniformément » est une variable aléatoire : c'est l'objet de "
               "base de tout générateur d'aléa."),
    Noeud("proba-esperance", "Espérance, variance, inégalités de concentration", 55,
        "Calculer une espérance par transfert et majorer une déviation par Markov, Tchebychev, Chernoff.",
        prereq=["proba-va"], l3="partiel",
        master="Donne le coût moyen d'une recherche exhaustive et les bornes qui rendent une "
               "probabilité d'erreur négligeable."),
    Noeud("proba-independance", "Indépendance et lemmes de Borel-Cantelli", 50,
        "Démontrer ou réfuter l'indépendance, et appliquer les deux lemmes de Borel-Cantelli.",
        prereq=["proba-bayes", "proba-va"], l3="partiel",
        master="Le XOR de bits indépendants et le lemme d'empilement sont le cœur de la "
               "cryptanalyse linéaire."),
    Noeud("proba-tcl", "Lois des grands nombres et théorème central limite", 60,
        "Démontrer la loi faible des grands nombres et appliquer le théorème central limite.",
        prereq=["proba-esperance", "proba-independance"], l3="partiel",
        master="Justifie tous les tests statistiques, et donc tous les tests d'aléa d'un générateur."),
    ])

NIVEAU_1 = Niveau(1, "Arithmétique, groupes, algèbre linéaire", "Le tronc",
    "C'est le niveau qui porte tout le reste. Une lacune ici ne se voit pas tout de suite : "
    "elle se manifeste trois mois plus tard, sous la forme d'un cours de géométrie algébrique "
    "ou de codes qui « ne passe pas ».",
    [M_ARITH, M_GROUPES, M_LIN, M_PROBA])


# ─────────────────────────────────────────────────────────────────────────────
# NIVEAU 2 — Anneaux, polynômes, modules
# ─────────────────────────────────────────────────────────────────────────────

M_ANNEAUX = Module("ann", "Anneaux et idéaux",
    "Quotients, idéaux, anneaux principaux : la clé de tout le niveau 3.",
    [
    Noeud("ann-base", "Anneaux, morphismes, unités", 45,
        "Reconnaître un anneau, ses inversibles et ses diviseurs de zéro.",
        prereq=["grp-morphismes"], l3="partiel",
        master="ℤ/nℤ n'est un corps que si n est premier : c'est la première condition de "
               "tout choix de paramètres."),
    Noeud("ann-ideaux", "Idéaux et anneaux quotients", 55,
        "Construire A/I et reconnaître quand un morphisme passe au quotient.",
        prereq=["ann-base", "quotients"], l3="non",
        master="𝔽p[X]/(P) est le corps dans lequel AES fait toutes ses multiplications."),
    Noeud("ann-premiers-max", "Idéaux premiers et maximaux", 50,
        "Décider si A/I est intègre ou un corps, en lisant l'idéal.",
        prereq=["ann-ideaux"], l3="non",
        master="C'est le critère qui dit si une construction donne un corps — donc si le "
               "cryptosystème a un sens."),
    Noeud("ann-euclidiens", "Euclidien ⊂ principal ⊂ factoriel", 55,
        "Situer un anneau dans la hiérarchie et savoir ce que chaque niveau garantit.",
        prereq=["ann-premiers-max", "arith-euclide"], l3="non",
        master="La factorisation unique est ce qui rend le problème de factorisation bien posé, "
               "et son échec dans certains anneaux a cassé des schémas réels."),
    Noeud("ann-chinois", "Le théorème chinois dans un anneau", 40,
        "Décomposer A/I₁I₂ en produit quand les idéaux sont comaximaux.",
        prereq=["ann-euclidiens", "arith-chinois"], l3="non",
        master="Généralise l'accélération CRT de RSA, et sert au partage de secret "
               "de Mignotte et Asmuth-Bloom."),
    ])

M_POLY = Module("poly", "Polynômes",
    "K[X] comme modèle d'anneau euclidien, et la fabrique des corps finis.",
    [
    Noeud("poly-division", "K[X] : division euclidienne, PGCD", 45,
        "Diviser, calculer un PGCD de polynômes, appliquer Bézout dans K[X].",
        prereq=["ann-euclidiens"], l3="oui",
        master="Le décodage de Reed-Solomon est un algorithme d'Euclide étendu arrêté à mi-chemin."),
    Noeud("poly-irreductible", "Irréductibilité, critère d'Eisenstein", 50,
        "Décider de l'irréductibilité d'un polynôme sur ℚ et sur 𝔽p.",
        prereq=["poly-division"], l3="partiel",
        master="Sans polynôme irréductible, pas de corps fini : c'est le premier paramètre "
               "d'une implémentation d'AES."),
    Noeud("poly-quotient", "Les quotients K[X]/(P)", 50,
        "Calculer dans K[X]/(P) et reconnaître quand c'est un corps.",
        prereq=["poly-irreductible", "ann-premiers-max"], l3="non",
        master="C'est littéralement la structure de données d'un corps fini dans le code."),
    ])

M_MODULES = Module("mod", "Modules",
    "Les espaces vectoriels sur un anneau : le cadre du post-quantique.",
    [
    Noeud("mod-base", "Modules, sous-modules, morphismes", 50,
        "Transposer le vocabulaire des espaces vectoriels aux modules et voir ce qui casse.",
        prereq=["ann-ideaux", "lin-ev"], l3="non",
        master="Le « Module » de Module-LWE, la base de ML-KEM (Kyber), c'est exactement cet objet."),
    Noeud("mod-libres", "Modules libres, de type fini, torsion", 50,
        "Distinguer libre, de type fini et sans torsion, avec des contre-exemples.",
        prereq=["mod-base"], l3="non",
        master="La torsion d'une courbe elliptique, qui sert aux couplages, est un module de torsion."),
    Noeud("mod-structure", "Modules sur un anneau principal", 60,
        "Appliquer le théorème de structure et retrouver les groupes abéliens finis.",
        prereq=["mod-libres", "ann-euclidiens", "grp-abeliens"], l3="non",
        master="Donne la forme normale de Smith, qui calcule la structure du groupe des "
               "points d'une courbe."),
    Noeud("mod-noetherien", "Anneaux et modules noethériens", 45,
        "Manipuler la condition de chaîne ascendante et le théorème de la base de Hilbert.",
        prereq=["mod-structure"], l3="non",
        master="C'est l'hypothèse qui rend la géométrie algébrique calculable, donc les "
               "bases de Gröbner et les attaques algébriques."),
    ])

M_STAT = Module("stat", "Statistique",
    "Estimer et décider à partir d'un échantillon : le langage des tests d'aléa et de l'apprentissage.",
    [
    Noeud("stat-echantillon", "Échantillonnage et estimateurs", 45,
        "Calculer espérance et variance d'une moyenne empirique et corriger le biais de la variance.",
        prereq=["proba-tcl"], l3="partiel",
        master="On ne teste jamais toutes les sorties d'un générateur : on en tire un échantillon."),
    Noeud("stat-lois", "Lois du khi-deux, de Student et de Fisher", 50,
        "Construire les trois lois et démontrer la loi de la moyenne studentisée.",
        prereq=["stat-echantillon"], l3="non",
        master="Ce sont les lois de référence de tous les tests utilisés en sécurité."),
    Noeud("stat-estimation", "Estimation et maximum de vraisemblance", 55,
        "Construire un estimateur par maximum de vraisemblance et comparer deux estimateurs.",
        prereq=["stat-echantillon"], l3="non",
        master="Entraîner un modèle d'apprentissage, c'est maximiser une vraisemblance."),
    Noeud("stat-ic", "Intervalles de confiance", 45,
        "Construire un intervalle de confiance pour une moyenne, une variance, une proportion.",
        prereq=["stat-lois", "stat-estimation"], l3="partiel",
        master="Comparer honnêtement deux implémentations d'un chiffrement suppose une marge d'erreur."),
    Noeud("stat-tests", "Tests d'hypothèses", 55,
        "Poser un test, calculer une p-valeur, et démontrer le lemme de Neyman-Pearson.",
        prereq=["stat-ic"], l3="non",
        master="Un distingueur en cryptanalyse est exactement un test statistique."),
    Noeud("stat-khi2", "Test du khi-deux et tests d'aléa", 50,
        "Tester l'uniformité et l'indépendance d'une suite de symboles.",
        prereq=["stat-tests"], l3="non",
        master="C'est la brique des batteries de tests d'aléa, dont celle du NIST."),
    ])

NIVEAU_2 = Niveau(2, "Anneaux, polynômes, modules", "La charnière",
    "Le niveau que presque personne n'a vu complètement en licence, et dont dépendent "
    "les niveaux 3 et 4. Si la géométrie algébrique paraît abstraite, la cause est ici.",
    [M_ANNEAUX, M_POLY, M_MODULES, M_STAT])


# ─────────────────────────────────────────────────────────────────────────────
# NIVEAU 3 — Corps
# ─────────────────────────────────────────────────────────────────────────────

M_EXT = Module("ext", "Extensions de corps",
    "Comment on fabrique un corps plus grand, et ce qu'on y gagne.",
    [
    Noeud("ext-degre", "Extensions, degré, multiplicativité", 45,
        "Calculer un degré d'extension et utiliser la formule des degrés.",
        prereq=["poly-quotient"], l3="non",
        master="Le degré fixe la taille du corps, donc la taille des clés et le coût des calculs."),
    Noeud("ext-algebrique", "Éléments algébriques, polynôme minimal", 50,
        "Déterminer le polynôme minimal d'un élément et le degré qu'il engendre.",
        prereq=["ext-degre"], l3="non",
        master="Représenter un élément d'un corps fini, c'est donner son polynôme minimal."),
    Noeud("ext-decomposition", "Corps de rupture et de décomposition", 50,
        "Construire un corps où un polynôme donné a toutes ses racines.",
        prereq=["ext-algebrique"], l3="non",
        master="C'est la construction qui garantit l'existence de 𝔽q pour tout q = pⁿ."),
    Noeud("ext-galois", "Notions de théorie de Galois", 55,
        "Décrire la correspondance entre sous-groupes et sous-corps sur un exemple.",
        prereq=["ext-decomposition", "grp-morphismes"], l3="non",
        master="Explique la structure des sous-corps de 𝔽q et les descentes de corps "
               "utilisées en cryptanalyse."),
    ])

M_CF = Module("cf", "Corps finis",
    "𝔽q : l'objet le plus utilisé de tout le master.",
    [
    Noeud("cf-existence", "Existence et unicité de 𝔽q", 50,
        "Démontrer qu'il existe un unique corps à q = pⁿ éléments, à isomorphisme près.",
        prereq=["ext-decomposition"], l3="non",
        master="Justifie qu'AES et un code Reed-Solomon parlent bien du même 𝔽₂₅₆."),
    Noeud("cf-construction", "Construction et sous-corps de 𝔽q", 50,
        "Construire 𝔽₈, 𝔽₁₆, 𝔽₂₅₆ et décrire leurs sous-corps.",
        prereq=["cf-existence", "poly-quotient"], l3="non",
        master="C'est l'implémentation : table de logarithmes, multiplication par réduction modulo P."),
    Noeud("cf-cyclique", "Cyclicité de 𝔽q* et éléments primitifs", 45,
        "Démontrer que 𝔽q* est cyclique et trouver un élément primitif.",
        prereq=["cf-construction", "grp-cycliques"], l3="non",
        master="Donne le générateur de Diffie-Hellman sur corps fini et les codes BCH primitifs."),
    Noeud("cf-frobenius", "Frobenius, trace, norme, factorisation", 55,
        "Utiliser le Frobenius pour factoriser un polynôme sur 𝔽q.",
        prereq=["cf-cyclique", "ext-galois"], l3="non",
        master="Le Frobenius est au cœur du comptage de points sur les courbes elliptiques "
               "et de l'algorithme de Berlekamp."),
    ])

NIVEAU_3 = Niveau(3, "Corps et corps finis", "La fabrique",
    "Tout ce que le master calcule — AES, les codes, les courbes — se calcule dans un corps fini. "
    "Ce niveau est court mais il est le passage obligé.",
    [M_EXT, M_CF])


# ─────────────────────────────────────────────────────────────────────────────
# NIVEAU 4 — Les branches spécialisées
# ─────────────────────────────────────────────────────────────────────────────

M_TAN = Module("tan", "Théorie algorithmique des nombres",
    "Les trois problèmes dont dépend la sécurité : primalité, factorisation, logarithme discret.",
    [
    Noeud("tan-primalite", "Tests et preuves de primalité", 55,
        "Démontrer les tests de Solovay-Strassen et Miller-Rabin, et certifier un premier par Pocklington.",
        prereq=["arith-residus", "proba-esperance"], l3="non",
        master="Chaque génération de clé RSA ou DSA commence par là."),
    Noeud("tan-factorisation", "Factorisation : Pollard p−1 et rho", 55,
        "Mettre en œuvre Pollard p−1 et rho, et justifier le coût en racine de p.",
        prereq=["tan-primalite", "grp-cycliques"], l3="non",
        master="Explique pourquoi les premiers d'une clé RSA doivent éviter certaines formes."),
    Noeud("tan-crible", "Le crible quadratique", 60,
        "Factoriser par congruences de carrés et ramener la recherche à de l'algèbre linéaire sur 𝔽₂.",
        prereq=["tan-factorisation", "lin-matrices"], l3="non",
        master="Ses successeurs décident de la taille des clés RSA : c'est pourquoi 2048 bits."),
    Noeud("tan-logdiscret", "Logarithme discret : pas de bébé, Pohlig-Hellman, rho", 60,
        "Calculer un logarithme discret par les trois méthodes génériques et majorer leur coût.",
        prereq=["tan-factorisation", "grp-abeliens"], l3="non",
        master="Attaques de référence contre Diffie-Hellman, ElGamal et ECDSA."),
    Noeud("tan-indices", "Le calcul d'indices", 55,
        "Calculer un logarithme discret dans 𝔽p* par une base de facteurs.",
        prereq=["tan-logdiscret", "tan-crible"], l3="non",
        master="Explique pourquoi les courbes elliptiques permettent des clés bien plus courtes que 𝔽p*."),
    ])

M_CODES = Module("codes", "Codes correcteurs",
    "L'algèbre linéaire sur 𝔽q mise au service de la fiabilité — et du post-quantique.",
    [
    Noeud("codes-lineaires", "Codes linéaires, distance, matrices G et H", 50,
        "Passer de G à H, calculer la distance minimale et le nombre d'erreurs corrigibles.",
        prereq=["lin-dualite", "cf-construction"], l3="partiel",
        master="Le modèle de tout code, du stockage aux communications spatiales."),
    Noeud("codes-syndrome", "Décodage par syndrome", 45,
        "Décoder un mot reçu en lisant son syndrome.",
        prereq=["codes-lineaires"], l3="partiel",
        master="Le décodage d'un code quelconque est NP-difficile : c'est l'hypothèse de McEliece."),
    Noeud("codes-bornes", "Bornes : Singleton, Hamming, Gilbert-Varshamov", 45,
        "Situer un code par rapport aux bornes et reconnaître un code MDS ou parfait.",
        prereq=["codes-syndrome", "denombrement"], l3="non",
        master="Dit ce qu'on peut espérer d'un code, et donc ce qu'un schéma peut promettre."),
    Noeud("codes-cycliques", "Codes cycliques et BCH", 55,
        "Décrire un code cyclique comme un idéal et construire un code BCH.",
        prereq=["codes-bornes", "poly-quotient", "cf-cyclique"], l3="non",
        master="Les codes qu'on sait implémenter en matériel, d'où leur présence partout."),
    Noeud("codes-rs", "Reed-Solomon et son décodage", 55,
        "Construire un code de Reed-Solomon, démontrer qu'il est MDS et le décoder par Euclide étendu.",
        prereq=["codes-cycliques", "poly-division"], l3="non",
        master="QR codes, disques, transmissions : Reed-Solomon est partout."),
    Noeud("codes-goppa", "Codes de Goppa et chiffrement de McEliece", 55,
        "Construire un code de Goppa et dérouler un chiffrement de McEliece jouet.",
        prereq=["codes-rs"], l3="non",
        master="Classic McEliece, candidat post-quantique fondé sur les codes."),
    ])

M_GA = Module("ga", "Géométrie algébrique et courbes",
    "Des variétés affines à Riemann-Roch, jusqu'aux courbes elliptiques et aux couplages.",
    [
    Noeud("ga-varietes", "Variétés affines et topologie de Zariski", 55,
        "Passer d'un système d'équations à un idéal, et décrire les fermés de Zariski.",
        prereq=["mod-noetherien", "ann-premiers-max"], l3="non",
        master="Le dictionnaire équations ↔ idéaux, base des attaques algébriques."),
    Noeud("ga-noether", "Extensions entières et normalisation de Noether", 60,
        "Démontrer le lemme de normalisation de Noether et ses conséquences sur la dimension.",
        prereq=["ga-varietes", "ext-algebrique"], l3="non",
        master="L'outil technique qui ouvre la preuve du Nullstellensatz."),
    Noeud("ga-nullstellensatz", "Le Nullstellensatz", 55,
        "Démontrer les formes faible et forte du théorème des zéros de Hilbert.",
        prereq=["ga-noether"], l3="non",
        master="Dit quand un système polynomial n'a pas de solution : c'est la logique des bases de Gröbner."),
    Noeud("ga-projectif", "Espace projectif et courbes planes", 50,
        "Homogénéiser une équation, trouver les points à l'infini et tester la lissité.",
        prereq=["ga-nullstellensatz"], l3="non",
        master="Les coordonnées projectives évitent les inversions coûteuses dans les calculs sur courbes."),
    Noeud("ga-locaux", "Anneaux locaux et valuations", 55,
        "Définir l'ordre d'annulation d'une fonction en un point lisse d'une courbe.",
        prereq=["ga-projectif", "ann-euclidiens"], l3="non",
        master="Mesurer zéros et pôles : la matière première des diviseurs et des couplages."),
    Noeud("ga-diviseurs", "Diviseurs et groupe de Picard", 55,
        "Calculer le diviseur d'une fonction et le groupe des classes de diviseurs.",
        prereq=["ga-locaux", "grp-abeliens"], l3="non",
        master="Le groupe de Picard d'une courbe elliptique, c'est la courbe elle-même."),
    Noeud("ga-riemann-roch", "Le théorème de Riemann-Roch", 60,
        "Énoncer Riemann-Roch, le démontrer en genre 0 et 1, et en déduire le genre d'une courbe.",
        prereq=["ga-diviseurs", "lin-ev"], l3="non",
        master="Justifie qu'une courbe de genre 1 a une équation de Weierstrass."),
    Noeud("ga-elliptiques", "Courbes elliptiques : la loi de groupe", 60,
        "Additionner deux points et démontrer que la loi définit un groupe abélien.",
        prereq=["ga-riemann-roch", "cf-construction"], l3="non",
        master="Le groupe de ECDH, ECDSA, des signatures de Bitcoin et de TLS 1.3."),
    Noeud("ga-isogenies", "Isogénies, Frobenius et points de torsion", 55,
        "Décrire la torsion et le Frobenius d'une courbe sur un corps fini.",
        prereq=["ga-elliptiques", "cf-frobenius", "mod-libres"], l3="non",
        master="Les isogénies fondent aussi une famille de schémas post-quantiques."),
    Noeud("ga-hasse", "Théorème de Hasse et comptage de points", 55,
        "Démontrer le théorème de Hasse et compter les points d'une courbe.",
        prereq=["ga-isogenies"], l3="non",
        master="Choisir une courbe sûre, c'est compter ses points et vérifier l'ordre."),
    Noeud("ga-couplages", "Couplages, algorithme de Miller, attaque MOV", 60,
        "Calculer un couplage de Weil ou de Tate et en déduire l'attaque MOV.",
        prereq=["ga-hasse"], l3="non",
        master="Cryptographie à base d'identité, signatures BLS — et une attaque."),
    ])

M_RESEAUX = Module("res", "Réseaux euclidiens",
    "La branche qui porte le post-quantique normalisé par le NIST.",
    [
    Noeud("res-base", "Réseaux, bases et Gram-Schmidt", 50,
        "Changer de base dans un réseau et calculer son déterminant par Gram-Schmidt.",
        prereq=["lin-dualite", "mod-libres"], l3="non",
        master="Un réseau est un ℤ-module libre plongé dans ℝⁿ : le niveau 2 sert ici directement."),
    Noeud("res-minkowski", "Le théorème de Minkowski", 50,
        "Démontrer le théorème de Minkowski et majorer le plus court vecteur.",
        prereq=["res-base"], l3="non",
        master="Dit à quelle taille de solution s'attendre : la base de toute estimation de sécurité."),
    Noeud("res-lll", "SVP, CVP et l'algorithme LLL", 60,
        "Démontrer que LLL termine et ce qu'il garantit, après la réduction de Gauss en dimension 2.",
        prereq=["res-minkowski"], l3="non",
        master="LLL est l'outil de cryptanalyse le plus polyvalent connu."),
    Noeud("res-cryptanalyse", "Cryptanalyse par réseaux", 55,
        "Casser un sac à dos et un RSA à petite racine par réduction de réseau.",
        prereq=["res-lll"], l3="non",
        master="Coppersmith et les attaques sur nonces biaisés de ECDSA."),
    Noeud("res-lwe", "LWE, Regev et Module-LWE", 60,
        "Énoncer LWE, démontrer la correction du chiffrement de Regev et passer à Module-LWE.",
        prereq=["res-lll", "mod-structure", "proba-tcl"], l3="non",
        master="L'hypothèse de ML-KEM et ML-DSA, standards post-quantiques du NIST."),
    ])

M_CPLX = Module("cplx", "Complexité et information",
    "Ce qui donne un sens précis au mot « difficile ».",
    [
    Noeud("cplx-turing", "Machines de Turing et décidabilité", 50,
        "Définir une machine de Turing et démontrer l'indécidabilité de l'arrêt.",
        prereq=["preuves", "arith-euclide"], l3="partiel",
        master="Le modèle de calcul sur lequel reposent toutes les définitions d'efficacité."),
    Noeud("cplx-p-np", "Les classes P et NP, réductions", 55,
        "Placer un problème dans P ou NP et construire une réduction polynomiale.",
        prereq=["cplx-turing"], l3="partiel",
        master="Sans ce vocabulaire, aucune affirmation de sécurité n'est formulable."),
    Noeud("cplx-cook", "Le théorème de Cook-Levin", 60,
        "Démontrer que SAT est NP-complet, puis 3-SAT.",
        prereq=["cplx-p-np"], l3="non",
        master="Explique pourquoi la NP-difficulté seule ne suffit pas à faire un cryptosystème."),
    Noeud("cplx-probabiliste", "Classes probabilistes", 50,
        "Définir BPP et RP et démontrer l'amplification d'un algorithme probabiliste.",
        prereq=["cplx-p-np", "proba-esperance"], l3="non",
        master="Les adversaires de la cryptographie sont des algorithmes probabilistes."),
    Noeud("cplx-sens-unique", "Fonctions à sens unique et pseudo-aléa", 55,
        "Définir une fonction à sens unique et un générateur pseudo-aléatoire.",
        prereq=["cplx-probabiliste"], l3="non",
        master="L'objet minimal dont dépend toute la cryptographie moderne."),
    Noeud("cplx-entropie", "Entropie et secret parfait de Shannon", 50,
        "Calculer une entropie et démontrer le théorème du secret parfait.",
        prereq=["proba-va", "denombrement"], l3="non",
        master="Démontre que le masque jetable est inviolable, et pourquoi il est inutilisable."),
    Noeud("cplx-reductions", "Preuves de sécurité par réduction", 55,
        "Écrire un jeu de sécurité et une preuve « si l'adversaire gagne, on résout le problème ».",
        prereq=["cplx-sens-unique", "cplx-entropie"], l3="non",
        master="La forme de toute preuve de sécurité moderne."),
    ])

M_IA = Module("ia", "Statistique, sécurité et IA",
    "Là où la statistique rencontre la sécurité et l'apprentissage automatique.",
    [
    Noeud("ia-tests-alea", "Tests statistiques d'aléa", 50,
        "Appliquer une batterie de tests d'aléa et interpréter correctement les p-valeurs.",
        prereq=["stat-khi2", "lin-reduction"], l3="non",
        master="Évaluer un générateur, de XORshift aux tests du NIST."),
    Noeud("ia-canaux", "Attaques par canaux auxiliaires", 55,
        "Retrouver une clé par corrélation entre consommation électrique et calcul.",
        prereq=["stat-tests", "cf-construction"], l3="non",
        master="La menace principale contre les cartes à puce et les objets connectés."),
    Noeud("ia-distingueurs", "La cryptanalyse comme test statistique", 55,
        "Construire un distingueur linéaire et estimer le nombre de données nécessaires.",
        prereq=["stat-tests", "proba-independance", "cplx-reductions"], l3="non",
        master="Cryptanalyse linéaire et différentielle, jusqu'aux distingueurs par réseaux de neurones."),
    Noeud("ia-apprentissage", "L'apprentissage vu comme estimation", 55,
        "Entraîner une régression logistique par maximum de vraisemblance et descente de gradient.",
        prereq=["stat-estimation", "lin-matrices"], l3="non",
        master="Le socle statistique de l'apprentissage automatique, juste ce qu'il faut."),
    Noeud("ia-attaques", "Attaquer un modèle d'apprentissage", 50,
        "Construire un exemple adverse et décrire empoisonnement, extraction et inférence d'appartenance.",
        prereq=["ia-apprentissage"], l3="non",
        master="La sécurité des systèmes d'IA eux-mêmes."),
    Noeud("ia-confidentialite", "Confidentialité différentielle", 50,
        "Démontrer la confidentialité du mécanisme de Laplace et composer les budgets.",
        prereq=["proba-esperance", "ia-apprentissage"], l3="non",
        master="Protéger les données qui ont servi à entraîner un modèle."),
    Noeud("ia-homomorphe", "Calculer sur des données chiffrées", 55,
        "Construire une addition homomorphe à partir de LWE et décrire l'apprentissage fédéré.",
        prereq=["res-lwe", "ia-apprentissage"], l3="non",
        master="Faire tourner un modèle sur des données qu'il ne voit jamais en clair."),
    ])

NIVEAU_4 = Niveau(4, "Les branches spécialisées", "Les applications",
    "Ici chaque branche correspond à un cours du master. Elles sont largement indépendantes "
    "les unes des autres, mais reposent toutes sur les niveaux 1 à 3.",
    [M_TAN, M_CODES, M_GA, M_RESEAUX, M_CPLX, M_IA])


NIVEAUX = [NIVEAU_0, NIVEAU_1, NIVEAU_2, NIVEAU_3, NIVEAU_4]

# index global id -> (noeud, niveau, module)
INDEX = {}
for _niv in NIVEAUX:
    for _mod in _niv.modules:
        for _n in _mod.noeuds:
            INDEX[_n.id] = (_n, _niv, _mod)


def lien(nid):
    """Lien HTML vers un nœud, depuis n'importe quelle page."""
    n, niv, _ = INDEX[nid]
    return '<a href="%s#%s">%s</a>' % (niv.fichier, nid, n.titre)


def ouvre_sur(nid):
    """Les nœuds qui ont celui-ci pour prérequis direct."""
    return [autre for autre in INDEX if nid in INDEX[autre][0].prereq]


def verifier():
    """Garde-fou : tout prérequis doit exister et précéder le nœud."""
    ordre = {}
    k = 0
    for niv in NIVEAUX:
        for n in niv.noeuds:
            ordre[n.id] = k
            k += 1
    problemes = []
    for nid, (n, _, _) in INDEX.items():
        for p in n.prereq:
            if p not in INDEX:
                problemes.append("%s : prérequis inconnu %r" % (nid, p))
            elif ordre[p] >= ordre[nid]:
                problemes.append("%s : prérequis %r vient après" % (nid, p))
    return problemes


if __name__ == "__main__":
    pbs = verifier()
    total = len(INDEX)
    print("%d nœuds, %d modules, %d niveaux" % (
        total, sum(len(n.modules) for n in NIVEAUX), len(NIVEAUX)))
    for niv in NIVEAUX:
        print("  niveau %d : %2d nœuds, %d min" % (
            niv.num, len(niv.noeuds), sum(n.duree for n in niv.noeuds)))
    heures = sum(v[0].duree for v in INDEX.values()) / 60
    print("heures de travail estimées : %.1f" % heures)
    print("problèmes :", pbs or "aucun")
