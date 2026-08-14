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
| `sections/aelo-product.liquid` | Page produit : galerie, bénéfices, urgence, offres radio (Découverte / Sérénité / Pack Duo), compte à rebours, garantie, FAQ |
| `sections/header-group.json` | Bandeau « OFFRE LIMITÉE » crème + logo centré |
| `templates/index.json` | Page d'accueil recomposée |
| `templates/product.json` | Page produit recomposée |
| `config/settings_data.json` | Palette crème/brun + boutons bruns |

Ces fichiers sont déployés sur le thème **« Talyss — v5 · Style AELOPARIS »**
(non publié) de la boutique `0fxqbv-9z.myshopify.com`. Les autres fichiers du
thème proviennent de Horizon et ne sont pas versionnés ici.

## À personnaliser dans l'éditeur de thème

- Les **avis clients** et la ligne « Noté Excellent » sont des exemples : remplacez-les
  par de vrais avis dès que vous en avez.
- Les offres de la page produit pointent vers les variantes réelles
  (Découverte 34,99 €, Sérénité 44,99 €, Pack Duo 59,90 €) — modifiables bloc par bloc.
