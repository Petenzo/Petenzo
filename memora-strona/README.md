# Strona produktu – Kula Wspomnień (PL)

Otwórz `index.html` w przeglądarce (telefon lub komputer).

## Podgląd jednym kliknięciem
`podglad.html` to cała strona w jednym pliku, z filmami w środku. Po zmianach w `index.html` albo w filmach odśwież go poleceniem `python3 zbuduj-podglad.py`.

## Filmy („Zobacz to w akcji”)
W folderze `filmy/` jest 5 filmów (`film1.mp4` … `film5.mp4`), wyciętych z nagrań ekranu i oczyszczonych z angielskich napisów.
Polskie napisy nakłada strona (`CONFIG.filmy`): każdy napis ma swoją sekundę startu (`od`).
Te filmy pochodzą z cudzego sklepu, więc przed startem podmień je na własne nagrania pod tymi samymi nazwami.

## Zdjęcia produktu
Wrzuć zdjęcia do `zdjecia/` i wpisz ścieżki w `CONFIG.zdjecia` (na dole pliku `index.html`), np. `["zdjecia/1.jpg","zdjecia/2.jpg"]`.

## Teksty, ceny, opinie
Wszystko jest w obiekcie `CONFIG` w `index.html`: nazwa marki, pakiety i ceny, statystyki, opinie, FAQ.

**Uwaga prawna:** opinie i statystyki (4.8/5, 5 800+ opinii, 93/89/97%) są przetłumaczone z szablonu.
Przed uruchomieniem sklepu podmień je na prawdziwe opinie Twoich klientów – w Polsce (dyrektywa Omnibus, UOKiK)
publikowanie nieprawdziwych opinii jest zakazane i grożą za to wysokie kary.
