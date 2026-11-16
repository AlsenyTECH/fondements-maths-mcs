# -*- coding: utf-8 -*-
"""Niveau 1 — Arithmétique de ℤ, groupes, algèbre linéaire. Le tronc du master."""

from briques import retenir, demo, prof, code, exo

CORPS = {}


# ═════════════════════════════════════════════════════════════════════════════
# Arithmétique de ℤ
# ═════════════════════════════════════════════════════════════════════════════

CORPS["arith-euclide"] = r"""
<p class="lead">L'algorithme d'Euclide est le plus vieil algorithme non trivial connu, et il est
encore aujourd'hui exécuté des milliards de fois par jour : chaque poignée de main TLS en
contient. C'est aussi le premier algorithme dont on démontre la terminaison et le coût.</p>

<h3>Division euclidienne</h3>
""" + retenir("Théorème (division euclidienne)", r"""
<p>Soient \(a\in\Z\) et \(b\in\Z^*\). Il existe un <strong>unique</strong> couple
\((q,r)\in\Z^2\) tel que</p>
\[a=bq+r \qquad\text{et}\qquad 0\le r<|b|.\]
""") + demo(r"""
<p><strong>Existence.</strong> Supposons \(b>0\) (le cas \(b<0\) s'en déduit en changeant le signe
de \(q\)). Considérons l'ensemble</p>
\[S=\{a-bk\ ;\ k\in\Z\}\cap\N.\]
<p>\(S\) est non vide : en prenant \(k=-|a|\), on obtient \(a+b|a|\ge a+|a|\ge0\) car \(b\ge1\).</p>
<p>\(S\) est une partie non vide de \(\N\), elle admet donc un plus petit élément \(r=a-bq\).</p>
<p>Montrons \(r<b\). Si l'on avait \(r\ge b\), alors \(r-b=a-b(q+1)\ge0\) appartiendrait à \(S\)
tout en étant strictement plus petit que \(r\) — contradiction avec la minimalité.</p>
<p>Donc \(0\le r<b\) et \(a=bq+r\).</p>
<p><strong>Unicité.</strong> Supposons \(a=bq+r=bq'+r'\) avec \(0\le r,r'<b\). Alors
\(b(q-q')=r'-r\), donc \(b\mid r'-r\). Or \(|r'-r|<b\), et le seul multiple de \(b\) de valeur
absolue strictement inférieure à \(b\) est \(0\). Donc \(r=r'\), puis \(q=q'\) car \(b\neq0\).</p>
""") + r"""

""" + prof(r"""
<p>La démonstration repose entièrement sur le fait que <em>toute partie non vide de \(\N\) a un
plus petit élément</em>. Cette propriété, équivalente à la récurrence, est l'outil qu'on
réutilisera pour prouver la terminaison de presque tous les algorithmes du master.</p>
""") + r"""

<h3>PGCD et algorithme d'Euclide</h3>
""" + retenir("Définition et lemme clé", r"""
<p>Le \(\pgcd(a,b)\) est le plus grand entier divisant à la fois \(a\) et \(b\), avec la
convention \(\pgcd(a,0)=|a|\).</p>
<p><strong>Lemme.</strong> Si \(a=bq+r\), alors \(\pgcd(a,b)=\pgcd(b,r)\).</p>
""") + demo(r"""
<p>Il suffit de montrer que les deux couples ont exactement les mêmes diviseurs communs.</p>
<p>Soit \(d\) un diviseur commun de \(a\) et \(b\). Alors \(d\mid a-bq=r\), donc \(d\) divise
\(b\) et \(r\).</p>
<p>Réciproquement, soit \(d\) un diviseur commun de \(b\) et \(r\). Alors \(d\mid bq+r=a\), donc
\(d\) divise \(a\) et \(b\).</p>
<p>Les deux ensembles de diviseurs communs coïncident, donc leurs plus grands éléments aussi.</p>
""") + r"""

<p>L'algorithme d'Euclide applique ce lemme en boucle :</p>
\[\pgcd(a,b)=\pgcd(b,a\bmod b)=\pgcd(a\bmod b,\ b\bmod(a\bmod b))=\dots\]

""" + retenir("Théorème (terminaison et coût)", r"""
<p>L'algorithme d'Euclide termine, et le nombre de divisions effectuées pour \(\pgcd(a,b)\)
avec \(a>b>0\) est majoré par</p>
\[5\log_{10} b + O(1),\qquad\text{soit } O(\log b)\ \text{divisions.}\]
<p>Le pire cas est atteint par deux termes consécutifs de la suite de Fibonacci.</p>
""") + demo(r"""
<p><strong>Terminaison.</strong> Les restes successifs \(r_0=b>r_1>r_2>\dots\ge0\) forment une
suite d'entiers naturels strictement décroissante. Une telle suite est finie, l'algorithme
s'arrête donc.</p>
<p><strong>Coût.</strong> Montrons qu'en deux étapes le reste est au moins divisé par deux,
c'est-à-dire \(r_{k+2}<\tfrac12 r_k\).</p>
<p>Deux cas, en écrivant \(r_k=r_{k+1}q+r_{k+2}\) :</p>
<ul>
<li>si \(r_{k+1}\le\tfrac12 r_k\), alors \(r_{k+2}<r_{k+1}\le\tfrac12 r_k\) ;</li>
<li>si \(r_{k+1}>\tfrac12 r_k\), alors le quotient vaut \(q=1\), donc
\(r_{k+2}=r_k-r_{k+1}<r_k-\tfrac12 r_k=\tfrac12 r_k\).</li>
</ul>
<p>Dans les deux cas \(r_{k+2}<\tfrac12 r_k\). Après \(2m\) étapes le reste est donc
\(<b/2^m\) ; il devient nul dès que \(2^m>b\), c'est-à-dire pour \(m>\log_2 b\).</p>
<p>Le nombre d'étapes est donc \(O(\log b)\).</p>
""") + r"""

""" + prof(r"""
<p>\(O(\log b)\) divisions, c'est-à-dire un coût <em>linéaire en la taille de l'entrée</em>
puisque \(b\) s'écrit avec \(\log_2 b\) bits. C'est la définition même d'un algorithme efficace,
et c'est le contraste avec la factorisation qui fonde toute la cryptographie à clé publique :
calculer un PGCD est facile, factoriser ne l'est pas.</p>
""") + r"""

""" + code(r"""
def euclide(a, b):
    "PGCD avec le compte des divisions."
    a, b, etapes = abs(a), abs(b), 0
    while b:
        a, b = b, a % b
        etapes += 1
    return a, etapes

print(euclide(1071, 462))
print(euclide(240, 46))

# Le pire cas : deux Fibonacci consecutifs
fib = [1, 1]
while len(fib) < 20:
    fib.append(fib[-1] + fib[-2])
print(euclide(fib[19], fib[18]))
""", "python", "(21, 3)\n(2, 5)\n(1, 18)", "Euclide, et le nombre réel de divisions") + r"""

<p>Sur deux Fibonacci consécutifs, chaque quotient vaut 1 : l'algorithme ne peut pas faire moins
de progrès à chaque étape. C'est exactement le pire cas annoncé par le théorème.</p>

""" + code(r"""
print(gcd(1071, 462))
# Le pire cas, verifie : le nombre d'etapes croit lineairement en l'indice
F = fibonacci
for k in [10, 20, 30]:
    a, b, n = F(k+1), F(k), 0
    while b: a, b, n = b, a % b, n + 1
    print(k, n)
""", "sagemath", "21\n10 9\n20 19\n30 29", "Vérification") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Calculer \(\pgcd(1386,322)\) en posant toutes les divisions euclidiennes.</p>
""", r"""
<p>On applique le lemme en boucle :</p>
<p>\(1386 = 4\times322 + 98\)</p>
<p>\(322 = 3\times98 + 28\)</p>
<p>\(98 = 3\times28 + 14\)</p>
<p>\(28 = 2\times14 + 0\)</p>
<p>Le dernier reste non nul est \(14\), donc <u>\(\pgcd(1386,322)=14\)</u>.</p>
""", r"""<p>Quatre divisions, conformément au \(O(\log b)\) : \(\log_2 322\approx 8{,}3\).</p>""") + r"""

""" + exo(2, r"""
<p>Soient \(a,b\in\N^*\). Démontrer que \(\pgcd(a,b)\times\ppcm(a,b)=ab\) dans le cas
\(\pgcd(a,b)=1\), puis dans le cas général.</p>
""", r"""
<p><u>Cas \(\pgcd(a,b)=1\).</u> Soit \(m=\ppcm(a,b)\). Comme \(ab\) est un multiple commun,
\(m\mid ab\). Réciproquement \(a\mid m\), écrivons \(m=ak\). Comme \(b\mid m=ak\) et
\(\pgcd(a,b)=1\), le lemme de Gauss donne \(b\mid k\), donc \(ab\mid ak=m\).</p>
<p>Les deux divisibilités donnent \(m=ab\), et l'égalité \(1\times m=ab\) est vérifiée.</p>
<p><u>Cas général.</u> Posons \(d=\pgcd(a,b)\), \(a=da'\), \(b=db'\) avec \(\pgcd(a',b')=1\).</p>
<p>Un multiple commun de \(a\) et \(b\) est un multiple de \(d\) fois un multiple commun de
\(a'\) et \(b'\), donc \(\ppcm(a,b)=d\,\ppcm(a',b')=d\,a'b'\) par le cas précédent.</p>
<p>Alors</p>
\[\pgcd(a,b)\times\ppcm(a,b)=d\times d\,a'b'=(da')(db')=ab.\]
""", r"""<p>Le lemme de Gauss utilisé ici se démontre avec Bézout, qui fait l'objet du nœud
suivant. On peut donc aussi lire cet exercice comme une motivation pour Bézout.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["arith-bezout"] = r"""
<p class="lead">Euclide étendu est l'algorithme qui calcule la clé privée RSA. C'est aussi lui
qui inverse un élément dans un corps fini, donc qui fait tourner AES et les courbes elliptiques.
Il faut savoir le dérouler à la main.</p>

<h3>Le théorème de Bézout</h3>
""" + retenir("Théorème (Bachet-Bézout)", r"""
<p>Soient \(a,b\in\Z\) non tous deux nuls, et \(d=\pgcd(a,b)\). Il existe \(u,v\in\Z\) tels que</p>
\[au+bv=d.\]
<p>De plus, \(d\) est <strong>le plus petit entier strictement positif</strong> de la forme
\(au+bv\).</p>
""") + demo(r"""
<p>Considérons \(S=\{au+bv\ ;\ u,v\in\Z\}\cap\N^*\).</p>
<p><strong>\(S\) est non vide</strong> : en prenant \(u=a\), \(v=b\), on obtient \(a^2+b^2>0\).</p>
<p>\(S\) est une partie non vide de \(\N^*\) : soit \(g=au_0+bv_0\) son plus petit élément.
Montrons \(g=d\).</p>
<p><strong>\(g\) divise \(a\).</strong> Divisons : \(a=gq+r\) avec \(0\le r<g\). Alors</p>
\[r=a-gq=a-(au_0+bv_0)q=a(1-u_0q)+b(-v_0q),\]
<p>donc \(r\) est de la forme \(au+bv\). Si \(r>0\), alors \(r\in S\) et \(r<g\), contredisant la
minimalité de \(g\). Donc \(r=0\), c'est-à-dire \(g\mid a\).</p>
<p>Le même raisonnement donne \(g\mid b\). Donc \(g\) est un diviseur commun, d'où \(g\le d\).</p>
<p><strong>\(d\) divise \(g\).</strong> Comme \(d\mid a\) et \(d\mid b\), on a
\(d\mid au_0+bv_0=g\), donc \(d\le g\).</p>
<p>Les deux inégalités donnent \(g=d\), et le couple \((u_0,v_0)\) convient.</p>
""") + r"""

""" + retenir("Corollaires indispensables", r"""
<ul>
<li><strong>Théorème de Bézout.</strong> \(\pgcd(a,b)=1 \iff \exists u,v,\ au+bv=1\).</li>
<li><strong>Lemme de Gauss.</strong> Si \(a\mid bc\) et \(\pgcd(a,b)=1\), alors \(a\mid c\).</li>
<li><strong>Inversibilité.</strong> \(a\) est inversible modulo \(n\) \(\iff \pgcd(a,n)=1\),
et son inverse est le \(u\) de Bézout.</li>
</ul>
""") + demo(r"""
<p><strong>Lemme de Gauss.</strong> Par Bézout, \(au+bv=1\). Multiplions par \(c\) :</p>
\[acu+bcv=c.\]
<p>Or \(a\mid acu\) (évident) et \(a\mid bc\) par hypothèse, donc \(a\mid bcv\). La somme des deux
étant \(c\), on a \(a\mid c\).</p>
<p><strong>Inversibilité.</strong> Si \(\pgcd(a,n)=1\), Bézout donne \(au+nv=1\), donc
\(au\equiv1\pmod n\) : \(u\) est l'inverse de \(a\).</p>
<p>Réciproquement, si \(au\equiv1\pmod n\), il existe \(k\) avec \(au-1=kn\), soit
\(au-kn=1\). Tout diviseur commun de \(a\) et \(n\) divise alors \(1\), donc
\(\pgcd(a,n)=1\).</p>
""") + r"""

<h3>L'algorithme d'Euclide étendu</h3>
<p>On déroule Euclide en gardant à chaque étape l'écriture du reste sous la forme \(au+bv\).
Sur \(\pgcd(240,46)\) :</p>

<div class="table-wrap"><table>
<thead><tr><th>Division</th><th>Reste</th><th>Écriture \(240u+46v\)</th></tr></thead>
<tbody>
<tr><td>—</td><td>\(240\)</td><td>\(240\cdot 1+46\cdot 0\)</td></tr>
<tr><td>—</td><td>\(46\)</td><td>\(240\cdot 0+46\cdot 1\)</td></tr>
<tr><td>\(240=5\cdot46+10\)</td><td>\(10\)</td><td>\(240\cdot 1+46\cdot(-5)\)</td></tr>
<tr><td>\(46=4\cdot10+6\)</td><td>\(6\)</td><td>\(240\cdot(-4)+46\cdot 21\)</td></tr>
<tr><td>\(10=1\cdot6+4\)</td><td>\(4\)</td><td>\(240\cdot 5+46\cdot(-26)\)</td></tr>
<tr><td>\(6=1\cdot4+2\)</td><td>\(2\)</td><td>\(240\cdot(-9)+46\cdot 47\)</td></tr>
<tr><td>\(4=2\cdot2+0\)</td><td>\(0\)</td><td>fin</td></tr>
</tbody></table></div>

<p>On lit \(\pgcd(240,46)=2\) et \(240\cdot(-9)+46\cdot47=-2160+2162=2\). ✓</p>

""" + prof(r"""
<p>Pour vérifier un calcul de Bézout, il suffit de recalculer \(au+bv\) : cela doit donner le
PGCD. Fais-le systématiquement en examen, cela prend dix secondes et rattrape toutes les erreurs
de signe.</p>
""") + r"""

""" + code(r"""
def euclide_etendu(a, b):
    "Renvoie (d, u, v) avec a*u + b*v = d = pgcd(a, b)."
    r, u, v = a, 1, 0          # invariant : r = a*u + b*v
    r2, u2, v2 = b, 0, 1       # invariant : r2 = a*u2 + b*v2
    while r2:
        q = r // r2
        r, u, v, r2, u2, v2 = r2, u2, v2, r - q*r2, u - q*u2, v - q*v2
    return r, u, v

d, u, v = euclide_etendu(240, 46)
print(d, u, v, 240*u + 46*v)

def inverse_mod(a, n):
    d, u, _ = euclide_etendu(a, n)
    if d != 1:
        raise ValueError("%d n'est pas inversible modulo %d" % (a, n))
    return u % n

print(inverse_mod(17, 3120))          # la cle privee RSA du manuel
print(17 * inverse_mod(17, 3120) % 3120)
""", "python", "2 -9 47 2\n2753\n1", "Euclide étendu et l'inverse modulaire") + r"""

<p>Le dernier calcul est exactement l'étape de génération de clé RSA : avec
\(\varphi(n)=3120\) et \(e=17\), la clé privée est \(d=e^{-1}\bmod\varphi(n)=2753\).</p>

""" + code(r"""
print(xgcd(240, 46))                  # (d, u, v)
print(inverse_mod(17, 3120))
R = Integers(3120)
print(R(17)^-1)
""", "sagemath", "(2, -9, 47)\n2753\n2753", "Vérification") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Déterminer l'inverse de \(7\) modulo \(26\) par l'algorithme d'Euclide étendu, puis déchiffrer
le chiffrement affine \(y=7x+3 \bmod 26\).</p>
""", r"""
<p><u>Euclide.</u> \(26=3\times7+5\), \(7=1\times5+2\), \(5=2\times2+1\), \(2=2\times1+0\).
Donc \(\pgcd(7,26)=1\).</p>
<p><u>Remontée.</u></p>
<p>\(1=5-2\times2\)</p>
<p>\(=5-2\times(7-5)=3\times5-2\times7\)</p>
<p>\(=3\times(26-3\times7)-2\times7=3\times26-11\times7\)</p>
<p>Donc \(-11\times7\equiv1\pmod{26}\), soit \(7^{-1}\equiv-11\equiv\underline{15}\pmod{26}\).</p>
<p><u>Déchiffrement.</u> De \(y=7x+3\) on tire \(x=7^{-1}(y-3)=15(y-3)=15y-45\), et
\(-45\equiv7\pmod{26}\), d'où</p>
\[x=15y+7 \bmod 26.\]
""", r"""<p>Vérification : \(x=1\) donne \(y=10\), et \(15\times10+7=157=6\times26+1\equiv1\). ✓</p>""") + r"""

""" + exo(2, r"""
<p>Résoudre dans \(\Z\) l'équation diophantienne \(15x+21y=9\). Combien y a-t-il de solutions ?</p>
""", r"""
<p><u>Condition d'existence.</u> \(\pgcd(15,21)=3\) et \(3\mid 9\) : il y a des solutions.</p>
<p><u>Solution particulière.</u> Bézout sur \((15,21)\) : \(21=1\times15+6\), \(15=2\times6+3\),
donc \(3=15-2\times6=15-2(21-15)=3\times15-2\times21\).</p>
<p>En multipliant par 3 : \(9=9\times15-6\times21\), d'où \((x_0,y_0)=(9,-6)\).</p>
<p><u>Solution générale.</u> Si \((x,y)\) est solution, \(15(x-9)=-21(y+6)\), soit après division
par 3 : \(5(x-9)=-7(y+6)\). Comme \(\pgcd(5,7)=1\), Gauss donne \(7\mid x-9\), donc
\(x=9+7k\) et alors \(y=-6-5k\).</p>
\[\boxed{\ (x,y)=(9+7k,\ -6-5k),\quad k\in\Z\ }\]
<p>Il y a donc une <u>infinité de solutions</u>, paramétrée par \(k\in\Z\).</p>
""", r"""<p>Schéma général : \(ax+by=c\) a des solutions si et seulement si \(\pgcd(a,b)\mid c\),
et l'ensemble des solutions est une droite d'entiers de pas \(\big(\tfrac{b}{d},-\tfrac{a}{d}\big)\).</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["arith-congruences"] = r"""
<p class="lead">\(\Z/n\Z\) est l'objet le plus manipulé du master. On l'a construit au niveau 0
comme quotient ; il s'agit maintenant d'y calculer avec aisance et de savoir exactement quand
une division est permise.</p>

<h3>L'anneau \(\Z/n\Z\)</h3>
""" + retenir("Structure", r"""
<p>\(\Z/n\Z=\{\bar0,\bar1,\dots,\overline{n-1}\}\) est un anneau commutatif unitaire à \(n\)
éléments, pour les lois \(\bar a+\bar b=\overline{a+b}\) et \(\bar a\,\bar b=\overline{ab}\)
(bien définies, cf. le nœud « quotients »).</p>
""") + r"""

""" + retenir("Théorème (inversibles)", r"""
<p>\(\bar a\) est inversible dans \(\Z/n\Z\) si et seulement si \(\pgcd(a,n)=1\).</p>
<p>En conséquence : <strong>\(\Z/n\Z\) est un corps si et seulement si \(n\) est premier.</strong></p>
""") + demo(r"""
<p><strong>Équivalence.</strong> C'est le corollaire de Bézout du nœud précédent :
\(\pgcd(a,n)=1 \iff \exists u,\ au\equiv1\pmod n\).</p>
<p><strong>Corps.</strong> \(\Z/n\Z\) est un corps si et seulement si tout élément non nul est
inversible, c'est-à-dire si \(\pgcd(a,n)=1\) pour tout \(a\in\{1,\dots,n-1\}\).</p>
<p>Si \(n\) est premier, aucun \(a<n\) ne partage de facteur avec \(n\) : c'est vrai.</p>
<p>Si \(n\) n'est pas premier, écrivons \(n=ab\) avec \(1<a,b<n\). Alors \(\bar a\neq\bar0\) mais
\(\pgcd(a,n)=a>1\), donc \(\bar a\) n'est pas inversible. Pire, \(\bar a\bar b=\bar n=\bar0\) :
\(\bar a\) est un diviseur de zéro.</p>
""") + r"""

""" + prof(r"""
<p>C'est la raison pour laquelle on travaille modulo un <em>nombre premier</em> dès qu'on veut
diviser. Dans \(\Z/12\Z\), l'équation \(2x=0\) a deux solutions (\(x=0\) et \(x=6\)) : les
diviseurs de zéro cassent tous les raisonnements habituels.</p>
""") + r"""

<h3>Exponentiation rapide</h3>
<p>Calculer \(a^{e}\bmod n\) par \(e\) multiplications est impossible dès que \(e\) a 2048 bits.
L'exponentiation binaire ramène le coût à \(O(\log e)\) multiplications.</p>

""" + retenir("Principe", r"""
\[a^{e}=\begin{cases}
\big(a^{e/2}\big)^2 & \text{si } e \text{ est pair,}\\[2pt]
a\cdot\big(a^{(e-1)/2}\big)^2 & \text{si } e \text{ est impair.}
\end{cases}\]
<p>Chaque étape divise \(e\) par deux : il y a \(\lfloor\log_2 e\rfloor+1\) étapes.</p>
""") + r"""

""" + code(r"""
def exp_rapide(a, e, n):
    "a^e mod n en O(log e) multiplications."
    resultat, base = 1, a % n
    while e > 0:
        if e & 1:
            resultat = resultat * base % n
        base = base * base % n
        e >>= 1
    return resultat

print(exp_rapide(7, 128, 13))
print(pow(7, 128, 13))                      # Python le fait nativement

# L'ordre de grandeur : 2048 bits
e = 2**2048 - 1
print(e.bit_length(), "multiplications au plus")
""", "python", "3\n3\n2048 multiplications au plus",
"Exponentiation modulaire rapide") + r"""

<p>2048 multiplications au lieu de \(2^{2048}\) : c'est tout l'écart entre un calcul instantané
et un calcul impossible. RSA repose entièrement sur cette asymétrie.</p>

""" + code(r"""
print(power_mod(7, 128, 13))
R = Integers(13)
print(R(7)^128)
print(R.unit_group_order(), [x for x in R if x.is_unit()])
""", "sagemath", "3\n3\n12 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]",
"Vérification, et les inversibles de ℤ/13ℤ") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Résoudre dans \(\Z/15\Z\) : (a) \(4x=7\) ; (b) \(6x=9\) ; (c) \(6x=7\).</p>
""", r"""
<p><u>(a)</u> \(\pgcd(4,15)=1\) donc \(4\) est inversible. Euclide : \(15=3\times4+3\),
\(4=1\times3+1\), d'où \(1=4-3=4-(15-3\times4)=4\times4-15\). Donc \(4^{-1}=4\).</p>
<p>\(x=4\times7=28=\underline{13}\). Solution unique.</p>
<p><u>(b)</u> \(\pgcd(6,15)=3\) et \(3\mid9\) : il y a des solutions. On divise tout par 3 :
l'équation devient \(2x=3\) dans \(\Z/5\Z\). Comme \(2^{-1}=3\) dans \(\Z/5\Z\),
\(x\equiv 3\times3=9\equiv4\pmod 5\).</p>
<p>Les solutions dans \(\Z/15\Z\) sont donc \(x\in\{\underline{4,9,14}\}\) : <u>trois</u> solutions.</p>
<p><u>(c)</u> \(\pgcd(6,15)=3\) et \(3\nmid7\) : <u>aucune solution</u>.</p>
""", r"""<p>Règle générale : \(ax=b\) dans \(\Z/n\Z\) a des solutions ssi \(d=\pgcd(a,n)\) divise
\(b\), et il y en a alors exactement \(d\).</p>""") + r"""

