<p align="center">
  <img src=".readme/header.svg" alt="Astrocorp - Une galaxie de divisions pour un seul serveur" width="900">
</p>

## À quoi ça sert ?

L'identité visuelle d'Astrocorp, le homelab d'astronas : un emblème par division, qui signe les notifications Discord du relais n8n. Ce dépôt est le seul à être public sur GitHub, pour que Discord puisse charger les images par jsDelivr ; il ne contient que des dessins.

## Principe

<p align="center">
  <img src=".readme/principle.svg" alt="Principe" width="900">
</p>

## Les divisions

| Emblème | Division | Signe | Accent |
|---|---|---|---|
| <img src="discord/astrocorp.png" width="48"> | **Astrocorp** | la maison mère : pied de toutes les cartes | ambre `#e0a458` |
| <img src="discord/astrops.png" width="48"> | **AstrOps** | supervision : alertes de Prometheus | turquoise `#4fd1c5` |
| <img src="discord/astro-security.png" width="48"> | **Astro Security** | SOC : alertes de CrowdSec | violet `#a78bfa` |
| <img src="discord/astro-forge.png" width="48"> | **Astro Forge** | CI/CD : pipelines GitLab en échec, déploiements | ambre `#e0a458` |
| <img src="discord/astro-core.png" width="48"> | **Astro Core** | infrastructure : notifications de Proxmox | bleu `#60a5fa` |
| <img src="discord/astro-update.png" width="48"> | **Astro Update** | mises à jour des applications par Renovate | vert `#4ade80` |
| <img src="discord/jarvis.png" width="48"> | **Jarvis** | le majordome : météo de l'infrastructure chaque matin à 7 h | aurore `#fbbf24` |

Fond commun : le ciel nocturne du portail Homepage (bleu-vert profond, étoiles, cœur ambré de la Voie lactée).

## Fichiers

| Chemin | Rôle |
|---|---|
| `tools/emblems.py` | dessine les emblèmes (SVG), puis les convertit en PNG fixe et en GIF animé par Chrome sans écran |
| `svg/` | emblèmes vectoriels, source de vérité |
| `discord/` | emblèmes fixes (PNG 256 px, avatars) et animés (GIF 160 px, vignettes des cartes), servis par `https://cdn.jsdelivr.net/gh/Astr0corp/<dépôt>@<étiquette>/discord/<division>.png` ou `.gif` |

## Publier une nouvelle version

1. Modifier `tools/emblems.py`, puis `python tools/emblems.py`.
2. Commit, étiquette `vX` (jsDelivr garde en cache une étiquette donnée pour toujours : une nouvelle image demande une nouvelle étiquette).
3. Changer l'étiquette dans les cartes du relais (`n8n-workflows`, constante `BRAND`).
