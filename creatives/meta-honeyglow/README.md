# Créa « Mielle Glow » → Talyss — deux versions

Rushes fournis : `4a78dbe0-…hd.mp4` (720×1280, 39,8 s, **avec voix off française**).
Contrairement à la première créa, la bande-son existe déjà : elle est conservée,
pas remplacée.

| | Version A | Version B |
|---|---|---|
| Fichier | `talyss-A.mp4` | `talyss-B.mp4` |
| Montage | ordre d'origine | remonté, 13 plans |
| Durée | 38,5 s | 19,9 s |
| Niveau | −14,3 LUFS | −14,3 LUFS |

Tout est produit par `build.py` (les deux versions en une passe).

## Le conflit de marque, et comment il est traité

La créa d'origine vend un concurrent. Trois traces, trois traitements :

| Trace | Où | Traitement |
|---|---|---|
| « honey glow » **dit** à 17,62–18,18 s | audio | **son coupé** sur ces mots |
| « Honey » **incrusté** vers 17,9 s | image, dans la bande de sous-titres | couvert par le cartouche |
| Carte de fin « Mielle GLOW − 50 % » | 36,07 s → fin | remplacée par la carte Talyss |
| « moins 50 % » **dit** à partir de 35,58 s | audio | absorbé par la carte de fin |

**On tait, on ne coupe pas.** Retirer 0,56 s de piste décalerait l'image ou
imposerait un saut visible en plein plan. Le silence, lui, ne décale rien — et
comme le sous-titre reste affiché, il porte « Talyss » exactement là où l'ancienne
marque était prononcée *et* incrustée. Le spectateur lit la bonne marque au bon
moment.

Le CTA d'origine (« clique, essaye et reviens me dire merci ») est neutre : gardé tel
quel. Seule la revendication −50 %, qui n'est pas l'offre Talyss, disparaît.

**Contrôle automatisé** : les deux sorties sont retranscrites après rendu et on vérifie
qu'aucune des chaînes `honey` / `glow` / `mielle` / `50 %` n'y figure — plutôt que de
s'en remettre à une écoute.

## Sous-titres

Sous-titres incrustés d'origine mesurés par profil des pixels quasi blancs :
**x 99–639, y 970–1053** — nettement plus larges que sur la créa précédente.
Le cartouche est dimensionné en conséquence (`x 60–680`, `y 920–1080`), avec deux
assertions dans `build.py` qui échouent si on le réduit sous cette emprise.

Position : texte à `y 985`, soit un bloc vers 950–1020, au-dessus de l'interface
Reels qui recouvre le bas à partir de `y 1024`. C'est pour tenir ces deux
contraintes opposées que le cartouche est plus haut que strictement nécessaire.

Habillage repris de `../meta-20s/` : cartouche blanc arrondi, texte encre `#1B1B1B`,
accent brun `#7E4E26`, Montserrat ExtraBold, karaoké mot par mot, mots-clés qui
restent colorés une fois prononcés.

**Le texte affiché est réécrit à la main.** L'ASR sert aux horodatages, pas aux mots :
il entend « crouchés », « racleés », « musiquet », « rappe », « faisse », « rédits ».
Les sous-titres affichent « croûtés », « ravagés », « moustiquaire », « râpe »,
« effet spa », « ready ».

## Découpe de la version B

Segments audio bornés sur des **mots entiers** : une borne approximative traînait un
fragment de la phrase voisine (« …résultat, rien. Et là, » au lieu de « …rien. »).
Une première sélection avait aussi fait tomber « et avec les 60 disques inclus » —
argument produit à ne pas perdre. Arc retenu :

1. crème, râpe, pierre, ponce, j'ai tout testé, résultat, rien
2. Puis j'ai testé **Talyss**, franchement, deux minutes, zéro galère
3. tu passes, la corne disparaît, résultat
4. T'as le talon ultra lisse et effet spa pédicure
5. et avec les **60 disques** inclus, je suis large tout l'été
6. clique, essaye et reviens me dire merci

La somme des plans (16,87 s) colle exactement à celle des segments audio, pour que
l'image ne devance pas la voix. Chaque plan tient dans une seule scène du rush.

La durée totale se cale sur `max(plans + carte, audio + 0,4 s)` : sans ça, `-t`
tronquait la piste et coupait le dernier mot du CTA.

## Points de vigilance

- **Attributs personnels (Meta).** L'accroche d'origine s'adresse au corps du
  spectateur (« toi tu as les pieds… ravagés par la misère »). C'est le type
  d'énoncé encadré par la politique Meta ; risque de refus ou de portée réduite.
  La **version A la conserve** — c'est le montage d'origine. La **version B démarre
  après**, sur « crème, râpe, pierre ponce… », qui raconte au lieu d'accuser.
- **Bandeau incrusté « 60 recharges disques offerts »** (~27 s) : il est au-dessus
  du cartouche, donc visible dans les deux versions. Le contenu est compatible avec
  Talyss (60 disques), mais « offerts » est une promesse à vérifier côté offre.
- **Droits.** Images et voix viennent du montage d'origine, avec des personnes
  reconnaissables face caméra. À vérifier avant diffusion.

## Régénérer

```bash
python3 build.py      # les deux versions
```
