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

JSONLD = '<script type="application/ld+json">\n{"@context": "https://schema.org", "@type": "ProfessionalService", "@id": "https://metricmind.fr/#org", "name": "Metricmind", "url": "https://metricmind.fr/", "logo": "https://metricmind.fr/icon-512.png", "email": "contact@metricmind.fr", "description": "Metricmind aide les PME à mesurer correctement leurs conversions : scan Trackmap gratuit, audit mesure & conversions, formation GA4 et Looker Studio, accompagnement data.", "areaServed": {"@type": "Country", "name": "France"}, "address": {"@type": "PostalAddress", "addressLocality": "Bois-Colombes", "postalCode": "92270", "addressCountry": "FR"}, "founder": {"@id": "https://metricmind.fr/a-propos#malick"}, "knowsAbout": ["Google Analytics 4", "Google Tag Manager", "Tracking server-side", "Addingwell", "Shopify", "Consent Mode v2", "Mesure des conversions", "Looker Studio", "Adobe Analytics", "Piano Analytics", "BigQuery", "CRO"], "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Offres Metricmind pour les PME", "itemListElement": [{"@type": "Offer", "name": "Scan Trackmap", "price": "0", "priceCurrency": "EUR", "url": "https://metricmind.fr/trackmap", "itemOffered": {"@type": "Service", "name": "Scan Trackmap", "description": "Cartographie des outils de mesure et de publicité d\'un site, avant et après le bandeau cookies, restituée en 30 minutes."}}, {"@type": "Offer", "name": "Audit mesure & conversions", "url": "https://metricmind.fr/offres", "itemOffered": {"@type": "Service", "name": "Audit mesure & conversions", "description": "Vérification de la mesure du clic publicitaire jusqu\'au lead ou à la vente, localisation des conversions perdues et pilotage des corrections."}}, {"@type": "Offer", "name": "Formation & autonomie", "url": "https://metricmind.fr/offres", "itemOffered": {"@type": "Service", "name": "Formation GA4, Looker Studio et GTM", "description": "Formation des équipes marketing sur leurs propres données pour être autonomes sur leurs rapports."}}, {"@type": "Offer", "name": "Accompagnement continu", "url": "https://metricmind.fr/offres", "itemOffered": {"@type": "Service", "name": "Référent data à temps partagé"}}]}}\n</script>\n'
PERSON_LD = '<script type="application/ld+json">\n{"@context": "https://schema.org", "@type": "Person", "@id": "https://metricmind.fr/a-propos#malick", "name": "Malick Ba", "jobTitle": "Consultant senior Data & Performance", "worksFor": {"@id": "https://metricmind.fr/#org"}, "url": "https://metricmind.fr/a-propos", "sameAs": ["https://www.linkedin.com/in/malick-ba-a3a88337/"], "knowsAbout": ["Google Analytics 4", "Adobe Analytics", "Piano Analytics", "Shopify", "Addingwell", "Google Tag Manager", "Tracking server-side", "BigQuery", "dbt", "Optimizely", "Microsoft Clarity", "Commanders Act"], "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "Certification Google Analytics"}, {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "Certification Piano Analytics"}, {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "Certification Commanders Act"}]}\n</script>\n'
FAQ_LD = '<script type="application/ld+json">\n{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Qu\'est-ce qu\'un audit de la mesure des conversions ?", "acceptedAnswer": {"@type": "Answer", "text": "C\'est la vérification, étape par étape, que vos conversions sont correctement mesurées : du clic sur une publicité Google, Meta ou LinkedIn jusqu\'au formulaire, au panier ou au CRM. L\'objectif est de localiser les conversions perdues ou mal attribuées et de dire ce qu\'elles vous coûtent."}}, {"@type": "Question", "name": "Comment savoir si mon site perd des conversions dans la mesure ?", "acceptedAnswer": {"@type": "Answer", "text": "Les signes habituels : des écarts entre GA4, vos plateformes publicitaires et votre CRM, une baisse des données depuis l\'installation du bandeau cookies, ou des campagnes dont personne ne sait dire lesquelles rapportent. Le scan Trackmap gratuit permet de le vérifier rapidement."}}, {"@type": "Question", "name": "Faut-il me donner des accès à mes outils ?", "acceptedAnswer": {"@type": "Answer", "text": "Pas pour le scan Trackmap, qui analyse ce que votre site envoie publiquement. Pour l\'audit complet, un accès en lecture à GA4, Google Tag Manager et vos plateformes publicitaires est nécessaire."}}, {"@type": "Question", "name": "Travaillez-vous avec notre agence ou notre intégrateur ?", "acceptedAnswer": {"@type": "Answer", "text": "Oui. Je fournis un plan de corrections priorisé, avec qui fait quoi, et je pilote les corrections avec votre agence, votre intégrateur ou votre équipe interne, puis je vérifie que tout fonctionne."}}, {"@type": "Question", "name": "Sur quels outils portent les formations ?", "acceptedAnswer": {"@type": "Answer", "text": "Principalement Google Analytics 4, Looker Studio et Google Tag Manager, sur vos propres comptes et vos propres données. J\'interviens aussi sur Adobe Analytics et Piano Analytics."}}, {"@type": "Question", "name": "Combien coûte l\'audit ?", "acceptedAnswer": {"@type": "Answer", "text": "L\'audit est vendu à prix fixe, annoncé avant de commencer. Il dépend de la taille du site et du nombre d\'outils ; le scan Trackmap gratuit permet d\'en cadrer le périmètre."}}]}\n</script>\n'
FAQ_HTML = '<section id="faq" aria-labelledby="faq-title">\n  <span class="label">Questions fréquentes</span>\n  <h2 id="faq-title">Avant de se lancer</h2>\n  <div class="faq">\n    <details><summary>Qu\'est-ce qu\'un audit de la mesure des conversions ?</summary><p>C\'est la vérification, étape par étape, que vos conversions sont correctement mesurées : du clic sur une publicité Google, Meta ou LinkedIn jusqu\'au formulaire, au panier ou au CRM. L\'objectif est de localiser les conversions perdues ou mal attribuées et de dire ce qu\'elles vous coûtent.</p></details>\n    <details><summary>Comment savoir si mon site perd des conversions dans la mesure ?</summary><p>Les signes habituels : des écarts entre GA4, vos plateformes publicitaires et votre CRM, une baisse des données depuis l\'installation du bandeau cookies, ou des campagnes dont personne ne sait dire lesquelles rapportent. Le scan Trackmap gratuit permet de le vérifier rapidement.</p></details>\n    <details><summary>Faut-il me donner des accès à mes outils ?</summary><p>Pas pour le scan Trackmap, qui analyse ce que votre site envoie publiquement. Pour l\'audit complet, un accès en lecture à GA4, Google Tag Manager et vos plateformes publicitaires est nécessaire.</p></details>\n    <details><summary>Travaillez-vous avec notre agence ou notre intégrateur ?</summary><p>Oui. Je fournis un plan de corrections priorisé, avec qui fait quoi, et je pilote les corrections avec votre agence, votre intégrateur ou votre équipe interne, puis je vérifie que tout fonctionne.</p></details>\n    <details><summary>Sur quels outils portent les formations ?</summary><p>Principalement Google Analytics 4, Looker Studio et Google Tag Manager, sur vos propres comptes et vos propres données. J\'interviens aussi sur Adobe Analytics et Piano Analytics.</p></details>\n    <details><summary>Combien coûte l\'audit ?</summary><p>L\'audit est vendu à prix fixe, annoncé avant de commencer. Il dépend de la taille du site et du nombre d\'outils ; le scan Trackmap gratuit permet d\'en cadrer le périmètre.</p></details>\n  </div>\n</section>\n'

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
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
    <a href="/offres#audit" class="ho main"><span class="ho-n">02 · Prix fixe</span><span class="ho-t">Audit mesure & conversions</span><span class="ho-d">Du clic publicitaire jusqu'au lead ou à la vente : je localise les conversions perdues et je pilote les corrections.</span><span class="ho-go">Voir l'offre →</span></a>
    <a href="/offres#formation" class="ho"><span class="ho-n">03</span><span class="ho-t">Formation & autonomie</span><span class="ho-d">Votre équipe marketing apprend à trouver ses réponses dans GA4 et à construire des tableaux de bord utiles.</span><span class="ho-go">Voir l'offre →</span></a>
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

