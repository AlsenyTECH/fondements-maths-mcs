/* Outils communs à toutes les pages : thème, recherche, progression globale,
   coloration de la carte, parcours guidés, test de positionnement. */
(function () {
  var racine = document.documentElement;

  // ----- thème clair / sombre -----
  function themeEffectif() {
    if (racine.dataset.theme) return racine.dataset.theme;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function majBoutons() {
    var sombre = themeEffectif() === 'dark';
    document.querySelectorAll('.theme-btn').forEach(function (b) {
      b.textContent = sombre ? 'Thème clair' : 'Thème sombre';
      b.setAttribute('aria-pressed', String(sombre));
    });
  }
  document.querySelectorAll('.theme-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = themeEffectif() === 'dark' ? 'light' : 'dark';
      racine.dataset.theme = t;
      try { localStorage.setItem('mcs-theme', t); } catch (e) {}
      majBoutons();
    });
  });
  majBoutons();

  // ----- progression : réunit les nœuds validés de tous les niveaux -----
  function progression() {
    var fait = {};
    for (var k = 0; k < 5; k++) {
      try {
        var o = JSON.parse(localStorage.getItem('mcs-maths-progression-' + k) || '{}') || {};
        for (var id in o) if (o[id]) fait[id] = true;
      } catch (e) {}
    }
    return fait;
  }
  var fait = progression();
  function compte(ids) { return ids.filter(function (id) { return fait[id]; }).length; }

  // carte
  document.querySelectorAll('.carte .n[data-noeuds]').forEach(function (a) {
    var ids = a.dataset.noeuds.split(' '), n = compte(ids);
    a.classList.toggle('encours', n > 0 && n < ids.length);
    a.classList.toggle('fini', n === ids.length);
    var pb = a.querySelector('.pb');
    if (pb) pb.setAttribute('width', (Number(pb.dataset.l) * n / ids.length).toFixed(1));
    if (n) { var t = a.querySelector('title'); if (t) t.textContent += ' — ' + n + ' nœud' + (n > 1 ? 's' : '') + ' sur ' + ids.length + ' validé' + (n > 1 ? 's' : ''); }
  });
  // cartes des niveaux
  document.querySelectorAll('.niv-card[data-noeuds]').forEach(function (c) {
    var ids = c.dataset.noeuds.split(' '), n = compte(ids), el = c.querySelector('.cpt-fait');
    if (n && el) el.textContent = ' · ' + n + ' validé' + (n > 1 ? 's' : '');
  });
  // progression globale sur l'accueil
  var pg = document.getElementById('prog-global');
  if (pg) {
    var total = 0, ok = 0;
    document.querySelectorAll('.carte .n[data-noeuds]').forEach(function (a) {
      var ids = a.dataset.noeuds.split(' '); total += ids.length; ok += compte(ids);
    });
    pg.textContent = ok
      ? 'Tu as validé ' + ok + ' nœud' + (ok > 1 ? 's' : '') + ' sur ' + total + '.'
      : 'Aucun nœud validé pour l\'instant. Commence par te situer.';
  }

  // ----- parcours guidés -----
  document.querySelectorAll('.parcours[data-noeuds]').forEach(function (p) {
    var ids = p.dataset.noeuds.split(' '), n = compte(ids), suivant = null;
    p.querySelectorAll('.pc-liste li').forEach(function (li) {
      var ok = !!fait[li.dataset.id];
      li.classList.toggle('fait', ok);
      if (!ok && !suivant) { suivant = li; li.classList.add('suivant'); }
    });
    var fill = p.querySelector('.prog-fill'); if (fill) fill.style.width = Math.round(100 * n / ids.length) + '%';
    var btn = p.querySelector('.pc-continuer');
    if (n && btn) {
      p.querySelector('.pc-prog').textContent = n + ' sur ' + ids.length + ' nœuds validés';
      if (suivant) { btn.href = suivant.querySelector('a').getAttribute('href'); btn.textContent = 'Continuer →'; }
      else { btn.textContent = 'Parcours terminé ✓'; btn.removeAttribute('href'); btn.classList.add('ghost'); }
    }
  });

  // ----- recherche -----
  var indexCharge = null;
  function chargerIndex() {
    if (!indexCharge) indexCharge = new Promise(function (ok, ko) {
      var s = document.createElement('script');
      s.src = 'assets/index-recherche.js';
      s.onload = function () {
        window.INDEX_RECHERCHE.forEach(function (e) { e.n = normaliser(e[1] + ' ' + e[3]); e.nt = normaliser(e[1]); });
        ok(window.INDEX_RECHERCHE);
      };
      s.onerror = function () { indexCharge = null; ko(); };
      document.head.appendChild(s);
    });
    return indexCharge;
  }
  function normaliser(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function echapper(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  document.querySelectorAll('.rech').forEach(function (bloc) {
    var champ = bloc.querySelector('.rech-in'), liste = bloc.querySelector('.rech-res'), actif = -1;
    function fermer() { liste.hidden = true; actif = -1; }
    function chercher() {
      var q = normaliser(champ.value.trim());
      if (q.length < 2) { fermer(); return; }
      var mots = q.split(/\s+/);
      chargerIndex().then(function (idx) {
        var res = idx.filter(function (e) { return mots.every(function (m) { return e.n.indexOf(m) >= 0; }); });
        res.sort(function (a, b) {
          var sa = (a.nt.indexOf(mots[0]) === 0 ? 0 : a.nt.indexOf(mots[0]) > 0 ? 1 : 2) + (a[0] === 'Nœud' ? 0 : 0.5);
          var sb = (b.nt.indexOf(mots[0]) === 0 ? 0 : b.nt.indexOf(mots[0]) > 0 ? 1 : 2) + (b[0] === 'Nœud' ? 0 : 0.5);
          return sa - sb;
        });
        liste.innerHTML = res.length
          ? res.slice(0, 8).map(function (e) {
              return '<li><a href="' + echapper(e[2]) + '"><span class="rech-type">' + echapper(e[0]) + '</span>' +
                     '<span class="rech-t">' + echapper(e[1]) + '</span>' +
                     '<span class="rech-x">' + echapper(e[3].slice(0, 120)) + '</span></a></li>';
            }).join('') + (res.length > 8 ? '<li class="rech-plus">' + (res.length - 8) + ' autres résultats : précise ta recherche.</li>' : '')
          : '<li class="rech-vide">Aucun résultat pour « ' + echapper(champ.value.trim()) + ' ».</li>';
        liste.hidden = false; actif = -1;
      }, function () {
        liste.innerHTML = '<li class="rech-vide">La recherche n\'a pas pu se charger.</li>'; liste.hidden = false;
      });
    }
    champ.addEventListener('focus', function () { chargerIndex().catch(function () {}); });
    champ.addEventListener('input', chercher);
    champ.addEventListener('keydown', function (ev) {
      var liens = liste.querySelectorAll('a');
      if (ev.key === 'Escape') { fermer(); champ.blur(); }
      else if ((ev.key === 'ArrowDown' || ev.key === 'ArrowUp') && liens.length) {
        ev.preventDefault();
        actif = (actif + (ev.key === 'ArrowDown' ? 1 : liens.length - 1)) % liens.length;
        liens.forEach(function (l, k) { l.classList.toggle('actif', k === actif); });
      } else if (ev.key === 'Enter' && liens.length) {
        ev.preventDefault(); location.href = liens[Math.max(actif, 0)].getAttribute('href'); fermer();
      }
    });
    liste.addEventListener('click', function (ev) { if (ev.target.closest('a')) fermer(); });
    document.addEventListener('click', function (ev) { if (!bloc.contains(ev.target)) fermer(); });
  });

  // ----- test de positionnement -----
  var test = document.querySelector('form.pos-test');
  if (test) test.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var qs = test.querySelectorAll('.qcm-q'), manque = 0, parNiv = {}, rates = [];
    qs.forEach(function (q) { if (!q.querySelector('input:checked')) manque++; });
    var res = test.querySelector('.qcm-res');
    if (manque) {
      res.hidden = false; res.className = 'qcm-res ko';
      res.textContent = 'Il reste ' + manque + ' question' + (manque > 1 ? 's' : '') + ' sans réponse.';
      return;
    }
    res.hidden = true;
    qs.forEach(function (q) {
      var niv = q.dataset.niv, bonne = Number(q.dataset.bonne), choisi = q.querySelector('input:checked');
      var juste = Number(choisi.value) === bonne;
      parNiv[niv] = parNiv[niv] || { ok: 0, n: 0 };
      parNiv[niv].n++; if (juste) parNiv[niv].ok++;
      q.querySelectorAll('.qcm-o').forEach(function (l) { l.classList.remove('juste', 'faux'); });
      choisi.closest('.qcm-o').classList.add(juste ? 'juste' : 'faux');
      q.querySelectorAll('.qcm-o')[bonne].classList.add('juste');
      q.querySelector('.qcm-x').hidden = false;
      if (!juste) rates.push(q);
    });
    var depart = null, lignes = '';
    document.querySelectorAll('.pos-niv').forEach(function (s) {
      var r = parNiv[s.dataset.niv]; if (!r) return;
      var acquis = r.ok >= Math.ceil(2 * r.n / 3);
      if (!acquis && !depart) depart = s;
      lignes += '<tr class="' + (acquis ? 'ok' : 'ko') + '"><td>Niveau ' + s.dataset.niv + ' · ' + echapper(s.dataset.titre) +
                '</td><td>' + r.ok + ' / ' + r.n + '</td><td>' + (acquis ? 'acquis' : 'à travailler') + '</td></tr>';
    });
    var h = '<h2 class="sec">Ton résultat</h2>';
    h += depart
      ? '<p class="lead">Commence par le <strong>niveau ' + depart.dataset.niv + ' · ' + echapper(depart.dataset.titre) +
        '</strong>. C\'est le premier niveau où des bases manquent : tout ce qui suit s\'appuie dessus.</p>' +
        '<p><a class="btn" href="' + echapper(depart.dataset.url) + '">Ouvrir le niveau ' + depart.dataset.niv + ' →</a></p>'
      : '<p class="lead">Tu as les bases de tous les niveaux. Choisis un parcours selon ton objectif.</p>' +
        '<p><a class="btn" href="parcours.html">Voir les parcours →</a></p>';
    h += '<div class="table-wrap"><table><thead><tr><th>Niveau</th><th>Score</th><th>Bilan</th></tr></thead><tbody>' + lignes + '</tbody></table></div>';
    if (rates.length) {
      h += '<h3>Les nœuds à revoir</h3><ul class="pos-revoir">' + rates.map(function (q) {
        return '<li><a href="' + echapper(q.dataset.url) + '">' + echapper(q.dataset.titre) + '</a> (niveau ' + q.dataset.niv + ')</li>';
      }).join('') + '</ul>';
    }
    h += '<p class="pos-note">Les explications sont affichées sous chaque question, plus haut.</p>';
    var bloc = document.querySelector('.pos-resultat');
    bloc.innerHTML = h; bloc.hidden = false;
    bloc.scrollIntoView({ block: 'start' });
    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([test]).catch(function () {});
  });
})();
