# Talyss — Habillage « style AELOPARIS »

Fichiers de thème Shopify (base **Horizon**) qui donnent à la boutique Talyss le look
d'aeloparis.com : palette crème/brun, logo centré, hero avec offre, texte défilant,
section « 3 étapes », avis style Trustpilot, section « Approuvée par », et page produit
avec sélecteur de packs + compte à rebours.

## Contenu

| Fichier | Rôle |
|---|---|
| `assets/aelo.css` | Styles communs des sections AELO (préfixe `.ae-`) |
| `sections/aelo-hero.liquid` | Hero accueil : image + note + gros titre offre + CTA |
| `sections/aelo-marquee.liquid` | Texte géant défilant (livraison offerte, -40%…) |
| `sections/aelo-steps.liquid` | « Une ponceuse qui travaille *Pour Vous* » — 3 étapes |
| `sections/aelo-reviews.liquid` | Carrousel d'avis, étoiles vertes style Trustpilot |
| `sections/aelo-approved.liquid` | Carte « Approuvée par … » avec checklist + CTA |
| `sections/aelo-product.liquid` | Page produit : galerie, bénéfices, urgence, offres radio (Découverte / Sérénité / Pack Duo), compte à rebours, garantie, FAQ. Accepte aussi les **blocs d'app** (`@app`) — voir Moon Bundles ci-dessous |
| `sections/header-group.json` | Bandeau « OFFRE LIMITÉE » crème + logo centré |
| `templates/index.json` | Page d'accueil recomposée |
| `templates/product.json` | Page produit recomposée |
| `config/settings_data.json` | Palette crème/brun + boutons bruns |

Ces fichiers sont déployés sur le thème **« Talyss — v5 · Style AELOPARIS »**
(non publié) de la boutique `0fxqbv-9z.myshopify.com`. Les autres fichiers du
thème proviennent de Horizon et ne sont pas versionnés ici.

## Optimisation mobile (thème v7)

- `snippets/aelo-image.liquid` — images responsives (`srcset` 400→1400 px) partagées par
  le hero, les étapes et la section « Approuvée par ». Accepte un objet image ou une URL
  du CDN. **Attention au découpage Liquid** : le descripteur (`400w`) doit être précédé
  d'un espace réel, sinon le srcset est invalide.
- `sections/aelo-product.liquid` — barre d'achat fixe en bas sur mobile (révélée par
  `IntersectionObserver` quand le bouton principal sort de l'écran, bouton relié au
  formulaire par l'attribut `form=`), galerie en `scroll-snap` avec points sur mobile et
  vignettes cliquables sur bureau.
- `assets/aelo.css` — paliers 900 / 640 / 430 px, variable `--pad` pour les carrousels
  pleine largeur, `@media (hover:hover)` pour éviter les états collés au tap,
  `prefers-reduced-motion`.

Paliers de prix (variantes du produit ponceuse) : 1 = 34,99 € · 2 = 59,90 € · 3 = 79,90 €.

## Moon Bundles (app de bundles)

L'app **Moon Bundles** (CScorp LLC) est installée sur la boutique. Ses bundles se
configurent dans l'app elle-même (base de données de l'app, pas l'API Shopify), et son
widget s'insère dans le thème sous forme de **bloc d'app**.

`sections/aelo-product.liquid` déclare `{"type": "@app"}` dans son schéma et rend les
blocs d'app juste au-dessus du bouton d'ajout au panier. Deux interrupteurs permettent
d'éviter les doublons avec les offres codées en dur :

- `show_offers` — décocher pour masquer le sélecteur d'offres intégré
- `show_atc` — décocher si le widget Moon Bundles affiche son propre bouton d'achat

Marche à suivre dans l'éditeur de thème : section « AELO — Page produit » →
*Ajouter un bloc* → **Moon Bundles** → décocher « Afficher mes offres intégrées ».

## À personnaliser dans l'éditeur de thème

- Les **avis clients** et la ligne « Noté Excellent » sont des exemples : remplacez-les
  par de vrais avis dès que vous en avez.
- Les offres de la page produit pointent vers les variantes réelles
  (Découverte 34,99 €, Sérénité 44,99 €, Pack Duo 59,90 €) — modifiables bloc par bloc.