OFFRES_NAV = '''<div class="offres-nav" role="navigation" aria-label="Sommaire des offres">
  <a href="#scan"><span>01</span> Scan Trackmap</a>
  <a href="#audit"><span>02</span> Audit mesure & conversions</a>
  <a href="#formation"><span>03</span> Formation & autonomie</a>
  <a href="#accompagnement"><span>04</span> Accompagnement continu</a>
</div>
'''

# ---------- Pages ----------
page('index.html',
     'Mesure des conversions pour les PME | Metricmind',
     'Metricmind aide les PME à mesurer correctement leurs conversions : scan gratuit Trackmap, audit mesure & conversions, formation GA4 et Looker Studio.',
     '/',
     S('hero') + '\n' + S('references') + '\n' + S('problem') + '\n' + HOME_OFFRES + '\n' + HOME_PROOF + '\n' + S('temoignages') + '\n' +
     cta_band('Prêt à voir où se cache <em>votre performance ?</em>', 'Un échange de 30 minutes, gratuit et sans engagement. Je vous dis honnêtement si je peux vous aider.', 'home_cta'),
     extra_head=JSONLD)

page('offres.html',
     'Offres PME : scan, audit des conversions, formation | Metricmind',
     'Scan Trackmap gratuit, audit mesure & conversions à prix fixe, formation GA4 et Looker Studio, accompagnement continu : les offres Metricmind pour les PME.',
     '/offres',
     page_head('Offres PME', 'Trois étapes pour reprendre la main sur vos conversions',
               "Des offres pensées pour les PME qui investissent en acquisition. On commence par un état des lieux gratuit, on corrige ce qui fuit, puis votre équipe apprend à s'en servir seule.") +
     OFFRES_NAV +
     '\n' + offres + '\n' + S('expertises') + '\n' + FAQ_HTML + '\n' +
     cta_band('Vous ne savez pas par où <em>commencer ?</em>', 'Commencez par le scan gratuit : on saura en 30 minutes ce qui mérite votre attention.', 'offres_cta'),
     extra_head=FAQ_LD)

