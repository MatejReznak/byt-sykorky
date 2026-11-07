# Byt 1.8 Sýkorky – pôdorys a 3D plánovač

Stránka: https://matejreznak.github.io/byt-sykorky/

- `index.html` – hotová stránka (pôdorys, nábytok, 3D s realistickým svetlom).
- Rozloženie nábytku sa ukladá do súboru `data/layout.json` vo vetve **data** (každé uloženie = commit, história = záloha).
- Ukladanie: v hlavičke stránky klikni na stav a vlož GitHub token (fine-grained, len tento repozitár, Contents: Read and write). Token sa uloží iba v danom prehliadači. Bez tokenu je stránka len na čítanie.

- **Verzie:** v hlavičke je výber verzie (Verzia 1 = `data/layout.json`, ďalšie v `data/versions/`, názvy v `data/versions.json`). Nová verzia = kópia aktuálnej.
- **Fotka pre Gemini:** v 3D → Fotka → ✨ Pre Gemini – fotka + pripravený pokyn na fotorealistický obrázok.
- Na telefóne je stránka len na prezeranie (pôdorys sa nedá upravovať, nič sa neukladá).

## Úpravy
Zdrojové súbory sú v `src/`. Po zmene spusti `./build.sh`, ktorý vytvorí `index.html`.
