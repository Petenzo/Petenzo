# Instrukcje dla Claude

## Komenda „Filmy”

Kiedy użytkownik napisze **„Filmy”** i wyśle filmiki (zwykle 3 lub więcej), od razu, bez dopytywania, robisz to:

### 1. Napisy: osobna tabelka do każdego filmu
- Wyciągasz **wszystkie napisy z ekranu**, dokładnie co do klatki (ffmpeg: wykrywanie cięć `select='gt(scene,0.2)'` + klatka po klatce tam, gdzie zmienia się napis).
- Czas zapisujesz **jak w CapCut: `sekundy:klatki`**, 30 klatek = 1 sekunda (np. `4:01`, `7:02`, `12:06`). Bez zaokrąglania, dokładnie z filmu.
- W tabelce są tylko kolumny: **Od | Do | Napis**.
- Napis wpisujesz **od razu po polsku**, z wszystkimi znakami i emotkami. **Nie tłumacz słowo w słowo**: ma brzmieć tak, jak napisałby to Polak na TikToku, naturalnie i chwytliwie.
- **Ostatni napis to zawsze dobre CTA** dopasowane do filmu, w stylu polskich kont: „Skomentuj „LIS”, a wyślę Ci link 👇”, „Napisz „lampki”, jeśli takie chcesz 🥰”. Hasło ma być krótkie, po polsku i pasować do produktu z filmu (np. LIS, SÓWKA, OPASKA). Jeśli film nie ma CTA albo ma słabe („Link in bio”), zamień je albo dodaj na ostatnim ujęciu i zaznacz, że to dodane.
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

Każda mama boi się lotu z płaczącym maluchem ✈️😰 Ten lisek zamienił nasz koszmar w drzemkę, napisz „LIS”, a Ci to wyślę 🦊👇

#podróżezdzieckiem #wakacjezdzieckiem #mama
```

- Nagłówek: emotka + „Film X – krótka nazwa”.
- Opis: **1 zdanie, maks. 2**, ale **mocny psychologicznie**: 1) zaczepka w ból/emocję mamy, z którą się utożsamia („Znasz ten wstyd, gdy…”, „Każda mama boi się…”), 2) produkt jako ulga/rozwiązanie, 3) CTA z tym samym hasłem co w filmie („napisz „LIS”, a Ci to wyślę 👇”). Emotki pasujące do emocji.
- Na końcu **dokładnie 3 hashtagi**, tylko **prawdziwe, popularne w Polsce** (np. #mama, #macierzyństwo, #rodzicielstwo, #maluch, #dziecko, #podróżezdzieckiem, #wakacjezdzieckiem, #prezentdladziecka). Dobór: 1 szeroki (grupa docelowa, np. #mama), 1 pod temat/sytuację z filmu (np. #podróżezdzieckiem), 1 zakupowy lub niszowy (np. #prezentdladziecka). Nigdy nie wymyślaj własnych.

### 3. Zasady
- Wszystko po polsku.
- Wynik zapisujesz też w `filmy/RRRR-MM-DD.md` i wypychasz na gałąź.
