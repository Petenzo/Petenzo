# Instrukcje dla Claude

## Komenda „Filmy”

Kiedy użytkownik napisze **„Filmy”** i wyśle filmiki (zwykle 3 lub więcej), wykonaj bez dopytywania:

1. **Wyciągnij napisy z ekranu z każdego filmu** – dokładnie, co do klatki:
   - dla każdego napisu podaj, od kiedy do kiedy jest widoczny,
   - czasy podawaj w formacie **CapCut `MM:SS:KK`** (KK = klatka, 30 klatek = 1 sekunda, czyli `00:03:15` = 3,5 s), a obok w sekundach,
   - zaznacz też momenty, kiedy na ekranie **nie ma żadnego napisu**,
   - przepisz oryginalny tekst 1:1, ze wszystkimi znakami i emotkami.
   - Metoda: `ffmpeg` (klatki co 0,5 s + wykrywanie cięć `select='gt(scene,0.2)'` + klatka po klatce w miejscach zmian napisu).
2. **Przetłumacz każdy napis na polski** – z zachowaniem wszystkich znaków, emotek i stylu (np. ✨, 😭, 👇🏻, cudzysłowy, wielkie litery), gotowe do wklejenia w CapCut.
3. **Na dole, do każdego filmu, krótki opis po polsku** na YouTube / TikTok / Facebook / Instagram: krótko, chwytliwie, z CTA (np. „Skomentuj …”) i kilkoma hashtagami.
4. **Wszystko po polsku.**
5. Wynik zapisz też w pliku `filmy/AAAA-MM-DD.md` i wypchnij na gałąź.
