# -*- coding: utf-8 -*-
"""Niveau 0 — Langage et outils.

Le cours de chaque nœud, en HTML. Les briques (retenir, demo, prof, code, exo…)
sont définies dans build.py et importées ici.
"""

from briques import retenir, demo, prof, code, exo, video_attente

CORPS = {}


# ─────────────────────────────────────────────────────────────────────────────
CORPS["log-quantif"] = r"""
<p class="lead">Un énoncé mathématique n'est pas une phrase française : c'est une formule dont
l'ordre des quantificateurs change complètement le sens. En master, l'essentiel des erreurs de
raisonnement vient de là, et en cryptographie une définition de sécurité mal quantifiée est
une définition fausse.</p>

<h3>Les deux quantificateurs</h3>
<p>On écrit \(\forall x \in E,\ P(x)\) pour « pour tout \(x\) de \(E\), la propriété \(P(x)\)
est vraie », et \(\exists x \in E,\ P(x)\) pour « il existe au moins un \(x\) de \(E\) tel que
\(P(x)\) soit vraie ».</p>

""" + retenir("L'ordre des quantificateurs", r"""
<p>Les deux énoncés suivants ne disent pas la même chose :</p>
\[\forall x\,\exists y,\ P(x,y) \qquad\text{et}\qquad \exists y\,\forall x,\ P(x,y)\]
<p>Dans le premier, \(y\) peut dépendre de \(x\). Dans le second, un même \(y\) doit convenir
pour tous les \(x\). Le second implique le premier, jamais l'inverse.</p>
""") + r"""

<p>Un exemple qui fixe les idées. Sur \(\Z\), prenons \(P(x,y) : x + y = 0\).</p>
<ul>
<li>\(\forall x\,\exists y,\ x+y=0\) est <strong>vrai</strong> : il suffit de prendre \(y=-x\).</li>
<li>\(\exists y\,\forall x,\ x+y=0\) est <strong>faux</strong> : aucun entier \(y\) ne convient
pour tous les \(x\) à la fois.</li>
</ul>

""" + prof(r"""
<p>Quand tu lis un énoncé quantifié, demande-toi toujours : <em>de quoi le second objet
a-t-il le droit de dépendre ?</em> C'est tout ce que l'ordre encode.</p>
""") + r"""

<h3>Nier un énoncé</h3>
""" + retenir("Règles de négation", r"""
\[\neg(\forall x,\ P(x)) \iff \exists x,\ \neg P(x)\]
\[\neg(\exists x,\ P(x)) \iff \forall x,\ \neg P(x)\]
\[\neg(A \Rightarrow B) \iff A \text{ et } \neg B\]
<p>On nie en échangeant les quantificateurs un à un, de gauche à droite, puis en niant
la propriété finale.</p>
""") + r"""

<p>Appliquons-le à la continuité en un point \(a\) :</p>
\[\forall \varepsilon>0,\ \exists \delta>0,\ \forall x,\ |x-a|<\delta \Rightarrow |f(x)-f(a)|<\varepsilon.\]
<p>Sa négation est :</p>
\[\exists \varepsilon>0,\ \forall \delta>0,\ \exists x,\ |x-a|<\delta \ \text{ et }\ |f(x)-f(a)|\ge\varepsilon.\]
<p>Remarquez que l'implication s'est transformée en « et ». C'est l'erreur la plus fréquente :
on ne nie pas une implication par une implication.</p>

""" + prof(r"""
<p>En cryptographie, la définition de sécurité sémantique a exactement cette forme :
<em>pour tout adversaire efficace, pour tout couple de messages, l'avantage est négligeable.</em>
Une attaque, c'est la négation : <em>il existe un adversaire, il existe deux messages, tels que
l'avantage n'est pas négligeable.</em> Savoir nier, c'est savoir ce qu'il faut exhiber
pour casser un schéma.</p>
""") + r"""

<h3>Vérifier mécaniquement</h3>
<p>Sur un ensemble fini, un énoncé quantifié se teste par force brute. C'est le meilleur moyen
de se convaincre qu'un ordre de quantificateurs compte vraiment.</p>

""" + code(r"""
E = range(-5, 6)

# forall x, exists y : x + y == 0
print(all(any(x + y == 0 for y in E) for x in E))

# exists y, forall x : x + y == 0
print(any(all(x + y == 0 for x in E) for y in E))
""", "python", "True\nFalse", "Les deux ordres, testés") + r"""

""" + code(r"""
# Vérification du contre-exemple sur un ensemble fini quelconque
E = Set([-2, -1, 0, 1, 2])
print(all(any(x + y == 0 for y in E) for x in E))   # True
print(any(all(x + y == 0 for x in E) for y in E))   # False
""", "sagemath", "True\nFalse", "Contre-vérification SageMath") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Nier l'énoncé suivant, qui définit une suite \((u_n)\) bornée :</p>
\[\exists M>0,\ \forall n\in\N,\ |u_n|\le M.\]
""", r"""
<p>On échange le \(\exists\) en \(\forall\), le \(\forall\) en \(\exists\), puis on nie la
propriété finale :</p>
\[\forall M>0,\ \exists n\in\N,\ |u_n|>M.\]
<p>En mots : <u>aussi grand qu'on choisisse \(M\), un terme de la suite finit par le dépasser.</u></p>
""", r"""<p>Noter que \(\neg(|u_n|\le M)\) est \(|u_n|>M\), et non \(|u_n|\ge M\).</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(f:\Z\to\Z\). Traduire en français, puis nier :</p>
\[\forall y\in\Z,\ \exists x\in\Z,\ f(x)=y.\]
<p>Quelle propriété de \(f\) cet énoncé décrit-il ?</p>
""", r"""
<p>En français : <u>tout entier \(y\) est atteint par \(f\)</u>. C'est la <strong>surjectivité</strong>
de \(f\).</p>
<p>Négation :</p>
\[\exists y\in\Z,\ \forall x\in\Z,\ f(x)\neq y.\]
<p>C'est-à-dire : <u>il existe un entier que \(f\) n'atteint jamais</u>.</p>
""", r"""<p>Pour prouver la négation, il suffit d'exhiber <em>un</em> tel \(y\). Pour prouver
l'énoncé, il faut traiter <em>tous</em> les \(y\).</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["preuves"] = r"""
<p class="lead">Il n'y a que quatre façons de démontrer, et savoir laquelle choisir fait gagner
un temps considérable. Le choix se lit presque toujours dans la forme de l'énoncé.</p>