""" + exo(2, r"""
<p>Calculer \(3^{100} \bmod 7\) de deux façons : par exponentiation rapide, puis en utilisant
le petit théorème de Fermat.</p>
""", r"""
<p><u>Exponentiation rapide.</u> \(100=1100100_2\). Les carrés successifs modulo 7 :</p>
<p>\(3^1=3\), \(3^2=2\), \(3^4=4\), \(3^8=2\), \(3^{16}=4\), \(3^{32}=2\), \(3^{64}=4\).</p>
<p>\(100=64+32+4\), donc \(3^{100}=4\times2\times4=32\equiv\underline{4}\pmod7\).</p>
<p><u>Par Fermat.</u> \(7\) est premier et \(7\nmid3\), donc \(3^{6}\equiv1\pmod7\).</p>
<p>\(100=16\times6+4\), donc \(3^{100}=(3^6)^{16}\times3^4\equiv1\times3^4=81=11\times7+4
\equiv\underline{4}\pmod7\).</p>
""", r"""<p>La seconde méthode est bien plus rapide : elle réduit l'exposant modulo 6 avant tout
calcul. C'est le réflexe à avoir dès qu'on connaît l'ordre du groupe — et c'est le nœud
« (ℤ/nℤ)*, indicatrice d'Euler, Fermat ».</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["arith-chinois"] = r"""
<p class="lead">Le théorème chinois casse un gros problème modulaire en plusieurs petits,
indépendants. C'est une accélération (le déchiffrement RSA en CRT est quatre fois plus rapide)
et c'est aussi une faiblesse (les attaques par fautes de Bellcore l'exploitent).</p>

<h3>L'énoncé</h3>
""" + retenir("Théorème chinois des restes", r"""
<p>Soient \(m_1,\dots,m_k\) deux à deux premiers entre eux, et \(M=m_1\cdots m_k\).
Alors l'application</p>
\[\varphi:\ \Z/M\Z\ \longrightarrow\ \Z/m_1\Z\times\dots\times\Z/m_k\Z,
\qquad \bar x\longmapsto(\bar x,\dots,\bar x)\]
<p>est un <strong>isomorphisme d'anneaux</strong>.</p>
<p>Autrement dit : le système \(x\equiv a_i \pmod{m_i}\) admet une solution, unique modulo \(M\).</p>
""") + demo(r"""
<p><strong>\(\varphi\) est bien définie et c'est un morphisme.</strong> Si \(x\equiv y\pmod M\),
alors \(m_i\mid M\mid x-y\) donc \(x\equiv y\pmod{m_i}\) pour tout \(i\). La compatibilité avec
\(+\) et \(\times\) est immédiate puisque chaque composante est une réduction.</p>
<p><strong>\(\varphi\) est injective.</strong> Soit \(x\in\Ker\varphi\) : \(m_i\mid x\) pour tout
\(i\). Les \(m_i\) étant deux à deux premiers entre eux, leur produit divise \(x\) — on le montre
par récurrence : si \(m_1\cdots m_j\mid x\) et \(m_{j+1}\mid x\), comme
\(\pgcd(m_1\cdots m_j,\ m_{j+1})=1\), le lemme de Gauss donne \(m_1\cdots m_{j+1}\mid x\).</p>
<p>Donc \(M\mid x\), c'est-à-dire \(\bar x=\bar0\) : le noyau est trivial.</p>
<p><strong>\(\varphi\) est surjective.</strong> Les deux ensembles ont le même cardinal \(M\), et
une application injective entre ensembles finis de même cardinal est bijective (cf. le nœud
« Ensembles, applications, cardinaux »).</p>
""") + r"""

""" + prof(r"""
<p>Remarque la structure de cette preuve : injectivité directe, puis surjectivité <em>par
comptage</em>. C'est un schéma qui revient sans arrêt en algèbre finie, et qui évite une
construction explicite pénible.</p>
""") + r"""

<h3>La construction explicite</h3>
<p>La preuve par comptage ne donne pas la solution. Pour l'obtenir, on construit des
« idempotents » :</p>

