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
sur 174 images : bande **y 960–1090, x 142–581**. Elle est masquée par un
bandeau dépoli (`y 930–1120`) — flou gaussien σ=26, −26 % de luminosité,
saturation 0,62 — aux bords adoucis sur 26 px via `feather.png` + `alphamerge`,
pour que la bande ne se voie pas comme un rectangle collé.

`align.py` transcrit la voix off finale avec `faster-whisper` (mots horodatés),
puis `subs.py` réaligne le vrai script sur ces horodatages (`difflib`, 127/140
mots ancrés, le reste réparti dans les trous) et écrit `subs.ass` : 45 cartons
façon karaoké, Montserrat ExtraBold 54 px, « Talyss » en doré.

Deux détails de découpe : un carton ne se termine jamais sur un chiffre ou un mot
outil (« toutes les **3** » → « les 3 semaines »), et les mots non reconnus par
l'ASR sont répartis sur toute la durée du trou, sinon ils recevraient tous le
même départ et les cartons sortiraient dans le désordre.

### 3 · Carte de fin

`endcard.html` rendue en PNG par Chromium (×2 puis réduit en lanczos), incrustée
à partir de **43,75 s** — l'image exacte de la coupe d'origine (image 1313 ; un
seuil à 43,767 s laissait passer une image de l'ancienne carte « Mielle Glow »).

Palette et texte repris du thème : crème `#f2eee2`, brun `#7e4e26`, accent
`#a06a3f`, Montserrat + EB Garamond, et l'offre telle qu'elle est déjà écrite
dans la boutique — « Jusqu'à -40 % sur les packs + livraison offerte »,
« Peau douce garantie 90 jours ». **Aucune promotion n'a été inventée** :
si l'offre change, éditez `endcard.html` et refaites le rendu.

---

### Régénérer

```bash
sudo apt-get install -y ffmpeg fonts-montserrat fonts-inter fonts-ebgaramond
pip install faster-whisper pillow

python3 fit-voix.py     # vo_raw.mp3 -> vo_tight.wav (silences resserrés)
python3 align.py        # vo_final2.wav -> words.json (mots horodatés)
python3 subs.py         # words.json  -> subs.ass
python3 bbox.py         # (contrôle) position des anciens sous-titres

chromium --headless --force-device-scale-factor=2 --window-size=720,1280 \
  --screenshot=endcard_2x.png file://$PWD/endcard.html
ffmpeg -i endcard_2x.png -vf scale=720:1280:flags=lanczos endcard.png

ffmpeg -i source.mp4 -i vo_final2.wav \
  -loop 1 -framerate 30 -t 47 -i feather.png \
  -loop 1 -framerate 30 -t 47 -i endcard.png \
  -filter_complex "\
[0:v]split[b][p];\
[p]crop=720:190:0:930,gblur=sigma=26,eq=brightness=-0.26:saturation=0.62,format=rgb24[bandrgb];\
[2:v]format=gray[mask];[bandrgb][mask]alphamerge[band];\
[b][band]overlay=0:930[plated];[plated]ass=subs.ass[subbed];\
[subbed][3:v]overlay=0:0:enable='gte(t,43.75)',format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 18 -preset medium \
  -c:a aac -b:a 192k -movflags +faststart talyss-final.mp4
```

### Reste à faire avant diffusion

Les **images** viennent toujours du montage d'origine (pieds, sandales, plans du
produit). Seuls la voix, les sous-titres et la carte de fin sont à vous — pensez
à vérifier vos droits sur les rushes avant de lancer la campagne.
