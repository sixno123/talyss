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

## Photos de clientes (preuve sociale)

Comme sur AELOPARIS, les avatars sont de vraies photos rondes et non des initiales :

- `aelo-product.liquid` → réglage `social_avatars` : une URL par ligne (ou séparées par
  des virgules). Repli automatique sur `social_initials` si le champ est vide.
- `aelo-reviews.liquid` → par bloc d'avis : `avatar` (sélecteur d'image) ou `avatar_url`,
  repli sur l'initiale du prénom.

Les 5 photos sont hébergées sur le CDN Shopify (`talyss-cliente-1..5.jpg`, 256×256,
~15 Ko chacune, recadrées en carré).

**Piège à connaître** : quand on ajoute un nouveau réglage à une section *et* qu'on
renseigne ce réglage dans un template JSON, il faut **deux envois séparés**. Shopify valide
le template contre le schéma déjà en place et supprime silencieusement les réglages qu'il
ne connaît pas encore.

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

## Talyss Fix™ — vitrine ruban (thème v8)

Second produit, second thème : **« Talyss Fix — v8 · Vitrine ruban »** (id `203529158999`,
non publié). Il réutilise toutes les sections `aelo-*` sans les modifier ; seuls les
templates changent. Le thème publié de la ponceuse reste intact.

| Fichier | Rôle |
|---|---|
| `talyss-fix/templates/index.json` | Accueil : hero « Fixez sans percer. », marquee, 3 gestes, avis, carte « Pensé pour les locataires » |
| `talyss-fix/templates/product.json` | Fiche ruban : 5 bénéfices, 3 offres, 4 questions fréquentes |
| `talyss-fix/sections/header-group.json` | Bandeau « FIXEZ SANS PERCER · LIVRAISON SUIVIE SOUS 24–48 H » |

L'accent brun est décalé vers le terracotta de la charte Fix par une section
`custom-liquid` placée en tête d'ordre (`accent`), qui redéfinit `--brown`, `--brown-d`
et `--serif-c` sur `.ae`. Aucune modification de `config/settings_data.json` n'est donc
nécessaire, et la ponceuse garde sa palette.

### Offres

| Bloc | Variante | Prix | Titre | Ruban |
|---|---|---|---|---|
| off1 | `54368982860119` (TLY-TAPE-1) | 24,90 € | 1 rouleau | — |
| off2 | `54368982892887` (TLY-TAPE-2) | 34,90 € | Pack locataire | LE PLUS CHOISI (présélectionné) |
| off3 | `54368982925655` (TLY-TAPE-4) | 49,90 € | Pack maison | MEILLEURE VALEUR |

Chaque offre a sa propre vignette via le nouveau réglage `image_url` du bloc `offer`
(`sections/aelo-product.liquid`). Sans valeur, la section retombe sur l'image principale
du produit.

### Ce qui n'est volontairement pas là

- **Pas de prix barré** : les variantes n'en ont aucun, et en France le prix de référence
  doit être le prix le plus bas pratiqué sur les 30 derniers jours.
- **Pas de barre de rareté** (`show_scarcity: false`) ni de note « Excellent »
  (`rating_text` vide) : aucun avis réel pour l'instant.
- **Pas de promesse « sans trace » ni de charge maximale en kg** tant que la variante
  exacte n'a pas été testée.
- Les 4 avis sont des exemples de structure, à remplacer avant toute publicité.

### Images

14 visuels préparés (recadrage carré, 1086–1254 px, marquage vert du mandrin retouché
sur 5 photos) et hébergés sur le CDN Shopify :

- Galerie produit : `talyss-fix-01-packshot` → `talyss-fix-07-cable`
- Vignettes d'offres : `talyss-fix-pack-1`, `-pack-2`, `-pack-4`
- Vitrine : `talyss-fix-hero`, `talyss-fix-etape-1`, `talyss-fix-etape-3`,
  `talyss-fix-approuvee` (l'étape 2 réutilise `talyss-fix-05-decoupe`)

### Reste à fournir avant publication

- Logo « Talyss FIX™ » détouré (PNG transparent) et favicon
- Photo lisible de l'étiquette : fabricant, adresse, référence ou lot
- Notice et avertissements en français (obligations GPSR)

Le produit reste en **brouillon** et le thème **non publié** tant que ces éléments ne sont
pas réunis.
