# -*- coding: utf-8 -*-
"""Pages et éléments transversaux : barre d'outils, accueil, parcours, glossaire,
test de positionnement, index de recherche. Appelé par build.py."""

import html
import json
import re
import unicodedata

import registre as R
import outils_donnees as D

AUTEUR = "MathNexus"
ANNEE = 2026


def verifier_donnees():
    """Tout identifiant de nœud cité par les outils doit exister."""
    pbs = []
    for p in D.PARCOURS:
        pbs += ["parcours %s : %s" % (p["id"], n) for n in p["noeuds"] if n not in R.INDEX]
    pbs += ["glossaire %s : %s" % (t, n) for t, _, n in D.GLOSSAIRE if n not in R.INDEX]
    pbs += ["notation %s : %s" % (s, n) for s, _, n in D.NOTATIONS if n not in R.INDEX]
    for niv, qs in D.POSITIONNEMENT.items():
        pbs += ["positionnement niveau %d : %s" % (niv, q[4]) for q in qs if q[4] not in R.INDEX]
    return pbs


def url(nid):
    n, niv, _ = R.INDEX[nid]
    return "%s#%s" % (niv.fichier, nid)


def lien_noeud(nid):
    return '<a href="%s">%s</a>' % (url(nid), html.escape(R.INDEX[nid][0].titre))


def ancre(texte):
    s = unicodedata.normalize("NFD", texte.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "g-" + re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# ─────────────────────────────────────────────────────────────────────────────
# éléments communs
# ─────────────────────────────────────────────────────────────────────────────

THEME_INIT = ("<script>try{var t=localStorage.getItem('mcs-theme');"
              "if(t)document.documentElement.dataset.theme=t;}catch(e){}</script>")

RECHERCHE = ('<div class="rech" role="search"><input type="search" class="rech-in" '
             'placeholder="Rechercher une notion…" aria-label="Rechercher une notion" autocomplete="off">'
             '<ul class="rech-res" hidden></ul></div>')

THEME_BTN = '<button type="button" class="theme-btn" aria-pressed="false">Thème sombre</button>'

LIENS = [("positionnement.html", "Je me situe"), ("parcours.html", "Parcours guidés"),
         ("glossaire.html", "Glossaire")]


def barre(courant=""):
    liens = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == courant else "", t)
                    for h, t in LIENS)
    return ('<header class="barre"><a class="barre-brand" href="index.html">Fondements MCS</a>'
            '<nav class="barre-liens" aria-label="Outils">%s</nav>%s%s</header>'
            % (liens, RECHERCHE, THEME_BTN))


def outils_sommaire():
    liens = "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in LIENS)
    return '<ul class="side-outils">%s</ul>' % liens


def pied():
    return ('<footer class="pied"><p>© %d %s · Contenu sous licence '
            '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr">CC BY-NC-SA 4.0</a>, '
            'code sous licence MIT. Site personnel, sans lien officiel avec une université.</p></footer>'
            % (ANNEE, AUTEUR))


# ─────────────────────────────────────────────────────────────────────────────
# accueil
# ─────────────────────────────────────────────────────────────────────────────