""" + retenir("Formule de reconstruction", r"""
<p>Posons \(M_i=M/m_i\). Comme \(\pgcd(M_i,m_i)=1\), soit \(N_i=M_i^{-1}\bmod m_i\). Alors</p>
\[x=\sum_{i=1}^{k} a_i\,M_i\,N_i \pmod M\]
<p>est l'unique solution du système.</p>
""") + demo(r"""
<p>Fixons \(j\) et réduisons \(x\) modulo \(m_j\).</p>
<p>Pour \(i\neq j\), \(m_j\) divise \(M_i=M/m_i\) (car \(m_j\) est l'un des facteurs de \(M_i\)),
donc le terme \(a_iM_iN_i\) est nul modulo \(m_j\).</p>
<p>Il ne reste que le terme \(i=j\) :</p>
\[x\equiv a_jM_jN_j\equiv a_j\times 1 = a_j \pmod{m_j},\]
<p>par définition de \(N_j\). Donc \(x\) est bien solution, et l'unicité modulo \(M\) vient de
l'injectivité démontrée plus haut.</p>
""") + r"""

""" + code(r"""
def crt(restes, modules):
    "Reconstruction chinoise explicite."
    M = 1
    for m in modules:
        M *= m
    x = 0
    for a, m in zip(restes, modules):
        Mi = M // m
        Ni = pow(Mi, -1, m)          # inverse modulaire (Python 3.8+)
        x += a * Mi * Ni
    return x % M

# x = 2 mod 3, x = 3 mod 5, x = 2 mod 7   (le probleme de Sun Zi)
x = crt([2, 3, 2], [3, 5, 7])
print(x, [x % m for m in (3, 5, 7)])
""", "python", "23 [2, 3, 2]", "Le théorème chinois, rendu effectif") + r"""

<h3>L'application à RSA</h3>
<p>Déchiffrer, c'est calculer \(m=c^{d}\bmod n\) avec \(n=pq\). Au lieu de travailler modulo
\(n\) (2048 bits), on travaille modulo \(p\) et \(q\) (1024 bits chacun), puis on recombine.</p>

""" + code(r"""
p, q = 1000003, 1000033                    # deux premiers (petits, pour l'exemple)
n, phi = p*q, (p-1)*(q-1)
e = 65537
d = pow(e, -1, phi)
m = 123456789

c = pow(m, e, n)                           # chiffrement

# Dechiffrement direct
m1 = pow(c, d, n)

# Dechiffrement en CRT : deux exponentiations deux fois plus petites
dp, dq = d % (p-1), d % (q-1)
mp, mq = pow(c, dp, p), pow(c, dq, q)
qinv = pow(q, -1, p)
h = qinv * (mp - mq) % p
m2 = mq + h*q                              # recombinaison (Garner)

print(m1, m2, m1 == m2 == m)
""", "python", "123456789 123456789 True",
"Le déchiffrement RSA, direct puis en CRT") + r"""

""" + prof(r"""
<p>Le coût d'une exponentiation modulaire est cubique en la taille du module. Diviser la taille
par deux divise donc le coût par huit, et comme il y a deux exponentiations au lieu d'une, le
gain net est d'un facteur quatre. C'est pour cette raison que toutes les implémentations
sérieuses de RSA utilisent le CRT.</p>
<p>Revers de la médaille : si une erreur matérielle survient pendant le calcul de \(m_p\) mais
pas de \(m_q\), alors \(\pgcd(m_2^{e}-c,\ n)\) donne \(q\) directement. C'est l'attaque de
Bellcore, et c'est pourquoi les cartes à puce vérifient leur propre résultat avant de le sortir.</p>
""") + r"""

""" + code(r"""
print(crt([2, 3, 2], [3, 5, 7]))
print(CRT_list([2, 3, 2], [3, 5, 7]))
# L'isomorphisme, vu comme tel
Z15 = Integers(15)
print([(x, (x % 3, x % 5)) for x in range(15)][:6])
""", "sagemath", "23\n23\n[(0, (0, 0)), (1, (1, 1)), (2, (2, 2)), (3, (0, 3)), (4, (1, 4)), (5, (2, 0))]",
"Vérification et lecture de l'isomorphisme") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Résoudre le système \(x\equiv1\pmod4\), \(x\equiv2\pmod{9}\), \(x\equiv3\pmod{25}\).</p>
""", r"""
<p>Les modules \(4,9,25\) sont deux à deux premiers entre eux, \(M=4\times9\times25=900\).</p>
<p><u>Calcul des \(M_i\) et \(N_i\).</u></p>
<p>\(M_1=225\) ; \(225\equiv1\pmod4\) donc \(N_1=1\).</p>
<p>\(M_2=100\) ; \(100\equiv1\pmod9\) donc \(N_2=1\).</p>
<p>\(M_3=36\) ; \(36\equiv11\pmod{25}\), et \(11\times16=176=7\times25+1\) donc \(N_3=16\).</p>
<p><u>Reconstruction.</u></p>
\[x=1\cdot225\cdot1+2\cdot100\cdot1+3\cdot36\cdot16=225+200+1728=2153.\]
<p>\(2153=2\times900+353\), donc \(x\equiv\underline{353}\pmod{900}\).</p>
<p><u>Vérification.</u> \(353=88\times4+1\) ✓, \(353=39\times9+2\) ✓, \(353=14\times25+3\) ✓.</p>
""", r"""<p>Vérifie toujours les trois congruences à la fin : la reconstruction est un calcul
long où une erreur d'inverse passe facilement inaperçue.</p>""") + r"""

""" + exo(2, r"""
<p>Montrer que \(\Z/6\Z\simeq\Z/2\Z\times\Z/3\Z\) mais que \(\Z/4\Z\not\simeq\Z/2\Z\times\Z/2\Z\).
Quelle hypothèse du théorème est en cause ?</p>
""", r"""
<p><u>Premier cas.</u> \(\pgcd(2,3)=1\), le théorème chinois s'applique directement.</p>
<p><u>Second cas.</u> \(\pgcd(2,2)=2\neq1\) : l'hypothèse « deux à deux premiers entre eux »
est en défaut, le théorème ne dit rien.</p>
<p>Et en effet les deux anneaux ne sont pas isomorphes. Dans \(\Z/4\Z\), l'élément \(\bar1\) est
d'ordre additif 4. Dans \(\Z/2\Z\times\Z/2\Z\), tout élément \((a,b)\) vérifie
\((a,b)+(a,b)=(0,0)\) : tous les éléments sont d'ordre au plus 2.</p>
<p>Un isomorphisme préservant l'ordre des éléments, <u>il ne peut pas en exister</u>.</p>
""", r"""<p>Ces deux anneaux à 4 éléments sont les deux seuls groupes abéliens d'ordre 4 :
\(\Z/4\Z\) (cyclique) et le groupe de Klein. On les reverra au nœud « Structure des groupes
abéliens finis ».</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["arith-euler"] = r"""
<p class="lead">C'est le nœud qui contient la démonstration de RSA. Tout tient dans une
observation : dans un groupe fini, élever à la puissance « ordre du groupe » ramène à l'élément
neutre.</p>

<h3>Le groupe des inversibles</h3>
""" + retenir("Définition", r"""
<p>\(\Znz\) est l'ensemble des éléments inversibles de \(\Z/n\Z\). C'est un <strong>groupe
multiplicatif</strong>, de cardinal noté \(\varphi(n)\) (indicatrice d'Euler) :</p>
\[\varphi(n)=\Card\{a\in\{1,\dots,n\}\ ;\ \pgcd(a,n)=1\}.\]
""") + r"""

""" + retenir("Calcul de φ", r"""
<ul>
<li>\(\varphi(p)=p-1\) si \(p\) est premier ;</li>
<li>\(\varphi(p^k)=p^k-p^{k-1}=p^{k-1}(p-1)\) ;</li>
<li>\(\varphi(mn)=\varphi(m)\varphi(n)\) si \(\pgcd(m,n)=1\) (multiplicativité) ;</li>
<li>d'où, si \(n=\prod p_i^{\alpha_i}\) : \(\displaystyle\varphi(n)=n\prod_{p\mid n}\Big(1-\frac1p\Big).\)</li>
</ul>
""") + demo(r"""
<p><strong>\(\varphi(p^k)\).</strong> Les entiers de \(\{1,\dots,p^k\}\) non premiers à \(p^k\)
sont exactement les multiples de \(p\), au nombre de \(p^{k-1}\). D'où
\(\varphi(p^k)=p^k-p^{k-1}\).</p>
<p><strong>Multiplicativité.</strong> Par le théorème chinois, l'application
\(\Z/mn\Z\to\Z/m\Z\times\Z/n\Z\) est un isomorphisme d'anneaux. Un isomorphisme d'anneaux envoie
les inversibles sur les inversibles, et un couple \((\bar a,\bar b)\) est inversible dans le
produit si et seulement si chaque composante l'est. Donc</p>
\[\Znz \simeq (\Z/m\Z)^{\times}\times(\Z/n\Z)^{\times},\]
<p>et en prenant les cardinaux, \(\varphi(mn)=\varphi(m)\varphi(n)\).</p>
<p><strong>Formule générale.</strong> On applique la multiplicativité à la décomposition en
facteurs premiers, puis la formule pour \(\varphi(p^k)\) :</p>
\[\varphi(n)=\prod_i p_i^{\alpha_i-1}(p_i-1)=\prod_i p_i^{\alpha_i}\Big(1-\frac1{p_i}\Big)
=n\prod_{p\mid n}\Big(1-\frac1p\Big).\]
""") + r"""

<h3>Fermat et Euler</h3>
""" + retenir("Théorème d'Euler", r"""
<p>Si \(\pgcd(a,n)=1\), alors</p>
\[a^{\varphi(n)}\equiv1 \pmod n.\]
<p><strong>Petit théorème de Fermat</strong> (cas \(n=p\) premier) : si \(p\nmid a\), alors
\(a^{p-1}\equiv1\pmod p\), et pour tout \(a\), \(a^{p}\equiv a\pmod p\).</p>
""") + demo(r"""
<p>Soit \(G=\Znz\), de cardinal \(\varphi(n)\), et \(a\in G\).</p>
<p>Considérons l'application \(\mu_a:G\to G,\ x\mapsto ax\). Elle est bien définie (un produit
d'inversibles est inversible) et <strong>bijective</strong>, d'inverse \(x\mapsto a^{-1}x\).</p>
<p>Donc \(\mu_a\) permute les éléments de \(G\). En multipliant tous les éléments de \(G\) entre
eux de deux façons :</p>
\[\prod_{x\in G} x \;=\; \prod_{x\in G}(ax) \;=\; a^{\varphi(n)}\prod_{x\in G} x.\]
<p>Le produit \(\prod_{x\in G}x\) est inversible (produit d'inversibles), on peut donc le
simplifier des deux côtés :</p>
\[1\equiv a^{\varphi(n)} \pmod n.\]
""") + r"""

""" + prof(r"""
<p>Cette preuve est en réalité le théorème de Lagrange déguisé, appliqué au groupe \(\Znz\) :
l'ordre d'un élément divise l'ordre du groupe. On la reverra dans ce cadre au nœud
« Le théorème de Lagrange ». La version ci-dessus a l'avantage de ne rien supposer connu
en théorie des groupes.</p>
""") + r"""

<h3>Pourquoi RSA fonctionne</h3>
""" + retenir("Théorème (correction de RSA)", r"""
<p>Soient \(p\neq q\) premiers, \(n=pq\), et \(e,d\) tels que \(ed\equiv1\pmod{\varphi(n)}\).
Alors pour <strong>tout</strong> \(m\in\Z\) :</p>
\[(m^{e})^{d}\equiv m \pmod n.\]
""") + demo(r"""
<p>Écrivons \(ed=1+k\varphi(n)\) avec \(k\in\N\).</p>
<p><strong>Cas \(\pgcd(m,n)=1\).</strong> Le théorème d'Euler donne directement</p>
\[m^{ed}=m^{1+k\varphi(n)}=m\cdot\big(m^{\varphi(n)}\big)^{k}\equiv m\cdot 1^k=m\pmod n.\]
<p><strong>Cas général.</strong> Il faut traiter les \(m\) divisibles par \(p\) ou \(q\) — un
point que beaucoup d'exposés oublient. Par le théorème chinois, il suffit de montrer
\(m^{ed}\equiv m\) modulo \(p\) et modulo \(q\) séparément.</p>
<p>Modulo \(p\), deux sous-cas :</p>
<ul>
<li>si \(p\mid m\), alors \(m\equiv0\) et \(m^{ed}\equiv0\equiv m\pmod p\) ;</li>
<li>si \(p\nmid m\), Fermat donne \(m^{p-1}\equiv1\pmod p\). Comme
\((p-1)\mid\varphi(n)=(p-1)(q-1)\), on a \(\varphi(n)=(p-1)\ell\), donc</li>
</ul>
\[m^{ed}=m\cdot\big(m^{p-1}\big)^{k\ell}\equiv m\pmod p.\]
<p>Le même argument vaut modulo \(q\). Les deux congruences et le théorème chinois donnent
\(m^{ed}\equiv m\pmod{pq}\).</p>
""") + r"""

""" + code(r"""
def phi(n):
    "Indicatrice d'Euler par la formule produit."
    resultat, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            resultat -= resultat // p
        p += 1
    if m > 1:
        resultat -= resultat // m
    return resultat

for n in [12, 13, 100, 3120]:
    print(n, phi(n))

# Euler, verifie exhaustivement sur Z/12Z
n = 12
from math import gcd
print([pow(a, phi(n), n) for a in range(1, n+1) if gcd(a, n) == 1])
""", "python", "12 4\n13 12\n100 40\n3120 768\n[1, 1, 1, 1]",
"L'indicatrice d'Euler, et son théorème") + r"""

""" + code(r"""
print([euler_phi(n) for n in [12, 13, 100, 3120]])
# RSA complet, sur de vrais premiers
p, q = next_prime(2^512), next_prime(2^513)
n, e = p*q, 65537
d = inverse_mod(e, (p-1)*(q-1))
m = 42
print(power_mod(power_mod(m, e, n), d, n) == m)
""", "sagemath", "[4, 12, 40, 768]\nTrue", "Vérification, et un RSA de 1024 bits") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Calculer \(\varphi(360)\), puis \(7^{1000}\bmod 360\) sans calculatrice.</p>
""", r"""
<p><u>Indicatrice.</u> \(360=2^3\times3^2\times5\), donc</p>
\[\varphi(360)=360\Big(1-\tfrac12\Big)\Big(1-\tfrac13\Big)\Big(1-\tfrac15\Big)
=360\times\tfrac12\times\tfrac23\times\tfrac45=\underline{96}.\]
<p><u>Puissance.</u> \(\pgcd(7,360)=1\), donc Euler donne \(7^{96}\equiv1\pmod{360}\).</p>
<p>\(1000=10\times96+40\), donc \(7^{1000}\equiv7^{40}\pmod{360}\).</p>
<p>Calculons \(7^{40}\) par carrés successifs modulo 360 :</p>
<p>\(7^2=49\), \(7^4=49^2=2401=6\times360+241\equiv241\),</p>
<p>\(7^8\equiv241^2=58081=161\times360+121\equiv121\),</p>
<p>\(7^{16}\equiv121^2=14641=40\times360+241\equiv241\),</p>
<p>\(7^{32}\equiv241^2\equiv121\).</p>
<p>\(40=32+8\), donc \(7^{40}\equiv121\times121=14641\equiv\underline{241}\pmod{360}\).</p>
""", r"""<p>On observe un cycle : \(7^4\equiv7^{16}\equiv241\) et \(7^8\equiv7^{32}\equiv121\).
L'ordre de 7 divise 96, et vaut ici 12 — toujours un diviseur de \(\varphi(n)\), conformément
à Lagrange.</p>""") + r"""

""" + exo(2, r"""
<p>Dans un RSA avec \(n=3233\) et \(e=17\), on sait que \(3233=61\times53\). Calculer \(d\),
puis déchiffrer \(c=2790\).</p>
""", r"""
<p><u>Indicatrice.</u> \(\varphi(3233)=(61-1)(53-1)=60\times52=3120\).</p>
<p><u>Clé privée.</u> \(d=17^{-1}\bmod 3120\). Euclide étendu :</p>
<p>\(3120=183\times17+9\), \(17=1\times9+8\), \(9=1\times8+1\).</p>
<p>Remontée : \(1=9-8=9-(17-9)=2\times9-17=2(3120-183\times17)-17=2\times3120-367\times17\).</p>
<p>Donc \(-367\times17\equiv1\pmod{3120}\), soit \(d=-367+3120=\underline{2753}\).</p>
<p><u>Déchiffrement.</u> \(m=2790^{2753}\bmod 3233\). En CRT, modulo 61 et 53 :</p>
<p>\(2790\equiv 11\pmod{61}\) et \(d\bmod 60=53\), d'où \(m\equiv11^{53}\equiv 4\pmod{61}\).</p>
<p>\(2790\equiv 30\pmod{53}\) et \(d\bmod 52=49\), d'où \(m\equiv30^{49}\equiv 13\pmod{53}\).</p>
<p>Reconstruction : \(m\equiv4\pmod{61}\) et \(m\equiv13\pmod{53}\) donnent
\(m=\underline{65}\).</p>
<p>Vérification : \(65^{17}\bmod3233=2790\) ✓</p>
""", r"""<p>C'est l'exemple historique de l'article de Rivest, Shamir et Adleman. Le message 65
est le code ASCII de la lettre « A ».</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["arith-premiers"] = r"""
<p class="lead">Générer une clé RSA, choisir un groupe pour Diffie-Hellman, construire un corps
fini : tout commence par trouver un grand nombre premier. Il faut donc savoir en tester un
sans le factoriser.</p>

<h3>Combien y a-t-il de premiers ?</h3>
""" + retenir("Théorème d'Euclide", r"""
<p>Il existe une infinité de nombres premiers.</p>
""") + demo(r"""
<p>Supposons qu'il n'y en ait qu'un nombre fini : \(p_1,\dots,p_k\).</p>
<p>Posons \(N=p_1p_2\cdots p_k+1\). Comme \(N\ge2\), il admet un diviseur premier \(p\)
(cf. le nœud « Les quatre techniques de preuve »).</p>
<p>Ce \(p\) est l'un des \(p_i\), donc \(p\) divise le produit \(p_1\cdots p_k\). Or \(p\) divise
aussi \(N\). Par différence, \(p\) divise \(N-p_1\cdots p_k=1\), ce qui est impossible pour un
nombre premier.</p>
<p>L'hypothèse est donc fausse : il y a une infinité de premiers.</p>
""") + r"""

""" + retenir("Théorème des nombres premiers (admis)", r"""
<p>En notant \(\pi(x)\) le nombre de premiers \(\le x\) :</p>
\[\pi(x)\ \sim\ \frac{x}{\ln x}.\]
<p>Conséquence pratique : parmi les entiers de \(k\) bits, environ un sur \(\ln(2^k)=k\ln2\approx
0{,}69\,k\) est premier.</p>
""") + r"""

""" + prof(r"""
<p>Pour une clé RSA de 2048 bits, il faut deux premiers de 1024 bits. La densité dit qu'un
entier impair de 1024 bits sur \(0{,}69\times1024/2\approx355\) est premier. En tirant au
hasard, quelques centaines d'essais suffisent : c'est pour cela que la génération de clé prend
une fraction de seconde et non des années.</p>
""") + r"""

<h3>Le test de Fermat et ses menteurs</h3>
<p>Fermat dit que si \(p\) est premier, \(a^{p-1}\equiv1\pmod p\). On teste la contraposée :
si \(a^{n-1}\not\equiv1\pmod n\), alors \(n\) est composé — avec certitude.</p>

""" + retenir("Limite du test de Fermat", r"""
<p>La réciproque est fausse. Un entier composé \(n\) tel que \(a^{n-1}\equiv1\pmod n\) pour tout
\(a\) premier à \(n\) est appelé <strong>nombre de Carmichael</strong>. Le plus petit est
\(561=3\times11\times17\), et il en existe une infinité.</p>
""") + demo(r"""
<p>Montrons que \(561\) est de Carmichael. Soit \(a\) premier à \(561\).</p>
<p>Comme \(561=3\times11\times17\), le théorème chinois permet de travailler modulo chaque
facteur. Par Fermat :</p>
<ul>
<li>\(a^{2}\equiv1\pmod3\), et \(2\mid560\) donc \(a^{560}\equiv1\pmod3\) ;</li>
<li>\(a^{10}\equiv1\pmod{11}\), et \(10\mid560\) donc \(a^{560}\equiv1\pmod{11}\) ;</li>
<li>\(a^{16}\equiv1\pmod{17}\), et \(16\mid560\) donc \(a^{560}\equiv1\pmod{17}\).</li>
</ul>
<p>Les trois congruences et le théorème chinois donnent \(a^{560}\equiv1\pmod{561}\), alors que
\(561\) est composé.</p>
<p>La clé est que \(p-1\) divise \(n-1\) pour chaque facteur premier \(p\) de \(n\) : c'est le
critère de Korselt.</p>
""") + r"""

<h3>Miller-Rabin</h3>
<p>Miller-Rabin corrige le défaut en exploitant une propriété supplémentaire : dans un corps,
l'équation \(x^2=1\) n'a que deux solutions.</p>

""" + retenir("Principe", r"""
<p>Écrivons \(n-1=2^{s}m\) avec \(m\) impair. Si \(n\) est premier, alors pour tout \(a\) :</p>
\[a^{m}\equiv1 \pmod n \qquad\text{ou}\qquad \exists\, r\in\{0,\dots,s-1\},\ a^{2^{r}m}\equiv-1\pmod n.\]
<p>Si aucune des deux conditions n'est remplie, \(n\) est composé et \(a\) est un
<strong>témoin</strong> de sa compositéité.</p>
<p><strong>Théorème (Rabin).</strong> Si \(n\) est composé, au moins \(3/4\) des \(a\) sont des
témoins. En testant \(k\) bases au hasard, la probabilité d'erreur est \(\le 4^{-k}\).</p>
""") + demo(r"""
<p>Démontrons la propriété directe (celle qu'on teste), en supposant \(n=p\) premier.</p>
<p>Par Fermat, \(a^{p-1}=a^{2^{s}m}\equiv1\). Considérons la suite</p>
\[a^{m},\ a^{2m},\ a^{4m},\ \dots,\ a^{2^{s}m}\equiv1,\]
<p>où chaque terme est le carré du précédent.</p>
<p>Dans le corps \(\Z/p\Z\), l'équation \(x^2=1\) s'écrit \((x-1)(x+1)=0\) ; un corps étant
intègre, ses seules solutions sont \(x=\pm1\).</p>
<p>Donc, en remontant la suite depuis son dernier terme qui vaut 1 : soit tous les termes valent
1 — et en particulier \(a^m\equiv1\) — soit il existe un premier indice \(r\) à partir duquel
les termes valent 1, et alors \(a^{2^{r}m}\) est une racine carrée de 1 différente de 1, donc
vaut \(-1\).</p>
<p>C'est exactement l'alternative annoncée.</p>
""") + r"""

""" + prof(r"""
<p>C'est l'intégrité du corps qui fait tout le travail : dans \(\Z/n\Z\) avec \(n\) composé, 1 a
en général plus de deux racines carrées, et c'est cette anomalie que le test détecte. Trouver
une racine carrée non triviale de 1 modulo \(n\), c'est d'ailleurs factoriser \(n\) : si
\(x^2\equiv1\) et \(x\neq\pm1\), alors \(\pgcd(x-1,n)\) est un facteur propre.</p>
""") + r"""

""" + code(r"""
import random

def miller_rabin(n, k=20):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    s, m = 0, n - 1
    while m % 2 == 0:
        s, m = s + 1, m // 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, m, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False                 # a est un temoin : n est compose
    return True                          # probablement premier

print(miller_rabin(561), miller_rabin(104729))

# Fermat se fait avoir par 561, Miller-Rabin non
print(all(pow(a, 560, 561) == 1 for a in range(2, 561) if __import__('math').gcd(a, 561) == 1))
""", "python", "False True\nTrue", "Miller-Rabin, et le menteur de Fermat") + r"""

<p>La dernière ligne confirme que 561 trompe le test de Fermat pour <em>toutes</em> les bases
premières à lui — et Miller-Rabin le démasque quand même.</p>

""" + code(r"""
print(is_prime(561), is_prime(104729))
print(factor(561))
# Generation d'un premier de 1024 bits, comme pour une cle RSA
p = random_prime(2^1024, lbound=2^1023)
print(p.nbits(), is_prime(p))
""", "sagemath", "False True\n3 * 11 * 17\n1024 True",
"Vérification, et une vraie génération de premier") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Appliquer le test de Miller-Rabin à \(n=221\) avec la base \(a=174\), puis avec \(a=137\).
Conclure.</p>
""", r"""
<p>\(n-1=220=2^2\times55\), donc \(s=2\) et \(m=55\).</p>
<p><u>Base \(a=174\).</u></p>
<p>\(174^{55}\bmod221=47\). Ce n'est ni \(1\) ni \(220\).</p>
<p>\(47^2=2209=9\times221+220\equiv220\equiv-1\). On tombe sur \(-1\) : le test
<u>passe</u>, 174 n'est pas un témoin.</p>
<p><u>Base \(a=137\).</u></p>
<p>\(137^{55}\bmod221=188\), différent de \(1\) et de \(220\).</p>
<p>\(188^2=35344=159\times221+205\equiv205\), différent de \(220\).</p>
<p>La suite est épuisée (\(s-1=1\) carré) sans rencontrer \(-1\) : <u>137 est un témoin</u>,
donc \(221\) est composé.</p>
<p>En effet \(221=13\times17\).</p>
""", r"""<p>Cet exemple montre pourquoi on teste plusieurs bases : une seule base peut échouer
à détecter un composé. Avec 20 bases, la probabilité d'erreur est inférieure à \(4^{-20}\approx
10^{-12}\).</p>""") + r"""

""" + exo(2, r"""
<p>Démontrer le critère de Korselt dans un sens : si \(n\) est sans facteur carré et si
\((p-1)\mid(n-1)\) pour tout premier \(p\mid n\), alors \(n\) est de Carmichael.</p>
""", r"""
<p>Soit \(a\) premier à \(n\), et \(p\) un facteur premier de \(n\). Comme \(n\) est sans facteur
carré, \(n=p_1\cdots p_k\) avec les \(p_i\) distincts.</p>
<p>Fixons \(i\). Comme \(\pgcd(a,n)=1\), on a \(p_i\nmid a\), donc Fermat donne</p>
\[a^{p_i-1}\equiv1\pmod{p_i}.\]
<p>Par hypothèse \((p_i-1)\mid(n-1)\), écrivons \(n-1=(p_i-1)\ell_i\). Alors</p>
\[a^{n-1}=\big(a^{p_i-1}\big)^{\ell_i}\equiv1^{\ell_i}=1\pmod{p_i}.\]
<p>Ceci vaut pour tout \(i\). Les \(p_i\) étant deux à deux premiers entre eux, le théorème
chinois donne</p>
\[a^{n-1}\equiv1\pmod{p_1\cdots p_k}=\pmod n.\]
<p>Donc \(n\) vérifie Fermat pour toute base première à lui : il est de Carmichael.</p>
""", r"""<p>La réciproque est vraie aussi, c'est le critère de Korselt complet. L'hypothèse
« sans facteur carré » est indispensable : si \(p^2\mid n\), on peut construire un \(a\) pour
lequel Fermat échoue.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["arith-residus"] = r"""
<p class="lead">Savoir si un nombre est un carré modulo \(p\) est une question facile (symbole
de Jacobi, en temps \(O(\log^2 p)\)), alors que calculer la racine carrée modulo \(n=pq\) est
aussi difficile que factoriser \(n\). Cet écart est la base de plusieurs cryptosystèmes.</p>

<h3>Le symbole de Legendre</h3>
""" + retenir("Définition", r"""
<p>Soit \(p\) un premier impair et \(a\in\Z\). On pose</p>
\[\legendre{a}{p}=\begin{cases}
0 & \text{si } p\mid a,\\
+1 & \text{si } a \text{ est un carré non nul modulo } p,\\
-1 & \text{sinon.}
\end{cases}\]
""") + r"""

""" + retenir("Critère d'Euler", r"""
<p>Pour \(p\) premier impair et \(p\nmid a\) :</p>
\[\legendre{a}{p}\equiv a^{\frac{p-1}{2}} \pmod p.\]
<p>Conséquence : <strong>le symbole de Legendre est multiplicatif</strong>,
\(\legendre{ab}{p}=\legendre{a}{p}\legendre{b}{p}\).</p>
""") + demo(r"""
<p>Posons \(q=\frac{p-1}{2}\) et travaillons dans le corps \(\Fp\).</p>
<p><strong>Les valeurs possibles.</strong> Par Fermat, \((a^{q})^2=a^{p-1}=1\). Dans un corps,
\(x^2=1\) entraîne \(x=\pm1\), donc \(a^{q}\equiv\pm1\).</p>
<p><strong>Si \(a\) est un carré</strong>, disons \(a=b^2\) avec \(p\nmid b\), alors</p>
\[a^{q}=b^{2q}=b^{p-1}\equiv1\pmod p.\]
<p><strong>Réciproque.</strong> Le polynôme \(X^{q}-1\) a au plus \(q\) racines dans le corps
\(\Fp\). Or on vient de voir que les carrés en sont racines. Combien y a-t-il de carrés non
nuls ? L'application \(x\mapsto x^2\) de \(\Fp^{\times}\) dans lui-même a pour noyau
\(\{\pm1\}\), de cardinal 2 ; son image est donc de cardinal \(\frac{p-1}{2}=q\).</p>
<p>Les \(q\) carrés sont donc exactement les \(q\) racines de \(X^{q}-1\). Un non-carré \(a\)
vérifie donc \(a^{q}\neq1\), et comme \(a^{q}\equiv\pm1\), il vient \(a^{q}\equiv-1\).</p>
<p><strong>Multiplicativité.</strong> Immédiate à partir du critère :
\((ab)^{q}=a^{q}b^{q}\).</p>
""") + r"""

<h3>La loi de réciprocité quadratique</h3>
""" + retenir("Théorème (Gauss, admis)", r"""
<p>Pour \(p\neq q\) premiers impairs :</p>
\[\legendre{p}{q}\legendre{q}{p}=(-1)^{\frac{p-1}{2}\cdot\frac{q-1}{2}}.\]
<p>Compléments :</p>
\[\legendre{-1}{p}=(-1)^{\frac{p-1}{2}},\qquad
\legendre{2}{p}=(-1)^{\frac{p^2-1}{8}}.\]
""") + r"""

<p>Autrement dit : \(\legendre{p}{q}=\legendre{q}{p}\) sauf si \(p\equiv q\equiv3\pmod4\),
auquel cas les deux symboles sont opposés. C'est ce qui permet de calculer un symbole sans
jamais factoriser, en renversant la fraction comme dans Euclide.</p>

""" + prof(r"""
<p>Le symbole de <strong>Jacobi</strong> étend Legendre à un dénominateur composé impair, en
posant \(\legendre{a}{n}=\prod\legendre{a}{p_i}^{\alpha_i}\). Il se calcule par réciprocité
<em>sans connaître la factorisation de \(n\)</em>. Attention : \(\legendre{a}{n}=1\) n'implique
plus que \(a\) soit un carré. C'est précisément cet écart qu'exploite le cryptosystème de
Goldwasser-Micali.</p>
""") + r"""

""" + code(r"""
def jacobi(a, n):
    "Symbole de Jacobi (a/n), n impair > 0. Calcule sans factoriser n."
    assert n > 0 and n % 2 == 1
    a, resultat = a % n, 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):          # complement pour 2
                resultat = -resultat
        a, n = n, a                      # reciprocite : on renverse
        if a % 4 == 3 and n % 4 == 3:
            resultat = -resultat
        a %= n
    return resultat if n == 1 else 0

p = 1009
carres = {x*x % p for x in range(1, p)}
print(all((jacobi(a, p) == 1) == (a in carres) for a in range(1, p)))
print(jacobi(1001, 9907))                 # calcule sans factoriser 9907
""", "python", "True\n-1", "Le symbole de Jacobi, par réciprocité") + r"""

<h3>Racines carrées et factorisation</h3>
""" + retenir("Théorème", r"""
<p>Soit \(n=pq\) avec \(p,q\) premiers impairs distincts. Savoir calculer une racine carrée
modulo \(n\) permet de factoriser \(n\) en temps polynomial.</p>
""") + demo(r"""
<p>Soit \(x\) tiré au hasard dans \(\Znz\), et \(a=x^2\bmod n\).</p>
<p>Par le théorème chinois, \(a\) a exactement quatre racines carrées modulo \(n\) :
\(\pm x\) et \(\pm y\), où \(y\equiv x\pmod p\) et \(y\equiv-x\pmod q\).</p>
<p>Supposons qu'un algorithme nous rende une racine carrée \(z\) de \(a\). Avec probabilité
\(1/2\), \(z\notin\{x,-x\}\), c'est-à-dire \(z\in\{y,-y\}\).</p>
<p>Dans ce cas \(z\equiv x\pmod p\) mais \(z\not\equiv x\pmod q\). Donc \(p\mid z-x\) tandis que
\(q\nmid z-x\), et par conséquent</p>
\[\pgcd(z-x,\ n)=p.\]
<p>On obtient un facteur propre de \(n\) par un simple calcul de PGCD. En répétant \(k\) fois,
la probabilité d'échec tombe à \(2^{-k}\).</p>
""") + r"""

""" + code(r"""
from math import gcd
import random

p, q = 10007, 10009
n = p * q

x = random.randrange(2, n)
while gcd(x, n) != 1:
    x = random.randrange(2, n)
a = x*x % n

# Les quatre racines carrees de a modulo n
racines = [z for z in (x, n-x, None, None)]
# on construit y par le theoreme chinois
y = (x * pow(q, -1, p) * q - x * pow(p, -1, q) * p) % n
racines[2], racines[3] = y, n - y
print(sorted(z*z % n == a for z in racines))

# Une racine "autre" factorise n
z = y
print(gcd(z - x, n), gcd(z + x, n))
""", "python", "[True, True, True, True]\n10007 10009",
"Une racine carrée de trop, et n est factorisé") + r"""

""" + prof(r"""
<p>C'est l'argument de sécurité du chiffrement de Rabin : déchiffrer, c'est extraire une racine
carrée modulo \(n\), et on vient de montrer que savoir le faire revient à factoriser. Rabin est
donc le rare cryptosystème dont la sécurité est <em>équivalente</em> à la factorisation — alors
que pour RSA, on sait seulement qu'elle y est au plus aussi difficile.</p>
""") + r"""

""" + code(r"""
p = 1009
print(legendre_symbol(3, p), jacobi_symbol(1001, 9907))
print(len(quadratic_residues(p)))          # (p-1)/2 + 1 avec 0
print(Mod(3, p).is_square(), Mod(3, p).sqrt())
""", "sagemath", "1 -1\n505\nTrue 149", "Vérification") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Calculer \(\legendre{30}{53}\) de deux façons : par le critère d'Euler, puis par la loi de
réciprocité.</p>
""", r"""
<p><u>Par Euler.</u> \(\frac{53-1}{2}=26\), il faut calculer \(30^{26}\bmod53\).</p>
<p>\(30^2=900=16\times53+52\equiv-1\pmod{53}\).</p>
<p>Donc \(30^{26}=(30^2)^{13}\equiv(-1)^{13}=\underline{-1}\).</p>
<p><u>Par réciprocité.</u> \(30=2\times3\times5\), et le symbole est multiplicatif :</p>
<p>\(\legendre{2}{53}\) : \(53\equiv5\pmod8\), donc \(\legendre{2}{53}=-1\).</p>
<p>\(\legendre{3}{53}\) : \(53\equiv1\pmod4\), donc pas de changement de signe :
\(\legendre{3}{53}=\legendre{53}{3}=\legendre{2}{3}=-1\) (car \(3\equiv3\pmod8\)).</p>
<p>\(\legendre{5}{53}\) : \(5\equiv1\pmod4\), donc
\(\legendre{5}{53}=\legendre{53}{5}=\legendre{3}{5}\). Les carrés modulo 5 sont \(\{1,4\}\),
donc \(\legendre{3}{5}=-1\).</p>
<p>Produit : \((-1)\times(-1)\times(-1)=\underline{-1}\). ✓</p>
""", r"""<p>Le fait que \(30^2\equiv-1\pmod{53}\) est un raccourci heureux. En général, la
réciprocité est bien plus rapide : elle coûte \(O(\log^2 p)\) contre une exponentiation
complète pour Euler.</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(p\equiv3\pmod4\) un premier et \(a\) un carré modulo \(p\). Montrer que
\(x=a^{(p+1)/4}\bmod p\) est une racine carrée de \(a\). Pourquoi cette formule ne marche-t-elle
pas si \(p\equiv1\pmod4\) ?</p>
""", r"""
<p>Comme \(p\equiv3\pmod4\), l'entier \(\frac{p+1}{4}\) est bien un entier.</p>
<p>Calculons \(x^2\) :</p>
\[x^2=a^{(p+1)/2}=a^{(p-1)/2}\cdot a.\]
<p>Comme \(a\) est un carré, le critère d'Euler donne \(a^{(p-1)/2}\equiv1\pmod p\). Donc</p>
\[x^2\equiv 1\times a=a\pmod p.\]
<p>\(x\) est bien une racine carrée de \(a\).</p>
<p><u>Cas \(p\equiv1\pmod4\).</u> Alors \(\frac{p+1}{4}\) n'est pas entier : la formule n'a
simplement pas de sens. Il faut l'algorithme de Tonelli-Shanks, nettement plus long.</p>
""", r"""<p>C'est la raison pour laquelle on choisit souvent \(p\equiv3\pmod4\) en pratique :
l'extraction de racine carrée se fait par une seule exponentiation. Les courbes elliptiques
standard, comme P-256, utilisent justement un tel premier pour décompresser les points.</p>""")


# ═════════════════════════════════════════════════════════════════════════════
# Groupes
# ═════════════════════════════════════════════════════════════════════════════

CORPS["grp-base"] = r"""
<p class="lead">Le groupe est la structure minimale qui permet de parler de logarithme discret.
Diffie-Hellman, ElGamal, ECDSA : tous se formulent dans « un groupe cyclique d'ordre premier »,
sans rien dire de plus. C'est cette abstraction qui permet de remplacer \(\Znz\) par une courbe
elliptique sans changer une ligne du protocole.</p>

<h3>Définition</h3>
""" + retenir("Groupe", r"""
<p>Un <strong>groupe</strong> est un couple \((G,*)\) où \(*\) est une loi interne sur \(G\)
telle que :</p>
<ul>
<li><strong>associativité</strong> : \(\forall x,y,z,\ (x*y)*z=x*(y*z)\) ;</li>
<li><strong>neutre</strong> : \(\exists e,\ \forall x,\ x*e=e*x=x\) ;</li>
<li><strong>inverse</strong> : \(\forall x,\ \exists x',\ x*x'=x'*x=e\).</li>
</ul>
<p>Le groupe est <strong>abélien</strong> si de plus \(x*y=y*x\) pour tous \(x,y\).</p>
<p>L'<strong>ordre</strong> de \(G\), noté \(|G|\), est son cardinal.</p>
""") + r"""

<p>Les groupes du master, à connaître par cœur :</p>
<div class="table-wrap"><table>
<thead><tr><th>Groupe</th><th>Loi</th><th>Ordre</th><th>Où il sert</th></tr></thead><tbody>
<tr><td>\((\Z/n\Z,+)\)</td><td>addition</td><td>\(n\)</td><td>décalages, chiffrement affine</td></tr>
<tr><td>\(\Znz\)</td><td>multiplication</td><td>\(\varphi(n)\)</td><td>RSA, Diffie-Hellman</td></tr>
<tr><td>\(\Fq^{\times}\)</td><td>multiplication</td><td>\(q-1\)</td><td>AES, codes BCH</td></tr>
<tr><td>\(E(\Fq)\)</td><td>loi de corde-tangente</td><td>\(\approx q\)</td><td>ECDH, ECDSA</td></tr>
<tr><td>\(S_n\)</td><td>composition</td><td>\(n!\)</td><td>permutations, S-boîtes</td></tr>
</tbody></table></div>

<h3>Unicité du neutre et de l'inverse</h3>
""" + retenir("Proposition", r"""
<p>Dans un groupe, le neutre est unique et chaque élément a un unique inverse.</p>
""") + demo(r"""
<p><strong>Neutre.</strong> Soient \(e\) et \(e'\) deux neutres. Alors</p>
\[e = e*e' \quad(\text{car } e' \text{ est neutre à droite})\]
\[e*e' = e' \quad(\text{car } e \text{ est neutre à gauche}).\]
<p>Donc \(e=e'\).</p>
<p><strong>Inverse.</strong> Soient \(x'\) et \(x''\) deux inverses de \(x\). Alors</p>
\[x'=x'*e=x'*(x*x'')=(x'*x)*x''=e*x''=x''.\]
<p>L'associativité est ce qui rend ce calcul possible : c'est elle qui porte toute la preuve.</p>
""") + r"""

<h3>Sous-groupes</h3>
""" + retenir("Caractérisation", r"""
<p>\(H\subset G\) est un sous-groupe si et seulement si</p>
<ul>
<li>\(H\neq\emptyset\) (en pratique : \(e\in H\)), et</li>
<li>\(\forall x,y\in H,\ x*y^{-1}\in H\).</li>
</ul>
""") + demo(r"""
<p>Le sens direct est immédiat. Montrons la réciproque.</p>
<p>Soit \(x\in H\) (possible car \(H\neq\emptyset\)). En prenant \(y=x\) dans le critère :
\(x*x^{-1}=e\in H\).</p>
<p>Soit \(y\in H\). En prenant le couple \((e,y)\) : \(e*y^{-1}=y^{-1}\in H\), donc \(H\) est
stable par inverse.</p>
<p>Soient \(x,y\in H\). Comme \(y^{-1}\in H\), le critère appliqué à \((x,y^{-1})\) donne
\(x*(y^{-1})^{-1}=x*y\in H\) : \(H\) est stable par la loi.</p>
<p>L'associativité est héritée de \(G\). Donc \(H\) est un groupe.</p>
""") + r"""

<h3>Ordre d'un élément</h3>
""" + retenir("Définition et propriété", r"""
<p>Soit \(G\) fini et \(x\in G\). L'<strong>ordre</strong> de \(x\), noté \(\ord(x)\), est le plus
petit entier \(k\ge1\) tel que \(x^{k}=e\).</p>
<p><strong>Propriété fondamentale.</strong> \(x^{m}=e \iff \ord(x)\mid m\).</p>
""") + demo(r"""
<p>Notons \(d=\ord(x)\), qui existe : les puissances \(x,x^2,x^3,\dots\) ne peuvent pas être
toutes distinctes dans un ensemble fini, donc \(x^{i}=x^{j}\) pour certains \(i<j\), d'où
\(x^{j-i}=e\) avec \(j-i\ge1\).</p>
<p><strong>(\(\Leftarrow\))</strong> Si \(d\mid m\), écrivons \(m=dk\) ; alors
\(x^{m}=(x^{d})^{k}=e^{k}=e\).</p>
<p><strong>(\(\Rightarrow\))</strong> Supposons \(x^{m}=e\). Division euclidienne : \(m=dq+r\)
avec \(0\le r<d\). Alors</p>
\[e=x^{m}=(x^{d})^{q}*x^{r}=e*x^{r}=x^{r}.\]
<p>Si \(r>0\), cela contredirait la minimalité de \(d\). Donc \(r=0\), c'est-à-dire \(d\mid m\).</p>
""") + r"""

""" + prof(r"""
<p>C'est <em>la</em> propriété à réflexe en cryptographie. Quand on veut savoir si un générateur
candidat \(g\) est d'ordre \(q\) dans un groupe d'ordre \(N\), on ne calcule jamais l'ordre : on
vérifie que \(g^{q}=e\) et que \(g^{q/p}\neq e\) pour chaque premier \(p\mid q\). Deux
exponentiations au lieu d'une recherche exhaustive.</p>
""") + r"""

""" + code(r"""
def ordre(x, n):
    "Ordre de x dans (Z/nZ)* par recherche directe."
    k, y = 1, x % n
    while y != 1:
        y = y * x % n
        k += 1
    return k

n = 13
for x in range(1, n):
    print(x, ordre(x, n))
""", "python",
"""1 1
2 12
3 3
4 6
5 4
6 12
7 12
8 4
9 3
10 6
11 12
12 2""",
"Les ordres dans (ℤ/13ℤ)*") + r"""

<p>Tous les ordres divisent 12, qui est l'ordre du groupe : c'est le théorème de Lagrange,
objet du nœud suivant. Les éléments d'ordre 12 — ici \(2, 6, 7, 11\) — sont les générateurs.</p>

""" + code(r"""
G = Integers(13).unit_group()
print(G.order())
R = Integers(13)
print([(x, R(x).multiplicative_order()) for x in range(1, 13)])
""", "sagemath",
"12\n[(1, 1), (2, 12), (3, 3), (4, 6), (5, 4), (6, 12), (7, 12), (8, 4), (9, 3), (10, 6), (11, 12), (12, 2)]",
"Vérification") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Montrer que l'ensemble \(H=\{x\in\Znz\ ;\ x^2=1\}\) est un sous-groupe de \(\Znz\).
Le déterminer pour \(n=8\), puis pour \(n=15\). Que remarque-t-on ?</p>
""", r"""
<p><u>Sous-groupe.</u> \(1\in H\) donc \(H\neq\emptyset\). Soient \(x,y\in H\) ; alors</p>
\[(xy^{-1})^2=x^2(y^{-1})^2=x^2(y^2)^{-1}=1\cdot1^{-1}=1,\]
<p>(on utilise la commutativité de \(\Znz\)), donc \(xy^{-1}\in H\). C'est un sous-groupe.</p>
<p><u>\(n=8\).</u> \((\Z/8\Z)^{\times}=\{1,3,5,7\}\). Or \(3^2=9=1\), \(5^2=25=1\),
\(7^2=49=1\). Donc \(H=\{1,3,5,7\}\) : <u>le groupe tout entier</u>.</p>
<p><u>\(n=15\).</u> \(1^2=1\), \(4^2=16=1\), \(11^2=121=8\times15+1=1\), \(14^2=196=13\times15+1=1\).
Donc \(H=\{1,4,11,14\}\), de cardinal 4 dans un groupe d'ordre \(\varphi(15)=8\).</p>
<p><u>Remarque.</u> Dans les deux cas \(|H|>2\) : il y a plus de deux racines carrées de 1.
C'est impossible dans un corps, donc \(\Z/8\Z\) et \(\Z/15\Z\) n'en sont pas.</p>
""", r"""<p>C'est exactement l'anomalie qu'exploite Miller-Rabin, et celle qui permet de
factoriser : \(\pgcd(4-1,15)=3\) et \(\pgcd(4+1,15)=5\).</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(G\) un groupe dans lequel \(x^2=e\) pour tout \(x\). Montrer que \(G\) est abélien.</p>
""", r"""
<p>L'hypothèse \(x^2=e\) signifie \(x=x^{-1}\) pour tout \(x\) : chaque élément est son propre
inverse.</p>
<p>Soient \(x,y\in G\). Appliquons l'hypothèse à l'élément \(xy\) :</p>
\[xy=(xy)^{-1}=y^{-1}x^{-1}=yx,\]
<p>la dernière égalité venant de \(y^{-1}=y\) et \(x^{-1}=x\).</p>
<p>Donc \(xy=yx\) : <u>\(G\) est abélien</u>.</p>
""", r"""<p>Un tel groupe est un espace vectoriel sur \(\F_2\). C'est le cas de
\((\{0,1\}^{n},\oplus)\), le groupe du XOR, omniprésent en cryptographie symétrique :
chiffrer deux fois avec la même clé redonne le clair.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["grp-lagrange"] = r"""
<p class="lead">Le théorème de Lagrange est l'énoncé le plus rentable de toute la théorie des
groupes : une seule idée — découper le groupe en classes de même taille — et il en tombe Fermat,
Euler, et la méthode standard de vérification d'un générateur.</p>

<h3>Classes à gauche</h3>
""" + retenir("Définition", r"""
<p>Soit \(H\) un sous-groupe de \(G\). Pour \(x\in G\), la <strong>classe à gauche</strong> de
\(x\) est</p>
\[xH=\{xh\ ;\ h\in H\}.\]
""") + r"""

""" + retenir("Lemme", r"""
<p>Les classes à gauche forment une partition de \(G\), et elles ont toutes le même cardinal
\(|H|\).</p>
""") + demo(r"""
<p><strong>C'est une partition.</strong> La relation \(x\mathcal R y \iff x^{-1}y\in H\) est une
relation d'équivalence :</p>
<ul>
<li>réflexive : \(x^{-1}x=e\in H\) ;</li>
<li>symétrique : si \(x^{-1}y\in H\), alors \((x^{-1}y)^{-1}=y^{-1}x\in H\) ;</li>
<li>transitive : si \(x^{-1}y\in H\) et \(y^{-1}z\in H\), alors
\((x^{-1}y)(y^{-1}z)=x^{-1}z\in H\).</li>
</ul>
<p>Sa classe d'équivalence est \(\{y\ ;\ x^{-1}y\in H\}=\{y\ ;\ y\in xH\}=xH\). Les classes
d'une relation d'équivalence formant une partition (nœud « Relations d'équivalence et
quotients »), c'est acquis.</p>
<p><strong>Même cardinal.</strong> L'application \(H\to xH,\ h\mapsto xh\) est surjective par
définition, et injective : si \(xh=xh'\), on multiplie à gauche par \(x^{-1}\) et il vient
\(h=h'\). C'est donc une bijection, d'où \(|xH|=|H|\).</p>
""") + r"""

<h3>Le théorème</h3>
""" + retenir("Théorème de Lagrange", r"""
<p>Si \(G\) est un groupe fini et \(H\) un sous-groupe, alors</p>
\[|H| \ \big|\ |G|,\qquad\text{plus précisément}\qquad |G|=[G:H]\cdot|H|,\]
<p>où \([G:H]\) est le nombre de classes à gauche (l'<strong>indice</strong> de \(H\)).</p>
""") + demo(r"""
<p>Par le lemme, \(G\) est la réunion disjointe de ses classes à gauche, qui ont toutes le
cardinal \(|H|\).</p>
<p>S'il y a \(m=[G:H]\) classes distinctes, le cardinal de la réunion disjointe est la somme des
cardinaux :</p>
\[|G|=\sum_{i=1}^{m}|x_iH|=m\cdot|H|.\]
<p>Donc \(|H|\) divise \(|G|\).</p>
""") + r"""

""" + retenir("Corollaires", r"""
<p>Soit \(G\) fini d'ordre \(N\) et \(x\in G\).</p>
<ol>
<li>\(\ord(x)\) divise \(N\) ;</li>
<li>\(x^{N}=e\) ;</li>
<li>si \(N\) est premier, \(G\) est cyclique et tout élément \(\neq e\) en est générateur.</li>
</ol>
""") + demo(r"""
<p><strong>(1)</strong> Le sous-groupe engendré \(\langle x\rangle=\{e,x,\dots,x^{d-1}\}\) où
\(d=\ord(x)\) est de cardinal exactement \(d\) (ces éléments sont distincts par minimalité de
\(d\)). Lagrange donne \(d\mid N\).</p>
<p><strong>(2)</strong> Écrivons \(N=d\cdot k\). Alors \(x^{N}=(x^{d})^{k}=e\).</p>
<p><strong>(3)</strong> Soit \(x\neq e\). Alors \(\ord(x)>1\) et \(\ord(x)\mid N\) avec \(N\)
premier, donc \(\ord(x)=N\). Le sous-groupe \(\langle x\rangle\) a donc \(N\) éléments, c'est
\(G\) tout entier.</p>
""") + r"""

""" + prof(r"""
<p>Le corollaire (2) appliqué à \(G=\Znz\), d'ordre \(\varphi(n)\), redonne le théorème d'Euler
\(a^{\varphi(n)}\equiv1\). On avait démontré Euler directement au niveau de l'arithmétique ;
on voit maintenant que ce n'est qu'un cas particulier de Lagrange. C'est le mouvement typique
du master : un résultat d'arithmétique devient une ligne de théorie des groupes.</p>
""") + r"""

""" + prof(r"""
<p>Attention au piège : la réciproque de Lagrange est <strong>fausse</strong>. Un diviseur de
\(|G|\) n'est pas toujours l'ordre d'un sous-groupe. Le contre-exemple standard est le groupe
alterné \(A_4\), d'ordre 12, qui n'a aucun sous-groupe d'ordre 6.</p>
""") + r"""

""" + code(r"""
from math import gcd

def sous_groupe_engendre(x, n):
    H, y = {1}, x % n
    while y != 1:
        H.add(y)
        y = y * x % n
    return sorted(H)

n = 13          # |(Z/13Z)*| = 12
for x in [1, 3, 5, 12]:
    H = sous_groupe_engendre(x, n)
    print(x, len(H), 12 % len(H) == 0, H)
""", "python",
"""1 1 True [1]
3 3 True [1, 3, 9]
5 4 True [1, 5, 8, 12]
12 2 True [1, 12]""",
"Tous les sous-groupes engendrés ont un ordre divisant 12") + r"""

""" + code(r"""
G = SymmetricGroup(4)
A4 = AlternatingGroup(4)
print(A4.order(), [H.order() for H in A4.subgroups()])
# 6 divise 12, mais n'apparait pas : la reciproque de Lagrange est fausse
""", "sagemath", "12 [1, 2, 2, 2, 3, 3, 3, 3, 4, 12]",
"A₄ n'a aucun sous-groupe d'ordre 6") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soit \(G\) un groupe d'ordre \(p\) premier. Montrer que \(G\) n'a que deux sous-groupes,
et qu'il est isomorphe à \((\Z/p\Z,+)\).</p>
""", r"""
<p><u>Sous-groupes.</u> Soit \(H\le G\). Par Lagrange \(|H|\mid p\), et \(p\) étant premier,
\(|H|\in\{1,p\}\), c'est-à-dire \(H=\{e\}\) ou \(H=G\). Il n'y a donc que
<u>deux sous-groupes</u>.</p>
<p><u>Isomorphisme.</u> Soit \(x\neq e\). Par le corollaire (3), \(\ord(x)=p\) et
\(G=\langle x\rangle=\{e,x,\dots,x^{p-1}\}\).</p>
<p>L'application \(\psi:\Z/p\Z\to G,\ \bar k\mapsto x^{k}\) est bien définie (si \(k\equiv k'\),
alors \(x^{k-k'}=e\) car \(p\mid k-k'\)), c'est un morphisme (\(x^{k+l}=x^kx^l\)), et elle est
surjective. Les deux ensembles ayant \(p\) éléments, elle est bijective.</p>
<p>Donc <u>\(G\simeq\Z/p\Z\)</u> : à isomorphisme près, il n'existe qu'un seul groupe d'ordre
premier \(p\).</p>
""", r"""<p>C'est pour cela que les protocoles disent « soit \(G\) un groupe cyclique d'ordre
premier \(q\) » sans préciser lequel : il n'y en a qu'un. Seule change la difficulté du
logarithme discret selon la <em>représentation</em> choisie — et c'est tout l'enjeu du choix
entre \(\Znz\) et une courbe elliptique.</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(G\) un groupe fini d'ordre \(N\), et \(q\) un diviseur premier de \(N\). On veut
vérifier qu'un élément \(g\) est d'ordre exactement \(N\). Proposer une méthode qui n'énumère
pas les puissances de \(g\).</p>
""", r"""
<p>Par Lagrange, \(\ord(g)\mid N\). Si \(\ord(g)\neq N\), alors \(\ord(g)\) est un diviseur
strict de \(N\), donc il divise \(N/p\) pour au moins un facteur premier \(p\) de \(N\).</p>
<p>En effet, si \(d\mid N\) et \(d<N\), alors \(N/d>1\) admet un diviseur premier \(p\), et
\(d\mid N/p\).</p>
<p>D'où le test :</p>
<div class="prof"><p>\(g\) est d'ordre \(N\) si et seulement si \(g^{N/p}\neq e\)
pour tout facteur premier \(p\) de \(N\).</p></div>
<p>Le coût est de \(k\) exponentiations, où \(k\) est le nombre de facteurs premiers distincts
de \(N\) — c'est-à-dire \(O(\log N)\) au pire, contre \(N\) multiplications pour l'énumération.</p>
""", r"""<p>Ce test exige de connaître la factorisation de \(N\). C'est pour cela que les
standards publient, avec le groupe, la factorisation de son ordre : sans elle, on ne peut pas
vérifier qu'un générateur en est un.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["grp-cycliques"] = r"""
<p class="lead">Le groupe cyclique est le terrain de jeu de Diffie-Hellman. Sa structure est
entièrement connue — on sait lister tous ses sous-groupes et tous ses générateurs — et c'est
justement parce qu'elle est si transparente que la question du logarithme discret est bien posée.</p>

<h3>Définition et premier exemple</h3>
""" + retenir("Définition", r"""
<p>\(G\) est <strong>cyclique</strong> s'il existe \(g\in G\) tel que \(G=\langle g\rangle=
\{g^{k}\ ;\ k\in\Z\}\). Un tel \(g\) est un <strong>générateur</strong> (ou élément primitif).</p>
""") + r"""

