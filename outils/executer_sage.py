# -*- coding: utf-8 -*-
"""Exécute tous les fichiers code/**/*.sage et enregistre leurs sorties dans code/sorties_sage.json.

    <python d'un environnement où Sage est installé> outils/executer_sage.py

Le site se construit ensuite sans Sage : build.py lit ce fichier, et refuse de construire
si un fichier .sage a changé depuis sa dernière exécution.
"""
import contextlib, glob, io, json, os
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(RACINE, "code")
from sage.repl.preparse import preparse

res = {}
for f in sorted(glob.glob(os.path.join(CODE, "**", "*.sage"), recursive=True)):
    rel = os.path.relpath(f, CODE).replace(os.sep, "/")
    src = open(f, encoding="utf-8").read()
    env, tampon = {}, io.StringIO()
    exec("from sage.all import *", env)
    with contextlib.redirect_stdout(tampon):
        exec(preparse(src), env)
    res[rel] = {"source": src, "sortie": tampon.getvalue()}
    print("ok ", rel)
json.dump(res, open(os.path.join(CODE, "sorties_sage.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("%d fichiers Sage exécutés" % len(res))
