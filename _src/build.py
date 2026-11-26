#!/usr/bin/env python3
"""Génère les pages du site metricmind.fr à partir des fragments de _src/.
Usage : python3 _src/build.py  (depuis la racine du repo)
Le dossier _src/ est ignoré par GitHub Pages (préfixe _)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
S = lambda n: open(os.path.join(SRC, 'sections', n + '.html'), encoding='utf-8').read()
R = lambda n: open(os.path.join(SRC, n), encoding='utf-8').read()

SITE = 'https://metricmind.fr'
TRACKING = R('head_tracking.html')
LOGO = R('nav_logo.html')

JSONLD = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Metricmind","url":"https://metricmind.fr/","email":"contact@metricmind.fr","description":"Audit de la mesure des conversions, scan Trackmap et formation GA4 pour les PME.","areaServed":"FR","address":{"@type":"PostalAddress","addressLocality":"Bois-Colombes","postalCode":"92270","addressCountry":"FR"},"founder":{"@type":"Person","name":"Malick","jobTitle":"Consultant senior Data & Performance","sameAs":["https://www.linkedin.com/in/malick-ba-a3a88337/"]}}
</script>
'''

NAV_ITEMS = [('/offres', 'Offres'), ('/trackmap', 'Trackmap'), ('/cas-clients', 'Cas clients'), ('/a-propos', 'À propos')]


def head(title, desc, path, extra=''):
    url = SITE + path
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#080808">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Metricmind">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
{extra}{TRACKING}<link rel="stylesheet" href="/assets/site.css">
'''


def nav():
    items = '\n'.join(f'    <li><a href="{h}">{t}</a></li>' for h, t in NAV_ITEMS)
    return f'''<nav>
{LOGO}
  <button class="nav-burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <ul class="nav-links" aria-label="Navigation principale">
{items}
    <li><a href="/contact" class="nav-cta">Parlons-en</a></li>
  </ul>
</nav>
'''


def page_head(label, h1, intro):
    return f'''<section class="page-head">
  <span class="label">{label}</span>
  <h1>{h1}</h1>
  <p>{intro}</p>
</section>
'''


def cta_band(title, text, lead):
    return f'''<section class="cta-band">
  <h2>{title}</h2>
  <p>{text}</p>
  <div class="actions">
    <a href="/contact" class="btn-p" data-lead="{lead}">Parlons de votre situation →</a>
    <a href="/contact?sujet=Scan" class="btn-g" data-lead="{lead}_scan">Demander un scan gratuit</a>
  </div>
</section>
'''


def foot(float_cta=True):
    fc = '<a href="/contact" class="float-cta" aria-label="Prendre contact">Parlons-en →</a>\n' if float_cta else ''
    return f'''{fc}{S("footer")}
<script src="/assets/site.js"></script>
<script src="/cc.js"></script>
</body>
</html>
'''


def page(fname, title, desc, path, body, extra_head='', page_style='', float_cta=True):
    html = head(title, desc, path, extra_head)
    if page_style:
        html += '<style>\n' + page_style + '\n</style>\n'
    html += '</head>\n<body>\n\n' + nav() + '\n' + body + '\n' + foot(float_cta)
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(html)
    print('écrit', fname)


# ---------- Sections dérivées ----------
HOME_OFFRES = '''<section id="offres-home" aria-labelledby="ho-title">
  <span class="label">Comment je peux vous aider</span>
  <h2 id="ho-title">Trois étapes pour reprendre la main</h2>
  <div class="home-offres">
    <a href="/trackmap" class="ho"><span class="ho-n">01 · Gratuit</span><span class="ho-t">Scan Trackmap</span><span class="ho-d">Ce qui tourne vraiment sur votre site, ce qui fuit, ce qui ne respecte pas le consentement. Restitution en 30 minutes.</span><span class="ho-go">Découvrir Trackmap →</span></a>
    <a href="/offres" class="ho main"><span class="ho-n">02 · Prix fixe</span><span class="ho-t">Audit mesure & conversions</span><span class="ho-d">Du clic publicitaire jusqu'au lead ou à la vente : je localise les conversions perdues et je pilote les corrections.</span><span class="ho-go">Voir l'offre →</span></a>
    <a href="/offres" class="ho"><span class="ho-n">03</span><span class="ho-t">Formation & autonomie</span><span class="ho-d">Votre équipe marketing apprend à trouver ses réponses dans GA4 et à construire des tableaux de bord utiles.</span><span class="ho-go">Voir l'offre →</span></a>
  </div>
</section>
'''

cas = S('cas')
# Accueil : seulement la première étude de cas, ouverte
first_case = cas[cas.index('    <div class="cas-card"'):cas.index('    <div class="cas-card"', cas.index('    <div class="cas-card"') + 10)]
HOME_PROOF = f'''<section id="cas" aria-labelledby="proof-title">
  <span class="label">Résultat</span>
  <h2 id="proof-title">Des résultats concrets, pas des livrables.</h2>
  <div class="cas-grid">
{first_case}  </div>
  <p class="more"><a href="/cas-clients">Voir toutes les études de cas →</a></p>
</section>
'''

offres = S('offres')
offres = offres.replace('<div class="offre-ideal">Idéal pour : équipes marketing de 1 à 10 personnes sans profil data.</div>',
                        '<div class="offre-ideal">Idéal pour : équipes marketing de 1 à 10 personnes sans profil data.</div>\n        <a href="/contact?sujet=Formation" class="cas-cta-link" data-lead="offres_formation">En parler →</a>')
offres = offres.replace('<div class="offre-ideal">Idéal pour : PME en croissance sans responsable data en interne.</div>',
                        '<div class="offre-ideal">Idéal pour : PME en croissance sans responsable data en interne.</div>\n        <a href="/contact?sujet=Accompagnement" class="cas-cta-link" data-lead="offres_accompagnement">En parler →</a>')
offres = offres.replace('<span class="label">Offres</span>\n  <h2 id="offres-title">Trois étapes pour reprendre la main</h2>\n', '<h2 id="offres-title" class="sr-only">Les offres</h2>\n')

# ---------- Pages ----------
page('index.html',
     'Metricmind — Votre site perd des conversions. Je vous montre où.',
     'Metricmind aide les PME à mesurer correctement leurs conversions : scan gratuit Trackmap, audit mesure & conversions, formation GA4 et Looker Studio.',
     '/',
     S('hero') + '\n' + S('problem') + '\n' + HOME_OFFRES + '\n' + HOME_PROOF + '\n' + S('temoignages') + '\n' +
     cta_band('Prêt à voir où se cache <em>votre performance ?</em>', 'Un échange de 30 minutes, gratuit et sans engagement. Je vous dis honnêtement si je peux vous aider.', 'home_cta'),
     extra_head=JSONLD)

page('offres.html',
     'Offres — Scan, audit mesure & conversions, formation | Metricmind',
     'Scan Trackmap gratuit, audit mesure & conversions à prix fixe, formation GA4 et Looker Studio, accompagnement continu : les offres Metricmind pour les PME.',
     '/offres',
     page_head('Offres', 'Trois étapes pour reprendre la main sur vos conversions',
               "On commence par un état des lieux gratuit. Ensuite, on corrige ce qui fuit. Enfin, votre équipe apprend à s'en servir seule.") +
     '\n' + offres + '\n' + S('expertises') + '\n' +
     cta_band('Vous ne savez pas par où <em>commencer ?</em>', 'Commencez par le scan gratuit : on saura en 30 minutes ce qui mérite votre attention.', 'offres_cta'))

page('cas-clients.html',
     'Études de cas & témoignages | Metricmind',
     'Server-side, migration Adobe sur 40 pays, montée en compétences GA4, reporting BigQuery : des résultats concrets, pas des livrables.',
     '/cas-clients',
     page_head('Cas clients', 'Des résultats concrets, pas des livrables', 'Quelques missions représentatives, anonymisées, et ce qu’en disent ceux avec qui j’ai travaillé.') +
     '\n' + cas.replace('<span class="label">Études de cas</span>\n  <h2 id="cas-title">Des résultats concrets, pas des livrables.</h2>\n', '<h2 id="cas-title" class="sr-only">Études de cas</h2>\n') +
     '\n' + S('temoignages') + '\n' +
     cta_band('Une situation <em>similaire ?</em>', 'Parlons-en. 30 minutes suffisent pour savoir si je peux vous aider.', 'cas_cta'))

page('a-propos.html',
     'À propos — Malick, consultant Data & Performance | Metricmind',
     "Consultant data senior depuis 2008, côté agence et annonceur. Tracking, server-side, GA4, Adobe, BigQuery : la technique au service des décisions.",
     '/a-propos',
     page_head('À propos', 'Quinze ans à faire parler les données, côté agence et côté annonceur',
               'Je suis Malick, consultant senior Data & Performance. Avec Metricmind, j’aide les PME à mesurer correctement ce qui compte, et à s’en servir pour décider.') +
     '\n' + S('about').replace('<span class="label">À propos</span>\n','') + '\n' + S('logos') + '\n' + S('outils') + '\n' +
     cta_band('Envie d’en <em>parler ?</em>', 'Un échange de 30 minutes, gratuit et sans engagement.', 'apropos_cta'))

page('contact.html',
     'Contact — Parlons de votre situation | Metricmind',
     'Réservez un créneau de 30 minutes ou laissez un message : scan Trackmap, audit mesure & conversions, formation.',
     '/contact',
     re.sub(r'<h2 class="contact-title" id="contact-title">(.*?)</h2>', r'<h1 class="contact-title" id="contact-title">\1</h1>', S('contact'), flags=re.S), float_cta=False)

# ---------- Trackmap : contenu propre, chrome commun ----------
tm = open(os.path.join(SRC, 'trackmap_body.html'), encoding='utf-8').read()
tm_css = open(os.path.join(SRC, 'trackmap.css'), encoding='utf-8').read()
page('trackmap.html',
     'Trackmap — ce qui tourne vraiment sur votre site | Metricmind',
     'Trackmap cartographie tous les outils de mesure, publicité et marketing qui se déclenchent sur votre site, avant et après le bandeau cookies, et détecte les anomalies RGPD.',
     '/trackmap', tm, page_style=tm_css)
