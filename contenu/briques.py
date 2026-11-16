# -*- coding: utf-8 -*-
"""Briques d'écriture des nœuds : encadrés, démonstrations, code, exercices.

Importées par build.py (pour la mise en page) et par les fichiers de contenu
niveau*.py (pour écrire le cours). Module séparé afin d'éviter un import
circulaire entre build.py et le contenu.
"""

import html


def retenir(label, corps):
    return '<div class="retenir"><p class="lab">%s</p>%s</div>' % (label, corps)


def demo(corps, label="Démonstration"):
    return '<div class="demo"><p class="lab">%s</p>%s<p class="cqfd">∎</p></div>' % (label, corps)


def prof(corps, label="Le conseil"):
    return '<div class="prof"><p class="lab">%s</p>%s</div>' % (label, corps)


def master(corps, label="Dans le master"):
    return '<div class="master"><p class="lab">%s</p>%s</div>' % (label, corps)


def code(src, lang="python", sortie=None, titre="Implémentation"):
    cls = "sage" if lang.lower().startswith("sage") else ""
    out = ""
    if sortie:
        out = '<pre class="sortie">%s</pre>' % html.escape(sortie.strip("\n"))
    return ('<div class="code tex2jax_ignore"><div class="code-h">'
            '<p class="lab">%s</p><span class="code-lang %s">%s</span>'
            '<button type="button" class="copier">copier</button></div>'
            '<pre>%s</pre>%s</div>'
            % (titre, cls, lang, html.escape(src.strip("\n")), out))


def exo(n, enonce, correction, remarque=None, niveau=None):
    niv = '<span class="niv">%s</span>' % niveau if niveau else ""
    rem = prof(remarque, "Remarque") if remarque else ""
    return ('<article class="exo"><p class="exo-n">Exercice %s%s</p>'
            '<div class="exo-q">%s</div>'
            '<details class="tex2jax_ignore"><summary>Voir la correction</summary>'
            '<div class="copie"><p class="lab">Correction</p>%s</div>%s</details></article>'
            % (n, niv, enonce, correction, rem))


def video(fichier, legende, duree):
    return ('<figure class="video"><video controls preload="metadata" playsinline src="videos/%s">'
            '</video><figcaption><span class="tag">Vidéo</span> %s '
            '<span class="dur">%s</span></figcaption></figure>' % (fichier, legende, duree))


def video_attente(sujet):
    return ('<figure class="video attente"><div class="ph"><p>Vidéo à venir : %s</p></div>'
            '<figcaption><span class="tag soon">Vidéo</span> en préparation</figcaption></figure>'
            % sujet)




# ─────────────────────────────────────────────────────────────────────────────
# Gabarit en quatre temps (nœud pilote et suivants)
# ─────────────────────────────────────────────────────────────────────────────

import json
import os
import subprocess
import sys

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CODE = os.path.join(_RACINE, "code")


def qcm(role, questions):
    """Test à choix, corrigé dans le navigateur.

    role       "entree" (3 questions, permet de sauter le nœud) ou "sortie" (valide le nœud)
    questions  liste de (énoncé, [options], indice de la bonne option, explication)
    """
    titre = {"entree": "Test d'entrée — as-tu besoin de ce nœud ?",
             "sortie": "Test de sortie — valide le nœud"}[role]
    seuil = len(questions) if role == "entree" else max(1, len(questions) - 1)
    blocs = []
    for i, (enonce, options, bonne, explication) in enumerate(questions):
        choix = "".join(
            '<label class="qcm-o"><input type="radio" name="q%d" value="%d"> <span>%s</span></label>'
            % (i, k, o) for k, o in enumerate(options))
        blocs.append('<fieldset class="qcm-q" data-bonne="%d"><legend>%d. %s</legend>%s'
                     '<p class="qcm-x" hidden>%s</p></fieldset>' % (bonne, i + 1, enonce, choix, explication))
    return ('<form class="qcm" data-role="%s" data-seuil="%d"><p class="lab">%s</p>%s'
            '<div class="qcm-bas"><button type="submit" class="btn">Corriger</button>'
            '<p class="qcm-res" role="status" hidden></p></div></form>'
            % (role, seuil, titre, "".join(blocs)))


