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

NIVEAU_1 = Niveau(1, "Arithmétique, groupes, algèbre linéaire", "Le tronc",
    "C'est le niveau qui porte tout le reste. Une lacune ici ne se voit pas tout de suite : "
    "elle se manifeste trois mois plus tard, sous la forme d'un cours de géométrie algébrique "
    "ou de codes qui « ne passe pas ».",
    [M_ARITH, M_GROUPES, M_LIN])


# ─────────────────────────────────────────────────────────────────────────────
# NIVEAU 2 — Anneaux, polynômes, modules
# ─────────────────────────────────────────────────────────────────────────────

M_ANNEAUX = Module("ann", "Anneaux et idéaux",
    "Le cours de Pr Diankha, et la clé de tout le niveau 3.",
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

NIVEAU_2 = Niveau(2, "Anneaux, polynômes, modules", "La charnière",
    "Le niveau que presque personne n'a vu complètement en licence, et dont dépendent "
    "les niveaux 3 et 4. Si la géométrie algébrique paraît abstraite, la cause est ici.",
    [M_ANNEAUX, M_POLY, M_MODULES])


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
    Noeud("tan-primalite", "Tests de primalité et preuves de primalité", 55,
        "Implémenter Miller-Rabin et majorer sa probabilité d'erreur.",
        prereq=["arith-residus", "denombrement"], l3="non",
        master="Chaque génération de clé RSA ou DSA commence par là."),
    Noeud("tan-factorisation", "Factorisation : Pollard, crible quadratique", 60,
        "Mettre en œuvre Pollard rho et p−1, et comprendre l'idée du crible.",
        prereq=["tan-primalite", "grp-cycliques"], l3="non",
        master="Fixe la taille de clé RSA : c'est le meilleur algorithme connu qui décide "
               "si 2048 bits suffisent."),
    Noeud("tan-logdiscret", "Logarithme discret : BSGS, rho, Pohlig-Hellman", 60,
        "Calculer un logarithme discret par pas de bébé et par Pohlig-Hellman.",
        prereq=["tan-factorisation", "grp-abeliens"], l3="non",
        master="C'est l'attaque de référence contre Diffie-Hellman, ElGamal et ECDSA."),
    ])

M_GA = Module("ga", "Géométrie algébrique et courbes",
    "Le cours de Pr Sankaré, jusqu'aux courbes elliptiques et aux couplages.",
    [
    Noeud("ga-varietes", "Variétés affines, idéaux, Nullstellensatz", 60,
        "Traduire un système d'équations en idéal et revenir aux solutions.",
        prereq=["mod-noetherien", "ann-premiers-max"], l3="non",
        master="Le dictionnaire équations ↔ idéaux est la base des attaques algébriques "
               "et des bases de Gröbner."),
    Noeud("ga-courbes", "Courbes algébriques, points singuliers, genre", 55,
        "Reconnaître une courbe lisse et calculer son genre dans les cas simples.",
        prereq=["ga-varietes"], l3="non",
        master="Le genre décide du cryptosystème : genre 1 pour les courbes elliptiques, "
               "genre supérieur pour les hyperelliptiques."),
    Noeud("ga-elliptiques", "Courbes elliptiques : la loi de groupe", 60,
        "Additionner deux points et démontrer que la loi est bien un groupe.",
        prereq=["ga-courbes", "cf-construction", "grp-base"], l3="non",
        master="C'est le groupe de ECDH, ECDSA et des signatures de Bitcoin et de TLS 1.3."),
    Noeud("ga-hasse", "Théorème de Hasse, torsion, comptage de points", 55,
        "Encadrer le nombre de points et décrire la structure du groupe.",
        prereq=["ga-elliptiques", "cf-frobenius", "mod-libres"], l3="non",
        master="Choisir une courbe sûre, c'est compter ses points et vérifier que l'ordre "
               "a un grand facteur premier."),
    Noeud("ga-couplages", "Diviseurs et couplages de Weil et Tate", 60,
        "Comprendre ce qu'est un couplage et à quelle condition il est calculable.",
        prereq=["ga-hasse"], l3="non",
        master="Fonde la cryptographie basée sur l'identité, les signatures courtes BLS, "
               "et aussi l'attaque MOV."),
    ])

