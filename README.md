# Fondements mathématiques du Master MCS

Site public sur le socle mathématique du Master Mathématiques, Cryptographie et Sécurité :
62 nœuds répartis en 5 niveaux, chacun relié à ce qu'il ouvre dans le master.

## Publier le site

Le site est **statique** : tout ce qui est dans `docs/` se publie tel quel.

```bash
python3 build.py          # régénère docs/ à partir du contenu
```

Pour GitHub Pages : pousser le dépôt, puis dans *Settings → Pages*, choisir la branche et
le dossier `/docs` (ou publier le contenu de `docs/` à la racine d'une branche `gh-pages`).
Le fichier `docs/.nojekyll` évite que GitHub ignore les dossiers commençant par `_`.

## Organisation

```
build.py              le générateur : lit le contenu, écrit docs/
contenu/
  registre.py         LES 62 NŒUDS — titres, prérequis, durées, liens vers le master
  briques.py          les blocs d'écriture (retenir, demo, prof, code, exo…)
  niveau0.py …        le cours rédigé, un fichier par niveau
modele/
  style.css           l'identité visuelle (cahier quadrillé / tableau noir)
  site.js             navigation, progression, rendu des formules
  vendor/tex-svg.js   MathJax embarqué : le site rend les formules hors ligne
docs/               LE SITE — ne rien y modifier à la main, c'est écrasé à chaque build
  videos/             les .mp4 ; un nœud sans vidéo affiche un emplacement « à venir »
outils/               génération des vidéos
```

## Ajouter ou modifier un nœud

Tout part de `contenu/registre.py`. Un nœud ajouté là apparaît automatiquement dans la carte,
dans le sommaire, et dans les listes « prérequis » et « ouvre sur » des autres nœuds.

```python
Noeud("cf-construction", "Construction et sous-corps de 𝔽q", 50,
    "Construire 𝔽₈, 𝔽₁₆, 𝔽₂₅₆ et décrire leurs sous-corps.",
    prereq=["cf-existence", "poly-quotient"],   # id d'autres nœuds
    l3="non",                                   # "oui" | "partiel" | "non"
    master="C'est l'implémentation : table de logarithmes, …"),
```

Le cours de ce nœud se rédige dans `contenu/niveau3.py` :

```python
CORPS["cf-construction"] = r"""
<p class="lead">…</p>
""" + retenir("Théorème", r"""…""") + demo(r"""…""") + code("…", "python", "sortie") + …
```

`build.py` vérifie au passage que tout prérequis existe et vient bien **avant** le nœud qui
l'utilise ; il refuse de construire sinon.

## Les briques d'écriture

| Brique | Rendu |
|---|---|
| `retenir(label, corps)` | encadré rouge — définition ou théorème à savoir |
| `demo(corps)` | démonstration, filet bleu, terminée par ∎ |
| `prof(corps)` | le conseil, stylo vert |
| `master(corps)` | encadré « dans le master » (généré automatiquement depuis le registre) |
| `code(src, lang, sortie, titre)` | bloc de code avec sa sortie et un bouton copier |
| `exo(n, énoncé, correction, remarque)` | exercice, correction repliée sur papier quadrillé |
| `video(fichier, légende, durée)` | lecteur vidéo |
| `video_attente(sujet)` | emplacement « vidéo à venir » |

Les formules s'écrivent en LaTeX entre `\(…\)` (en ligne) et `\[…\]` (centré).
Macros disponibles : `\Z \N \Q \R \C \F \Fq \Fp \Zn \Znz \pgcd \ppcm \ord \Card \Vect \Ker`,
et `\legendre{a}{p}` pour le symbole de Legendre.

## État de la rédaction

Lancer `python3 build.py` affiche l'avancement nœud par nœud.
