# -*- coding: utf-8 -*-
"""Générateur du site « Fondements mathématiques du Master MCS ».

    python3 build.py

Lit contenu/registre.py (les nœuds) et contenu/niveau*.py (le cours rédigé),
écrit docs/index.html, docs/niveau-0.html … niveau-4.html et docs/assets/.
"""

import html
import re
import importlib
import os
import shutil
import sys

RACINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RACINE, "contenu"))
sys.path.insert(0, RACINE)

import registre as R  # noqa: E402
import pages_outils as PO  # noqa: E402
from briques import (retenir, demo, prof, master, code, exo,  # noqa: E402,F401
                     video, video_attente)

PUBLIC = os.path.join(RACINE, "docs")
MODELE = os.path.join(RACINE, "modele")

SITE_TITRE = "Fondements mathématiques du Master MCS"
SITE_SOUS_TITRE = "Mathématiques, Cryptographie et Sécurité"

POLICES = ("https://fonts.googleapis.com/css2?family=Caveat:wght@500;700"
           "&family=Kalam:wght@400;700&family=JetBrains+Mono:wght@400;600"
           "&family=Source+Sans+3:wght@400;600;700&display=swap")

MATHJAX = """<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']],
    macros: {
      N:'\\\\mathbb{N}', Z:'\\\\mathbb{Z}', Q:'\\\\mathbb{Q}', R:'\\\\mathbb{R}',
      C:'\\\\mathbb{C}', F:'\\\\mathbb{F}', P:'\\\\mathbb{P}', A:'\\\\mathbb{A}',
      Vect:'\\\\operatorname{Vect}', Ker:'\\\\operatorname{Ker}', Img:'\\\\operatorname{Im}',
      pgcd:'\\\\operatorname{pgcd}', ppcm:'\\\\operatorname{ppcm}', ord:'\\\\operatorname{ord}',
      Card:'\\\\operatorname{Card}', rg:'\\\\operatorname{rg}', car:'\\\\operatorname{car}',
      Tr:'\\\\operatorname{Tr}', Nm:'\\\\operatorname{N}', Gal:'\\\\operatorname{Gal}',
      Frob:'\\\\operatorname{Frob}', wt:'\\\\operatorname{wt}', dmin:'d_{\\\\min}',
      Fq:'\\\\mathbb{F}_q', Fp:'\\\\mathbb{F}_p', Zn:'\\\\mathbb{Z}/n\\\\mathbb{Z}',
      Znz:'(\\\\mathbb{Z}/n\\\\mathbb{Z})^{\\\\times}', legendre:['\\\\left(\\\\frac{#1}{#2}\\\\right)',2]
    }
  },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'],
             ignoreHtmlClass: 'tex2jax_ignore' },
  svg: { fontCache: 'global' }
};
</script>
<!-- MathJax est embarqué dans le dépôt : le site rend les formules même hors ligne.
     Si le fichier local manque, on retombe sur le CDN. -->
<script defer src="assets/mathjax/tex-svg.js"
        onerror="var s=document.createElement('script');s.defer=true;
                 s.src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js';
                 document.head.appendChild(s);"></script>"""


# ─────────────────────────────────────────────────────────────────────────────
# briques d'écriture — utilisées par les fichiers de contenu
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# la carte des dépendances
# ─────────────────────────────────────────────────────────────────────────────

BOITE_H = 84
BANDE_H, MARGE_X, MARGE_HAUT, ECART = 172, 150, 16, 24
LARGEUR = 1240
BOITE_MAX = 200


def _coupe(titre, largeur):
    """Coupe un titre en deux lignes s'il ne tient pas dans la boîte."""
    max_car = int((largeur - 24) / 6.6)
    if len(titre) <= max_car:
        return [titre]
    mots, lignes, cour = titre.split(), [], ""
    for mot in mots:
        essai = (cour + " " + mot).strip()
        if len(essai) <= max_car or not cour:
            cour = essai
        else:
            lignes.append(cour)
            cour = mot
    lignes.append(cour)
    return lignes[:3]


