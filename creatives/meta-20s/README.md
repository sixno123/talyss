# Créa Meta Ads — `talyss-meta-20s.mp4`

Seconde créa, remontée à partir des **mêmes rushes** que `../talyss-final.mp4` :
nouvel ordre de plans, format court, script resserré. Angle problème → solution
conservé.

| | |
|---|---|
| Durée | 21,9 s · 720×1280 · 30 fps |
| Vidéo | H.264 CRF 18, `+faststart` |
| Audio | AAC 192 kb/s · 44,1 kHz · stéréo |
| Niveau | −14,3 LUFS intégré |

Tout est produit par `build.py`.

## Montage

14 plans, ~19,2 s d'images puis 2,7 s de carte de fin. Chaque plan est pris
**à l'intérieur d'une seule scène du rush** (coupes détectées au préalable), pour
ne jamais démarrer ni finir sur une transition d'origine.

L'ordre suit les répliques : institut → talons secs → alternatives en N&B →
présentation de l'appareil → action → résultat → sandales → carte.

## Voix off

⚠️ **La voix est recoupée dans la bande existante, pas réenregistrée.**
ElevenLabs a refusé tous les appels au moment du montage
(`MCP error -32602: Unknown tool: text_to_speech`, dans les deux formes d'appel),
donc impossible de graver un texte inédit. Le script est un **remontage** de
6 extraits de la voix des 47 s, découpés au mot près grâce à `../words.json` :

1. Avant, c'était pédicure toutes les 3 semaines, parce que mes talons étaient une catastrophe.
2. râpes manuelles, soit ça irrite, soit ça ne fait rien.
3. Et puis, une amie m'a fait découvrir la râpe électrique Talyss.
4. elle enlève toute la peau morte, sans douleur.
5. Résultat : des pieds incroyablement doux et lisses.
6. Les stocks partent vite, alors commandez maintenant sur Talyss !

Pour un texte réellement neuf, regénérer la voix quand ElevenLabs répond, puis
remplacer le bloc `VO` de `build.py` — le reste de la chaîne suit tout seul.

## Sous-titres

Les mots sont recalés sur la nouvelle timeline à partir de `../words.json`
(décalage par segment), donc **aucune retranscription n'est nécessaire** : le
karaoké mot par mot et les mots-clés dorés se recalculent tout seuls.

**Fond plein noir** au lieu du bandeau flouté de la créa 47 s : un aplat opaque
efface l'ancien texte incrusté sans avoir besoin de flou.

Deux contraintes se croisent sur sa position, et elles tirent en sens inverse :

- il doit couvrir l'ancien texte incrusté, à `y 960–1090` ;
- les sous-titres doivent rester au-dessus de l'interface Reels, qui démarre
  vers `y 1024`.

D'où un bandeau **agrandi vers le haut** (`y 870–1100`) avec le texte à `y 985` :
le bloc de texte tombe vers 950–1020, dans la zone sûre, et le bas du bandeau
couvre quand même l'ancien texte. Le déplacer vers le haut sans l'agrandir
aurait redécouvert le bas des anciens sous-titres.

Découpe des cartons : fermeture forcée en fin de phrase (sinon la fin d'une
réplique et le début de la suivante partagent une ligne) **et** mesure de la
largeur réelle en Montserrat ExtraBold 54 px — compter les mots ne suffit pas,
quatre mots longs débordent du cadre. 23 cartons, le plus large à 609 px pour
une limite de 610.

## Points de vigilance

- **Conformité Meta.** L'angle « problème » est conservé à la demande du client.
  Meta restreint l'avant/après et les gros plans de peau abîmée en beauté/santé :
  ce montage peut voir sa diffusion limitée. Les plans « problème » et les plans
  « résultat » ne sont jamais juxtaposés directement, et le témoignage reste à la
  première personne (« mes talons »), jamais « vos talons ».
- **Droits.** Les images restent celles du montage d'origine, y compris deux
  plans où une personne est reconnaissable face caméra. À vérifier avant diffusion.

## Régénérer

```bash
python3 build.py     # voix, plans, sous-titres et rendu final
```
