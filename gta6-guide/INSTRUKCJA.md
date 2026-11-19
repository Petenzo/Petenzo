# Leonida Playbook — instrukcja uruchomienia sprzedaży

Produkt: PDF-poradnik do GTA VI (po angielsku, rynek USA) + strona sprzedażowa.
Klient płaci → **automatycznie dostaje maila z PDF-em**. Nic nie wysyłasz ręcznie.

---

## Co masz

| Plik | Co to jest |
|---|---|
| `Leonida-Playbook-GTA-VI-Guide.pdf` | Gotowy poradnik, 21 stron (wysłany Ci jako plik, **NIE ma go w repo**) |
| `site/index.html` + `site/img/` | Strona sprzedażowa |
| `guide/guide.html` | Źródło PDF (nie w repo) |
| `tools/build.js` | Skrypt, który robi PDF ze źródła |

> ⚠️ Repo `Petenzo/Petenzo` jest **publiczne**. Nigdy nie wrzucaj tam PDF-a ani `guide.html`.
> PDF **nie może** też leżeć w folderze `site/`, bo strona jest publiczna.

---

## Krok 1: Shopify (płatności i automatyczna wysyłka PDF)

1. Na swoim koncie Shopify załóż **nowy sklep** tylko pod poradnik (nie w Petenzo). Plan **Basic**.
2. **Apps** → wyszukaj **Digital Downloads** → wybierz tę od **Shopify**, cena **Free** → Install.
3. **Products → Add product**
   - Title: `Leonida Playbook — The Unofficial GTA VI Survival Guide`
   - Price: **$14.99**
   - Odznacz „This is a physical product” (bez wysyłki)
   - Zdjęcie: `site/img/cover.jpg`
   - Opis: wklej tekst z sekcji „Opis produktu” poniżej
4. W aplikacji Digital Downloads przypisz plik `Leonida-Playbook-GTA-VI-Guide.pdf` do produktu.
5. **Settings → Store details**: wpisz osobnego Gmaila do kontaktu z klientami.
6. Zrób **testowy zakup** z kodem rabatowym 100% i sprawdź, czy PDF przychodzi na maila.

Możesz też podłączyć nowy sklep do mnie, a dodam produkt i wysyłkę za Ciebie.

## Krok 2: Podepnij link na stronie

W `site/index.html`, na samym dole:

```js
const CONFIG = {
  checkoutUrl: "#buy",               // ← link do produktu albo koszyka w Shopify
  price: "$14.99",
  supportEmail: "support@example.com" // ← Twój Gmail do kontaktu
};
```

## Krok 3: Wrzuć stronę do internetu (za darmo)

- **app.netlify.com/drop** → przeciągnij folder `site`. Dostajesz link do bio.
- Albo poproś mnie, a wrzucę ją za Ciebie.
- Domena nie jest potrzebna. Możesz ją dokupić później.

---

## Ważne

1. **Marki:** poradnik i strona mają dopisek „unofficial, not affiliated with Rockstar”. W reklamach **nie używaj** logo GTA VI ani screenów z gry. Używaj naszych grafik.
2. **Aktualizacje:** gracze ciągle odkrywają nowe kody i sekrety. Co kilka dni możemy dorzucać nowe rzeczy i podmieniać PDF w Digital Downloads.
3. **Podatki w Polsce:** przychód trzeba rozliczyć. Zapytaj księgowego.

---

## Opis produktu (wklej do Shopify)

> **GTA VI is huge and doesn't explain much. Run Leonida like a pro.**
>
> Leonida Playbook packs 70+ fact-checked tricks into one clean PDF:
>
> - Six ways to make money from your first hour, and who to sell to
> - The exact order for a clean robbery, and how to find any safe code
> - How to scan, register, refuel and recover your cars
> - The best early weapons, body armor, and how to never lose your guns
> - How the six-star police system finds you, and the checkmate getaway
> - The best hiding spots in the city and outside it
> - Partner tricks, hidden mechanics, cheats and the first big secrets
> - Phone numbers for GTA VI, plus every GTA V phone cheat
>
> 21 pages · PDF · Instant download right after checkout
>
> *Unofficial fan guide. Not affiliated with Rockstar Games or Take-Two Interactive.*

---

## Jak przebudować PDF po zmianach

```bash
cd gta6-guide/tools && npm install && cd .. && node tools/build.js
```

PDF pojawi się w `dist/`, podglądy dla strony w `site/img/`.
