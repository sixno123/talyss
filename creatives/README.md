# Créatives vidéo

## `talyss-vo-fr.mp4`

Vidéo publicitaire Talyss avec voix off féminine française ajoutée.
Vidéo source muette (46,97 s · 720×1280 · 30 fps) + piste voix générée.

| | |
|---|---|
| Durée | 46,97 s (vidéo et audio alignées) |
| Vidéo | H.264 copiée telle quelle (aucun ré-encodage, qualité d'origine) |
| Audio | AAC 192 kb/s · 44,1 kHz · stéréo |
| Niveau | −14,1 LUFS intégré, true peak −1,5 dBTP (norme réseaux sociaux) |
| Voix | ElevenLabs `eleven_multilingual_v2`, voix « Charlotte » (`XB0fDUnXU5powFXDhCwa`), `language_code=fr` |

### Script dit par la voix off

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

Les nombres sont écrits en toutes lettres (« trois semaines », « soixante disques »)
pour éviter toute lecture erronée par la synthèse vocale.

### Mise à la durée

La voix brute durait 52,74 s pour une vidéo de 46,97 s. Plutôt que d'accélérer
la lecture de 12 % (effet précipité), `fit-voix.py` raccourcit les silences
entre les phrases à 0,30 s maximum et supprime le silence final — ce qui
récupère 4,78 s **sans toucher au débit de parole**. Le reliquat est absorbé
par un `atempo=1.01669` (+1,7 %, inaudible).

La phrase d'appel à l'action démarre à ~43,0 s, juste avant l'apparition de la
carte de fin à 43,77 s.

### Point de vigilance

⚠️ La vidéo source contient des **sous-titres incrustés d'un autre script**
(mot à mot, marque « Mielle Glow ») qui ne correspondent pas à ce texte, et sa
carte de fin affiche « Mielle GLOW − 50 % » au lieu de Talyss. La voix off est
correcte, mais l'image reste à retravailler avant diffusion.

### Régénérer

```bash
# 1. générer la voix (ElevenLabs, voix Charlotte, fr)
# 2. resserrer les silences
python3 fit-voix.py                     # vo_raw.mp3 -> vo_tight.wav

# 3. tempo + normalisation en deux passes + calage sur la durée vidéo
ffmpeg -i vo_tight.wav -af "atempo=1.01669" vo_tempo.wav
ffmpeg -i vo_tempo.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null -
ffmpeg -i vo_tempo.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=…:linear=true,\
afade=t=out:st=46.45:d=0.30,apad=whole_dur=46.9667" vo_final.wav

# 4. muxer (vidéo copiée, jamais ré-encodée)
ffmpeg -i source.mp4 -i vo_final.wav -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart talyss-vo-fr.mp4
```