""" + retenir("Les quatre techniques", r"""
<table><thead><tr><th>Technique</th><th>Forme de l'énoncé</th><th>Ce qu'on suppose</th></tr></thead>
<tbody>
<tr><td>Directe</td><td>\(A \Rightarrow B\)</td><td>\(A\), on déduit \(B\)</td></tr>
<tr><td>Contraposée</td><td>\(A \Rightarrow B\)</td><td>\(\neg B\), on déduit \(\neg A\)</td></tr>
<tr><td>Absurde</td><td>\(A\) quelconque</td><td>\(\neg A\), on déduit une contradiction</td></tr>
<tr><td>Récurrence</td><td>\(\forall n\in\N,\ P(n)\)</td><td>\(P(n)\), on déduit \(P(n+1)\)</td></tr>
</tbody></table>
""") + r"""

<h3>Contraposée : quand l'hypothèse est inutilisable</h3>
<p>On utilise la contraposée quand \(\neg B\) est plus maniable que \(A\). Exemple typique :</p>

""" + retenir("Proposition", r"""
<p>Soit \(n\in\N\). Si \(n^2\) est pair, alors \(n\) est pair.</p>
""") + demo(r"""
<p>La preuve directe demanderait de factoriser \(n^2=2k\), ce qui n'est pas commode. On démontre
la contraposée : <em>si \(n\) est impair, alors \(n^2\) est impair.</em></p>
<p>Supposons \(n\) impair : \(n=2k+1\) avec \(k\in\N\). Alors</p>
\[n^2=(2k+1)^2=4k^2+4k+1=2(2k^2+2k)+1,\]
<p>qui est bien de la forme \(2m+1\) : \(n^2\) est impair.</p>
<p>La contraposée étant démontrée, l'énoncé initial l'est aussi.</p>
""") + r"""

