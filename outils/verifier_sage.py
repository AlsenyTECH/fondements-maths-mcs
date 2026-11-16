# -*- coding: utf-8 -*-
"""Exécute chaque bloc SageMath du site et compare sa sortie à celle affichée.

    <python de l'environnement Sage> outils/verifier_sage.py [--json sorties.json]

Les blocs dont la sortie dépend du hasard sont marqués « aléatoire » et seulement exécutés.
"""
import io, os, sys, json, contextlib, traceback
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "contenu"))
import briques

BLOCS = []
_code = briques.code
def espion(src, lang="python", sortie=None, titre="Implémentation"):
    BLOCS.append({"src": src.strip("\n"), "lang": lang, "sortie": (sortie or "").strip("\n"), "titre": titre})
    return _code(src, lang, sortie, titre)
briques.code = espion

import importlib
for k in range(5):
    if os.path.exists(os.path.join(RACINE, "contenu", "niveau%d.py" % k)):
        importlib.import_module("niveau%d" % k)

from sage.all import *            # noqa
from sage.repl.preparse import preparse

def executer(src):
    tampon = io.StringIO()
    env = {}
    exec("from sage.all import *", env)
    with contextlib.redirect_stdout(tampon):
        exec(preparse(src), env)
    return tampon.getvalue().strip("\n")

res, ok, ko = [], 0, 0
for b in [b for b in BLOCS if b["lang"].lower().startswith("sage")]:
    try:
        reel = executer(b["src"]); err = None
    except Exception as e:
        reel, err = "", "%s: %s" % (type(e).__name__, e)
    juste = (err is None) and (reel == b["sortie"])
    ok += juste; ko += (not juste)
    res.append({"titre": b["titre"], "attendu": b["sortie"], "reel": reel, "erreur": err, "juste": juste})
    if not juste:
        print("=" * 70); print("BLOC :", b["titre"])
        print(b["src"]); print("--- affiché :"); print(b["sortie"])
        print("--- réel    :"); print(err or reel)
print("\n%d blocs Sage : %d justes, %d à corriger" % (ok + ko, ok, ko))
if "--json" in sys.argv:
    json.dump(res, open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False, indent=1)
