"""Application logos of the Discord cards, copied from homarr-labs/dashboard-icons (Apache-2.0).

    python tools/apps.py        -> discord/apps/<name>.png (128 px)

jsDelivr no longer serves dashboard-icons straight from GitHub (repository over its 50 MB limit):
the logos used by the cards live here, next to the emblems, under the same tag.
"""
import io
import pathlib
import subprocess
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/homarr-labs/dashboard-icons"
SIZE = 128

# Every name an ICON() of the relay or Jarvis can ask for
ICONS = """
alertmanager alloy alpine-linux ansible cadvisor crowdsec docker evebox flaresolverr fortinet gitlab glpi
grafana harbor homepage hp linux loki mariadb n8n netgear nvidia ollama open-webui openbao opentofu outline
plex portabase portainer postgres prometheus prowlarr proxmox python qbittorrent radarr recyclarr redis
renovate seerr sonarr tailscale traefik
""".split()


def head():
    out = subprocess.run(["git", "ls-remote", REPO, "HEAD"], capture_output=True, text=True, check=True)
    return out.stdout.split()[0]


def main():
    sha = head()
    out = ROOT / "discord" / "apps"
    out.mkdir(parents=True, exist_ok=True)
    for name in ICONS:
        url = f"https://raw.githubusercontent.com/homarr-labs/dashboard-icons/{sha}/png/{name}.png"
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "astrocorp-brand"}), timeout=30) as r:
            img = Image.open(io.BytesIO(r.read())).convert("RGBA")
        img.thumbnail((SIZE, SIZE), Image.LANCZOS)
        img.save(out / f"{name}.png", optimize=True)
    print(f"{len(ICONS)} logos from dashboard-icons@{sha[:8]}")


if __name__ == "__main__":
    main()
