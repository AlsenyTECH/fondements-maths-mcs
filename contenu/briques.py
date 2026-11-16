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