<h3>Absurde : quand on nie pour obtenir prise</h3>
""" + retenir("Proposition", r"""
<p>\(\sqrt{2}\) est irrationnel.</p>
""") + demo(r"""
<p>Supposons \(\sqrt2\in\Q\). On peut alors écrire \(\sqrt2=\dfrac{p}{q}\) avec \(p,q\in\Z\),
\(q\neq0\), et la fraction <strong>irréductible</strong> (c'est l'hypothèse qui fournira la
contradiction).</p>
<p>En élevant au carré : \(2q^2=p^2\). Donc \(p^2\) est pair, donc \(p\) est pair par la
proposition précédente. Écrivons \(p=2p'\).</p>
<p>Alors \(2q^2=4p'^2\), soit \(q^2=2p'^2\). Donc \(q^2\) est pair, donc \(q\) est pair.</p>
<p>Ainsi \(p\) et \(q\) sont tous deux pairs, ce qui contredit l'irréductibilité de \(p/q\).</p>
<p>L'hypothèse \(\sqrt2\in\Q\) est donc fausse.</p>
""") + r"""

""" + prof(r"""
<p>En rédigeant une preuve par l'absurde, écris toujours la contradiction en clair à la fin :
« ceci contredit… ». Un correcteur de master sanctionne une preuve qui se termine sans dire
<em>quoi</em> a été contredit.</p>
""") + r"""

<h3>Récurrence, et sa variante forte</h3>
""" + retenir("Principe de récurrence", r"""
<p>Soit \(P(n)\) une propriété portant sur \(n\in\N\). Si</p>
<ol>
<li>\(P(n_0)\) est vraie (initialisation), et</li>
<li>pour tout \(n\ge n_0\), \(P(n)\Rightarrow P(n+1)\) (hérédité),</li>
</ol>
<p>alors \(P(n)\) est vraie pour tout \(n\ge n_0\).</p>
<p><strong>Récurrence forte</strong> : on peut remplacer l'hérédité par
« \(P(n_0),\dots,P(n)\) tous vrais \(\Rightarrow P(n+1)\) ». C'est la version nécessaire dès
qu'on raisonne sur des diviseurs.</p>
""") + r"""

""" + retenir("Proposition", r"""
<p>Tout entier \(n\ge2\) admet un diviseur premier.</p>
""") + demo(r"""
<p>Récurrence forte sur \(n\ge2\).</p>
<p><strong>Initialisation.</strong> \(n=2\) : 2 est premier et se divise lui-même.</p>
<p><strong>Hérédité.</strong> Soit \(n\ge2\) ; supposons la propriété vraie pour tout entier
\(k\) avec \(2\le k\le n\). Considérons \(n+1\).</p>
<ul>
<li>Si \(n+1\) est premier, il est son propre diviseur premier.</li>
<li>Sinon, \(n+1\) admet un diviseur \(d\) avec \(2\le d\le n\). Par hypothèse de récurrence
forte, \(d\) admet un diviseur premier \(p\). Comme \(p\mid d\) et \(d\mid n+1\), on a
\(p\mid n+1\).</li>
</ul>
<p>Dans les deux cas \(n+1\) admet un diviseur premier.</p>
""") + r"""

""" + prof(r"""
<p>Ici la récurrence simple ne suffit pas : pour traiter \(n+1\) on a besoin de l'hypothèse sur
\(d\), qui n'est pas \(n\). Dès qu'un raisonnement descend vers un diviseur ou coupe un problème
en deux, c'est la récurrence forte qu'il faut.</p>
""") + r"""

""" + code(r"""
def diviseur_premier(n):
    "Le plus petit diviseur premier de n >= 2 — la preuve, rendue effective."
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d          # d est forcement premier : aucun diviseur < d
        d += 1
    return n                  # n est premier

for n in [2, 15, 91, 97, 1001]:
    print(n, "->", diviseur_premier(n))
""", "python", "2 -> 2\n15 -> 3\n91 -> 7\n97 -> 97\n1001 -> 7", "La preuve devient un algorithme") + r"""

""" + code(r"""
for n in [2, 15, 91, 97, 1001]:
    print(n, '->', factor(n))
""", "sagemath", "2 -> 2\n15 -> 3 * 5\n91 -> 7 * 13\n97 -> 97\n1001 -> 7 * 11 * 13",
"Vérification") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soient \(a,b\in\Z\). Démontrer que si \(ab\) est impair, alors \(a\) et \(b\) sont impairs.
Quelle technique choisir ?</p>
""", r"""
<p>Par <u>contraposée</u> : supposons que \(a\) ou \(b\) soit pair, et montrons que \(ab\) est pair.</p>
<p>Quitte à échanger les rôles, supposons \(a\) pair : \(a=2k\). Alors \(ab=2(kb)\) est pair.</p>
<p>La contraposée est démontrée, donc l'énoncé aussi.</p>
""", r"""<p>La preuve directe obligerait à écrire \(ab=2m+1\) et à en déduire la parité de
\(a\) et \(b\) séparément : beaucoup plus pénible. La négation de « \(a\) et \(b\) impairs »
est « \(a\) pair <em>ou</em> \(b\) pair ».</p>""") + r"""

""" + exo(2, r"""
<p>Démontrer par récurrence que pour tout \(n\ge1\) :</p>
\[\sum_{k=1}^{n} k^3=\left(\frac{n(n+1)}{2}\right)^{2}.\]
""", r"""
<p><u>Initialisation</u> (\(n=1\)) : à gauche \(1^3=1\) ; à droite \(\left(\tfrac{1\cdot2}{2}\right)^2=1\). Vrai.</p>
<p><u>Hérédité</u>. Supposons la formule vraie au rang \(n\). Alors</p>
\[\sum_{k=1}^{n+1}k^3=\left(\frac{n(n+1)}{2}\right)^{2}+(n+1)^3
=\frac{n^2(n+1)^2+4(n+1)^3}{4}=\frac{(n+1)^2\big(n^2+4n+4\big)}{4}\]
\[=\frac{(n+1)^2(n+2)^2}{4}=\left(\frac{(n+1)(n+2)}{2}\right)^{2}.\]
<p>C'est la formule au rang \(n+1\). La propriété est donc vraie pour tout \(n\ge1\).</p>
""", r"""<p>Le point technique est la factorisation par \((n+1)^2\). Prendre l'habitude de
factoriser avant de développer fait gagner beaucoup de temps.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["ensembles"] = r"""
<p class="lead">Le vocabulaire des applications sert tous les jours en master : un chiffrement
est une bijection à clé fixée, une fonction de hachage une surjection qu'on ne sait pas inverser,
une projection canonique une surjection sur un quotient.</p>

<h3>Image et image réciproque</h3>
""" + retenir("Définitions", r"""
<p>Soit \(f:E\to F\), \(A\subset E\) et \(B\subset F\).</p>
\[f(A)=\{f(x)\ ;\ x\in A\}\subset F \qquad
f^{-1}(B)=\{x\in E\ ;\ f(x)\in B\}\subset E\]
<p>La notation \(f^{-1}(B)\) a un sens <strong>même si \(f\) n'est pas bijective</strong> :
c'est un ensemble, pas l'image par une application réciproque.</p>
""") + r"""

""" + prof(r"""
<p>C'est le piège classique. \(f^{-1}(\{y\})\) peut être vide, ou contenir mille éléments.
Écrire \(f^{-1}(y)\) sans accolades quand \(f\) n'est pas bijective est une faute de rédaction.</p>
""") + r"""

<h3>Injection, surjection, bijection</h3>
""" + retenir("Les trois propriétés", r"""
<p>\(f:E\to F\) est :</p>
<ul>
<li><strong>injective</strong> si \(\forall x,x'\in E,\ f(x)=f(x')\Rightarrow x=x'\) ;</li>
<li><strong>surjective</strong> si \(\forall y\in F,\ \exists x\in E,\ f(x)=y\) ;</li>
<li><strong>bijective</strong> si elle est injective et surjective — il existe alors une unique
\(f^{-1}:F\to E\) telle que \(f\circ f^{-1}=\mathrm{id}_F\) et \(f^{-1}\circ f=\mathrm{id}_E\).</li>
</ul>
""") + r"""

""" + retenir("Proposition (cas fini)", r"""
<p>Si \(E\) et \(F\) sont finis de <strong>même cardinal</strong>, alors pour \(f:E\to F\) :</p>
\[f \text{ injective} \iff f \text{ surjective} \iff f \text{ bijective}.\]
""") + demo(r"""
<p>Posons \(n=\Card E=\Card F\).</p>
<p><strong>Injective \(\Rightarrow\) surjective.</strong> Si \(f\) est injective, les \(n\) images
\(f(x)\), \(x\in E\), sont deux à deux distinctes, donc \(\Card f(E)=n=\Card F\). Un sous-ensemble
de \(F\) de cardinal \(\Card F\) est \(F\) tout entier, donc \(f(E)=F\) : \(f\) est surjective.</p>
<p><strong>Surjective \(\Rightarrow\) injective.</strong> Si \(f\) est surjective, \(f(E)=F\) donc
\(\Card f(E)=n\). Or \(f(E)\) est l'image de \(n\) éléments ; si deux d'entre eux avaient la même
image, on aurait \(\Card f(E)\le n-1\). Donc les images sont distinctes : \(f\) est injective.</p>
<p>Les deux implications réciproques donnent l'équivalence, et la conjonction donne la bijectivité.</p>
""") + r"""

""" + prof(r"""
<p>Cette proposition est utilisée en permanence en cryptographie : pour montrer qu'un chiffrement
par bloc est bijectif sur \(\{0,1\}^{128}\), il suffit de montrer qu'il est injectif. C'est ce qui
permet de définir le déchiffrement sans le construire.</p>
""") + r"""

""" + code(r"""
def est_injective(f, E):
    images = [f(x) for x in E]
    return len(set(images)) == len(images)

def est_surjective(f, E, F):
    return set(f(x) for x in E) == set(F)

E = range(8)
chiffre = lambda x: (3 * x + 5) % 8      # bijectif : pgcd(3, 8) = 1
casse   = lambda x: (2 * x + 5) % 8      # pas bijectif : pgcd(2, 8) = 2

for nom, f in [("3x+5", chiffre), ("2x+5", casse)]:
    print(nom, "inj:", est_injective(f, E), " surj:", est_surjective(f, E, E))
""", "python", "3x+5 inj: True  surj: True\n2x+5 inj: False  surj: False",
"Une application affine modulo 8 est-elle bijective ?") + r"""

<p>On retrouve ici un fait qu'on démontrera au niveau 1 : \(x\mapsto ax+b\) est bijective
sur \(\Z/n\Z\) si et seulement si \(a\) est inversible modulo \(n\), c'est-à-dire
\(\pgcd(a,n)=1\). C'est le cœur du chiffrement affine.</p>

""" + code(r"""
n = 8
for a in range(n):
    f = lambda x: (a*x + 5) % n
    images = [f(x) for x in range(n)]
    print(a, gcd(a, n), len(set(images)) == n)
""", "sagemath", "0 8 False\n1 1 True\n2 2 False\n3 1 True\n4 4 False\n5 1 True\n6 2 False\n7 1 True",
"La bijectivité suit exactement pgcd(a, n) = 1") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soit \(f:E\to F\) et \(A,A'\subset E\). Démontrer que \(f(A\cap A')\subset f(A)\cap f(A')\),
puis donner un contre-exemple à l'égalité.</p>
""", r"""
<p><u>Inclusion.</u> Soit \(y\in f(A\cap A')\). Il existe \(x\in A\cap A'\) avec \(y=f(x)\).
Comme \(x\in A\), \(y\in f(A)\) ; comme \(x\in A'\), \(y\in f(A')\). Donc \(y\in f(A)\cap f(A')\).</p>
<p><u>Contre-exemple.</u> Prenons \(f:\R\to\R,\ x\mapsto x^2\), \(A=\{1\}\), \(A'=\{-1\}\).</p>
<p>\(A\cap A'=\emptyset\) donc \(f(A\cap A')=\emptyset\), tandis que
\(f(A)\cap f(A')=\{1\}\cap\{1\}=\{1\}\neq\emptyset\).</p>
""", r"""<p>L'égalité vaut dès que \(f\) est injective. En revanche, pour l'image <em>réciproque</em>,
l'égalité \(f^{-1}(B\cap B')=f^{-1}(B)\cap f^{-1}(B')\) est toujours vraie : l'image réciproque
se comporte bien, l'image directe non.</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(E\) un ensemble fini à \(n\) éléments. Combien y a-t-il d'applications de \(E\) dans
\(E\) ? Combien de bijections ? Quelle proportion cela fait-il pour \(n=8\) ?</p>
""", r"""
<p><u>Applications</u> : chaque élément a \(n\) images possibles, indépendamment, d'où \(n^n\).</p>
<p><u>Bijections</u> : ce sont les permutations de \(E\), il y en a \(n!\).</p>
<p>Pour \(n=8\) : \(8^8=16\,777\,216\) applications et \(8!=40\,320\) bijections, soit une
proportion de \(\dfrac{40320}{16777216}\approx 0{,}24\,\%\).</p>
""", r"""<p>Une application tirée au hasard n'a donc presque aucune chance d'être bijective.
C'est pourquoi un chiffrement par bloc n'est jamais une fonction quelconque : il est construit
par composition de briques elles-mêmes bijectives.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["quotients"] = r"""
<p class="lead">C'est la construction la plus importante du niveau 0, et celle qui coûte le plus
cher quand elle reste floue. \(\Z/n\Z\), les corps finis \(\Fp[X]/(P)\), les groupes quotients,
les courbes elliptiques : tout le master est fait de quotients.</p>

<h3>Relation d'équivalence</h3>
""" + retenir("Définition", r"""
<p>Une relation \(\mathcal R\) sur \(E\) est une <strong>relation d'équivalence</strong> si elle est :</p>
<ul>
<li><strong>réflexive</strong> : \(\forall x,\ x\,\mathcal R\,x\) ;</li>
<li><strong>symétrique</strong> : \(\forall x,y,\ x\,\mathcal R\,y \Rightarrow y\,\mathcal R\,x\) ;</li>
<li><strong>transitive</strong> : \(\forall x,y,z,\ (x\,\mathcal R\,y \text{ et } y\,\mathcal R\,z)
\Rightarrow x\,\mathcal R\,z\).</li>
</ul>
<p>La <strong>classe</strong> de \(x\) est \(\bar x=\{y\in E\ ;\ x\,\mathcal R\,y\}\), et l'ensemble
quotient est \(E/\mathcal R=\{\bar x\ ;\ x\in E\}\).</p>
""") + r"""

""" + retenir("Théorème", r"""
<p>Les classes d'équivalence forment une <strong>partition</strong> de \(E\) : elles sont non vides,
deux à deux disjointes, et leur réunion est \(E\).</p>
""") + demo(r"""
<p><strong>Non vides.</strong> Par réflexivité, \(x\in\bar x\).</p>
<p><strong>Réunion égale à \(E\).</strong> Tout \(x\in E\) appartient à \(\bar x\), donc à la réunion.</p>
<p><strong>Disjointes ou confondues.</strong> Supposons \(\bar x\cap\bar y\neq\emptyset\) et
soit \(z\) dans l'intersection : \(x\,\mathcal R\,z\) et \(y\,\mathcal R\,z\).</p>
<p>Soit \(t\in\bar x\), c'est-à-dire \(x\,\mathcal R\,t\). Par symétrie \(z\,\mathcal R\,x\),
puis par transitivité \(z\,\mathcal R\,t\). Comme \(y\,\mathcal R\,z\), la transitivité donne
\(y\,\mathcal R\,t\), donc \(t\in\bar y\). Ainsi \(\bar x\subset\bar y\).</p>
<p>Par symétrie des rôles, \(\bar y\subset\bar x\), donc \(\bar x=\bar y\).</p>
<p>Deux classes sont donc soit disjointes, soit égales.</p>
""") + r"""

""" + prof(r"""
<p>Retiens le mouvement : <em>partition \(\leftrightarrow\) relation d'équivalence</em>. Se donner
une relation d'équivalence sur \(E\), c'est exactement se donner une façon de découper \(E\) en
paquets. Passer au quotient, c'est décider de ne plus distinguer les éléments d'un même paquet.</p>
""") + r"""

<h3>Passer une opération au quotient</h3>
<p>C'est ici que tout se joue. Une opération sur \(E\) ne descend pas automatiquement sur
\(E/\mathcal R\) : il faut vérifier qu'elle est <strong>compatible</strong>.</p>

""" + retenir("Compatibilité", r"""
<p>Une loi \(*\) sur \(E\) est compatible avec \(\mathcal R\) si</p>
\[x\,\mathcal R\,x' \ \text{ et }\ y\,\mathcal R\,y' \ \Longrightarrow\ (x*y)\,\mathcal R\,(x'*y').\]
<p>On peut alors définir \(\bar x\,\bar*\,\bar y=\overline{x*y}\) : le résultat ne dépend pas
des représentants choisis.</p>
""") + r"""

<p>Appliquons-le à \(\Z\) avec la congruence modulo \(n\) : \(x\,\mathcal R\,y \iff n\mid (x-y)\).</p>

""" + retenir("Proposition", r"""
<p>L'addition et la multiplication de \(\Z\) sont compatibles avec la congruence modulo \(n\).
L'ensemble quotient \(\Z/n\Z\) hérite donc d'une structure d'anneau.</p>
""") + demo(r"""
<p>Supposons \(x\equiv x'\) et \(y\equiv y'\) modulo \(n\). Il existe donc \(k,\ell\in\Z\) tels que
\(x-x'=kn\) et \(y-y'=\ell n\).</p>
<p><strong>Addition.</strong></p>
\[(x+y)-(x'+y')=(x-x')+(y-y')=(k+\ell)n,\]
<p>donc \(x+y\equiv x'+y' \pmod n\).</p>
<p><strong>Multiplication.</strong> On écrit \(x=x'+kn\) et \(y=y'+\ell n\), puis</p>
\[xy=(x'+kn)(y'+\ell n)=x'y'+n\big(x'\ell+y'k+k\ell n\big),\]
<p>donc \(xy-x'y'\) est multiple de \(n\), c'est-à-dire \(xy\equiv x'y'\pmod n\).</p>
<p>Les deux lois passent au quotient.</p>
""") + r"""

""" + prof(r"""
<p>Quand on te demandera de définir une opération sur un quotient — en théorie des groupes,
des anneaux, ou sur une courbe elliptique — la première chose à écrire est toujours :
« vérifions que c'est bien défini », c'est-à-dire que le résultat ne dépend pas du représentant.
Oublier cette vérification est l'erreur de rédaction la plus pénalisée en master.</p>
""") + r"""

""" + code(r"""
n = 7

def classe(x):
    return x % n

# Le resultat ne depend pas du representant choisi
x, x2 = 3, 3 + 2*n       # memes classes
y, y2 = 5, 5 - 3*n

print(classe(x + y), classe(x2 + y2))     # addition
print(classe(x * y), classe(x2 * y2))     # multiplication

# Les classes partitionnent bien Z (vu sur un intervalle)
paquets = {}
for z in range(-10, 11):
    paquets.setdefault(z % n, []).append(z)
for c in sorted(paquets):
    print(c, paquets[c])
""", "python",
"""1 1
1 1
0 [-7, 0, 7]
1 [-6, 1, 8]
2 [-5, 2, 9]
3 [-4, 3, 10]
4 [-10, -3, 4]
5 [-9, -2, 5]
6 [-8, -1, 6]""",
"La compatibilité, vérifiée sur des représentants différents") + r"""

<p>Les deux premières lignes sont la compatibilité : changer de représentant ne change pas le
résultat. Les suivantes sont la partition : chaque entier tombe dans exactement un paquet, et
les sept paquets recouvrent tout.</p>

""" + code(r"""
Z7 = Integers(7)
print(Z7(3) + Z7(5), Z7(3 + 2*7) + Z7(5 - 3*7))
print(Z7(3) * Z7(5), Z7(3 + 2*7) * Z7(5 - 3*7))
print(Z7.list())
""", "sagemath", "1 1\n1 1\n[0, 1, 2, 3, 4, 5, 6]", "Le même quotient, construit par SageMath") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Sur \(\R\), on pose \(x\,\mathcal R\,y \iff x-y\in\Z\). Montrer que c'est une relation
d'équivalence, décrire les classes, et dire si l'addition passe au quotient. Et la multiplication ?</p>
""", r"""
<p><u>Équivalence.</u> Réflexive : \(x-x=0\in\Z\). Symétrique : si \(x-y\in\Z\) alors
\(y-x=-(x-y)\in\Z\). Transitive : si \(x-y\in\Z\) et \(y-z\in\Z\), alors
\(x-z=(x-y)+(y-z)\in\Z\).</p>
<p><u>Classes.</u> \(\bar x=\{x+k\ ;\ k\in\Z\}\). Chaque classe a un unique représentant dans
\([0,1[\), donc \(\R/\Z\) s'identifie au cercle.</p>
<p><u>Addition.</u> Si \(x-x'\in\Z\) et \(y-y'\in\Z\), alors \((x+y)-(x'+y')\in\Z\) : compatible.</p>
<p><u>Multiplication.</u> <strong>Non compatible.</strong> Contre-exemple :
\(x=\tfrac12,\ x'=\tfrac32\) (même classe) et \(y=y'=\tfrac12\). Alors \(xy=\tfrac14\) et
\(x'y'=\tfrac34\), or \(\tfrac34-\tfrac14=\tfrac12\notin\Z\).</p>
""", r"""<p>C'est exactement pour cela que \(\R/\Z\) est un <em>groupe</em> additif et non un anneau.
La compatibilité n'est jamais automatique : elle se vérifie loi par loi.</p>""") + r"""

""" + exo(2, r"""
<p>Sur \(\Z\), on pose \(x\,\mathcal R\,y \iff x^2\equiv y^2 \pmod 5\). Est-ce une relation
d'équivalence ? Combien y a-t-il de classes ? L'addition est-elle compatible ?</p>
""", r"""
<p><u>Équivalence.</u> Oui : c'est l'image réciproque de l'égalité par \(x\mapsto x^2 \bmod 5\),
donc les trois propriétés sont immédiates.</p>
<p><u>Classes.</u> Les carrés modulo 5 valent \(0^2=0,\ 1^2=1,\ 2^2=4,\ 3^2=4,\ 4^2=1\).
Les valeurs atteintes sont \(\{0,1,4\}\), donc il y a <u>3 classes</u> :</p>
<ul>
<li>\(x\equiv0\) : carré \(\equiv0\) ;</li>
<li>\(x\equiv\pm1\) : carré \(\equiv1\) ;</li>
<li>\(x\equiv\pm2\) : carré \(\equiv4\).</li>
</ul>
<p><u>Addition : non compatible.</u> Prenons \(x=1\) et \(x'=4\) : ils sont équivalents car
\(1^2=1\) et \(4^2=16\equiv1\). Prenons \(y=y'=1\).</p>
<p>Alors \(x+y=2\), de carré \(4\) ; tandis que \(x'+y'=5\), de carré \(25\equiv0\).</p>
<p>Comme \(4\not\equiv0 \pmod 5\), on a \((x+y)\,\cancel{\mathcal R}\,(x'+y')\) : l'addition ne
passe pas au quotient.</p>
<p><u>Multiplication : compatible.</u> Si \(x^2\equiv x'^2\) et \(y^2\equiv y'^2\), alors
\((xy)^2=x^2y^2\equiv x'^2y'^2=(x'y')^2\).</p>
""", r"""<p>Cette relation est celle des « résidus quadratiques », qu'on retrouvera au nœud
<em>Résidus quadratiques, Legendre, Jacobi</em>. Elle est compatible avec la multiplication
mais pas avec l'addition — d'où le fait que le symbole de Legendre soit multiplicatif.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["denombrement"] = r"""
<p class="lead">Compter, c'est mesurer la sécurité. La taille d'un espace de clés, le coût d'une
recherche exhaustive, la probabilité qu'une collision apparaisse : tout cela est du dénombrement,
et les ordres de grandeur comptent plus que les formules exactes.</p>

<h3>Les quatre comptages de base</h3>
""" + retenir("À connaître", r"""
<table><thead><tr><th>Situation</th><th>Nombre</th><th>Exemple</th></tr></thead><tbody>
<tr><td>Listes de \(k\) éléments parmi \(n\), avec répétition</td><td>\(n^k\)</td>
<td>clés de 128 bits : \(2^{128}\)</td></tr>
<tr><td>Listes de \(k\) éléments distincts parmi \(n\)</td><td>\(\dfrac{n!}{(n-k)!}\)</td>
<td>arrangements</td></tr>
<tr><td>Permutations de \(n\)</td><td>\(n!\)</td><td>tables de substitution</td></tr>
<tr><td>Parties à \(k\) éléments parmi \(n\)</td><td>\(\binom{n}{k}=\dfrac{n!}{k!(n-k)!}\)</td>
<td>mots de poids \(k\) d'un code</td></tr>
</tbody></table>
""") + r"""

<h3>Le lemme de l'union</h3>
""" + retenir("Lemme", r"""
<p>Pour des événements \(A_1,\dots,A_m\) :</p>
\[\Pr\Big(\bigcup_{i=1}^{m} A_i\Big)\ \le\ \sum_{i=1}^{m}\Pr(A_i).\]
""") + demo(r"""
<p>Par récurrence sur \(m\). Pour \(m=1\) c'est une égalité.</p>
<p>Supposons l'inégalité vraie au rang \(m\). Posons \(B=\bigcup_{i\le m}A_i\). La formule
d'inclusion-exclusion à deux termes donne</p>
\[\Pr(B\cup A_{m+1})=\Pr(B)+\Pr(A_{m+1})-\Pr(B\cap A_{m+1})\ \le\ \Pr(B)+\Pr(A_{m+1}),\]
<p>car une probabilité est positive. En appliquant l'hypothèse de récurrence à \(\Pr(B)\) :</p>
\[\Pr\Big(\bigcup_{i\le m+1}A_i\Big)\le\sum_{i\le m}\Pr(A_i)+\Pr(A_{m+1})=\sum_{i\le m+1}\Pr(A_i).\]
""") + r"""

""" + prof(r"""
<p>C'est la majoration la plus utilisée de toute la cryptographie : on découpe l'événement
« l'adversaire gagne » en plusieurs mauvais cas, on majore chacun, et on additionne. Grossier,
mais suffisant quand chaque terme est négligeable.</p>
""") + r"""

<h3>Le paradoxe des anniversaires</h3>
""" + retenir("Théorème", r"""
<p>On tire \(k\) valeurs indépendantes et uniformes dans un ensemble à \(N\) éléments. La
probabilité qu'au moins deux coïncident vaut</p>
\[p(k,N)=1-\prod_{i=1}^{k-1}\Big(1-\frac{i}{N}\Big)\ \ge\ 1-e^{-k(k-1)/(2N)}.\]
<p>En particulier, elle dépasse \(1/2\) dès que \(k\approx 1{,}18\sqrt N\).</p>
""") + demo(r"""
<p>Comptons l'événement contraire : les \(k\) valeurs sont deux à deux distinctes.</p>
<p>Le premier tirage est libre. Le \(i+1\)-ième doit éviter les \(i\) valeurs déjà sorties, ce qui
arrive avec probabilité \(\dfrac{N-i}{N}=1-\dfrac iN\). Par indépendance,</p>
\[\Pr(\text{tous distincts})=\prod_{i=1}^{k-1}\Big(1-\frac iN\Big).\]
<p>On utilise maintenant \(1-u\le e^{-u}\), valable pour tout \(u\in\R\) (la fonction
\(u\mapsto e^{-u}-1+u\) a une dérivée \(1-e^{-u}\) qui s'annule en \(0\) en changeant de signe,
et vaut \(0\) en \(0\), donc elle est positive). D'où</p>
\[\prod_{i=1}^{k-1}\Big(1-\frac iN\Big)\ \le\ \prod_{i=1}^{k-1}e^{-i/N}
= e^{-\frac1N\sum_{i=1}^{k-1} i}=e^{-k(k-1)/(2N)}.\]
<p>En passant au complémentaire, \(p(k,N)\ge 1-e^{-k(k-1)/(2N)}\).</p>
<p>Cette borne vaut \(1/2\) quand \(k(k-1)/(2N)=\ln 2\), c'est-à-dire \(k\approx\sqrt{2\ln2}\,\sqrt N
\approx1{,}18\sqrt N\).</p>
""") + r"""

