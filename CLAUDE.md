# Instrukcje dla Claude

## Komenda „Filmy”

Kiedy użytkownik napisze **„Filmy”** i wyśle filmiki (zwykle 3 lub więcej), wykonaj bez dopytywania:

1. **Wyciągnij napisy z ekranu z każdego filmu** – dokładnie, co do klatki:
   - dla każdego napisu podaj, od kiedy do kiedy jest widoczny,
   - czasy podawaj **prosto, co pół sekundy, jak na osi CapCut**: `3.00`, `3.30`, `4.00`, `4.30`… (`.30` = pół sekundy). Bez klatek, bez setnych, zaokrąglaj do najbliższego pół sekundy,
   - zaznacz też momenty, kiedy na ekranie **nie ma żadnego napisu**,
   - przepisz oryginalny tekst 1:1, ze wszystkimi znakami i emotkami.
   - Metoda: `ffmpeg` (klatki co 0,5 s + wykrywanie cięć `select='gt(scene,0.2)'` + klatka po klatce w miejscach zmian napisu).
2. **Przetłumacz każdy napis na polski** – z zachowaniem wszystkich znaków, emotek i stylu (np. ✨, 😭, 👇🏻, cudzysłowy, wielkie litery), gotowe do wklejenia w CapCut.
3. **Na dole, do każdego filmu, krótki opis po polsku** na YouTube / TikTok / Facebook / Instagram: krótko, chwytliwie, z CTA (np. „Skomentuj …”) i kilkoma hashtagami.
4. **Wszystko po polsku.**
5. Wynik zapisz też w pliku `filmy/AAAA-MM-DD.md` i wypchnij na gałąź.
