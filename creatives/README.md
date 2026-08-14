# Créatives vidéo

## `talyss-final.mp4`

Vidéo publicitaire Talyss : voix off féminine française, sous-titres calés sur
cette voix, et carte de fin aux couleurs Talyss.

| | |
|---|---|
| Durée | 47,0 s · 720×1280 · 30 fps |
| Vidéo | H.264 CRF 18, `+faststart` |
| Audio | AAC 192 kb/s · 44,1 kHz · stéréo |
| Niveau | −14,1 LUFS intégré, true peak −1,5 dBTP (norme réseaux sociaux) |
| Voix | ElevenLabs `eleven_multilingual_v2`, voix « Charlotte » (`XB0fDUnXU5powFXDhCwa`), `language_code=fr` |

La vidéo source était **muette** et portait les sous-titres incrustés et la carte
de fin d'une **autre marque** (« Mielle Glow »). Les trois problèmes ont été traités.

---

### 1 · Voix off

Script dit par la voix off :

> Voici comment j'ai arrêté de jeter mon argent dans les soins des pieds.
> Avant, c'était pédicure toutes les trois semaines… parce que mes talons étaient une catastrophe.
> Dès qu'ils séchaient, ça craquelait, et ça ressemblait à ça.
> Impossible de mettre des sandales ou des talons sans complexer.
> J'ai testé toutes les alternatives : pierre ponce, râpes manuelles… soit ça irrite, soit ça ne fait rien.
> Certaines, on dirait carrément des râpes à fromage !
> Et puis, une amie m'a fait découvrir la râpe électrique Talyss.
> Elle utilise des petits disques abrasifs à usage unique, et elle enlève toute la peau morte, sans douleur.
> Vitesse réglable, et ça marche sur peau sèche ou humide.
> Résultat : des pieds incroyablement doux et lisses.
> Le kit arrive avec soixante disques, de quoi tenir des mois.
> Les stocks partent vite, alors commandez maintenant sur Talyss !

Les nombres sont écrits en toutes lettres pour éviter une lecture erronée par la
synthèse vocale ; les sous-titres réaffichent « 3 » et « 60 ».

**Mise à la durée.** La voix brute durait 52,74 s pour 46,97 s de vidéo.
Plutôt que d'accélérer la lecture de 12 % (effet précipité), `fit-voix.py`
raccourcit les silences entre les phrases à 0,30 s maximum et supprime le silence
final — 4,78 s récupérées **sans toucher au débit de parole**. Le reliquat est
absorbé par un `atempo=1.01669` (+1,7 %, inaudible).

### 2 · Sous-titres

`bbox.py` localise les anciens sous-titres en profilant les pixels quasi blancs
sur 174 images : bande **y 960–1090, x 142–581**.