""" + prof(r"""
<p>Conséquence directe et contre-intuitive : une fonction de hachage sur \(n\) bits n'offre que
\(n/2\) bits de résistance aux collisions. C'est pour cela que SHA-256 vise 128 bits de sécurité,
et que MD5 (128 bits, donc 64 bits de résistance) est mort.</p>
""") + r"""

""" + code(r"""
from math import exp, sqrt

def p_exacte(k, N):
    p = 1.0
    for i in range(1, k):
        p *= (1 - i / N)
    return 1 - p

def p_borne(k, N):
    return 1 - exp(-k * (k - 1) / (2 * N))

N = 365
for k in [10, 23, 50, 70]:
    print(k, round(p_exacte(k, N), 4), round(p_borne(k, N), 4))

print("seuil 1/2 :", round(1.18 * sqrt(N), 1))
""", "python",
"""10 0.1169 0.116
23 0.5073 0.5
50 0.9704 0.9651
70 0.9992 0.9987
seuil 1/2 : 22.5""",
"Le paradoxe des anniversaires, exact et majoré") + r"""

<p>Vingt-trois personnes suffisent : c'est exactement le \(1{,}18\sqrt{365}\approx 22{,}5\)
annoncé par le théorème.</p>

""" + code(r"""
N = 2^128                      # sortie d'une fonction de hachage 128 bits
k = ceil(1.18 * sqrt(N))
print(k, log(k, 2).n())        # nombre de hachages avant collision
""", "sagemath", "22300745198530623141535718272648361505  64.2...",
"Pourquoi 128 bits de sortie ne valent que 64 bits de sécurité") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Un mot de passe est formé de 8 caractères choisis parmi les 26 minuscules, les 26 majuscules
et les 10 chiffres. Combien y a-t-il de mots de passe ? À \(10^{9}\) essais par seconde, combien
de temps pour tous les essayer ? Combien de bits de sécurité cela représente-t-il ?</p>
""", r"""
<p>Il y a \(62\) caractères possibles et 8 positions indépendantes, donc</p>
\[62^{8}=218\,340\,105\,584\,896\approx 2{,}18\times10^{14}\ \text{mots de passe.}\]
<p>À \(10^9\) essais par seconde : \(2{,}18\times10^{5}\) secondes, soit environ
<u>2 jours et demi</u>.</p>
<p>En bits : \(\log_2(62^8)=8\log_2 62\approx 8\times5{,}954\approx \underline{47{,}6}\) bits.</p>
""", r"""<p>47 bits, c'est très peu : on considère aujourd'hui qu'il faut au moins 128 bits.
C'est l'argument chiffré en faveur des phrases de passe longues plutôt que des mots courts
« compliqués ».</p>""") + r"""

""" + exo(2, r"""
<p>Une fonction de hachage produit des sorties sur \(n\) bits. Combien de hachages faut-il
calculer, en ordre de grandeur, pour avoir une chance sur deux de trouver une collision ?
Application à \(n=64\), \(n=128\), \(n=256\).</p>
""", r"""
<p>Ici \(N=2^{n}\), et le seuil est \(k\approx1{,}18\sqrt N=1{,}18\cdot 2^{n/2}\), donc en ordre
de grandeur <u>\(2^{n/2}\)</u>.</p>
<table><thead><tr><th>\(n\)</th><th>\(2^{n/2}\)</th><th>Faisable ?</th></tr></thead><tbody>
<tr><td>64</td><td>\(2^{32}\approx4\times10^{9}\)</td><td>quelques minutes sur un PC</td></tr>
<tr><td>128</td><td>\(2^{64}\approx1{,}8\times10^{19}\)</td><td>à la limite des grands moyens</td></tr>
<tr><td>256</td><td>\(2^{128}\)</td><td>hors de portée</td></tr>
</tbody></table>
""", r"""<p>Règle à retenir : <strong>résistance aux collisions = moitié de la taille de sortie</strong>.
La résistance à la préimage, elle, reste à \(2^{n}\) — les deux notions n'ont pas le même coût.</p>""")