page('cas-clients.html',
     'Études de cas et témoignages | Metricmind',
     'Server-side, migration Adobe sur 40 pays, montée en compétences GA4, reporting BigQuery : des résultats concrets, pas des livrables.',
     '/cas-clients',
     page_head('Cas clients', 'Des résultats concrets, pas des livrables', 'Quelques missions représentatives, anonymisées, et ce qu’en disent ceux avec qui j’ai travaillé.') +
     '\n' + cas.replace('<span class="label">Études de cas</span>\n  <h2 id="cas-title">Des résultats concrets, pas des livrables.</h2>\n', '<h2 id="cas-title" class="sr-only">Études de cas</h2>\n') +
     '\n' + S('temoignages') + '\n' +
     cta_band('Une situation <em>similaire ?</em>', 'Parlons-en. 30 minutes suffisent pour savoir si je peux vous aider.', 'cas_cta'))

page('a-propos.html',
     'À propos de Malick, consultant Data & Performance | Metricmind',
     "Consultant data senior depuis 2008, côté agence et annonceur. Tracking, server-side, GA4, Adobe, BigQuery : la technique au service des décisions.",
     '/a-propos',
     page_head('À propos', 'Quinze ans à faire parler les données, côté agence et côté annonceur',
               'Je suis Malick, consultant senior Data & Performance. Avec Metricmind, j’aide les PME à mesurer correctement ce qui compte, et à s’en servir pour décider.') +
     '\n' + S('about').replace('<span class="label">À propos</span>\n','') + '\n' + S('references') + S('logos') + '\n' + S('outils') + '\n' +
     cta_band('Envie d’en <em>parler ?</em>', 'Un échange de 30 minutes, gratuit et sans engagement.', 'apropos_cta'),
     extra_head=PERSON_LD)

page('contact.html',
     'Contact | Metricmind',
     'Réservez un créneau de 30 minutes ou laissez un message : scan Trackmap, audit mesure & conversions, formation.',
     '/contact',
     re.sub(r'<h2 class="contact-title" id="contact-title">(.*?)</h2>', r'<h1 class="contact-title" id="contact-title">\1</h1>', S('contact'), flags=re.S), float_cta=False)

# ---------- Trackmap : contenu propre, chrome commun ----------
tm = open(os.path.join(SRC, 'trackmap_body.html'), encoding='utf-8').read()
tm_css = open(os.path.join(SRC, 'trackmap.css'), encoding='utf-8').read()
tm_faq = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', tm, flags=re.S)
TM_LD = '<script type="application/ld+json">\n' + __import__('json').dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',r)}} for q,r in tm_faq]}, ensure_ascii=False) + '\n</script>\n'
page('trackmap.html',
     'Trackmap : ce qui tourne vraiment sur votre site | Metricmind',
     'Trackmap cartographie tous les outils de mesure, publicité et marketing qui se déclenchent sur votre site, avant et après le bandeau cookies, et détecte les anomalies RGPD.',
     '/trackmap', tm, page_style=tm_css, extra_head=TM_LD)