def page_accueil(carte_svg):
    total = len(R.INDEX)
    heures = round(sum(v[0].duree for v in R.INDEX.values()) / 60)
    neufs = sum(1 for v in R.INDEX.values() if v[0].l3 == "non")
    nb_q = sum(len(q) for q in D.POSITIONNEMENT.values())
    nb_mod = sum(len(n.modules) for n in R.NIVEAUX)

    cartes = "".join(
        '<a class="niv-card" href="%s" data-noeuds="%s"><span class="k">Niveau %d · %s</span><h3>%s</h3>'
        '<p>%s</p><span class="cpt">%d nœuds · environ %d h<span class="cpt-fait"></span></span></a>'
        % (niv.fichier, " ".join(n.id for n in niv.noeuds), niv.num, html.escape(niv.sous_titre),
           html.escape(niv.titre), html.escape(niv.resume.split('.')[0] + '.'), len(niv.noeuds),
           round(sum(n.duree for n in niv.noeuds) / 60))
        for niv in R.NIVEAUX)

    return """%s<div class="accueil">
  <header class="hero">
    <h1>Fondements mathématiques<br>du Master MCS</h1>
    <p>Le master Mathématiques, Cryptographie et Sécurité repose sur deux troncs : l'algèbre et les
    probabilités. Ce site les met à plat en %d nœuds, chacun relié à ce qu'il ouvre dans le master.
    <strong>%d d'entre eux ne sont pas vus en licence</strong> : ce sont eux qui font décrocher.</p>
  </header>

  <div class="entrees">
    <a class="entree" href="positionnement.html"><span class="entree-n">1</span>
      <h2>Je me situe</h2><p>%d questions, une dizaine de minutes. Tu sauras par quel niveau commencer
      et quels nœuds revoir.</p></a>
    <a class="entree" href="parcours.html"><span class="entree-n">2</span>
      <h2>Je suis un parcours</h2><p>%d objectifs : RSA, AES, codes, post-quantique, IA… Chacun
      déroule sa chaîne de nœuds, dans l'ordre.</p></a>
    <a class="entree" href="#carte"><span class="entree-n">3</span>
      <h2>J'explore la carte</h2><p>Les %d modules et leurs dépendances. Une flèche veut dire :
      sans ceci, la suite ne passe pas.</p></a>
  </div>
  <p class="prog-global" id="prog-global" role="status"></p>

  <h2 class="sec" id="carte">La carte</h2>
  <p>Chaque boîte est un module ; les flèches sont les dépendances réelles, déduites nœud par nœud.
  Les modules se colorent au fur et à mesure que tu valides leurs nœuds.</p>
  <div class="carte-wrap">%s</div>
  <p class="legende">
    <span><i class="lg-vide"></i>pas commencé</span><span><i class="lg-cours"></i>en cours</span>
    <span><i class="lg-fini"></i>terminé</span>
    <span>Environ %d heures de travail. Cliquer une boîte ouvre son premier nœud.</span>
  </p>

  <h2 class="sec">Les cinq niveaux</h2>
  <div class="cartes">%s</div>

  <h2 class="sec">Comment s'en servir</h2>
  <div class="howto">
    <div><p class="num">1</p><p><strong>Situe-toi.</strong> Le test de positionnement dit où commencer.
    Un cours qui « ne passe pas » a presque toujours sa cause deux niveaux plus bas.</p></div>
    <div><p class="num">2</p><p><strong>Comprends, puis démontre.</strong> Chaque nœud part d'un
    problème concret ; les preuves se construisent sur un squelette avant d'être lues.</p></div>
    <div><p class="num">3</p><p><strong>Code.</strong> Dans chaque nœud, un atelier te fait écrire
    l'algorithme et le teste ; SageMath sert d'arbitre.</p></div>
    <div><p class="num">4</p><p><strong>Valide.</strong> Un nœud est validé quand son test de sortie et
    son atelier sont réussis. La progression reste sur ton appareil.</p></div>
  </div>

  <h2 class="sec">Ce que ce site n'est pas</h2>
  <p>Ce n'est pas un substitut aux cours du master, ni une liste de recettes. C'est une boussole :
  il dit où l'on est, ce qui manque pour avancer, et à quoi chaque notion va servir. Les
  démonstrations y sont faites entièrement, parce qu'en master une notion non démontrée
  n'est pas une notion acquise.</p>
</div>%s""" % (barre(), total, neufs, nb_q, len(D.PARCOURS), nb_mod, carte_svg, heures, cartes, pied())


# ─────────────────────────────────────────────────────────────────────────────
# parcours guidés
# ─────────────────────────────────────────────────────────────────────────────