def _positions():
    """Place chaque module : une bande par niveau, modules centrés.
    La largeur des boîtes s'adapte au nombre de modules de la bande."""
    pos, larg = {}, {}
    y = MARGE_HAUT
    bandes = []
    dispo = LARGEUR - MARGE_X - 20
    for niv in R.NIVEAUX:
        mods = niv.modules
        L = min(BOITE_MAX, (dispo - (len(mods) - 1) * ECART) / len(mods))
        total = len(mods) * L + (len(mods) - 1) * ECART
        x0 = MARGE_X + (dispo - total) / 2
        for i, m in enumerate(mods):
            pos[m.id] = (x0 + i * (L + ECART), y + 48)
            larg[m.id] = L
        bandes.append((niv, y))
        y += BANDE_H
    return pos, larg, bandes, y + 10


def _aretes():
    """Dépendances entre modules, déduites des prérequis des nœuds."""
    mod_de = {}
    for niv in R.NIVEAUX:
        for m in niv.modules:
            for n in m.noeuds:
                mod_de[n.id] = m.id
    vues, out = set(), []
    for nid, (n, _, _) in R.INDEX.items():
        for p in n.prereq:
            a, b = mod_de[p], mod_de[nid]
            if a != b and (a, b) not in vues:
                vues.add((a, b))
                out.append((a, b))
    return out


def carte_svg():
    pos, larg, bandes, hauteur = _positions()
    p = ['<svg class="carte" viewBox="0 0 %d %d" role="img" '
         'aria-label="Carte des dépendances entre les modules du master">' % (LARGEUR, hauteur)]
    p.append('<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
             'markerHeight="7" orient="auto-start-reverse">'
             '<path d="M0,0 L10,5 L0,10 z" fill="currentColor" opacity=".45"/></marker></defs>')

    for niv, y in bandes:
        if niv.num % 2 == 0:
            p.append('<rect class="bande" x="0" y="%d" width="%d" height="%d" rx="4"/>'
                     % (y, LARGEUR, BANDE_H - 8))
        p.append('<text class="bande-t" x="16" y="%d">Niveau %d</text>' % (y + 34, niv.num))
        p.append('<text class="bande-t" x="16" y="%d" style="font-size:13px">%s</text>'
                 % (y + 56, html.escape(niv.sous_titre)))

    for a, b in _aretes():
        xa, ya = pos[a]
        xb, yb = pos[b]
        if ya == yb:
            # dépendance entre deux modules d'un même niveau
            entre = [m for m, (x, y) in pos.items() if y == ya and min(xa, xb) < x < max(xa, xb)]
            if not entre:
                # voisins : flèche horizontale
                gauche, droite = (xa + larg[a], xb) if xa < xb else (xa, xb + larg[b])
                p.append('<path class="lk" marker-end="url(#fl)" d="M%.1f,%.1f L%.1f,%.1f"/>'
                         % (gauche, ya + BOITE_H / 2, droite + (-3 if xa < xb else 3), yb + BOITE_H / 2))
            else:
                # non voisins : arc sous les boîtes, pour ne traverser aucun module
                xa2, xb2, bas = xa + larg[a] / 2, xb + larg[b] / 2, ya + BOITE_H
                p.append('<path class="lk" marker-end="url(#fl)" d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>'
                         % (xa2, bas, xa2, bas + 34, xb2, bas + 34, xb2, bas + 3))
            continue
        xa += larg[a] / 2
        ya += BOITE_H
        xb += larg[b] / 2
        dy = (yb - ya) / 2
        p.append('<path class="lk" marker-end="url(#fl)" d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>'
                 % (xa, ya, xa, ya + dy, xb, yb - dy, xb, yb - 4))

    for niv in R.NIVEAUX:
        for m in niv.modules:
            x, y = pos[m.id]
            L = larg[m.id]
            cible = "%s#%s" % (niv.fichier, m.noeuds[0].id)
            p.append('<a class="n" href="%s" data-noeuds="%s"><title>%s</title>'
                     % (cible, " ".join(n.id for n in m.noeuds), html.escape(m.resume)))
            p.append('<rect class="box" x="%.1f" y="%.1f" width="%.1f" height="%d" rx="4"/>' % (x, y, L, BOITE_H))
            p.append('<rect class="pb" x="%.1f" y="%.1f" width="0" height="4" rx="2" data-l="%.1f"/>'
                     % (x + 6, y + BOITE_H - 9, L - 12))
            lignes = _coupe(m.titre, L)
            for k, ligne in enumerate(lignes):
                p.append('<text class="tt" x="%.1f" y="%.1f">%s</text>'
                         % (x + 12, y + 23 + k * 16, html.escape(ligne)))
            p.append('<text x="%.1f" y="%.1f" opacity=".65" style="font-size:11.5px">%d nœuds · %d h</text>'
                     % (x + 12, y + 23 + len(lignes) * 16 + 6,
                        len(m.noeuds), round(sum(n.duree for n in m.noeuds) / 60)))
            p.append('</a>')
    p.append('</svg>')
    return "\n".join(p)


