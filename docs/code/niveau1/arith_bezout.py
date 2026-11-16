"""Nœud 1.2 — Bézout et l'algorithme d'Euclide étendu."""


def euclide_etendu(a, b):
    """Renvoie (d, u, v) avec a*u + b*v = d = pgcd(a, b).

    Invariants maintenus à chaque tour de boucle :
        r  = a*u  + b*v
        r2 = a*u2 + b*v2
    """
    r, u, v = a, 1, 0
    r2, u2, v2 = b, 0, 1
    while r2 != 0:
        q = r // r2
        r, r2 = r2, r - q * r2
        u, u2 = u2, u - q * u2
        v, v2 = v2, v - q * v2
    return r, u, v


def inverse_mod(a, n):
    """Inverse de a modulo n, ou erreur si pgcd(a, n) != 1."""
    d, u, _ = euclide_etendu(a, n)
    if d != 1:
        raise ValueError("%d n'est pas inversible modulo %d (pgcd = %d)" % (a, n, d))
    return u % n


if __name__ == "__main__":
    d, u, v = euclide_etendu(240, 46)
    print("pgcd(240, 46) =", d, " avec u =", u, "et v =", v)
    print("vérification : 240*u + 46*v =", 240 * u + 46 * v)

    # La clé privée RSA : d = e^(-1) mod phi(n)
    p, q, e = 61, 53, 17
    phi = (p - 1) * (q - 1)
    cle = inverse_mod(e, phi)
    print("phi(n) =", phi, " clé privée d =", cle, " contrôle e*d mod phi =", e * cle % phi)

    try:
        inverse_mod(15, phi)
    except ValueError as err:
        print("refus attendu :", err)