def page_parcours():
    blocs = []
    for p in D.PARCOURS:
        etapes = []
        for k, nid in enumerate(p["noeuds"], 1):
            n, niv, _ = R.INDEX[nid]
            avenir = "" if n.corps else '<span class="badge avenir">à venir</span>'
            etapes.append('<li data-id="%s"><span class="pc-etat" aria-hidden="true"></span>'
                          '<span class="pc-k">%d</span><span class="pc-t"><a href="%s">%s</a>'
                          '<span class="pc-niv">Niveau %d · %d min</span></span>%s</li>'
                          % (nid, k, url(nid), html.escape(n.titre), niv.num, n.duree, avenir))
        heures = round(sum(R.INDEX[i][0].duree for i in p["noeuds"]) / 60)
        blocs.append(
            '<article class="parcours" id="%s" data-noeuds="%s"><header>'
            '<h2>%s</h2><p class="pc-pour">%s</p><p><strong>Tu arrives à :</strong> %s</p>'
            '<div class="pc-bas"><div class="prog-bar"><div class="prog-fill"></div></div>'
            '<p class="pc-prog">%d nœuds · environ %d h</p>'
            '<a class="btn pc-continuer" href="%s">Commencer →</a></div></header>'
            '<ol class="pc-liste">%s</ol></article>'
            % (p["id"], " ".join(p["noeuds"]), html.escape(p["titre"]), p["pour"], p["aboutit"],
               len(p["noeuds"]), heures, url(p["noeuds"][0]), "".join(etapes)))

    return """%s<div class="accueil outil">
  <header class="hero"><h1>Parcours guidés</h1>
    <p>Choisis un objectif : le parcours déroule, dans l'ordre, les nœuds qui y mènent. Chaque nœud
    rappelle ses propres prérequis ; si l'un te manque, remonte-le avant de continuer.</p></header>
  <nav class="pc-sommaire" aria-label="Parcours">%s</nav>
  %s
</div>%s""" % (barre("parcours.html"),
               "".join('<a href="#%s">%s</a>' % (p["id"], html.escape(p["titre"])) for p in D.PARCOURS),
               "\n".join(blocs), pied())


# ─────────────────────────────────────────────────────────────────────────────
# glossaire et notations
# ─────────────────────────────────────────────────────────────────────────────

def _cle_tri(t):
    s = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def page_glossaire():
    termes = sorted(D.GLOSSAIRE, key=lambda x: _cle_tri(x[0]))
    lettres, blocs, courante = [], [], None
    for terme, definition, nid in termes:
        l = _cle_tri(terme)[0].upper()
        if l != courante:
            if courante is not None:
                blocs.append("</dl>")
            blocs.append('<h3 class="gl-lettre" id="lettre-%s">%s</h3><dl class="gl">' % (l, l))
            lettres.append(l)
            courante = l
        blocs.append('<dt id="%s">%s</dt><dd>%s <span class="gl-voir">→ %s</span></dd>'
                     % (ancre(terme), html.escape(terme), definition, lien_noeud(nid)))
    blocs.append("</dl>")
    notations = "".join('<tr><td class="nt-s">%s</td><td>%s</td><td>%s</td></tr>' % (s, sens, lien_noeud(n))
                        for s, sens, n in D.NOTATIONS)
    return """%s<div class="accueil outil">
  <header class="hero"><h1>Notations et glossaire</h1>
    <p>Chaque terme renvoie au nœud où il est défini et démontré. Pour retrouver une notion depuis
    n'importe quelle page, utilise la recherche en haut.</p></header>
  <h2 class="sec" id="notations">Notations</h2>
  <div class="table-wrap"><table class="notations"><thead><tr><th>Notation</th><th>Signification</th>
  <th>Où elle est définie</th></tr></thead><tbody>%s</tbody></table></div>
  <h2 class="sec" id="glossaire">Glossaire</h2>
  <nav class="gl-index" aria-label="Lettres">%s</nav>
  %s
</div>%s""" % (barre("glossaire.html"), notations,
               "".join('<a href="#lettre-%s">%s</a>' % (l, l) for l in lettres), "".join(blocs), pied())


# ─────────────────────────────────────────────────────────────────────────────
# test de positionnement
# ─────────────────────────────────────────────────────────────────────────────

def page_positionnement():
    parties, i = [], 0
    for niv in R.NIVEAUX:
        qs = D.POSITIONNEMENT.get(niv.num, [])
        champs = []
        for enonce, options, bonne, explication, nid in qs:
            choix = "".join('<label class="qcm-o"><input type="radio" name="p%d" value="%d"> <span>%s</span></label>'
                            % (i, k, o) for k, o in enumerate(options))
            champs.append('<fieldset class="qcm-q" data-bonne="%d" data-niv="%d" data-noeud="%s" '
                          'data-url="%s" data-titre="%s"><legend>%s</legend>%s'
                          '<p class="qcm-x" hidden>%s</p></fieldset>'
                          % (bonne, niv.num, nid, url(nid), html.escape(R.INDEX[nid][0].titre),
                             enonce, choix, explication))
            i += 1
        parties.append('<section class="pos-niv" data-niv="%d" data-titre="%s" data-url="%s">'
                       '<h2 class="sec">Niveau %d · %s</h2>%s</section>'
                       % (niv.num, html.escape(niv.titre), niv.fichier, niv.num,
                          html.escape(niv.titre), "".join(champs)))
    return """%s<div class="accueil outil">
  <header class="hero"><h1>Je me situe</h1>
    <p>%d questions, de la logique de base aux branches du master. Réponds sans chercher : le but est
    de savoir ce que tu maîtrises <em>maintenant</em>. À la fin, tu sauras par quel niveau commencer et
    quels nœuds revoir.</p></header>
  <form class="qcm pos-test" novalidate>
  %s
  <div class="qcm-bas"><button type="submit" class="btn">Voir mon résultat</button>
  <p class="qcm-res" role="status" hidden></p></div>
  </form>
  <div class="pos-resultat" hidden></div>
</div>%s""" % (barre("positionnement.html"), i, "\n".join(parties), pied())