# ─────────────────────────────────────────────────────────────────────────────
# pages
# ─────────────────────────────────────────────────────────────────────────────

BADGES = {"oui": ('l3', 'Vu en licence'),
          "partiel": ('partiel', 'Entrevu en licence'),
          "non": ('neuf', 'Nouveau en master')}


def fiche(n):
    b_cls, b_txt = BADGES[n.l3]
    pre = ", ".join(R.lien(p) for p in n.prereq) or '<span class="rien">aucun — on peut commencer ici</span>'
    suite = ouvre = R.ouvre_sur(n.id)
    ouv = ", ".join(R.lien(o) for o in suite) or '<span class="rien">nœud terminal d\'une branche</span>'
    return ('<div class="fiche"><dl>'
            '<dt>Prérequis</dt><dd>%s</dd>'
            '<dt>Ouvre sur</dt><dd>%s</dd>'
            '<dt>En licence</dt><dd><span class="badge %s">%s</span></dd>'
            '</dl></div>' % (pre, ouv, b_cls, b_txt))


_MATHS = re.compile(r"(\\\((?:.|\n)+?\\\)|\\\[(?:.|\n)+?\\\])")


def proteger_maths(texte):
    """Dans les formules, remplace < et > par \\lt et \\gt.

    Sans cela, le navigateur lit « r<g » comme le début d'une balise <g> et avale la suite du texte.
    """
    def corrige(m):
        return m.group(0).replace("<", r"\lt ").replace(">", r"\gt ")
    return _MATHS.sub(corrige, texte)


def section_noeud(n, numero, module):
    corps = n.corps or (
        '<div class="prof"><p class="lab">En cours de rédaction</p>'
        '<p>Le cours de ce nœud arrive. En attendant, la fiche ci-dessus dit à quoi il sert, '
        'ce qu\'il faut avoir avant et ce qu\'il ouvre.</p></div>')
    return ('<section class="lesson" id="%s" data-part="%s" data-num="%s" data-title="%s" hidden>'
            '<header class="lhead"><p class="eyebrow">%s · Nœud %s<span class="meta">%d min</span></p>'
            '<h2>%s</h2></header><div class="lbody">'
            '<p class="objectif">%s</p>%s%s%s</div></section>'
            % (n.id, html.escape(module.titre), numero, html.escape(n.titre),
               html.escape(module.titre), numero, n.duree, html.escape(n.titre),
               n.objectif, fiche(n),
               master('<p>%s</p>' % n.master) if n.master else "",
               proteger_maths(corps)))