def preuve(enonce_label, enonce, idee, etapes, complete):
    """Un théorème à démontrer soi-même : l'idée, le squelette, puis la preuve repliée."""
    plan = "".join("<li>%s</li>" % e for e in etapes)
    return ('<div class="preuve">%s'
            '<div class="idee"><p class="lab">L\'idée en une phrase</p><p>%s</p></div>'
            '<div class="squelette"><p class="lab">Le squelette — complète chaque étape sur ta feuille</p>'
            '<ol>%s</ol></div>'
            '<details class="tex2jax_ignore"><summary>Voir la démonstration complète</summary>%s</details>'
            '</div>' % (retenir(enonce_label, enonce), idee, plan, demo(complete)))


def exercice(n, niveau, enonce, indice, correction, remarque=None):
    """Exercice gradué : énoncé, indice replié, correction manuscrite repliée."""
    rem = prof(remarque, "Remarque") if remarque else ""
    return ('<article class="exo"><p class="exo-n">Exercice %s<span class="niv">%s</span></p>'
            '<div class="exo-q">%s</div>'
            '<details class="indice tex2jax_ignore"><summary>Un indice</summary><div class="prof">%s</div></details>'
            '<details class="tex2jax_ignore"><summary>Voir la correction</summary>'
            '<div class="copie"><p class="lab">Correction</p>%s</div>%s</details></article>'
            % (n, niveau, enonce, indice, correction, rem))


def a_toi(enonce, solution):
    return ('<div class="atoi"><p class="lab">À toi</p>%s'
            '<details class="tex2jax_ignore"><summary>Voir une solution</summary>%s</details></div>'
            % (enonce, solution))


def a_retenir(lignes):
    return retenir("À retenir", "<ul>%s</ul>" % "".join("<li>%s</li>" % l for l in lignes))


def code_fichier(chemin, titre="Implémentation"):
    """Bloc de code tiré d'un fichier de code/ ; la sortie affichée est celle d'une exécution réelle,
    faite à chaque construction du site. Le fichier est téléchargeable depuis le nœud."""
    abs_ = os.path.join(_CODE, chemin)
    src = open(abs_, encoding="utf-8").read()
    r = subprocess.run([sys.executable, abs_], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("code/%s échoue :\n%s" % (chemin, r.stderr))
    return (code(src, "python", r.stdout, titre)
            + '<p class="dl"><a href="code/%s" download>Télécharger %s</a></p>'
            % (chemin, os.path.basename(chemin)))


def code_sage(chemin, titre="Vérification SageMath"):
    """Bloc SageMath tiré de code/ ; la sortie vient de code/sorties_sage.json, produit par
    outils/executer_sage.py dans un environnement où Sage est installé."""
    src = open(os.path.join(_CODE, chemin), encoding="utf-8").read()
    cache = json.load(open(os.path.join(_CODE, "sorties_sage.json"), encoding="utf-8"))
    if chemin not in cache or cache[chemin]["source"] != src:
        raise RuntimeError("Sortie Sage absente ou périmée pour code/%s : "
                           "relancer outils/executer_sage.py" % chemin)
    return (code(src, "sagemath", cache[chemin]["sortie"], titre)
            + '<p class="dl"><a href="code/%s" download>Télécharger %s</a></p>'
            % (chemin, os.path.basename(chemin)))


def noeud(entree, comprendre, demontrer, implementer, exercer, sortie, retenir_):
    """Assemble un nœud au gabarit : test d'entrée, quatre temps en onglets, test de sortie."""
    temps = [("Comprendre", comprendre), ("Démontrer", demontrer),
             ("Implémenter", implementer), ("S'exercer", exercer + sortie + retenir_)]
    onglets = "".join(
        '<button type="button" role="tab" class="onglet" aria-selected="%s" data-t="%d">'
        '<span class="o-n">%d</span>%s</button>' % ("true" if i == 0 else "false", i, i + 1, nom)
        for i, (nom, _) in enumerate(temps))
    panneaux = "".join(
        '<div class="panneau" role="tabpanel" data-t="%d"%s>%s'
        '<p class="suite">%s</p></div>'
        % (i, "" if i == 0 else " hidden", contenu,
           '<button type="button" class="btn ghost aller" data-t="%d">Temps suivant : %s →</button>'
           % (i + 1, temps[i + 1][0]) if i + 1 < len(temps) else "")
        for i, (_, contenu) in enumerate(temps))
    return ('%s<div class="temps"><div class="onglets" role="tablist">%s</div>%s</div>'
            % (entree, onglets, panneaux))