`make-mask.py` génère le masque qui l'efface. La zone **opaque** doit couvrir
cette boîte : un bandeau simplement plus court casserait le masquage (avec 45 px
de dégradé, un bandeau 940–1112 n'est plein qu'entre 985 et 1067, soit *dans*
l'ancien texte). Le bandeau est donc **plus haut mais au dégradé bien plus long** —
`y 905–1145`, fondu vertical de 45 px en smoothstep, cœur opaque 947–1102 — plus
un **fondu horizontal** pour qu'il ne touche pas les bords du cadre comme une
barre. Flou gaussien σ=34, −20 % de luminosité : c'est le flou qui détruit les
lettres, l'assombrissement ne fait que baisser le contraste.

`verify-mask.py` est le garde-fou : il rend le masque **sans** les nouveaux
sous-titres (blancs et au même endroit, ils seraient comptés comme des restes) et
profile la boîte d'origine. Résultat actuel : **816 862 → 85 pixels quasi blancs
(0,010 %)**, pire ligne 3 px sur 174 images.

`align.py` transcrit la voix off finale avec `faster-whisper` (mots horodatés),
puis `subs.py` réaligne le vrai script sur ces horodatages (`difflib`, 127/140
mots ancrés, le reste réparti dans les trous) et écrit `subs.ass` : 45 cartons,
131 événements, Montserrat ExtraBold 54 px.

**Karaoké mot par mot.** Un événement ASS par mot prononcé : le carton entier est
redessiné à chaque fois, seul le mot en cours passe en doré, au même `\pos` pour
que rien ne bouge. Le fondu n'est appliqué qu'aux **bords du carton**, sinon
chaque mot clignoterait.

**Mots-clés.** `sans douleur`, `doux et lisses`, `usage unique`, `60 disques`,
`peau morte`, `Talyss` restent dorés une fois prononcés (effet d'accumulation) —
ainsi le surlignage karaoké et la couleur mot-clé ne se disputent jamais le même
mot, sans avoir besoin d'une troisième couleur. Les expressions sont repérées sur
**tout le script**, pas carton par carton, pour que celles coupées par une
découpe (« …peau morte, sans » / « douleur ») se colorent des deux côtés.

Deux détails de découpe : un carton ne se termine jamais sur un chiffre ou un mot
outil (« toutes les **3** » → « les 3 semaines »), et les mots non reconnus par
l'ASR sont répartis sur toute la durée du trou, sinon ils recevraient tous le
même départ et les cartons sortiraient dans le désordre.

### 3 · Carte de fin

La carte est **fournie par le client** : `endcard-source.png` (941×1672), récupérée
depuis la branche `claude/shopify-boutique-design-yywqe5` où elle avait été déposée
à la racine. Soie rose, « Talyss » en serif, « -40 % » doré métallisé, rendu produit
avec les disques abrasifs.

Son ratio (0,5628) est à trois millièmes de la cible 720×1280 (0,5625) : un simple
`scale=720:1280:force_original_aspect_ratio=increase:flags=lanczos,crop=720:1280`
perd moins d'un demi-pixel de largeur. Aucun remplissage nécessaire, et tous les
éléments sont conservés — vérifié : « OFFRE LIMITÉE », le « -40 % » entier,
« Commandez maintenant » et « Peau douce garantie 90 jours ».

> Si une future carte a un ratio nettement différent (une image ChatGPT en 1024×1536,
> par exemple), **ne pas garder le rognage « cover »** : il retirerait ~66 px de
> chaque côté et couperait le « -40 % », qui court presque d'un bord à l'autre.
> Ajuster sur la largeur et compléter le haut/bas avec une copie floutée de l'image
> en arrière-plan, pour éviter la couture qu'un aplat crème laisserait sur la soie.

Elle est incrustée à partir de **43,75 s** — l'image exacte de la coupe d'origine
(image 1313 ; un seuil à 43,767 s laissait passer une image de l'ancienne carte
« Mielle Glow »).

`endcard.html` est la carte typographique qui servait avant, conservée comme repli :
palette du thème (crème `#f2eee2`, brun `#7e4e26`, accent `#a06a3f`) et offre reprise
telle quelle de la boutique, sans promotion inventée.

---

### Régénérer

```bash
sudo apt-get install -y ffmpeg fonts-montserrat fonts-inter fonts-ebgaramond
pip install faster-whisper pillow

python3 fit-voix.py     # vo_raw.mp3 -> vo_tight.wav (silences resserrés)
python3 align.py        # vo_final2.wav -> words.json (mots horodatés)
python3 make-mask.py    # -> feather.png (masque, vérifie qu'il couvre l'ancien texte)
python3 subs.py         # words.json  -> subs.ass (karaoké + mots-clés)
python3 bbox.py         # (contrôle) position des anciens sous-titres
python3 verify-mask.py  # (garde-fou) l'ancien texte a-t-il disparu ?

# carte de fin fournie -> normalisation (repli HTML : voir endcard.html)
ffmpeg -i endcard-source.png \
  -vf "scale=720:1280:force_original_aspect_ratio=increase:flags=lanczos,crop=720:1280" endcard.png

ffmpeg -i source.mp4 -i vo_final2.wav \
  -loop 1 -framerate 30 -t 47 -i feather.png \
  -loop 1 -framerate 30 -t 47 -i endcard.png \
  -filter_complex "\
[0:v]split[b][p];\
[p]crop=720:240:0:905,gblur=sigma=34,eq=brightness=-0.20:saturation=0.62,format=rgb24[bandrgb];\
[2:v]format=gray[mask];[bandrgb][mask]alphamerge[band];\
[b][band]overlay=0:905[plated];[plated]ass=subs.ass[subbed];\
[subbed][3:v]overlay=0:0:enable='gte(t,43.75)',format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 18 -preset medium \
  -c:a aac -b:a 192k -movflags +faststart talyss-final.mp4
```

### Reste à faire avant diffusion

Les **images** viennent toujours du montage d'origine (pieds, sandales, plans du
produit). Seuls la voix, les sous-titres et la carte de fin sont à vous — pensez
à vérifier vos droits sur les rushes avant de lancer la campagne.