def coquille(titre, body, niveau=None, suivant=None, accueil=False):
    data = ''
    if niveau is not None:
        data = ' data-niveau="%d"' % niveau.num
        if suivant:
            data += ' data-suivant="%s"' % suivant
    script = '<script defer src="assets/outils.js"></script>'
    if niveau is not None:
        script = ('<script defer src="assets/site.js"></script>'
                  '<script defer src="assets/atelier.js"></script>' + script)
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="Les fondements mathématiques du Master Mathématiques, Cryptographie et Sécurité : arithmétique, groupes, anneaux, modules, corps finis, courbes, codes, réseaux et complexité.">
<link rel="stylesheet" href="%s">
<link rel="stylesheet" href="assets/style.css">
%s
%s
</head>
<body%s>
%s
%s
</body>
</html>
""" % (html.escape(titre), POLICES, PO.THEME_INIT, MATHJAX, data, body, script)


def page_niveau(niv, suivant):
    liste = []
    for m in niv.modules:
        liste.extend((n, m) for n in m.noeuds)

    accueil = ('<section class="lesson" id="depart" data-part="" data-title="Ce niveau en bref" hidden>'
               '<header class="lhead"><p class="eyebrow">Niveau %d · %s</p><h2>%s</h2></header>'
               '<div class="lbody"><p class="lead">%s</p>%s'
               '<h3>Les %d nœuds de ce niveau</h3>%s</div></section>'
               % (niv.num, html.escape(niv.sous_titre), html.escape(niv.titre), niv.resume,
                  '<div class="howto">'
                  '<div><p class="num">1</p><p><strong>Lis la fiche d\'en-tête.</strong> '
                  'Elle dit ce qu\'il faut savoir avant, et ce que le nœud ouvre.</p></div>'
                  '<div><p class="num">2</p><p><strong>Refais les démonstrations</strong> '
                  'sur une feuille, sans regarder.</p></div>'
                  '<div><p class="num">3</p><p><strong>Fais tourner le code.</strong> '
                  'Python pour construire, SageMath pour vérifier.</p></div>'
                  '<div><p class="num">4</p><p><strong>Valide le nœud</strong> avec le bouton du bas. '
                  'Ta progression est gardée sur cet appareil.</p></div></div>',
                  len(liste), _table_noeuds(niv)))

    sections = [accueil]
    for i, (n, m) in enumerate(liste, 1):
        sections.append(section_noeud(n, "%d.%d" % (niv.num, i), m))

    nav_niveaux = "".join(
        '<li><a href="%s"%s><span class="n-num">%d</span>%s</a></li>'
        % (x.fichier, ' class="ici"' if x is niv else '', x.num, html.escape(x.titre))
        for x in R.NIVEAUX)

    body = """<div class="app">
  <div class="topbar">
    <button type="button" class="btn ghost" id="menu-btn" aria-controls="side" aria-expanded="false">Sommaire</button>
    <p class="brand">Niveau %d</p>
    <p class="mini" id="mini-prog"></p>
  </div>
  <div class="scrim" id="scrim" hidden></div>

  <nav class="side" id="side" aria-label="Sommaire du niveau">
    <p class="brand"><a href="index.html">Fondements MCS</a></p>
    <p class="brand-sub">%s</p>
    %s
    <ul class="niveaux"><li><a href="index.html"><span class="n-num">·</span>La carte</a></li>%s</ul>
    <div class="prog"><div class="prog-bar"><div class="prog-fill" id="prog-fill"></div></div>
      <p class="prog-txt" id="prog-txt"></p></div>
    <div id="nav"></div>
    %s
    %s
  </nav>

  <main class="main" id="main">
%s
    <nav class="pager">
      <a class="btn ghost" id="prev" href="#">← Précédent</a>
      <span class="right"><p class="done-note" id="done-note" hidden>Nœud validé ✓</p>
      <a class="btn" id="next" href="#">Suivant →</a></span>
    </nav>
    %s
  </main>
</div>""" % (niv.num, html.escape(SITE_SOUS_TITRE), PO.RECHERCHE, nav_niveaux, PO.outils_sommaire(),
       PO.THEME_BTN, "\n".join(sections), PO.pied())

    return coquille("Niveau %d · %s — %s" % (niv.num, niv.titre, SITE_TITRE),
                    body, niveau=niv, suivant=suivant)


def _table_noeuds(niv):
    lignes = []
    for m in niv.modules:
        lignes.append('<tr><th colspan="3">%s</th></tr>' % html.escape(m.titre))
        for n in m.noeuds:
            b_cls, b_txt = BADGES[n.l3]
            lignes.append('<tr><td><a href="#%s">%s</a></td><td>%s</td>'
                          '<td><span class="badge %s">%s</span></td></tr>'
                          % (n.id, html.escape(n.titre), n.objectif, b_cls, b_txt))
    return ('<div class="table-wrap"><table><thead><tr><th>Nœud</th><th>Ce qu\'on doit savoir faire</th>'
            '<th>Statut</th></tr></thead><tbody>%s</tbody></table></div>' % "".join(lignes))


def page_accueil():
    return coquille(SITE_TITRE, PO.page_accueil(carte_svg()), accueil=True)


# ─────────────────────────────────────────────────────────────────────────────

def charger_contenu():
    """Injecte le cours rédigé dans les nœuds, s'il existe."""
    charges = 0
    for niv in R.NIVEAUX:
        nom = "niveau%d" % niv.num
        chemin = os.path.join(RACINE, "contenu", nom + ".py")
        if not os.path.exists(chemin):
            continue                      # niveau pas encore rédigé : normal
        try:
            mod = importlib.import_module(nom)
        except Exception as err:
            # un fichier de contenu présent mais cassé doit se voir, pas être ignoré
            raise SystemExit("Erreur dans contenu/%s.py : %s: %s"
                             % (nom, type(err).__name__, err))
        corps = getattr(mod, "CORPS", {})
        for nid, texte in corps.items():
            if nid not in R.INDEX:
                print("  ! contenu orphelin : %s (dans %s.py)" % (nid, nom))
                continue
            R.INDEX[nid][0].corps = texte
            charges += 1
    return charges


