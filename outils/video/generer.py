# -*- coding: utf-8 -*-
"""Génère une vidéo « Tuto MathNexus » à partir d'un script JSON.

    python3 outils/video/generer.py outils/video/scripts/arith-bezout.json

Étapes : voix off de chaque scène (Kokoro, voix française) -> durées -> capture image par image
de page.html (Playwright) -> assemblage ffmpeg en 1280x720. La vidéo va dans docs/videos/.

Prérequis : pip install kokoro-onnx soundfile ; Playwright (Node) ; ffmpeg ;
les fichiers kokoro-v1.0.onnx et voices-v1.0.bin (variable KOKORO_DIR).
"""
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
KOKORO = os.environ.get("KOKORO_DIR", os.path.join(ICI, "modeles"))
IPS, PAUSE = 20, 0.7


def main(chemin):
    script = json.load(open(chemin, encoding="utf-8"))
    k = Kokoro(os.path.join(KOKORO, "kokoro-v1.0.onnx"), os.path.join(KOKORO, "voices-v1.0.bin"))
    piste, t, scenes = [], 0.0, []
    for sc in script["scenes"]:
        son, hz = k.create(sc["voix"], voice="ff_siwis", speed=0.95, lang="fr-fr")
        duree = len(son) / hz
        silence = np.zeros(int(PAUSE * hz), dtype=son.dtype)
        piste += [son, silence]
        scenes.append({"debut": t, "voix": duree, "fin": t + duree + PAUSE,
                       "lignes": sc["lignes"], "legende": sc["legende"], "efface": sc.get("efface", False)})
        t += duree + PAUSE
    total = t + 1.0
    piste.append(np.zeros(int(1.0 * hz), dtype=piste[0].dtype))
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "voix.wav")
    sf.write(wav, np.concatenate(piste), hz)
    plan = os.path.join(tmp, "plan.json")
    json.dump({"scenes": scenes, "total": total, "ips": IPS}, open(plan, "w"))
    muet = os.path.join(tmp, "muet.mp4")
    subprocess.run(["node", os.path.join(ICI, "capturer.js"), plan, muet], check=True)
    sortie = os.path.join(RACINE, "docs", "videos", script["fichier"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", muet, "-i", wav, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-shortest", "-movflags", "+faststart", sortie],
                   check=True)
    m, s = divmod(int(round(total)), 60)
    print("%s : %d min %02d, %.1f Mo" % (script["fichier"], m, s, os.path.getsize(sortie) / 1e6))


if __name__ == "__main__":
    main(sys.argv[1])