# ─────────────────────────────────────────────────────────────────────────────
# index de recherche
# ─────────────────────────────────────────────────────────────────────────────

_TEX = [(r"\Fq", "𝔽q"), (r"\Fp", "𝔽p"), (r"\Znz", "(ℤ/nℤ)*"), (r"\Zn", "ℤ/nℤ"), (r"\Z", "ℤ"),
        (r"\N", "ℕ"), (r"\Q", "ℚ"), (r"\R", "ℝ"), (r"\C", "ℂ"), (r"\F", "𝔽"), (r"\pgcd", "pgcd"),
        (r"\ppcm", "ppcm"), (r"\varphi", "φ"), (r"\equiv", "≡"), (r"\pmod", "mod"), (r"\bmod", "mod"),
        (r"\times", "×"), (r"\le", "≤"), (r"\ge", "≥"), (r"\neq", "≠"), (r"\in", "∈"), (r"\mid", "|"),
        (r"\cdot", "·"), (r"\iff", "⇔"), (r"\Rightarrow", "⇒"), (r"\forall", "∀"), (r"\exists", "∃"),
        (r"\lt", "<"), (r"\gt", ">"), (r"\sigma", "σ"), (r"\mu", "μ"), (r"\varepsilon", "ε"),
        (r"\Omega", "Ω"), (r"\infty", "∞"), (r"\sqrt", "√"), (r"\to", "→"), (r"\ord", "ord"),
        (r"\Ker", "Ker"), (r"\Img", "Im"), (r"\perp", "⊥"), (r"\simeq", "≃"), (r"\varphi", "φ"), (r"\lfloor", "⌊"), (r"\rfloor", "⌋"), (r"\langle", "⟨"), (r"\rangle", "⟩")]


def texte_brut(h):
    s = re.sub(r"<[^>]+>", " ", h)
    s = html.unescape(s)
    s = s.replace(r"\(", "").replace(r"\)", "").replace(r"\[", "").replace(r"\]", "")
    for a, b in sorted(_TEX, key=lambda x: -len(x[0])):
        s = re.sub(re.escape(a) + r"(?![A-Za-z])", lambda m, b=b: b, s)
    s = re.sub(r"\\[A-Za-z]+", "", s)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


_RETENIR = re.compile(r'<div class="retenir"><p class="lab">(.*?)</p>(.*?)</div>', re.S)


def index_recherche():
    entrees = []
    for niv in R.NIVEAUX:
        for m in niv.modules:
            for n in m.noeuds:
                u = "%s#%s" % (niv.fichier, n.id)
                entrees.append(["Nœud", n.titre, u, texte_brut(n.objectif + " " + m.titre)])
                for lab, corps in _RETENIR.findall(n.corps or ""):
                    lab = texte_brut(lab)
                    if lab.lower() in ("à retenir", "attention"):
                        continue
                    entrees.append([lab, "%s — %s" % (lab, n.titre), u, texte_brut(corps)[:220]])
    for terme, definition, nid in D.GLOSSAIRE:
        entrees.append(["Glossaire", terme, "glossaire.html#" + ancre(terme), texte_brut(definition)])
    for p in D.PARCOURS:
        entrees.append(["Parcours", p["titre"], "parcours.html#" + p["id"], texte_brut(p["pour"] + " " + p["aboutit"])])
    return "window.INDEX_RECHERCHE=%s;" % json.dumps(entrees, ensure_ascii=False, separators=(",", ":"))