def construire():
    pbs = R.verifier()
    if pbs:
        print("Dépendances incohérentes :")
        for p in pbs:
            print("  -", p)
        return 1

    pbs = PO.verifier_donnees()
    if pbs:
        print("Identifiants inconnus dans contenu/outils_donnees.py :")
        for p in pbs:
            print("  -", p)
        return 1

    os.makedirs(os.path.join(PUBLIC, "assets"), exist_ok=True)
    os.makedirs(os.path.join(PUBLIC, "videos"), exist_ok=True)
    for f in ("style.css", "site.js", "atelier.js", "atelier-worker.js", "outils.js"):
        shutil.copy(os.path.join(MODELE, f), os.path.join(PUBLIC, "assets", f))

    # Python dans le navigateur (Pyodide), pour les ateliers de code
    pyo = os.path.join(MODELE, "vendor", "pyodide")
    if os.path.isdir(pyo):
        shutil.copytree(pyo, os.path.join(PUBLIC, "assets", "pyodide"), dirs_exist_ok=True)

    # MathJax embarqué : le site fonctionne sans connexion
    vendor = os.path.join(MODELE, "vendor", "tex-svg.js")
    if os.path.exists(vendor):
        os.makedirs(os.path.join(PUBLIC, "assets", "mathjax"), exist_ok=True)
        shutil.copy(vendor, os.path.join(PUBLIC, "assets", "mathjax", "tex-svg.js"))

    # le code des nœuds, téléchargeable depuis le site
    src_code = os.path.join(RACINE, "code")
    if os.path.isdir(src_code):
        cible = os.path.join(PUBLIC, "code")
        shutil.rmtree(cible, ignore_errors=True)
        shutil.copytree(src_code, cible, ignore=shutil.ignore_patterns("__pycache__", "*.json"))

    charges = charger_contenu()

    with open(os.path.join(PUBLIC, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_accueil())

    outils = {"parcours.html": ("Parcours guidés", PO.page_parcours),
              "glossaire.html": ("Notations et glossaire", PO.page_glossaire),
              "positionnement.html": ("Je me situe", PO.page_positionnement)}
    for fichier, (titre, fabrique) in outils.items():
        with open(os.path.join(PUBLIC, fichier), "w", encoding="utf-8") as f:
            f.write(coquille("%s — %s" % (titre, SITE_TITRE), fabrique(), accueil=True))
    with open(os.path.join(PUBLIC, "assets", "index-recherche.js"), "w", encoding="utf-8") as f:
        f.write(PO.index_recherche())

    for i, niv in enumerate(R.NIVEAUX):
        suivant = R.NIVEAUX[i + 1].fichier if i + 1 < len(R.NIVEAUX) else None
        with open(os.path.join(PUBLIC, niv.fichier), "w", encoding="utf-8") as f:
            f.write(page_niveau(niv, suivant))

    total = len(R.INDEX)
    print("Site construit dans docs/")
    print("  %d pages, %d nœuds, %d rédigés (%d %%)"
          % (len(R.NIVEAUX) + 1, total, charges, round(100 * charges / total)))
    for niv in R.NIVEAUX:
        faits = sum(1 for n in niv.noeuds if n.corps)
        print("  niveau %d : %2d/%2d rédigés" % (niv.num, faits, len(niv.noeuds)))
    return 0


if __name__ == "__main__":
    sys.exit(construire())
