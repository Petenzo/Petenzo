# Instrukcje dla Claude

## Komenda „Filmy”

Kiedy użytkownik napisze **„Filmy”** i wyśle filmiki (zwykle 3 lub więcej), od razu, bez dopytywania, robisz to:

### 1. Napisy: osobna tabelka do każdego filmu
- Wyciągasz **wszystkie napisy z ekranu**, dokładnie co do klatki (ffmpeg: wykrywanie cięć `select='gt(scene,0.2)'` + klatka po klatce tam, gdzie zmienia się napis).
- Czas zapisujesz **jak w CapCut: `sekundy:klatki`**, 30 klatek = 1 sekunda (np. `4:01`, `7:02`, `12:06`). Bez zaokrąglania, dokładnie z filmu.
- W tabelce są tylko kolumny: **Od | Do | Napis**.
- Napis wpisujesz **od razu po polsku**: przetłumaczony, z wszystkimi znakami i emotkami (możesz dodać pasujące emotki). Hasło do komentarza też tłumaczysz (np. „LIS”).
- Jeśli przez chwilę nie ma napisu, robisz wiersz `(bez napisu)`.

Wzór:

| Od | Do | Napis |
|---|---|---|
| 0:00 | 4:01 | POV: lecę sama z dwójką chłopaków 😩👦👦 |
| 4:01 | 7:02 | Nie minęło nawet 45 minut… 😮‍💨⏰ |
| 7:02 | 10:02 | …a przed nami jeszcze 4 godziny lotu 😳✈️ |

### 2. Opisy na dole, wszystkie razem
Do każdego filmu dajesz krótki opis na YT, TikTok, FB i IG. Robisz go według tego wzoru:

```
🦊 Film 1 – Lis

Lot z maluchem? Już bez łez 🦊🎧 Napisz „LIS”, a podeślę link 👇

#mama #dziecko #maluch #podróż #samolot #spokój #cisza #sen #słuchawki #lis
```

- Nagłówek: emotka + „Film X – krótka nazwa”.
- Opis ma 1–2 krótkie zdania z emotkami i CTA (to samo hasło co w filmie).
- Na końcu ok. 10 hashtagów, każdy jako jedno polskie słowo.

### 3. Zasady
- Wszystko po polsku.
- Wynik zapisujesz też w `filmy/RRRR-MM-DD.md` i wypychasz na gałąź.