M_CODES = Module("codes", "Codes correcteurs",
    "L'algèbre linéaire sur 𝔽q mise au service de la fiabilité — et de la cryptographie post-quantique.",
    [
    Noeud("codes-lineaires", "Codes linéaires, distance, matrices G et H", 50,
        "Passer de G à H, calculer la distance minimale et le nombre d'erreurs corrigibles.",
        prereq=["lin-dualite", "cf-construction"], l3="partiel",
        master="C'est le modèle de tout code : du CD-ROM aux communications spatiales."),
    Noeud("codes-syndrome", "Décodage par syndrome", 45,
        "Décoder un mot reçu en lisant son syndrome.",
        prereq=["codes-lineaires"], l3="partiel",
        master="Le problème du décodage par syndrome est NP-difficile : c'est l'hypothèse "
               "de sécurité de McEliece."),
    Noeud("codes-bornes", "Bornes : Singleton, Hamming, Gilbert-Varshamov", 45,
        "Situer un code par rapport aux bornes et reconnaître un code MDS ou parfait.",
        prereq=["codes-syndrome", "denombrement"], l3="non",
        master="Dit ce qu'on peut espérer d'un code — et donc ce qu'un schéma peut promettre."),
    Noeud("codes-cycliques", "Codes cycliques et BCH", 55,
        "Décrire un code cyclique par son polynôme générateur et construire un BCH.",
        prereq=["codes-bornes", "poly-quotient", "cf-cyclique"], l3="non",
        master="Les codes cycliques sont ceux qu'on sait implémenter en matériel, "
               "d'où leur omniprésence industrielle."),
    Noeud("codes-rs-goppa", "Reed-Solomon et codes de Goppa", 55,
        "Construire un code de Reed-Solomon et décrire le rôle des codes de Goppa.",
        prereq=["codes-cycliques"], l3="non",
        master="Reed-Solomon est partout (QR codes, stockage) ; Goppa est la brique de "
               "Classic McEliece, finaliste post-quantique."),
    ])

M_RESEAUX = Module("res", "Réseaux euclidiens",
    "La branche qui porte le post-quantique normalisé par le NIST.",
    [
    Noeud("res-base", "Réseaux, déterminant, théorème de Minkowski", 55,
        "Manipuler une base de réseau et majorer la norme du plus court vecteur.",
        prereq=["lin-dualite", "mod-libres"], l3="non",
        master="Un réseau est un module libre sur ℤ plongé dans ℝⁿ : le niveau 2 sert ici directement."),
    Noeud("res-lll", "SVP, CVP et l'algorithme LLL", 60,
        "Dérouler LLL sur un petit exemple et savoir ce qu'il garantit.",
        prereq=["res-base"], l3="non",
        master="LLL casse les sacs à dos, les RSA à petit exposant (Coppersmith) et les "
               "signatures à nonce biaisé."),
    Noeud("res-lwe", "LWE, Ring-LWE, Module-LWE", 60,
        "Énoncer le problème LWE et sa variante sur les modules.",
        prereq=["res-lll", "mod-structure"], l3="non",
        master="C'est l'hypothèse de ML-KEM (Kyber) et ML-DSA (Dilithium), les standards "
               "post-quantiques du NIST."),
    ])

M_CPLX = Module("cplx", "Complexité et information",
    "Le cours de complexité : ce qui donne un sens au mot « difficile ».",
    [
    Noeud("cplx-turing", "Machines de Turing, P, NP, réductions", 55,
        "Définir une classe de complexité et construire une réduction polynomiale.",
        prereq=["preuves", "arith-euclide"], l3="partiel",
        master="Sans ce vocabulaire, aucune affirmation de sécurité n'est formulable."),
    Noeud("cplx-probabiliste", "Algorithmes probabilistes, fonctions à sens unique", 50,
        "Distinguer BPP de P et définir une fonction à sens unique.",
        prereq=["cplx-turing", "denombrement"], l3="non",
        master="La fonction à sens unique est l'objet minimal dont dépend toute la "
               "cryptographie moderne."),
    Noeud("cplx-entropie", "Entropie, secret parfait de Shannon", 50,
        "Calculer une entropie et démontrer le théorème du secret parfait.",
        prereq=["denombrement"], l3="non",
        master="Démontre que le masque jetable est inviolable, et pourquoi il est inutilisable "
               "en pratique."),
    Noeud("cplx-reductions", "Preuves de sécurité par réduction", 55,
        "Lire et écrire une preuve « si l'adversaire gagne, alors on résout le problème ».",
        prereq=["cplx-probabiliste", "cplx-entropie"], l3="non",
        master="C'est la forme que prend toute preuve de sécurité d'un schéma moderne."),
    ])

NIVEAU_4 = Niveau(4, "Les branches spécialisées", "Les applications",
    "Ici chaque branche est un cours du master. Elles sont indépendantes les unes des autres, "
    "mais elles reposent toutes sur les niveaux 1 à 3.",
    [M_TAN, M_GA, M_CODES, M_RESEAUX, M_CPLX])


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