""" + retenir("Théorème (classification)", r"""
<p>Tout groupe cyclique d'ordre \(n\) est isomorphe à \((\Z/n\Z,+)\).</p>
""") + demo(r"""
<p>Soit \(G=\langle g\rangle\) d'ordre \(n\), donc \(\ord(g)=n\).</p>
<p>Considérons \(\psi:\Z\to G,\ k\mapsto g^{k}\). C'est un morphisme de \((\Z,+)\) dans \(G\),
surjectif par définition.</p>
<p>Son noyau est \(\{k\ ;\ g^{k}=e\}=\{k\ ;\ n\mid k\}=n\Z\), par la propriété fondamentale
de l'ordre.</p>
<p>Le premier théorème d'isomorphisme (nœud « Les théorèmes d'isomorphisme ») donne alors</p>
\[\Z/n\Z=\Z/\Ker\psi\ \simeq\ \Img\psi=G.\]
<p>On peut aussi le voir à la main : \(\bar k\mapsto g^{k}\) est bien définie, morphique,
surjective, et entre ensembles de même cardinal \(n\), donc bijective.</p>
""") + r"""

<h3>Les sous-groupes</h3>
""" + retenir("Théorème", r"""
<p>Soit \(G=\langle g\rangle\) cyclique d'ordre \(n\).</p>
<ol>
<li>Pour chaque diviseur \(d\mid n\), il existe un <strong>unique</strong> sous-groupe d'ordre
\(d\), à savoir \(\langle g^{n/d}\rangle\).</li>
<li>\(\ord(g^{k})=\dfrac{n}{\pgcd(n,k)}\).</li>
<li>\(g^{k}\) est un générateur \(\iff \pgcd(n,k)=1\). Il y a donc \(\varphi(n)\) générateurs.</li>
</ol>
""") + demo(r"""
<p><strong>(2) d'abord.</strong> Posons \(d=\pgcd(n,k)\), \(n=dn'\), \(k=dk'\) avec
\(\pgcd(n',k')=1\).</p>
<p>On a \((g^{k})^{m}=e \iff n\mid km \iff n'\mid k'm\). Comme \(\pgcd(n',k')=1\), le lemme de
Gauss donne \(n'\mid m\).</p>
<p>Le plus petit tel \(m\ge1\) est \(n'=n/d\), donc \(\ord(g^{k})=n/\pgcd(n,k)\).</p>
<p><strong>(3).</strong> \(g^{k}\) engendre \(G\) si et seulement si \(\ord(g^{k})=n\),
c'est-à-dire \(n/\pgcd(n,k)=n\), soit \(\pgcd(n,k)=1\). Le nombre de tels \(k\) dans
\(\{0,\dots,n-1\}\) est \(\varphi(n)\) par définition.</p>
<p><strong>(1) Existence.</strong> Par (2), \(\ord(g^{n/d})=n/\pgcd(n,n/d)=n/(n/d)=d\).
Donc \(\langle g^{n/d}\rangle\) est d'ordre \(d\).</p>
<p><strong>(1) Unicité.</strong> Soit \(H\le G\) d'ordre \(d\). Tout \(x\in H\) vérifie
\(x^{d}=e\) (Lagrange). Or les solutions de \(x^{d}=e\) dans \(G\) sont les \(g^{k}\) avec
\(n\mid kd\), c'est-à-dire \((n/d)\mid k\) : il y en a exactement \(d\), et elles forment
précisément \(\langle g^{n/d}\rangle\).</p>
<p>Comme \(H\) est inclus dans cet ensemble de cardinal \(d\) et que \(|H|=d\), on a
\(H=\langle g^{n/d}\rangle\).</p>
""") + r"""

""" + prof(r"""
<p>La conséquence pratique est brutale : dans un groupe cyclique d'ordre \(n\) composé, le
logarithme discret se résout séparément dans chaque sous-groupe d'ordre premier, puis on
recolle par le théorème chinois. C'est l'algorithme de Pohlig-Hellman, et c'est pourquoi on
exige que \(n\) ait un <strong>grand facteur premier</strong>. Un groupe d'ordre
\(2^{40}\times3^{30}\) est aussi faible que ses plus gros morceaux.</p>
""") + r"""

""" + code(r"""
from math import gcd

n = 12
g = 2                        # on travaille dans (Z/12Z, +) : g^k devient k*g
def ordre_additif(k, n):
    return n // gcd(n, k)

print("ordres :", [(k, ordre_additif(k, n)) for k in range(n)])
print("generateurs :", [k for k in range(n) if gcd(k, n) == 1])
print("phi(12) =", sum(1 for k in range(n) if gcd(k, n) == 1))

# un sous-groupe par diviseur, et un seul
for d in [1, 2, 3, 4, 6, 12]:
    H = sorted({(k * (n // d)) % n for k in range(d)})
    print("ordre", d, ":", H)
""", "python",
"""ordres : [(0, 1), (1, 12), (2, 6), (3, 4), (4, 3), (5, 12), (6, 2), (7, 12), (8, 3), (9, 4), (10, 6), (11, 12)]
generateurs : [1, 5, 7, 11]
phi(12) = 4
ordre 1 : [0]
ordre 2 : [0, 6]
ordre 3 : [0, 4, 8]
ordre 4 : [0, 3, 6, 9]
ordre 6 : [0, 2, 4, 6, 8, 10]
ordre 12 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]""",
"La structure complète d'un groupe cyclique d'ordre 12") + r"""

<h3>Diffie-Hellman, enfin</h3>
<p>Tout le protocole tient maintenant en quatre lignes.</p>

""" + code(r"""
p = 2^255 - 19                      # un premier standard (Curve25519)
g = 2
# Alice et Bob
a = randint(2, p-2);  A = power_mod(g, a, p)
b = randint(2, p-2);  B = power_mod(g, b, p)
# Secret commun : (g^a)^b = (g^b)^a
print(power_mod(B, a, p) == power_mod(A, b, p))
""", "sagemath", "True", "Diffie-Hellman, dans un groupe cyclique") + r"""

""" + prof(r"""
<p>Ce que l'adversaire voit, c'est \(g\), \(g^{a}\) et \(g^{b}\). Pour retrouver le secret il lui
faudrait \(a\) ou \(b\) : c'est le <strong>problème du logarithme discret</strong>. Toute la
sécurité tient à ce que l'exponentiation soit facile (\(O(\log a)\) multiplications, cf.
« Congruences et l'anneau ℤ/nℤ ») et son inverse difficile.</p>
""") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Dans \((\Z/20\Z,+)\), déterminer l'ordre de chaque élément, la liste des générateurs, et
tous les sous-groupes.</p>
""", r"""
<p><u>Ordres.</u> \(\ord(k)=\dfrac{20}{\pgcd(20,k)}\).</p>
<div class="table-wrap"><table><tbody>
<tr><td>\(\pgcd(20,k)=1\)</td><td>\(k\in\{1,3,7,9,11,13,17,19\}\)</td><td>ordre 20</td></tr>
<tr><td>\(\pgcd=2\)</td><td>\(k\in\{2,6,14,18\}\)</td><td>ordre 10</td></tr>
<tr><td>\(\pgcd=4\)</td><td>\(k\in\{4,8,12,16\}\)</td><td>ordre 5</td></tr>
<tr><td>\(\pgcd=5\)</td><td>\(k\in\{5,15\}\)</td><td>ordre 4</td></tr>
<tr><td>\(\pgcd=10\)</td><td>\(k=10\)</td><td>ordre 2</td></tr>
<tr><td>\(\pgcd=20\)</td><td>\(k=0\)</td><td>ordre 1</td></tr>
</tbody></table></div>
<p><u>Générateurs.</u> Les 8 éléments d'ordre 20, et \(\varphi(20)=20(1-\tfrac12)(1-\tfrac15)=8\) ✓</p>
<p><u>Sous-groupes.</u> Un par diviseur de 20 :</p>
<p>\(\{0\}\) ; \(\{0,10\}\) ; \(\{0,4,8,12,16\}\) ; \(\{0,5,10,15\}\) ;
\(\{0,2,4,\dots,18\}\) ; \(\Z/20\Z\).</p>
""", r"""<p>Six diviseurs de 20, six sous-groupes : c'est la bijection du théorème. Dans un groupe
non cyclique, cette bijection tombe.</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(p=2q+1\) avec \(p\) et \(q\) premiers (on dit que \(p\) est un <em>premier sûr</em>).
Quels sont les ordres possibles des éléments de \(\Z/p\Z^{\times}\) ? Pourquoi ce choix de \(p\)
est-il recommandé pour Diffie-Hellman ?</p>
""", r"""
<p>\(|\Fp^{\times}|=p-1=2q\). Par Lagrange, les ordres divisent \(2q\), donc appartiennent à
\(\{1,2,q,2q\}\).</p>
<p>Comptons : un seul élément d'ordre 1 (\(x=1\)) ; un seul d'ordre 2 (\(x=p-1\), car
\(x^2=1\) n'a que deux solutions dans un corps) ; \(\varphi(q)=q-1\) éléments d'ordre \(q\) ;
et \(\varphi(2q)=q-1\) éléments d'ordre \(2q\).</p>
<p>Total : \(1+1+(q-1)+(q-1)=2q\) ✓</p>
<p><u>Intérêt pour Diffie-Hellman.</u> Pohlig-Hellman ramène le logarithme discret aux
sous-groupes d'ordre premier. Ici les seuls facteurs premiers de \(p-1\) sont \(2\) et \(q\) :
le problème ne se décompose qu'en un sous-groupe trivial d'ordre 2 et un sous-groupe d'ordre
\(q\), qui reste de taille maximale.</p>
<p>Autrement dit, <u>la structure du groupe n'offre aucune prise à l'attaquant</u>. Si au
contraire \(p-1\) avait beaucoup de petits facteurs, le logarithme discret serait facile.</p>
""", r"""<p>En pratique on travaille dans le sous-groupe d'ordre \(q\) (les carrés), ce qui
supprime aussi la fuite d'un bit d'information par le symbole de Legendre.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["grp-morphismes"] = r"""
<p class="lead">Le passage au quotient est la technique qui transforme un gros problème en
plusieurs petits. En cryptanalyse, c'est l'idée exacte de Pohlig-Hellman : projeter le
logarithme discret dans chaque sous-groupe d'ordre premier, puis recoller.</p>

<h3>Morphismes</h3>
""" + retenir("Définition", r"""
<p>\(f:G\to G'\) est un <strong>morphisme de groupes</strong> si
\(f(xy)=f(x)f(y)\) pour tous \(x,y\in G\).</p>
<p>On pose \(\Ker f=\{x\in G\ ;\ f(x)=e'\}\) et \(\Img f=f(G)\).</p>
""") + r"""

""" + retenir("Proposition", r"""
<ol>
<li>\(f(e)=e'\) et \(f(x^{-1})=f(x)^{-1}\) ;</li>
<li>\(\Ker f\) est un sous-groupe de \(G\), \(\Img f\) un sous-groupe de \(G'\) ;</li>
<li>\(f\) est injective \(\iff \Ker f=\{e\}\).</li>
</ol>
""") + demo(r"""
<p><strong>(1)</strong> De \(f(e)=f(ee)=f(e)f(e)\), on multiplie par \(f(e)^{-1}\) :
\(e'=f(e)\). Puis \(f(x)f(x^{-1})=f(xx^{-1})=f(e)=e'\), donc \(f(x^{-1})=f(x)^{-1}\).</p>
<p><strong>(2)</strong> \(e\in\Ker f\) par (1). Si \(x,y\in\Ker f\), alors
\(f(xy^{-1})=f(x)f(y)^{-1}=e'e'^{-1}=e'\), donc \(xy^{-1}\in\Ker f\) : c'est un sous-groupe
(critère du nœud « Groupes, sous-groupes, ordre »). Même argument pour \(\Img f\).</p>
<p><strong>(3)</strong> Si \(f\) est injective, \(f(x)=e'=f(e)\) force \(x=e\).</p>
<p>Réciproquement, si \(\Ker f=\{e\}\) et \(f(x)=f(y)\), alors \(f(xy^{-1})=f(x)f(y)^{-1}=e'\),
donc \(xy^{-1}\in\Ker f=\{e\}\), d'où \(x=y\).</p>
""") + r"""

<h3>Sous-groupes distingués</h3>
<p>Pour que \(G/H\) soit un groupe, il ne suffit pas que \(H\) soit un sous-groupe : il faut que
la multiplication passe au quotient (cf. nœud « Relations d'équivalence et quotients »).</p>

""" + retenir("Définition et théorème", r"""
<p>\(H\le G\) est <strong>distingué</strong> (noté \(H\trianglelefteq G\)) si</p>
\[\forall x\in G,\ xHx^{-1}=H,\qquad\text{de façon équivalente}\qquad \forall x\in G,\ xH=Hx.\]
<p><strong>Théorème.</strong> \(G/H\) est un groupe pour \(\overline{x}\cdot\overline{y}
=\overline{xy}\) si et seulement si \(H\trianglelefteq G\).</p>
<p>Dans un groupe <strong>abélien</strong>, tout sous-groupe est distingué.</p>
""") + demo(r"""
<p>Montrons que la loi est bien définie si et seulement si \(H\) est distingué.</p>
<p><strong>(\(\Leftarrow\))</strong> Supposons \(H\trianglelefteq G\), et soient \(xH=x'H\),
\(yH=y'H\). Il existe \(h_1,h_2\in H\) tels que \(x'=xh_1\) et \(y'=yh_2\). Alors</p>
\[x'y'=xh_1yh_2=xy\,(y^{-1}h_1y)\,h_2.\]
<p>Comme \(H\) est distingué, \(y^{-1}h_1y\in H\), donc \(x'y'\in xyH\), c'est-à-dire
\(\overline{x'y'}=\overline{xy}\) : la loi ne dépend pas des représentants.</p>
<p><strong>(\(\Rightarrow\))</strong> Supposons la loi bien définie. Soient \(x\in G\) et
\(h\in H\). Comme \(\overline{h}=\overline{e}\), on a
\(\overline{xhx^{-1}}=\overline{x}\,\overline{h}\,\overline{x^{-1}}
=\overline{x}\,\overline{e}\,\overline{x^{-1}}=\overline{xx^{-1}}=\overline{e}\),
donc \(xhx^{-1}\in H\).</p>
<p>Ainsi \(xHx^{-1}\subset H\) pour tout \(x\) ; en appliquant à \(x^{-1}\) on obtient
l'inclusion inverse, d'où l'égalité.</p>
<p><strong>Cas abélien.</strong> \(xhx^{-1}=hxx^{-1}=h\in H\) immédiatement.</p>
""") + r"""

""" + retenir("Proposition", r"""
<p>\(\Ker f\) est toujours distingué.</p>
""") + demo(r"""
<p>Soient \(x\in G\) et \(h\in\Ker f\). Alors</p>
\[f(xhx^{-1})=f(x)f(h)f(x)^{-1}=f(x)\,e'\,f(x)^{-1}=e',\]
<p>donc \(xhx^{-1}\in\Ker f\). Ceci valant pour tout \(x\), \(\Ker f\trianglelefteq G\).</p>
""") + r"""

""" + prof(r"""
<p>Tous les groupes du master étant abéliens (\(\Znz\), \(\Fq^{\times}\), \(E(\Fq)\)), la
question « distingué ou non » ne se pose jamais en cryptographie à clé publique. Elle redevient
centrale dès qu'on travaille avec des groupes de permutations — en cryptanalyse d'AES, ou dans
l'étude du groupe de Galois d'un corps fini.</p>
""") + r"""

""" + code(r"""
# Projection canonique Z -> Z/nZ : le morphisme le plus utilise du master
n = 12
pi = lambda x: x % n
print(all(pi(x + y) == (pi(x) + pi(y)) % n for x in range(-20, 20) for y in range(-20, 20)))
print("noyau :", [x for x in range(-24, 25) if pi(x) == 0])

# Reduction d'un groupe cyclique dans un sous-groupe : l'idee de Pohlig-Hellman
p, g = 31, 3                   # |(Z/31Z)*| = 30 = 2 * 3 * 5
ordre_g = next(k for k in range(1, 31) if pow(g, k, p) == 1)
print("ordre de g :", ordre_g)
for q in (2, 3, 5):
    proj = pow(g, ordre_g // q, p)
    print("  sous-groupe d'ordre", q, ":",
          sorted({pow(proj, k, p) for k in range(q)}))
""", "python",
"""True
noyau : [-24, -12, 0, 12, 24]
ordre de g : 30
  sous-groupe d'ordre 2 : [1, 30]
  sous-groupe d'ordre 3 : [1, 5, 25]
  sous-groupe d'ordre 5 : [1, 2, 4, 8, 16]""",
"Morphisme, noyau, et la décomposition qu'exploite Pohlig-Hellman") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soit \(f:\Znz\to\Znz,\ x\mapsto x^{2}\). Montrer que c'est un morphisme, déterminer son noyau
pour \(n=p\) premier impair, et en déduire le nombre de carrés dans \(\Fp^{\times}\).</p>
""", r"""
<p><u>Morphisme.</u> \(f(xy)=(xy)^2=x^2y^2=f(x)f(y)\), en utilisant la commutativité.</p>
<p><u>Noyau.</u> \(\Ker f=\{x\ ;\ x^2=1\}\). Dans le corps \(\Fp\), l'équation
\((x-1)(x+1)=0\) a exactement deux solutions, \(x=\pm1\), distinctes car \(p\) est impair.</p>
<p>Donc \(\Ker f=\{1,-1\}\), de cardinal 2.</p>
<p><u>Nombre de carrés.</u> Les classes modulo \(\Ker f\) ont toutes 2 éléments (Lagrange), donc</p>
\[|\Img f|=\frac{|\Fp^{\times}|}{|\Ker f|}=\frac{p-1}{2}.\]
<p>Il y a donc <u>\(\frac{p-1}{2}\) carrés non nuls</u> modulo \(p\) : exactement la moitié.</p>
""", r"""<p>C'est le comptage utilisé dans la preuve du critère d'Euler (nœud « Résidus
quadratiques »). On le retrouve ici comme simple conséquence du premier théorème
d'isomorphisme.</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(G\) un groupe et \(H\le G\) d'indice 2. Montrer que \(H\) est distingué.</p>
""", r"""
<p>Indice 2 signifie qu'il y a exactement deux classes à gauche : \(H\) et son complémentaire
\(G\setminus H\). De même pour les classes à droite.</p>
<p>Soit \(x\in G\). Deux cas :</p>
<ul>
<li><u>\(x\in H\)</u> : alors \(xH=H=Hx\).</li>
<li><u>\(x\notin H\)</u> : la classe \(xH\) est différente de \(H\) (sinon \(x\in H\)), donc
\(xH=G\setminus H\). De même \(Hx\neq H\) donc \(Hx=G\setminus H\).</li>
</ul>
<p>Dans les deux cas \(xH=Hx\), donc <u>\(H\trianglelefteq G\)</u>.</p>
""", r"""<p>Exemple : le groupe alterné \(A_n\) est d'indice 2 dans \(S_n\), il est donc toujours
distingué. Et le sous-groupe des carrés de \(\Fp^{\times}\) est d'indice 2, ce qui redonne la
multiplicativité du symbole de Legendre.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["grp-isomorphismes"] = r"""
<p class="lead">Le premier théorème d'isomorphisme est l'outil qui permet d'<em>identifier</em>
un quotient au lieu de le décrire élément par élément. C'est lui qui montre que deux groupes
d'apparence très différente portent le même problème de logarithme discret.</p>

<h3>Le théorème</h3>
""" + retenir("Premier théorème d'isomorphisme", r"""
<p>Soit \(f:G\to G'\) un morphisme de groupes. Alors</p>
\[G/\Ker f\ \simeq\ \Img f.\]
<p>Plus précisément, \(\bar f:\overline{x}\mapsto f(x)\) est un isomorphisme bien défini de
\(G/\Ker f\) sur \(\Img f\).</p>
""") + demo(r"""
<p>Posons \(K=\Ker f\), qui est distingué (nœud précédent), donc \(G/K\) est bien un groupe.</p>
<p><strong>\(\bar f\) est bien définie.</strong> Si \(\overline{x}=\overline{y}\), alors
\(xy^{-1}\in K\), donc \(f(xy^{-1})=e'\), c'est-à-dire \(f(x)=f(y)\). Le choix du représentant
n'influe pas.</p>
<p><strong>C'est un morphisme.</strong>
\(\bar f(\overline{x}\,\overline{y})=\bar f(\overline{xy})=f(xy)=f(x)f(y)
=\bar f(\overline{x})\bar f(\overline{y})\).</p>
<p><strong>Injective.</strong> Si \(\bar f(\overline{x})=e'\), alors \(f(x)=e'\) donc \(x\in K\),
c'est-à-dire \(\overline{x}=\overline{e}\). Le noyau de \(\bar f\) est trivial.</p>
<p><strong>Surjective sur \(\Img f\).</strong> Immédiat : tout élément de \(\Img f\) s'écrit
\(f(x)=\bar f(\overline{x})\).</p>
""") + r"""

""" + retenir("Corollaire (comptage)", r"""
<p>Si \(G\) est fini :</p>
\[|G|=|\Ker f|\cdot|\Img f|.\]
""") + demo(r"""
<p>Par Lagrange, \(|G/\Ker f|=\dfrac{|G|}{|\Ker f|}\). Le théorème donne
\(|G/\Ker f|=|\Img f|\), d'où le résultat.</p>
""") + r"""

""" + prof(r"""
<p>C'est le théorème du rang de l'algèbre linéaire, dans un cadre plus général :
\(\dim E=\dim\Ker u+\dim\Img u\). On le retrouvera encore pour les anneaux et les modules.
Retenir le schéma plutôt que les trois énoncés séparés.</p>
""") + r"""

<h3>Trois usages concrets</h3>

""" + retenir("Application 1 — identifier un quotient", r"""
<p>\(\Z/n\Z\simeq\) le groupe des racines \(n\)-ièmes de l'unité dans \(\C^{\times}\).</p>
""") + demo(r"""
<p>Considérons \(f:\Z\to\C^{\times},\ k\mapsto e^{2i\pi k/n}\).</p>
<p>C'est un morphisme de \((\Z,+)\) dans \((\C^{\times},\times)\) car
\(f(k+l)=e^{2i\pi(k+l)/n}=f(k)f(l)\).</p>
<p>Son noyau est \(\{k\ ;\ e^{2i\pi k/n}=1\}=\{k\ ;\ n\mid k\}=n\Z\), et son image est
\(\mu_n=\{z\ ;\ z^{n}=1\}\).</p>
<p>Le théorème donne \(\Z/n\Z\simeq\mu_n\).</p>
""") + r"""

""" + retenir("Application 2 — le logarithme discret est un isomorphisme", r"""
<p>Si \(G=\langle g\rangle\) est cyclique d'ordre \(n\), l'application
\(\log_g:G\to\Z/n\Z\) est un isomorphisme.</p>
""") + demo(r"""
<p>C'est l'inverse de l'isomorphisme \(\psi:\Z/n\Z\to G,\ \bar k\mapsto g^{k}\) construit au
nœud « Groupes cycliques et générateurs ».</p>
<p>La propriété de morphisme s'écrit \(\log_g(xy)=\log_g(x)+\log_g(y)\) : c'est exactement la
règle du logarithme, transposée dans un groupe fini.</p>
""") + r"""

""" + prof(r"""
<p>Ce résultat est troublant la première fois : <em>tout</em> groupe cyclique d'ordre \(n\) est
isomorphe à \(\Z/n\Z\), où le logarithme discret est trivial (c'est une division !).
La difficulté n'est donc pas dans la <strong>structure</strong> du groupe, mais dans sa
<strong>représentation</strong> : l'isomorphisme existe, mais le calculer est précisément le
problème qu'on suppose difficile. Toute la cryptographie à clé publique vit dans cet écart
entre « exister » et « savoir calculer ».</p>
""") + r"""

""" + retenir("Application 3 — la signature d'une permutation", r"""
<p>\(\varepsilon:S_n\to\{\pm1\}\) est un morphisme surjectif pour \(n\ge2\), de noyau \(A_n\).
Donc \(S_n/A_n\simeq\{\pm1\}\) et \(|A_n|=n!/2\).</p>
""") + r"""

""" + code(r"""
# Le logarithme discret est bien un morphisme... quand on sait le calculer
p, g = 31, 3
dlog = {pow(g, k, p): k for k in range(30)}

x, y = 7, 11
print(dlog[x], dlog[y], dlog[x*y % p])
print((dlog[x] + dlog[y]) % 30)      # log(xy) = log(x) + log(y) mod 30

# |G| = |Ker| x |Im| sur le morphisme carre
carre = lambda a: a*a % p
noyau = [a for a in range(1, p) if carre(a) == 1]
image = sorted({carre(a) for a in range(1, p)})
print(len(noyau), len(image), len(noyau) * len(image))
""", "python",
"""28 23 21
21
2 15 30""",
"Le logarithme discret comme morphisme, et le comptage") + r"""

<p>\(\log(7)=28\), \(\log(11)=23\), et \(28+23=51\equiv21 \pmod{30}\) : c'est bien
\(\log(7\times11)\). Le logarithme discret transforme la multiplication en addition — exactement
comme le logarithme réel.</p>

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soit \(f:\R\to\C^{\times},\ t\mapsto e^{it}\). Déterminer \(\Ker f\) et \(\Img f\), puis
identifier \(\R/\Ker f\).</p>
""", r"""
<p><u>Morphisme.</u> \(f(s+t)=e^{i(s+t)}=e^{is}e^{it}=f(s)f(t)\) : morphisme de \((\R,+)\) dans
\((\C^{\times},\times)\).</p>
<p><u>Noyau.</u> \(e^{it}=1 \iff t\in2\pi\Z\), donc \(\Ker f=2\pi\Z\).</p>
<p><u>Image.</u> \(\Img f=\{z\in\C\ ;\ |z|=1\}=\mathbb U\), le cercle unité.</p>
<p><u>Identification.</u> Le théorème donne</p>
\[\R/2\pi\Z\ \simeq\ \mathbb U.\]
<p>C'est la formalisation de « l'angle est défini modulo \(2\pi\) ».</p>
""", r"""<p>On avait rencontré \(\R/\Z\) à l'exercice du nœud « Relations d'équivalence et
quotients ». On sait maintenant le <em>nommer</em> : c'est le cercle, et l'isomorphisme est
explicite.</p>""") + r"""

""" + exo(2, r"""
<p>Soient \(m,n\ge1\) avec \(d=\pgcd(m,n)\). Déterminer l'image du morphisme
\(f:\Z/n\Z\to\Z/n\Z,\ \bar x\mapsto \overline{mx}\), ainsi que son noyau. Vérifier le corollaire
de comptage.</p>
""", r"""
<p><u>Bien défini.</u> Si \(x\equiv x'\pmod n\), alors \(mx\equiv mx'\pmod n\). ✓</p>
<p><u>Image.</u> \(\Img f=\{\overline{mx}\ ;\ x\in\Z\}=m\Z/n\Z\). Or l'ensemble
\(\{mx+ny\}\) est l'ensemble des multiples de \(d=\pgcd(m,n)\) (Bézout), donc</p>
\[\Img f=d\,\Z/n\Z=\{\bar0,\bar d,\overline{2d},\dots\},\quad\text{de cardinal } n/d.\]
<p><u>Noyau.</u> \(\overline{mx}=\bar0 \iff n\mid mx \iff \frac nd \mid \frac md x\). Comme
\(\pgcd(\frac nd,\frac md)=1\), Gauss donne \(\frac nd\mid x\).</p>
<p>Donc \(\Ker f=\frac nd\Z/n\Z\), de cardinal \(d\).</p>
<p><u>Comptage.</u> \(|\Ker f|\cdot|\Img f|=d\times\frac nd=n=|\Z/n\Z\)| ✓</p>
""", r"""<p>On retrouve au passage le résultat du nœud « Congruences » : \(\bar m\) est inversible
(donc \(f\) bijective) exactement quand \(d=1\).</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["grp-abeliens"] = r"""
<p class="lead">Ce théorème dit à quoi ressemble <em>exactement</em> n'importe quel groupe
abélien fini. Appliqué au groupe des points d'une courbe elliptique, il donne sa forme
\(\Z/n_1\Z\times\Z/n_2\Z\) — et c'est cette forme qui décide de la sécurité de la courbe.</p>

<h3>L'énoncé</h3>
""" + retenir("Théorème de structure", r"""
<p>Tout groupe abélien fini \(G\) est isomorphe à un produit de groupes cycliques. Deux
présentations équivalentes :</p>
<p><strong>Facteurs invariants.</strong> Il existe une unique suite \(n_1\mid n_2\mid\dots\mid n_k\)
(avec \(n_1>1\)) telle que</p>
\[G\simeq \Z/n_1\Z\times\Z/n_2\Z\times\dots\times\Z/n_k\Z.\]
<p><strong>Diviseurs élémentaires.</strong> \(G\) est isomorphe à un produit de
\(\Z/p^{\alpha}\Z\) avec \(p\) premier, et cette décomposition est unique à l'ordre près.</p>
""") + r"""

<p>La démonstration complète se fait au niveau 2, comme cas particulier du théorème de structure
des modules sur un anneau principal (\(\Z\) en est un) : un groupe abélien <em>est</em> un
\(\Z\)-module. On admet ici le résultat et on apprend à s'en servir.</p>

<h3>Passer d'une présentation à l'autre</h3>
<p>Le pont entre les deux est le théorème chinois : \(\Z/mn\Z\simeq\Z/m\Z\times\Z/n\Z\)
dès que \(\pgcd(m,n)=1\).</p>

""" + retenir("Méthode", r"""
<p>Des diviseurs élémentaires aux facteurs invariants : on range les puissances de chaque
premier par ordre décroissant en colonnes, puis on multiplie <strong>ligne par ligne</strong>
en partant de la droite.</p>
""") + r"""

<p>Exemple. Soit \(G\simeq \Z/4\Z\times\Z/2\Z\times\Z/9\Z\times\Z/3\Z\times\Z/5\Z\).</p>
<div class="table-wrap"><table>
<thead><tr><th>\(p\)</th><th></th><th></th></tr></thead><tbody>
<tr><td>2</td><td>\(2^2=4\)</td><td>\(2^1=2\)</td></tr>
<tr><td>3</td><td>\(3^2=9\)</td><td>\(3^1=3\)</td></tr>
<tr><td>5</td><td>\(5^1=5\)</td><td>—</td></tr>
<tr><th>produit</th><th>\(4\cdot9\cdot5=180\)</th><th>\(2\cdot3=6\)</th></tr>
</tbody></table></div>
<p>Donc \(G\simeq\Z/6\Z\times\Z/180\Z\), avec bien \(6\mid180\). Vérification des ordres :
\(6\times180=1080=4\times2\times9\times3\times5\) ✓</p>

<h3>Combien de groupes abéliens d'ordre donné ?</h3>
""" + retenir("Corollaire", r"""
<p>Le nombre de groupes abéliens d'ordre \(n=\prod p_i^{\alpha_i}\), à isomorphisme près, est</p>
\[\prod_i P(\alpha_i),\]
<p>où \(P(\alpha)\) est le nombre de <strong>partitions</strong> de l'entier \(\alpha\).</p>
""") + demo(r"""
<p>Par le théorème chinois, \(G\) se décompose en produit de ses \(p\)-composantes, et deux
groupes sont isomorphes si et seulement si leurs \(p\)-composantes le sont. Le compte est donc
multiplicatif sur les \(p_i\).</p>
<p>Pour un \(p\) fixé, un groupe abélien d'ordre \(p^{\alpha}\) s'écrit de façon unique
\(\Z/p^{\beta_1}\Z\times\dots\times\Z/p^{\beta_r}\Z\) avec
\(\beta_1\ge\dots\ge\beta_r\ge1\) et \(\sum\beta_j=\alpha\).</p>
<p>Une telle suite décroissante de sommes \(\alpha\) est exactement une partition de \(\alpha\).
Il y en a \(P(\alpha)\).</p>
""") + r"""

<p>Par exemple pour \(n=8=2^3\) : \(P(3)=3\) partitions (\(3\), \(2+1\), \(1+1+1\)), donc trois
groupes abéliens d'ordre 8 :</p>
\[\Z/8\Z,\qquad \Z/4\Z\times\Z/2\Z,\qquad \Z/2\Z\times\Z/2\Z\times\Z/2\Z.\]

""" + code(r"""
from itertools import product

def partitions(n, maxi=None):
    if maxi is None: maxi = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxi), 0, -1):
        for reste in partitions(n - k, k):
            yield (k,) + reste

for a in range(1, 7):
    print(a, len(list(partitions(a))), list(partitions(a))[:4])

# Les trois groupes abeliens d'ordre 8
print([tuple(2**b for b in p) for p in partitions(3)])
""", "python",
"""1 1 [(1,)]
2 2 [(2,), (1, 1)]
3 3 [(3,), (2, 1), (1, 1, 1)]
4 5 [(4,), (3, 1), (2, 2), (2, 1, 1)]
5 7 [(5,), (4, 1), (3, 2), (3, 1, 1)]
6 11 [(6,), (5, 1), (4, 2), (4, 1, 1)]
[(8,), (4, 2), (2, 2, 2)]""",
"Les partitions comptent les groupes abéliens") + r"""

<h3>L'application : le groupe d'une courbe elliptique</h3>

""" + retenir("Théorème (admis ici, démontré au niveau 4)", r"""
<p>Pour une courbe elliptique \(E\) sur \(\Fq\), le groupe des points vérifie</p>
\[E(\Fq)\ \simeq\ \Z/n_1\Z\times\Z/n_2\Z \qquad\text{avec } n_1\mid n_2 \text{ et } n_1\mid q-1.\]
<p>Il y a donc <strong>au plus deux facteurs</strong> : c'est une contrainte très forte, et c'est
ce qui rend les courbes elliptiques intéressantes.</p>
""") + r"""

""" + prof(r"""
<p>Le cas favorable est \(n_1=1\) : le groupe est alors cyclique d'ordre \(n_2\), et si \(n_2\)
est premier, aucune décomposition à la Pohlig-Hellman n'est possible. C'est pourquoi les courbes
standard (P-256, Curve25519) publient leur <em>cofacteur</em> \(h\) et l'ordre premier \(n\) du
sous-groupe utilisé : \(|E(\Fq)|=h\cdot n\) avec \(h\) tout petit (1, 4 ou 8).</p>
""") + r"""

""" + code(r"""
E = EllipticCurve(GF(1009), [1, 3])
print(E.order(), E.abelian_group().invariants())

# La courbe standard P-256 : groupe cyclique d'ordre premier
p = 2^256 - 2^224 + 2^192 + 2^96 - 1
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
P256 = EllipticCurve(GF(p), [a, b])
n = P256.order()
print(n.is_prime())                 # cofacteur 1 : pas de Pohlig-Hellman
""", "sagemath", "1060 (2, 530)\nTrue",
"La structure du groupe décide de la sécurité") + r"""

<p>La première courbe a 1060 points et son groupe est \(\Z/2\Z\times\Z/530\Z\) : deux facteurs,
avec bien \(2\mid530\) et \(2\mid 1009-1\). Elle n'est donc pas cyclique. P-256, elle, a un
ordre premier : son groupe est cyclique et n'offre aucune décomposition.</p>

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Lister tous les groupes abéliens d'ordre 360, à isomorphisme près, sous forme de facteurs
invariants.</p>
""", r"""
<p>\(360=2^3\times3^2\times5\).</p>
<p>Nombre de groupes : \(P(3)\times P(2)\times P(1)=3\times2\times1=\underline{6}\).</p>
<p>Les diviseurs élémentaires possibles :</p>
<div class="table-wrap"><table>
<thead><tr><th>2-part</th><th>3-part</th><th>5-part</th><th>Facteurs invariants</th></tr></thead>
<tbody>
<tr><td>8</td><td>9</td><td>5</td><td>\(\Z/360\Z\)</td></tr>
<tr><td>8</td><td>3,3</td><td>5</td><td>\(\Z/3\Z\times\Z/120\Z\)</td></tr>
<tr><td>4,2</td><td>9</td><td>5</td><td>\(\Z/2\Z\times\Z/180\Z\)</td></tr>
<tr><td>4,2</td><td>3,3</td><td>5</td><td>\(\Z/6\Z\times\Z/60\Z\)</td></tr>
<tr><td>2,2,2</td><td>9</td><td>5</td><td>\(\Z/2\Z\times\Z/2\Z\times\Z/90\Z\)</td></tr>
<tr><td>2,2,2</td><td>3,3</td><td>5</td><td>\(\Z/2\Z\times\Z/6\Z\times\Z/30\Z\)</td></tr>
</tbody></table></div>
<p>Vérification sur la dernière ligne : \(2\times6\times30=360\) ✓ et \(2\mid6\mid30\) ✓</p>
""", r"""<p>Méthode : on range les puissances de chaque premier en colonnes alignées à droite,
puis on multiplie ligne par ligne. La colonne la plus à droite donne \(n_1\), la plus à gauche
donne \(n_k\).</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(G\) un groupe abélien fini d'ordre \(n\). Montrer que \(G\) est cyclique si et
seulement si, pour tout diviseur \(d\mid n\), l'équation \(x^{d}=e\) a au plus \(d\) solutions
dans \(G\). En déduire que \(\Fq^{\times}\) est cyclique.</p>
""", r"""
<p><u>(\(\Rightarrow\))</u> Si \(G=\langle g\rangle\) est cyclique d'ordre \(n\), on a vu
(nœud « Groupes cycliques ») que les solutions de \(x^{d}=e\) forment l'unique sous-groupe
d'ordre \(d\) : il y en a exactement \(d\).</p>
<p><u>(\(\Leftarrow\))</u> Écrivons \(G\simeq\Z/n_1\Z\times\dots\times\Z/n_k\Z\) avec
\(n_1\mid\dots\mid n_k\).</p>
<p>Si \(k\ge2\), posons \(d=n_1\). Tout élément de \(\Z/n_1\Z\times\Z/n_2\Z\) tué par \(n_1\)
donne une solution, et comme \(n_1\mid n_2\), le sous-groupe de \(n_1\)-torsion contient
\(n_1\times n_1=n_1^2>n_1=d\) éléments.</p>
<p>Cela contredit l'hypothèse. Donc \(k=1\) et \(G\simeq\Z/n\Z\) est cyclique.</p>
<p><u>Application à \(\Fq^{\times}\).</u> C'est un groupe abélien d'ordre \(q-1\). Pour
\(d\mid q-1\), les solutions de \(x^{d}=1\) sont les racines du polynôme \(X^{d}-1\) dans le
<strong>corps</strong> \(\Fq\). Un polynôme de degré \(d\) sur un corps a au plus \(d\) racines.</p>
<p>Le critère s'applique : <u>\(\Fq^{\times}\) est cyclique</u>.</p>
""", r"""<p>C'est la démonstration standard de la cyclicité de \(\Fq^{\times}\), qu'on reprendra
au nœud « Cyclicité de 𝔽q* et éléments primitifs ». Tout repose sur « un polynôme de degré
\(d\) sur un corps a au plus \(d\) racines » — un énoncé faux dans \(\Z/n\Z\) composé, et c'est
pourquoi \(\Znz\) n'est pas toujours cyclique.</p>""")


# ═════════════════════════════════════════════════════════════════════════════
# Algèbre linéaire
# ═════════════════════════════════════════════════════════════════════════════

CORPS["lin-ev"] = r"""
<p class="lead">L'algèbre linéaire de licence se fait sur \(\R\) ou \(\C\). En master, le corps
de base est \(\Fq\) — et presque tout survit, à une exception près qui change tout : on peut
compter les vecteurs.</p>

<h3>Ce qui ne change pas</h3>
""" + retenir("Définition", r"""
<p>Un \(K\)-espace vectoriel est un groupe abélien \((E,+)\) muni d'une loi externe
\(K\times E\to E\) vérifiant, pour \(\lambda,\mu\in K\) et \(u,v\in E\) :</p>
\[\lambda(u+v)=\lambda u+\lambda v,\quad (\lambda+\mu)u=\lambda u+\mu u,\quad
\lambda(\mu u)=(\lambda\mu)u,\quad 1\cdot u=u.\]
<p>Toute la théorie — familles libres, génératrices, bases, dimension, théorème du rang — est
valable sur un corps <strong>quelconque</strong>, y compris fini.</p>
""") + r"""

<h3>Ce qui change : on peut compter</h3>
""" + retenir("Théorème (cardinal)", r"""
<p>Si \(E\) est un \(\Fq\)-espace vectoriel de dimension \(n\), alors</p>
\[\Card E=q^{n}.\]
<p>Le nombre de bases de \(E\) est</p>
\[(q^{n}-1)(q^{n}-q)(q^{n}-q^{2})\cdots(q^{n}-q^{n-1}).\]
""") + demo(r"""
<p><strong>Cardinal.</strong> Soit \((e_1,\dots,e_n)\) une base. Tout vecteur s'écrit de façon
<em>unique</em> \(\sum\lambda_ie_i\) avec \(\lambda_i\in\Fq\). Il y a \(q\) choix indépendants
pour chaque coordonnée, soit \(q^{n}\) vecteurs.</p>
<p><strong>Bases.</strong> On construit une base vecteur par vecteur.</p>
<ul>
<li>\(v_1\) doit être non nul : \(q^{n}-1\) choix ;</li>
<li>\(v_2\) ne doit pas être dans \(\Vect(v_1)\), qui a \(q\) éléments : \(q^{n}-q\) choix ;</li>
<li>plus généralement \(v_{k+1}\notin\Vect(v_1,\dots,v_k)\), sous-espace de dimension \(k\)
donc de cardinal \(q^{k}\) : \(q^{n}-q^{k}\) choix.</li>
</ul>
<p>Le produit de ces choix donne la formule.</p>
""") + r"""

""" + prof(r"""
<p>Ce comptage est le cœur de la théorie des codes : un code linéaire \([n,k]\) sur \(\Fq\) est
un sous-espace de dimension \(k\) de \(\Fq^{n}\), il contient donc exactement \(q^{k}\) mots.
Le <em>rendement</em> \(k/n\) mesure l'information transmise par symbole.</p>
""") + r"""

<h3>Une subtilité propre à la caractéristique p</h3>
""" + retenir("Attention", r"""
<p>Dans \(\F_2\), on a \(u+u=2u=0\) pour tout vecteur. Plus généralement, dans un espace sur
\(\Fp\), \(\underbrace{u+\dots+u}_{p}=0\).</p>
<p>Conséquences : il n'y a pas de notion d'« orientation », la forme bilinéaire
\(\langle u,u\rangle\) peut être nulle pour \(u\neq0\) (vecteurs <em>isotropes</em>), et
un sous-espace peut être égal à son orthogonal.</p>
""") + r"""

""" + code(r"""
# Un code lineaire [7,4] sur F2 : le code de Hamming
G = [[1,0,0,0,0,1,1],
     [0,1,0,0,1,0,1],
     [0,0,1,0,1,1,0],
     [0,0,0,1,1,1,1]]

def combinaison(coeffs, G):
    n = len(G[0])
    return tuple(sum(c*g[j] for c, g in zip(coeffs, G)) % 2 for j in range(n))

from itertools import product
code = sorted({combinaison(c, G) for c in product([0,1], repeat=4)})
print(len(code), "mots =", 2**4)
print(code[1], code[-1])

# distance minimale = plus petit poids d'un mot non nul (code lineaire)
poids = lambda m: sum(m)
print("distance minimale :", min(poids(m) for m in code if any(m)))
""", "python",
"""16 mots = 16
(0, 0, 0, 1, 1, 1, 1) (1, 1, 1, 1, 1, 1, 1)
distance minimale : 3""",
"Un espace vectoriel sur 𝔽₂, qui est un code correcteur") + r"""

<p>\(2^4=16\) mots dans \(\F_2^{7}\) : le code occupe une fraction \(16/128=1/8\) de l'espace.
Sa distance minimale 3 lui permet de corriger une erreur — on le démontrera au niveau 4.</p>

""" + code(r"""
V = VectorSpace(GF(2), 7)
print(V.cardinality())
C = codes.HammingCode(GF(2), 3)
print(C.dimension(), C.length(), C.minimum_distance(), C.cardinality())
# Nombre de bases de F_2^3
q, n = 2, 3
print(prod(q^n - q^k for k in range(n)))
""", "sagemath", "128\n4 7 3 16\n168", "Vérification, et le comptage des bases") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Combien y a-t-il de sous-espaces de dimension 1 dans \(\F_q^{n}\) ? Et de dimension \(n-1\) ?</p>
""", r"""
<p><u>Dimension 1.</u> Une droite est engendrée par un vecteur non nul, et deux vecteurs
non nuls \(u,v\) engendrent la même droite si et seulement si \(v=\lambda u\) avec
\(\lambda\in\Fq^{\times}\).</p>
<p>Il y a \(q^{n}-1\) vecteurs non nuls, regroupés par paquets de \(q-1\) :</p>
\[\#\{\text{droites}\}=\frac{q^{n}-1}{q-1}=1+q+q^2+\dots+q^{n-1}.\]
<p><u>Dimension \(n-1\).</u> Un hyperplan est le noyau d'une forme linéaire non nulle, et deux
formes proportionnelles ont même noyau. L'espace dual \((\Fq^{n})^{*}\) étant aussi de dimension
\(n\), le même comptage donne</p>
\[\#\{\text{hyperplans}\}=\frac{q^{n}-1}{q-1}.\]
<p>Il y a donc <u>autant de droites que d'hyperplans</u>.</p>
""", r"""<p>Ce nombre \(\frac{q^n-1}{q-1}\) est le cardinal de l'espace projectif
\(\P^{n-1}(\Fq)\). La dualité droites/hyperplans est le phénomène qui, au niveau 4, donnera
le code dual et la matrice de contrôle de parité.</p>""") + r"""

""" + exo(2, r"""
<p>Dans \(\F_2^{n}\), on munit l'espace du produit scalaire usuel
\(\langle u,v\rangle=\sum u_iv_i\). Donner un exemple de vecteur isotrope non nul, puis un
sous-espace \(C\) de \(\F_2^{4}\) tel que \(C=C^{\perp}\).</p>
""", r"""
<p><u>Vecteur isotrope.</u> Prenons \(u=(1,1,0,0)\). Alors</p>
\[\langle u,u\rangle=1+1+0+0=2\equiv0\pmod2.\]
<p>\(u\) est orthogonal à lui-même bien qu'il soit non nul — impossible sur \(\R\).</p>
<p><u>Sous-espace auto-dual.</u> Posons \(C=\Vect\big((1,1,0,0),(0,0,1,1)\big)\), donc</p>
\[C=\{(0,0,0,0),(1,1,0,0),(0,0,1,1),(1,1,1,1)\},\quad \dim C=2.\]
<p>Vérifions \(C\subset C^{\perp}\) : les produits scalaires des générateurs valent
\(\langle(1,1,0,0),(1,1,0,0)\rangle=0\), \(\langle(1,1,0,0),(0,0,1,1)\rangle=0\),
\(\langle(0,0,1,1),(0,0,1,1)\rangle=0\). Donc tout \(C\) est orthogonal à tout \(C\).</p>
<p>Par la formule \(\dim C+\dim C^{\perp}=4\), on a \(\dim C^{\perp}=2=\dim C\), et l'inclusion
devient une égalité : <u>\(C=C^{\perp}\)</u>.</p>
""", r"""<p>Ces codes auto-duaux sont très étudiés : ils interviennent en cryptographie quantique
(codes CSS, correction d'erreurs quantiques) justement parce que l'isotropie, pathologique sur
\(\R\), devient une ressource sur \(\F_2\).</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["lin-matrices"] = r"""
<p class="lead">Le pivot de Gauss sur \(\Fq\) est l'algorithme le plus utilisé du master après
Euclide : il décode les codes linéaires, résout les systèmes de la cryptanalyse linéaire, et
calcule les rangs partout. Sur \(\F_2\), il devient d'une simplicité redoutable — il n'y a plus
de division.</p>

<h3>Le pivot, sur un corps quelconque</h3>
""" + retenir("Théorème", r"""
<p>Toute matrice \(A\in\mathcal M_{m,n}(K)\) peut être transformée, par opérations élémentaires
sur les lignes, en une unique matrice <strong>échelonnée réduite</strong>.</p>
<p>Le nombre de pivots obtenus est le <strong>rang</strong> de \(A\) ; il ne dépend pas des
opérations effectuées.</p>
<p>Coût : \(O(mn\min(m,n))\) opérations dans \(K\).</p>
""") + r"""

""" + retenir("Théorème du rang", r"""
<p>Pour \(u:E\to F\) linéaire avec \(E\) de dimension finie :</p>
\[\dim E=\dim\Ker u+\rg u.\]
""") + demo(r"""
<p>Soit \((v_1,\dots,v_k)\) une base de \(\Ker u\), complétée en une base
\((v_1,\dots,v_k,w_1,\dots,w_r)\) de \(E\) (théorème de la base incomplète). On a
\(\dim E=k+r\).</p>
<p>Montrons que \(\big(u(w_1),\dots,u(w_r)\big)\) est une base de \(\Img u\).</p>
<p><strong>Génératrice.</strong> Soit \(y=u(x)\in\Img u\). Décomposons
\(x=\sum\alpha_iv_i+\sum\beta_jw_j\). Comme \(u(v_i)=0\),</p>
\[y=u(x)=\sum_j\beta_j\,u(w_j).\]
<p><strong>Libre.</strong> Supposons \(\sum\beta_ju(w_j)=0\), c'est-à-dire
\(u\big(\sum\beta_jw_j\big)=0\). Alors \(\sum\beta_jw_j\in\Ker u\), donc il s'écrit
\(\sum\alpha_iv_i\). D'où</p>
\[\sum_i\alpha_iv_i-\sum_j\beta_jw_j=0.\]
<p>La famille \((v_i,w_j)\) étant une base de \(E\), tous les coefficients sont nuls ; en
particulier \(\beta_j=0\) pour tout \(j\).</p>
<p>Donc \(\rg u=r\) et \(\dim E=k+r=\dim\Ker u+\rg u\).</p>
""") + r"""

""" + prof(r"""
<p>Ce théorème est le premier théorème d'isomorphisme (nœud « Les théorèmes d'isomorphisme »)
appliqué aux espaces vectoriels : \(E/\Ker u\simeq\Img u\), et on prend les dimensions. Dès
qu'on a compris une version, les autres sont gratuites.</p>
""") + r"""

<h3>Le pivot sur \(\F_2\)</h3>
<p>Sur \(\F_2\), les seuls scalaires sont 0 et 1 : multiplier une ligne ne sert à rien, et
« ajouter \(\lambda L_i\) à \(L_j\) » devient un simple XOR. Une ligne se représente alors par
un entier, et l'opération élémentaire tient en un `^=`.</p>

""" + code(r"""
def rang_f2(lignes, n):
    "Pivot de Gauss sur F2. Chaque ligne est un entier dont les bits sont les coefficients."
    lignes, rang = list(lignes), 0
    for col in reversed(range(n)):               # on traite les colonnes de gauche a droite
        bit = 1 << col
        pivot = next((i for i in range(rang, len(lignes)) if lignes[i] & bit), None)
        if pivot is None:
            continue
        lignes[rang], lignes[pivot] = lignes[pivot], lignes[rang]
        for i in range(len(lignes)):
            if i != rang and lignes[i] & bit:
                lignes[i] ^= lignes[rang]        # l'operation elementaire : un XOR
        rang += 1
    return rang, lignes

# La matrice generatrice du code de Hamming [7,4], en binaire
G = [0b1000011, 0b0100101, 0b0010110, 0b0001111]
r, ech = rang_f2(G, 7)
print("rang :", r)
print([format(l, '07b') for l in ech])

# Une famille liee : la 4e ligne est la somme des trois premieres
H = [0b1100, 0b1010, 0b1001, 0b1111]
print("rang :", rang_f2(H, 4)[0], "sur 4 lignes")
""", "python",
"""rang : 4
['1000011', '0100101', '0010110', '0001111']
rang : 3 sur 4 lignes""",
"Le pivot de Gauss sur 𝔽₂, en XOR") + r"""

<p>Sur \(\F_2\), le pivot de Gauss d'une matrice \(n\times n\) coûte \(O(n^3)\) opérations
<em>sur des mots machine entiers</em> : on traite 64 colonnes par instruction. C'est pourquoi
les attaques par décodage sur \(\F_2\) sont redoutablement efficaces en pratique.</p>

<h3>Résoudre un système</h3>
""" + retenir("Structure des solutions", r"""
<p>L'ensemble des solutions de \(AX=B\) est :</p>
<ul>
<li><strong>vide</strong> si \(\rg(A)\neq\rg(A|B)\) ;</li>
<li>sinon, \(X_0+\Ker A\), un sous-espace affine de dimension \(n-\rg A\).</li>
</ul>
<p>Sur \(\Fq\), il y a donc \(0\) ou exactement \(q^{\,n-\rg A}\) solutions.</p>
""") + demo(r"""
<p>Supposons une solution \(X_0\) connue. Alors</p>
\[AX=B \iff AX=AX_0 \iff A(X-X_0)=0 \iff X-X_0\in\Ker A.\]
<p>L'ensemble des solutions est donc \(X_0+\Ker A\).</p>
<p>Son cardinal est celui de \(\Ker A\), qui est un espace vectoriel de dimension
\(n-\rg A\) par le théorème du rang, donc de cardinal \(q^{\,n-\rg A}\).</p>
""") + r"""

""" + code(r"""
A = matrix(GF(2), [[1,0,1,1],[0,1,1,0],[1,1,0,1]])
print(A.rank(), A.right_kernel().dimension())
print(A.echelon_form())
b = vector(GF(2), [1,0,1])
print(A.solve_right(b))
print(len(A.right_kernel().list()), "solutions")
""", "sagemath",
"""2 2
[1 0 1 1]
[0 1 1 0]
[0 0 0 0]
(1, 0, 0, 0)
4 solutions""",
"Résolution sur 𝔽₂") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Sur \(\F_2\), déterminer le rang et une base du noyau de</p>
\[A=\begin{pmatrix}1&1&0&1\\0&1&1&1\\1&0&1&0\end{pmatrix}.\]
""", r"""
<p><u>Pivot.</u> \(L_3\leftarrow L_3+L_1\) (sur \(\F_2\), ajouter = soustraire) :</p>
\[\begin{pmatrix}1&1&0&1\\0&1&1&1\\0&1&1&1\end{pmatrix}\]
<p>\(L_3\leftarrow L_3+L_2\) :</p>
\[\begin{pmatrix}1&1&0&1\\0&1&1&1\\0&0&0&0\end{pmatrix}\]
<p>Puis \(L_1\leftarrow L_1+L_2\) pour réduire :</p>
\[\begin{pmatrix}1&0&1&0\\0&1&1&1\\0&0&0&0\end{pmatrix}\]
<p>Il y a 2 pivots (colonnes 1 et 2), donc <u>\(\rg A=2\)</u>.</p>
<p><u>Noyau.</u> \(\dim\Ker A=4-2=2\). Le système réduit s'écrit
\(x_1=x_3\), \(x_2=x_3+x_4\), avec \(x_3,x_4\) libres.</p>
<p>\(x_3=1,x_4=0\) donne \((1,1,1,0)\) ; \(x_3=0,x_4=1\) donne \((0,1,0,1)\).</p>
\[\Ker A=\Vect\big((1,1,1,0),\ (0,1,0,1)\big),\qquad |\Ker A|=2^2=4.\]
""", r"""<p>Vérification rapide : \(A\cdot(1,1,1,0)^{T}=(1+1,\ 1+1,\ 1+1)=(0,0,0)\) ✓</p>""") + r"""

""" + exo(2, r"""
<p>Soit \(A\in\mathcal M_n(\Fq)\). Montrer que les conditions suivantes sont équivalentes :
\(A\) inversible, \(\rg A=n\), \(\Ker A=\{0\}\), \(\det A\neq0\). Combien y a-t-il de matrices
inversibles \(n\times n\) sur \(\Fq\) ?</p>
""", r"""
<p><u>Équivalences.</u> Par le théorème du rang, \(\rg A=n\iff\dim\Ker A=0\iff\Ker A=\{0\}\),
c'est-à-dire \(A\) injective. En dimension finie égale, injective \(\iff\) bijective
\(\iff\) inversible. L'équivalence avec \(\det A\neq0\) est la caractérisation habituelle,
valable sur tout corps.</p>
<p><u>Comptage.</u> Une matrice est inversible si et seulement si ses colonnes forment une base
de \(\Fq^{n}\). Le nombre de bases a été calculé au nœud « Espaces vectoriels, bases,
dimension » :</p>
\[|GL_n(\Fq)|=(q^{n}-1)(q^{n}-q)\cdots(q^{n}-q^{n-1}).\]
<p>Par exemple \(|GL_3(\F_2)|=(8-1)(8-2)(8-4)=7\times6\times4=\underline{168}\).</p>
""", r"""<p>Ce groupe \(GL_n(\F_2)\) intervient directement dans McEliece : la clé privée contient
une matrice inversible aléatoire de \(GL_k(\F_2)\), qui masque la structure du code.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["lin-dualite"] = r"""
<p class="lead">L'orthogonal est l'objet qui transforme un code en son dual, et une matrice
génératrice en matrice de contrôle. C'est aussi là qu'apparaît la différence la plus nette
entre \(\R\) et \(\Fq\) : sur un corps fini, \(C\cap C^{\perp}\) peut être non nul.</p>

<h3>Formes linéaires et dual</h3>
""" + retenir("Définition", r"""
<p>Le <strong>dual</strong> de \(E\) est \(E^{*}=\mathcal L(E,K)\), l'espace des formes
linéaires sur \(E\).</p>
<p>Si \(\dim E=n\), alors \(\dim E^{*}=n\), et à toute base \((e_i)\) correspond la
<strong>base duale</strong> \((e_i^{*})\) définie par \(e_i^{*}(e_j)=\delta_{ij}\).</p>
""") + r"""

<h3>Orthogonal d'un sous-espace</h3>
""" + retenir("Définition et théorème", r"""
<p>Munissons \(\Fq^{n}\) de la forme bilinéaire \(\langle u,v\rangle=\sum_{i=1}^{n}u_iv_i\).
Pour \(C\subset\Fq^{n}\) sous-espace :</p>
\[C^{\perp}=\{v\in\Fq^{n}\ ;\ \forall u\in C,\ \langle u,v\rangle=0\}.\]
<p><strong>Théorème.</strong> \(C^{\perp}\) est un sous-espace et</p>
\[\dim C+\dim C^{\perp}=n,\qquad (C^{\perp})^{\perp}=C.\]
""") + demo(r"""
<p><strong>Sous-espace.</strong> \(C^{\perp}\) est l'intersection des noyaux des formes
linéaires \(v\mapsto\langle u,v\rangle\) pour \(u\in C\) : c'est donc un sous-espace.</p>
<p><strong>Dimension.</strong> Soit \(G\) une matrice \(k\times n\) dont les lignes forment une
base de \(C\) (donc \(\rg G=k\)). Par définition,</p>
\[C^{\perp}=\{v\ ;\ Gv=0\}=\Ker G.\]
<p>Le théorème du rang appliqué à \(G:\Fq^{n}\to\Fq^{k}\) donne</p>
\[\dim\Ker G=n-\rg G=n-k,\]
<p>c'est-à-dire \(\dim C^{\perp}=n-\dim C\).</p>
<p><strong>Biorthogonal.</strong> L'inclusion \(C\subset(C^{\perp})^{\perp}\) est immédiate :
tout \(u\in C\) est orthogonal à tout élément de \(C^{\perp}\).</p>
<p>En appliquant deux fois la formule des dimensions :</p>
\[\dim(C^{\perp})^{\perp}=n-\dim C^{\perp}=n-(n-k)=k=\dim C.\]
<p>Une inclusion entre espaces de même dimension finie est une égalité, d'où
\((C^{\perp})^{\perp}=C\).</p>
""") + r"""

""" + prof(r"""
<p>Attention : sur \(\Fq\), la forme \(\langle\cdot,\cdot\rangle\) <strong>n'est pas un produit
scalaire</strong> — elle n'est pas définie positive, cette notion n'ayant aucun sens sans ordre
sur le corps. On n'a donc <em>pas</em> \(E=C\oplus C^{\perp}\) en général.</p>
<p>La formule des dimensions reste vraie, mais la somme peut ne pas être directe : c'est
exactement le cas des codes auto-duaux, où \(C=C^{\perp}\).</p>
""") + r"""

<h3>L'application : matrice génératrice et matrice de contrôle</h3>
""" + retenir("Théorème", r"""
<p>Soit \(C\) un code \([n,k]\) de matrice génératrice \(G\) sous forme systématique
\(G=(I_k\mid A)\). Alors une matrice de contrôle de \(C\) est</p>
\[H=(-A^{T}\mid I_{n-k}),\]
<p>c'est-à-dire \(C=\Ker H\) et \(H\) engendre \(C^{\perp}\).</p>
""") + demo(r"""
<p>Calculons \(GH^{T}\). Avec \(G=(I_k\mid A)\) et \(H^{T}=\begin{pmatrix}-A\\ I_{n-k}\end{pmatrix}\) :</p>
\[GH^{T}=I_k\cdot(-A)+A\cdot I_{n-k}=-A+A=0.\]
<p>Donc toute ligne de \(G\) est orthogonale à toute ligne de \(H\), c'est-à-dire
\(C\subset\Ker H\).</p>
<p>Par ailleurs \(H\) contient le bloc \(I_{n-k}\), donc \(\rg H=n-k\), et par le théorème du
rang \(\dim\Ker H=n-(n-k)=k=\dim C\).</p>
<p>L'inclusion entre espaces de même dimension est une égalité : \(C=\Ker H\).</p>
""") + r"""

""" + code(r"""
# Le code de Hamming [7,4] : de G a H
A = [[0,1,1],
     [1,0,1],
     [1,1,0],
     [1,1,1]]
k, n = 4, 7

G = [[1 if i == j else 0 for j in range(k)] + A[i] for i in range(k)]
# Sur F2, -A^T = A^T
At = [[A[i][j] for i in range(k)] for j in range(n-k)]
H = [At[i] + [1 if i == j else 0 for j in range(n-k)] for i in range(n-k)]

print("G =", G)
print("H =", H)

# Verification : G H^T = 0
produit = [[sum(G[i][c]*H[j][c] for c in range(n)) % 2 for j in range(n-k)] for i in range(k)]
print("G.H^T =", produit)
""", "python",
"""G = [[1, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]]
H = [[0, 1, 1, 1, 1, 0, 0], [1, 0, 1, 1, 0, 1, 0], [1, 1, 0, 1, 0, 0, 1]]
G.H^T = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]""",
"De la matrice génératrice à la matrice de contrôle") + r"""

""" + prof(r"""
<p>Ce \(H\) est exactement ce qui sert à décoder : pour un mot reçu \(y\), le
<strong>syndrome</strong> \(s=Hy^{T}\) vaut \(0\) si et seulement si \(y\) est un mot du code.
Sinon, \(s\) désigne l'erreur. Tout le niveau 4 « Codes correcteurs » part de là.</p>
""") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soit \(C=\Vect\big((1,1,1,1)\big)\subset\F_2^{4}\). Déterminer \(C^{\perp}\), sa dimension,
et dire si \(C\subset C^{\perp}\).</p>
""", r"""
<p>\(v=(v_1,v_2,v_3,v_4)\in C^{\perp}\) si et seulement si
\(\langle(1,1,1,1),v\rangle=v_1+v_2+v_3+v_4=0\).</p>
<p>C'est l'ensemble des mots de <strong>poids pair</strong> :</p>
\[C^{\perp}=\{0000,1100,1010,1001,0110,0101,0011,1111\},\quad \dim C^{\perp}=3.\]
<p>Vérification : \(\dim C+\dim C^{\perp}=1+3=4\) ✓</p>
<p><u>Inclusion.</u> \((1,1,1,1)\) est de poids 4, donc pair : il appartient à \(C^{\perp}\).
Donc <u>\(C\subset C^{\perp}\)</u>, strictement.</p>
""", r"""<p>Ce couple (code de répétition, code de parité) est l'exemple le plus simple de codes
duaux l'un de l'autre. Sur \(\R\), une droite incluse dans son orthogonal serait impossible.</p>""") + r"""

""" + exo(2, r"""
<p>Montrer qu'un code auto-dual (\(C=C^{\perp}\)) sur \(\Fq\) a nécessairement une longueur
\(n\) paire, et que tous ses mots sont isotropes.</p>
""", r"""
<p><u>Longueur paire.</u> Si \(C=C^{\perp}\), alors \(\dim C=\dim C^{\perp}\). En reportant dans
la formule des dimensions :</p>
\[n=\dim C+\dim C^{\perp}=2\dim C,\]
<p>donc <u>\(n\) est pair</u>, et \(\dim C=n/2\).</p>
<p><u>Isotropie.</u> Soit \(u\in C\). Comme \(C=C^{\perp}\), on a aussi \(u\in C^{\perp}\), donc
\(u\) est orthogonal à tout élément de \(C\) — en particulier à lui-même :</p>
\[\langle u,u\rangle=0.\]
<p>Tout mot du code est donc isotrope.</p>
""", r"""<p>Sur \(\F_2\), \(\langle u,u\rangle=\sum u_i^2=\sum u_i\) (car \(u_i^2=u_i\)), donc
l'isotropie signifie que tous les mots sont de <strong>poids pair</strong>. Un code auto-dual
binaire est toujours contenu dans le code de parité.</p>""")


# ─────────────────────────────────────────────────────────────────────────────
CORPS["lin-reduction"] = r"""
<p class="lead">Le polynôme annulateur est l'outil qui analyse les registres à décalage : un
LFSR, un générateur XORshift, une suite récurrente linéaire sont tous décrits par leur polynôme
caractéristique sur \(\F_2\). Sa période maximale s'obtient exactement quand ce polynôme est
primitif.</p>

<h3>Polynôme annulateur et polynôme minimal</h3>
""" + retenir("Définitions", r"""
<p>\(P\in K[X]\) est <strong>annulateur</strong> de \(A\in\mathcal M_n(K)\) si \(P(A)=0\).</p>
<p>L'ensemble des polynômes annulateurs est un idéal de \(K[X]\), engendré par un unique
polynôme unitaire : le <strong>polynôme minimal</strong> \(\mu_A\).</p>
<p><strong>Cayley-Hamilton.</strong> \(\chi_A(A)=0\), où \(\chi_A=\det(XI-A)\). Donc
\(\mu_A\mid\chi_A\).</p>
""") + demo(r"""
<p>Montrons que l'ensemble \(I\) des polynômes annulateurs est un idéal non nul.</p>
<p><strong>Idéal.</strong> Si \(P,Q\in I\) alors \((P+Q)(A)=P(A)+Q(A)=0\), et pour tout
\(R\in K[X]\), \((RP)(A)=R(A)P(A)=R(A)\cdot0=0\).</p>
<p><strong>Non nul.</strong> \(\mathcal M_n(K)\) est de dimension \(n^2\), donc la famille
\((I,A,A^2,\dots,A^{n^2})\) de \(n^2+1\) matrices est liée : il existe une combinaison
linéaire nulle non triviale, c'est-à-dire un polynôme annulateur non nul.</p>
<p>\(K[X]\) étant principal (nœud « Euclidien ⊂ principal ⊂ factoriel », niveau 2), \(I=(\mu_A)\)
pour un unique \(\mu_A\) unitaire.</p>
""") + r"""

<h3>Calculer des puissances</h3>
<p>C'est l'usage pratique : un polynôme annulateur de degré \(d\) permet de calculer \(A^{k}\)
pour tout \(k\) avec seulement \(d\) coefficients.</p>

""" + retenir("Méthode", r"""
<p>Si \(\mu_A\) est de degré \(d\), la division euclidienne \(X^{k}=\mu_A Q+R\) avec
\(\deg R<d\) donne</p>
\[A^{k}=\mu_A(A)Q(A)+R(A)=R(A).\]
<p>Il suffit donc de calculer \(R=X^{k}\bmod\mu_A\), ce qui se fait par exponentiation rapide
dans \(K[X]/(\mu_A)\).</p>
""") + r"""

""" + prof(r"""
<p>Retenir le mouvement : <em>calculer dans \(K[X]/(\mu_A)\) au lieu de \(\mathcal M_n(K)\)</em>.
On remplace des produits de matrices \(n\times n\) par des produits de polynômes de degré
\(<d\). C'est exactement la même idée que l'exponentiation modulaire, transposée aux polynômes
— et c'est ce qui fera tourner les corps finis au niveau 3.</p>
""") + r"""

<h3>Suites récurrentes linéaires et LFSR</h3>
""" + retenir("Théorème", r"""
<p>Soit \((u_k)\) la suite sur \(\F_2\) définie par la récurrence</p>
\[u_{k+n}=c_{n-1}u_{k+n-1}+\dots+c_0u_k,\]
<p>de polynôme caractéristique \(P(X)=X^{n}-c_{n-1}X^{n-1}-\dots-c_0\).</p>
<p>Si \(P\) est <strong>primitif</strong> de degré \(n\) (irréductible, et \(X\) est générateur
de \(\F_{2^{n}}^{\times}\)), alors la suite est périodique de période maximale
\(2^{n}-1\).</p>
""") + r"""

""" + code(r"""
def lfsr(taps, etat, n_sorties):
    "Registre a decalage : taps est le masque des positions retroactives."
    sorties, vu = [], []
    for _ in range(n_sorties):
        sorties.append(etat & 1)
        vu.append(etat)
        bit = bin(etat & taps).count('1') & 1     # XOR des positions actives
        etat = (etat >> 1) | (bit << 3)           # registre de 4 bits
    return sorties, vu

# P(X) = X^4 + X + 1, primitif : periode 2^4 - 1 = 15
sorties, etats = lfsr(0b1001, 0b0001, 20)
print(sorties)
print("periode :", len(set(etats)))

# P(X) = X^4 + X^2 + 1 = (X^2+X+1)^2, non primitif
sorties2, etats2 = lfsr(0b0101, 0b0001, 20)
print("periode :", len(set(etats2)))
""", "python",
"""[1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1]
periode : 15
periode : 6""",
"Un LFSR atteint la période maximale si et seulement si son polynôme est primitif") + r"""

<p>Quinze états distincts sur les seize possibles (l'état nul est absorbant) : c'est la période
maximale. Avec un polynôme non primitif, la période tombe à 6 — un générateur pseudo-aléatoire
inutilisable.</p>

""" + code(r"""
F.<x> = GF(2)[]
for P in [x^4 + x + 1, x^4 + x^2 + 1, x^4 + x^3 + x^2 + x + 1]:
    print(P, P.is_irreducible(), P.is_primitive() if P.is_irreducible() else "-")
# Les polynomes primitifs de degre 4 sur F2
print([P for P in F.polynomials(of_degree=4) if P.is_irreducible() and P.is_primitive()])
""", "sagemath",
"""x^4 + x + 1 True True
x^4 + x^2 + 1 False -
x^4 + x^3 + x^2 + x + 1 True False
[x^4 + x + 1, x^4 + x^3 + 1]""",
"Irréductible ne suffit pas : il faut primitif") + r"""

""" + prof(r"""
<p>Le troisième polynôme est irréductible mais pas primitif : \(X\) y est d'ordre 5 et non 15.
Un LFSR construit dessus aurait une période de 5. C'est la distinction qu'il faut avoir en tête
au nœud « Cyclicité de 𝔽q* et éléments primitifs », et c'est exactement la même qui gouverne
le choix des constantes d'un XORshift.</p>
""") + r"""

<h3 class="exos-h">Vérifie que tu as compris</h3>
""" + exo(1, r"""
<p>Soit \(A=\begin{pmatrix}1&1\\0&1\end{pmatrix}\in\mathcal M_2(\R)\). Déterminer \(\chi_A\) et
\(\mu_A\), puis calculer \(A^{k}\) pour tout \(k\).</p>
""", r"""
<p><u>Polynôme caractéristique.</u> \(A\) est triangulaire, donc</p>
\[\chi_A=(X-1)^2.\]
<p><u>Polynôme minimal.</u> \(\mu_A\) divise \((X-1)^2\), donc \(\mu_A\in\{X-1,(X-1)^2\}\).
Or \(A-I=\begin{pmatrix}0&1\\0&0\end{pmatrix}\neq0\), donc \(\mu_A=(X-1)^2\).</p>
<p><u>Puissances.</u> Posons \(N=A-I\), de carré nul. Comme \(I\) et \(N\) commutent, le binôme
de Newton donne</p>
\[A^{k}=(I+N)^{k}=\sum_{j=0}^{k}\binom kj N^{j}=I+kN,\]
<p>tous les termes \(j\ge2\) étant nuls. D'où</p>
\[A^{k}=\begin{pmatrix}1&k\\0&1\end{pmatrix}.\]
""", r"""<p>On peut aussi diviser : \(X^{k}=(X-1)^2Q+R\) avec \(R=aX+b\). En évaluant en 1 :
\(1=a+b\) ; en dérivant et évaluant en 1 : \(k=a\). D'où \(R=kX+1-k\) et
\(A^k=kA+(1-k)I\) — le même résultat.</p>""") + r"""

""" + exo(2, r"""
<p>Combien y a-t-il de polynômes irréductibles de degré 4 sur \(\F_2\) ? Lesquels sont
primitifs ? Combien de LFSR de longueur 4 atteignent la période maximale ?</p>
""", r"""
<p><u>Irréductibles.</u> Les 16 polynômes unitaires de degré 4 sur \(\F_2\). Un polynôme
irréductible n'a pas de racine, donc \(P(0)=P(1)=1\) : le terme constant vaut 1 et le nombre
de termes est impair. Restent</p>
\[X^4+X+1,\quad X^4+X^3+1,\quad X^4+X^2+1,\quad X^4+X^3+X^2+X+1.\]
<p>Or \(X^4+X^2+1=(X^2+X+1)^2\) est réductible. Il reste donc <u>3 irréductibles</u>.</p>
<p>(Formule générale : \(\frac14\sum_{d\mid4}\mu(d)2^{4/d}=\frac14(16-4)=3\) ✓)</p>
<p><u>Primitifs.</u> Un \(P\) irréductible de degré 4 est primitif si \(X\) est d'ordre
\(15\) dans \(\F_{16}^{\times}\). Le nombre de primitifs est</p>
\[\frac{\varphi(15)}{4}=\frac{8}{4}=\underline{2},\]
<p>à savoir \(X^4+X+1\) et \(X^4+X^3+1\). Le troisième, \(X^4+X^3+X^2+X+1\), divise
\(X^5-1\) : \(X\) y est d'ordre 5.</p>
<p><u>LFSR.</u> <u>Deux</u> configurations de branchements atteignent la période 15.</p>
""", r"""<p>La formule \(\varphi(q-1)/n\) compte les polynômes primitifs de degré \(n\) sur
\(\F_p\) avec \(q=p^n\). On la démontrera au nœud « Cyclicité de 𝔽q* et éléments primitifs ».</p>""")


# ═════════════════════════════════════════════════════════════════════════════
# NŒUD PILOTE — gabarit en quatre temps. Remplace la version ci-dessus de arith-bezout.
# ═════════════════════════════════════════════════════════════════════════════

from briques import (noeud, qcm, preuve, exercice, a_toi, a_retenir, atelier, sage_atelier,
                     code_fichier, code_sage, video, video_attente)

_ENTREE = qcm("entree", [
    (r"Que vaut \(\pgcd(240, 46)\) ?",
     [r"\(1\)", r"\(2\)", r"\(4\)", r"\(6\)"], 1,
     r"\(240=5\times46+10\), \(46=4\times10+6\), \(10=6+4\), \(6=4+2\), \(4=2\times2\) : le dernier reste non nul est 2."),
    (r"L'équation \(6x+9y=4\) a-t-elle des solutions entières ?",
     ["Oui, une seule", "Oui, une infinité", "Non, aucune", "On ne peut pas savoir"], 2,
     r"\(6x+9y\) est toujours un multiple de \(\pgcd(6,9)=3\), et 3 ne divise pas 4."),
    (r"Quel est l'inverse de \(3\) modulo \(7\) ?",
     [r"\(2\)", r"\(4\)", r"\(5\)", "3 n'est pas inversible modulo 7"], 2,
     r"\(3\times5=15=2\times7+1\), donc \(3^{-1}\equiv5\pmod 7\)."),
])

_COMPRENDRE = r"""
<h3>Le problème</h3>
<p class="lead">Alice fabrique une clé RSA. Elle a choisi \(p=61\), \(q=53\), donc
\(\varphi(n)=60\times52=3120\), et son exposant public \(e=17\). Il lui faut l'exposant privé :
l'entier \(d\) tel que</p>
\[17\,d\equiv1 \pmod{3120}.\]
<p>Essayer \(d=1,2,3,\dots\) fonctionne ici (on trouve \(d=2753\) après 2753 essais). Avec une vraie
clé, \(\varphi(n)\) a plus de 600 chiffres : aucune machine n'essaiera jamais tous les candidats.
Il faut une méthode directe. C'est l'objet de ce nœud.</p>

<h3>L'observation qui débloque tout</h3>
<p>Chercher \(d\) avec \(17d\equiv1\pmod{3120}\), c'est chercher deux entiers \(d\) et \(k\) tels que</p>
\[17\,d+3120\,k=1.\]
<p>Autrement dit : écrire \(1\) comme combinaison de \(17\) et \(3120\). Or l'algorithme d'Euclide,
quand on le déroule, fabrique justement des combinaisons de ses deux nombres de départ.</p>

<h3>Un exemple entièrement à la main</h3>
<p>Prenons \(a=240\) et \(b=46\). On déroule Euclide, mais on note à chaque ligne comment le reste
s'écrit à partir de \(240\) et \(46\).</p>
<div class="table-wrap"><table>
<thead><tr><th>Division</th><th>Reste</th><th>Le reste, écrit \(240u+46v\)</th></tr></thead>
<tbody>
<tr><td>départ</td><td>\(240\)</td><td>\(240\times1+46\times0\)</td></tr>
<tr><td>départ</td><td>\(46\)</td><td>\(240\times0+46\times1\)</td></tr>
<tr><td>\(240=5\times46+10\)</td><td>\(10\)</td><td>\(240\times1+46\times(-5)\)</td></tr>
<tr><td>\(46=4\times10+6\)</td><td>\(6\)</td><td>\(240\times(-4)+46\times21\)</td></tr>
<tr><td>\(10=1\times6+4\)</td><td>\(4\)</td><td>\(240\times5+46\times(-26)\)</td></tr>
<tr><td>\(6=1\times4+2\)</td><td>\(2\)</td><td>\(240\times(-9)+46\times47\)</td></tr>
<tr><td>\(4=2\times2+0\)</td><td>\(0\)</td><td>on s'arrête</td></tr>
</tbody></table></div>
<p>Chaque ligne se déduit des deux précédentes : <em>nouvelle ligne = avant-dernière − quotient ×
dernière</em>. Par exemple, la ligne du reste 6 : \((0,1)-4\times(1,-5)=(-4,21)\).</p>
<p>On lit le résultat sur la dernière ligne non nulle :
\(\pgcd(240,46)=2\) et \(240\times(-9)+46\times47=-2160+2162=2\).</p>

""" + prof(r"""
<p>Vérifie toujours en recalculant \(au+bv\). Cela prend dix secondes et rattrape toutes les
erreurs de signe, qui sont de loin les plus fréquentes dans ce calcul.</p>
""") + r"""

<h3>Ce que l'on vient de découvrir, énoncé proprement</h3>
""" + retenir("Théorème de Bachet-Bézout", r"""
<p>Soient \(a,b\in\Z\) non tous deux nuls et \(d=\pgcd(a,b)\). Il existe \(u,v\in\Z\) tels que</p>
\[au+bv=d.\]
<p>De plus, \(d\) est le plus petit entier strictement positif de la forme \(au+bv\).</p>
""") + retenir("Trois conséquences", r"""
<ul>
<li><strong>Bézout.</strong> \(\pgcd(a,b)=1\iff\) il existe \(u,v\) avec \(au+bv=1\).</li>
<li><strong>Lemme de Gauss.</strong> Si \(a\mid bc\) et \(\pgcd(a,b)=1\), alors \(a\mid c\).</li>
<li><strong>Inverse modulaire.</strong> \(a\) est inversible modulo \(n\iff\pgcd(a,n)=1\), et son
inverse est le coefficient \(u\) de Bézout.</li>
</ul>
""") + r"""

<h3>Les deux pièges</h3>
""" + prof(r"""
<p><strong>Piège 1.</strong> Si \(au+bv=6\), on ne peut <em>pas</em> conclure que \(\pgcd(a,b)=6\) :
seulement que le pgcd <em>divise</em> 6. Exemple : \(2\times5+3\times(-1)=7\), et pourtant
\(\pgcd(2,3)=1\). La réciproque n'est vraie que lorsque la combinaison vaut 1.</p>
<p><strong>Piège 2.</strong> Le couple \((u,v)\) n'est pas unique. Si \((u,v)\) convient, alors
\((u+b,\ v-a)\) convient aussi. L'algorithme en donne un, il y en a une infinité.</p>
""", "Attention") + r"""

<h3>Retour à Alice</h3>
<p>Euclide étendu sur \((17,3120)\) donne \(17\times(-367)+3120\times2=1\). Donc
\(d\equiv-367\equiv2753\pmod{3120}\), en trois divisions au lieu de 2753 essais.</p>
"""

_DEMONTRER = r"""
<p class="lead">Trois énoncés à démontrer. Pour chacun : lis l'idée, écris la preuve en suivant
le squelette, et seulement ensuite compare avec la démonstration complète.</p>

""" + video("arith-bezout.mp4", "Bachet-Bézout : la preuve par le plus petit élément", "1 min 45") + preuve(
"Théorème de Bachet-Bézout",
r"""<p>Soient \(a,b\in\Z\) non tous deux nuls, \(d=\pgcd(a,b)\). Il existe \(u,v\in\Z\) tels que
\(au+bv=d\).</p>""",
r"""Parmi tous les entiers strictement positifs de la forme \(au+bv\), le plus petit divise
\(a\) et \(b\) — sinon un reste de division serait encore plus petit.""",
[r"Poser \(S=\{au+bv\ ;\ u,v\in\Z\}\cap\N^*\) et justifier que \(S\) est non vide.",
 r"Appeler \(g=au_0+bv_0\) le plus petit élément de \(S\). Pourquoi existe-t-il ?",
 r"Diviser \(a\) par \(g\) : \(a=gq+r\). Écrire \(r\) sous la forme \(au+bv\) et en déduire \(r=0\).",
 r"Faire de même pour \(b\). Conclure que \(g\le d\).",
 r"Montrer que \(d\mid g\), donc \(d\le g\). Conclure."],
r"""
<p>Soit \(S=\{au+bv\ ;\ u,v\in\Z\}\cap\N^*\).</p>
<p><strong>\(S\) est non vide</strong> : avec \(u=a\), \(v=b\), on obtient \(a^2+b^2>0\).</p>
<p>Toute partie non vide de \(\N^*\) a un plus petit élément : notons-le \(g=au_0+bv_0\).</p>
<p><strong>\(g\) divise \(a\).</strong> Division euclidienne : \(a=gq+r\) avec \(0\le r<g\). Alors</p>
\[r=a-gq=a-(au_0+bv_0)q=a(1-u_0q)+b(-v_0q).\]
<p>Donc \(r\) est de la forme \(au+bv\). Si \(r>0\), alors \(r\in S\) et \(r<g\), ce qui contredit
la minimalité de \(g\). Donc \(r=0\) et \(g\mid a\).</p>
<p>Le même raisonnement donne \(g\mid b\). Ainsi \(g\) est un diviseur commun, donc \(g\le d\).</p>
<p><strong>\(d\) divise \(g\).</strong> Comme \(d\mid a\) et \(d\mid b\), on a
\(d\mid au_0+bv_0=g\), donc \(d\le g\).</p>
<p>Les deux inégalités donnent \(g=d\) : le couple \((u_0,v_0)\) convient, et \(d\) est bien le
plus petit élément strictement positif de la forme \(au+bv\).</p>
""") + preuve(
"Lemme de Gauss",
r"""<p>Si \(a\mid bc\) et \(\pgcd(a,b)=1\), alors \(a\mid c\).</p>""",
r"""On écrit \(1=au+bv\), puis on multiplie tout par \(c\) pour faire apparaître \(bc\).""",
[r"Écrire la relation de Bézout pour \(a\) et \(b\).",
 r"Multiplier cette relation par \(c\).",
 r"Montrer que \(a\) divise chacun des deux termes du membre de gauche."],
r"""
<p>Comme \(\pgcd(a,b)=1\), Bézout donne \(u,v\) tels que \(au+bv=1\). En multipliant par \(c\) :</p>
\[acu+bcv=c.\]
<p>Or \(a\mid acu\), et \(a\mid bc\) par hypothèse donc \(a\mid bcv\). Donc \(a\) divise leur somme,
qui est \(c\).</p>
""") + preuve(
"Inverse modulaire",
r"""<p>\(a\) est inversible modulo \(n\) si et seulement si \(\pgcd(a,n)=1\). Dans ce cas, l'inverse
est le coefficient \(u\) d'une relation \(au+nv=1\).</p>""",
r"""« \(au\equiv1\pmod n\) » et « \(au+nv=1\) » sont la même phrase, écrite de deux façons.""",
[r"Sens direct : partir de \(au+nv=1\) et réduire modulo \(n\).",
 r"Sens réciproque : traduire \(au\equiv1\pmod n\) en une égalité dans \(\Z\).",
 r"Montrer que tout diviseur commun de \(a\) et \(n\) divise alors \(1\)."],
r"""
<p><strong>(\(\Leftarrow\))</strong> Si \(\pgcd(a,n)=1\), Bézout donne \(au+nv=1\). Modulo \(n\),
le terme \(nv\) disparaît : \(au\equiv1\pmod n\). Donc \(u\) est l'inverse de \(a\).</p>
<p><strong>(\(\Rightarrow\))</strong> Si \(au\equiv1\pmod n\), il existe \(k\in\Z\) avec
\(au-1=kn\), soit \(au-kn=1\). Tout diviseur commun de \(a\) et \(n\) divise \(au-kn=1\), donc vaut
\(\pm1\). Ainsi \(\pgcd(a,n)=1\).</p>
""") + preuve(
"Correction de l'algorithme d'Euclide étendu",
r"""<p>L'algorithme qui maintient, pour chaque reste \(r_k\), un couple \((u_k,v_k)\) par la règle
\((u_{k+1},v_{k+1})=(u_{k-1},v_{k-1})-q_k(u_k,v_k)\) renvoie bien \((d,u,v)\) avec \(au+bv=d\).</p>""",
r"""La propriété \(r_k=au_k+bv_k\) est vraie au départ et se conserve à chaque étape : c'est un
invariant de boucle.""",
[r"Vérifier l'invariant pour les deux lignes de départ.",
 r"Supposer l'invariant vrai aux rangs \(k-1\) et \(k\), et calculer \(r_{k+1}=r_{k-1}-q_kr_k\).",
 r"Conclure avec le fait que le dernier reste non nul est le pgcd."],
r"""
<p><strong>Initialisation.</strong> \(r_0=a=a\times1+b\times0\) et \(r_1=b=a\times0+b\times1\).</p>
<p><strong>Conservation.</strong> Supposons \(r_{k-1}=au_{k-1}+bv_{k-1}\) et \(r_k=au_k+bv_k\).
La division \(r_{k-1}=q_kr_k+r_{k+1}\) donne</p>
\[r_{k+1}=r_{k-1}-q_kr_k=a(u_{k-1}-q_ku_k)+b(v_{k-1}-q_kv_k)=au_{k+1}+bv_{k+1}.\]
<p><strong>Conclusion.</strong> L'algorithme d'Euclide termine et son dernier reste non nul est
\(d=\pgcd(a,b)\) (nœud précédent). L'invariant appliqué à ce reste donne \(d=au+bv\).</p>
""") + prof(r"""
<p>Les deux premières preuves reposent sur le même ressort que la division euclidienne : toute
partie non vide de \(\N\) a un plus petit élément. La dernière introduit l'<em>invariant de
boucle</em>, l'outil standard pour prouver qu'un algorithme est correct. Tu le retrouveras dans
tout le cours de complexité.</p>
""")

_DEPART = r"""
def euclide_etendu(a, b):
    '''Renvoie (d, u, v) tels que a*u + b*v == d == pgcd(a, b).'''
    # À toi. Rappel du tableau :
    #   nouvelle ligne = avant-dernière - quotient * dernière
    pass


def inverse_mod(a, n):
    '''Renvoie l'inverse de a modulo n, entre 0 et n-1.
    Lève ValueError si a n'est pas inversible modulo n.'''
    pass
"""

_G = "__import__('math').gcd"
_TESTS = [
    {"appel": "euclide_etendu(240, 46)", "attendu": "(d, u, v) avec d = 2 et 240*u + 46*v = 2",
     "verif": "isinstance(r, tuple) and len(r) == 3 and r[0] == 2 and 240*r[1] + 46*r[2] == 2"},
    {"appel": "euclide_etendu(1071, 462)", "attendu": "d = 21 et 1071*u + 462*v = 21",
     "verif": "isinstance(r, tuple) and len(r) == 3 and r[0] == 21 and 1071*r[1] + 462*r[2] == 21"},
    {"appel": "euclide_etendu(46, 240)", "attendu": "d = 2 et 46*u + 240*v = 2 (arguments dans l'autre ordre)",
     "verif": "isinstance(r, tuple) and len(r) == 3 and r[0] == 2 and 46*r[1] + 240*r[2] == 2"},
    {"appel": "euclide_etendu(17, 3120)", "attendu": "d = 1 et 17*u + 3120*v = 1",
     "verif": "isinstance(r, tuple) and len(r) == 3 and r[0] == 1 and 17*r[1] + 3120*r[2] == 1"},
    {"appel": "euclide_etendu(5, 0)", "attendu": "d = 5 et 5*u + 0*v = 5 (cas b = 0)",
     "verif": "isinstance(r, tuple) and len(r) == 3 and r[0] == 5 and 5*r[1] == 5"},
    {"appel": "euclide_etendu(2**127 - 1, 2**89 - 1)", "attendu": "d = 1 et la relation de Bézout, sur de grands entiers",
     "verif": "isinstance(r, tuple) and len(r) == 3 and r[0] == 1 and (2**127 - 1)*r[1] + (2**89 - 1)*r[2] == 1"},
    {"appel": "inverse_mod(17, 3120)", "attendu": "2753", "verif": "r == 2753"},
    {"appel": "inverse_mod(7, 26)", "attendu": "15 (et non -11 : le résultat doit être entre 0 et n-1)", "verif": "r == 15"},
    {"appel": "inverse_mod(10, 21)", "attendu": "19", "verif": "r == 19"},
    {"appel": "inverse_mod(15, 3120)", "attendu": "une erreur ValueError, car pgcd(15, 3120) = 15", "leve": "ValueError"},
]

_IMPLEMENTER = r"""
<p class="lead">Ici, c'est toi qui codes. Tu écris les deux fonctions, tu lances les tests, et tu
corriges jusqu'à ce qu'ils passent tous. Python tourne dans ton navigateur : rien à installer.</p>
""" + atelier("arith-bezout", r"""
<p>Complète les deux fonctions.</p>
<ul>
<li><code>euclide_etendu(a, b)</code> renvoie un triplet \((d,u,v)\) avec \(au+bv=d=\pgcd(a,b)\).
Sers-toi du tableau du temps 1 : garde deux lignes en mémoire, et fabrique la suivante.</li>
<li><code>inverse_mod(a, n)</code> utilise la première. Si le pgcd ne vaut pas 1, elle doit lever
une erreur avec <code>raise ValueError(...)</code>.</li>
</ul>
<p><strong>Exécuter</strong> lance ton programme tel quel (pratique avec des <code>print</code>).
<strong>Tester mon code</strong> le confronte à dix cas, dont des cas limites.</p>
""", _DEPART, _TESTS,
    r"""<p>Une solution possible. La tienne peut être différente et tout aussi juste : les tests
vérifient la relation \(au+bv=d\), pas des valeurs précises de \(u\) et \(v\), puisqu'il en existe
une infinité.</p>"""
    + code_fichier("niveau1/arith_bezout.py", "Corrigé : Euclide étendu et inverse modulaire")) + r"""

<h3>Confronte ton résultat à la référence</h3>
<p>Ton programme passe les tests : il reste à le comparer à l'outil que les cryptographes
utilisent. SageMath connaît déjà ces fonctions, sous les noms <code>xgcd</code> et
<code>inverse_mod</code>.</p>
""" + sage_atelier(r"""
<p>Exécute la cellule, puis <strong>modifie-la</strong> : remplace les nombres par ceux d'un
exercice du temps 4, et compare avec ton calcul à la main.</p>
<p>Question à te poser : Sage renvoie-t-il les mêmes \(u\) et \(v\) que ton programme ? Si non,
est-ce une erreur ?</p>
""", r"""
print(xgcd(240, 46))            # (pgcd, u, v)
print(inverse_mod(17, 3120))    # la clé privée RSA
print(gcd(15, 3120))            # pourquoi inverse_mod(15, 3120) échoue
""") + prof(r"""
<p>Deux programmes corrects peuvent donner des couples \((u,v)\) différents : si \((u,v)\)
convient, \((u+b/d,\ v-a/d)\) aussi. Ce n'est pas une erreur. C'est pour cela qu'on vérifie
toujours la <em>relation</em> \(au+bv=d\), jamais des valeurs apprises.</p>
""") + a_toi(r"""
<p>Pour aller plus loin : écris une version <strong>récursive</strong> de
<code>euclide_etendu</code> dans l'atelier, fondée sur \(\pgcd(a,b)=\pgcd(b,\ a\bmod b)\), et
vérifie qu'elle passe les mêmes tests. Si l'appel sur \((b,\ a\bmod b)\) renvoie \((d,u',v')\),
que faut-il renvoyer pour \((a,b)\) ?</p>
""", r"""
<p>Si \(d=bu'+(a\bmod b)v'\) et \(a\bmod b=a-qb\) avec \(q=\lfloor a/b\rfloor\), alors
\(d=av'+b(u'-qv')\). Donc \((u,v)=(v',\ u'-qv')\).</p>
""" + code(r"""
def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    d, u1, v1 = euclide_etendu(b, a % b)
    return d, v1, u1 - (a // b) * v1
""", "python", None, "Version récursive"))

_EXERCER = r"""
<p class="lead">Cinq exercices, du calcul direct au problème de master. Cherche sur une feuille,
ouvre l'indice si tu bloques, et la correction seulement à la fin.</p>
""" + exercice(1, "Application", r"""
<p>Déterminer des entiers \(u,v\) tels que \(1071u+462v=\pgcd(1071,462)\).</p>
""", r"""<p>Déroule Euclide (trois divisions), puis remonte en exprimant chaque reste à partir des
précédents.</p>""", r"""
<p>\(1071=2\times462+147\)</p>
<p>\(462=3\times147+21\)</p>
<p>\(147=7\times21+0\), donc \(\pgcd(1071,462)=21\).</p>
<p><u>Remontée.</u> \(21=462-3\times147=462-3\times(1071-2\times462)=7\times462-3\times1071\).</p>
<p>Donc <u>\(u=-3\), \(v=7\)</u>.</p>
<p>Vérification : \(-3\times1071+7\times462=-3213+3234=21\). ✓</p>
""") + exercice(2, "Application", r"""
<p>Calculer l'inverse de \(7\) modulo \(26\), puis donner la formule de déchiffrement du
chiffrement affine \(y=7x+3\bmod26\).</p>
""", r"""<p>L'inverse de 7 est le coefficient de 7 dans une relation \(7u+26v=1\). Ensuite, isole
\(x\) dans \(y=7x+3\).</p>""", r"""
<p>\(26=3\times7+5\), \(7=1\times5+2\), \(5=2\times2+1\).</p>
<p>\(1=5-2\times2=5-2\times(7-5)=3\times5-2\times7=3\times(26-3\times7)-2\times7=3\times26-11\times7\).</p>
<p>Donc \(7^{-1}\equiv-11\equiv\underline{15}\pmod{26}\).</p>
<p>De \(y=7x+3\) : \(x=15(y-3)=15y-45\), et \(-45\equiv7\pmod{26}\), d'où</p>
\[x=15y+7 \bmod 26.\]
""", r"""<p>Contrôle : \(x=1\) donne \(y=10\), et \(15\times10+7=157=6\times26+1\). ✓</p>""") + exercice(
3, "Raisonnement", r"""
<p>Résoudre dans \(\Z^2\) l'équation \(15x+21y=9\).</p>
""", r"""<p>Trois étapes : y a-t-il des solutions (comparer 9 au pgcd) ? En trouver une par Bézout.
Puis soustraire deux solutions et utiliser le lemme de Gauss.</p>""", r"""
<p><u>Existence.</u> \(\pgcd(15,21)=3\) et \(3\mid9\) : il y a des solutions.</p>
<p><u>Une solution.</u> \(21=15+6\), \(15=2\times6+3\), donc
\(3=15-2\times(21-15)=3\times15-2\times21\). En multipliant par 3 :
\(9=9\times15-6\times21\). Solution particulière : \((9,-6)\).</p>
<p><u>Toutes les solutions.</u> Si \((x,y)\) est solution, \(15(x-9)=-21(y+6)\), soit
\(5(x-9)=-7(y+6)\). Comme \(\pgcd(5,7)=1\), Gauss donne \(7\mid x-9\) : \(x=9+7k\), puis
\(y=-6-5k\).</p>
<p>Réciproquement ces couples conviennent. Donc</p>
\[(x,y)=(9+7k,\ -6-5k),\quad k\in\Z.\]
""", r"""<p>Schéma général : \(ax+by=c\) a des solutions si et seulement si \(\pgcd(a,b)\mid c\), et
elles forment alors une « droite » d'entiers.</p>""") + exercice(4, "Raisonnement", r"""
<p>Montrer que si \(\pgcd(a,b)=1\) et \(\pgcd(a,c)=1\), alors \(\pgcd(a,bc)=1\).</p>
""", r"""<p>Écris les deux relations de Bézout, puis multiplie-les membre à membre.</p>""", r"""
<p>Bézout donne \(au+bv=1\) et \(au'+cv'=1\). En multipliant :</p>
\[1=(au+bv)(au'+cv')=a\,(auu'+ucv'+bvu')+bc\,(vv').\]
<p>On a écrit \(1\) sous la forme \(aU+(bc)V\). Par Bézout (sens réciproque, valable car la
combinaison vaut 1), <u>\(\pgcd(a,bc)=1\)</u>.</p>
""", r"""<p>C'est la raison pour laquelle le produit de deux inversibles modulo \(n\) est encore
inversible : \((\Z/n\Z)^{\times}\) est stable par produit.</p>""") + exercice(
5, "Problème — vers le master", r"""
<p>Dans RSA, on prend \(n=pq\), \(\varphi=(p-1)(q-1)\), et un exposant public \(e\).</p>
<ol>
<li>Pourquoi faut-il \(\pgcd(e,\varphi)=1\) ?</li>
<li>Pourquoi \(e\) est-il toujours impair ?</li>
<li>Montrer que l'exposant privé \(d\) est unique modulo \(\varphi\).</li>
</ol>
""", r"""<p>(1) À quelle condition \(e\) a-t-il un inverse modulo \(\varphi\) ? (2) Quelle est la
parité de \(p-1\) ? (3) Suppose deux inverses \(d\) et \(d'\) et calcule \(d\,(e\,d')\) de deux
façons.</p>""", r"""
<p><u>1.</u> L'exposant privé est l'inverse de \(e\) modulo \(\varphi\). Par le théorème de
l'inverse modulaire, il existe si et seulement si \(\pgcd(e,\varphi)=1\).</p>
<p><u>2.</u> \(p\) et \(q\) sont des premiers impairs, donc \(p-1\) et \(q-1\) sont pairs et
\(\varphi\) est pair. Si \(e\) était pair, 2 diviserait \(e\) et \(\varphi\) : impossible.</p>
<p><u>3.</u> Soient \(d,d'\) avec \(ed\equiv ed'\equiv1\pmod\varphi\). Alors</p>
\[d\equiv d\cdot(ed')=(de)\cdot d'\equiv d'\pmod\varphi.\]
<p>L'inverse est donc <u>unique modulo \(\varphi\)</u>.</p>
""", r"""<p>En pratique on fixe \(e=65537\) et on tire \(p,q\) jusqu'à ce que
\(\pgcd(e,\varphi)=1\) : comme 65537 est premier, il suffit que \(p\not\equiv1\) et
\(q\not\equiv1\pmod{65537}\).</p>""")

_SORTIE = qcm("sortie", [
    (r"On sait qu'il existe \(u,v\) avec \(au+bv=6\). Que peut-on affirmer ?",
     [r"\(\pgcd(a,b)=6\)", r"\(\pgcd(a,b)\) divise \(6\)", r"\(6\) divise \(\pgcd(a,b)\)",
      r"\(a\) et \(b\) sont pairs"], 1,
     r"Le pgcd divise toute combinaison \(au+bv\). L'égalité n'est garantie que si la combinaison est la plus petite possible."),
    (r"Quel est l'inverse de \(10\) modulo \(21\) ?",
     [r"\(2\)", r"\(11\)", r"\(19\)", "10 n'est pas inversible modulo 21"], 2,
     r"\(\pgcd(10,21)=1\) donc l'inverse existe, et \(10\times19=190=9\times21+1\)."),
    (r"« Si \(a\mid bc\) et \(a\nmid b\), alors \(a\mid c\). » Cet énoncé est :",
     ["Vrai, c'est le lemme de Gauss", r"Faux : il faut \(\pgcd(a,b)=1\), pas seulement \(a\nmid b\)",
      "Vrai seulement si a est pair", "Faux dans tous les cas"], 1,
     r"Contre-exemple : \(6\mid4\times9\), mais \(6\nmid4\) et \(6\nmid9\). Ne pas diviser n'est pas être premier avec."),
    (r"Pour deux entiers de 2048 bits, Euclide étendu effectue de l'ordre de :",
     ["quelques milliers de divisions", r"\(2^{1024}\) divisions", r"\(2^{2048}\) divisions",
      "un nombre imprévisible de divisions"], 0,
     r"Le nombre de divisions est en \(O(\log b)\), soit au plus environ \(2\times2048\) ici."),
])

_RETENIR = a_retenir([
    r"\(\pgcd(a,b)\) est le plus petit entier \(>0\) de la forme \(au+bv\).",
    r"\(au+bv=1\iff\pgcd(a,b)=1\) ; pour une autre valeur, le pgcd la <em>divise</em> seulement.",
    r"Gauss : \(a\mid bc\) et \(\pgcd(a,b)=1\) entraînent \(a\mid c\).",
    r"\(a\) inversible modulo \(n\iff\pgcd(a,n)=1\) ; l'inverse est le \(u\) de Bézout.",
    r"Euclide étendu : nouvelle ligne = avant-dernière − quotient × dernière. Toujours vérifier \(au+bv\).",
])

CORPS["arith-bezout"] = noeud(_ENTREE, _COMPRENDRE, _DEMONTRER, _IMPLEMENTER,
                              _EXERCER, _SORTIE, _RETENIR)
