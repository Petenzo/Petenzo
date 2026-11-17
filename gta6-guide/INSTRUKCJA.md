# Leonida: Day One — instrukcja uruchomienia sprzedaży

Produkt: PDF-poradnik do GTA VI (po angielsku, rynek USA) + strona sprzedażowa.
Klient płaci → **automatycznie dostaje maila z linkiem do PDF**. Nie musisz nic robić ręcznie.

---

## Co masz

| Plik | Co to jest |
|---|---|
| `Leonida-Day-One-GTA-VI-Guide.pdf` | Gotowy poradnik, 19 stron (wysłany Ci jako plik, **NIE ma go w repo**) |
| `site/index.html` + `site/img/` | Strona sprzedażowa (landing page) |
| `guide/guide.html` | Źródło PDF (też wysłane jako plik, **nie w repo**) |
| `tools/build.js` | Skrypt, który robi PDF ze źródła |

> ⚠️ Repo `Petenzo/Petenzo` jest **publiczne**. Nigdy nie wrzucaj tam PDF-a ani `guide.html`, bo każdy pobierze go za darmo.
> PDF **nie może** też leżeć w folderze `site/` (strona jest publiczna).

---

## Krok 1: Gumroad (płatności i automatyczna wysyłka PDF), ok. 10 minut

1. Załóż konto na **gumroad.com**.
2. **Settings → Payments**: podepnij wypłaty (PayPal albo konto bankowe).
3. **Products → New product → Digital product**
   - Name: `Leonida: Day One — The Unofficial GTA VI Field Guide`
   - Price: **$14.99** (ok. 55 zł)
   - Upload: wgraj `Leonida-Day-One-GTA-VI-Guide.pdf`
   - Cover: wgraj `site/img/cover.jpg`
   - Description: wklej tekst z sekcji „Opis produktu” poniżej
4. **Publish**, potem skopiuj link do produktu (np. `https://twojanazwa.gumroad.com/l/leonida`).

Gumroad sam wysyła klientowi maila z PDF-em zaraz po zapłacie.
Prowizja Gumroada to ok. 10% + 0,50 $ od sprzedaży (sprawdź aktualny cennik na ich stronie).
Alternatywa: **Lemon Squeezy** działa tak samo.

## Krok 2: Podepnij link na stronie, 1 minuta

Otwórz `site/index.html`, na samym dole znajdź:

```js
const CONFIG = {
  checkoutUrl: "#buy",               // ← TU wklej link z Gumroada
  price: "$14.99",                   // ← cena (zmienia się wszędzie na stronie)
  supportEmail: "support@example.com" // ← Twój mail do kontaktu
};
```

## Krok 3: Wrzuć stronę do internetu, 2 minuty, za darmo

- Wejdź na **app.netlify.com/drop** i przeciągnij folder `site`. Dostajesz link od razu.
- Możesz też poprosić mnie, a zrobię to przez Netlify.
- Własna domena (np. `leonidadayone.com`) kosztuje ok. 10–15 $ rocznie i podpinasz ją w Netlify.

---

## Ważne: przeczytaj

1. **Premiera GTA VI to 19 listopada 2026, czyli za 2 dni.** Najwięcej sprzedasz w tym tygodniu, więc odpal to dziś.
2. **Prawo/marki:** poradnik i strona mają dopisek „unofficial, not affiliated with Rockstar”. W reklamach **nie używaj** logo GTA VI, screenów z gry ani grafik Rockstara. Używaj tylko naszych grafik (okładka i podglądy stron).
3. **Fakty:** wszystko w poradniku jest sprawdzone i oznaczone (CONFIRMED / PREVIEW / VETERAN / UNCONFIRMED). Gra jeszcze nie wyszła, więc to **wydanie przedpremierowe**. Po premierze warto zrobić v2 z prawdziwymi trikami z gry. Gumroad pozwala podmienić plik i kupujący dostaną nową wersję.
4. **Podatki w Polsce:** przychód ze sprzedaży trzeba rozliczyć (np. działalność nierejestrowana albo firma). Zapytaj księgowego.

---

## Opis produktu (wklej do Gumroada)

> **GTA VI launches November 19. Walk into Leonida knowing everything.**
>
> Leonida: Day One is a fact-checked, no-filler PDF guide for launch night:
>
> - Every confirmed GTA VI feature, with sources
> - Leonida's six regions and the main cast (spoiler-light)
> - How the new police system sees you, and the outfit trick to lose the heat
> - The phone car scanner, ride-share fast travel and every app shown so far
> - Gym, food and grooming systems explained
> - A tick-box plan for your first 10 hours
> - The Veteran Playbook: money, heists, chases and stealth from GTA IV & V
> - A verified cheat vault for GTA V & GTA IV
> - A printable quick-reference card
>
> Every claim is labeled Confirmed, Preview, Veteran or Unconfirmed, so you never fall for fake leaks.
>
> 19 pages · PDF · Instant download
>
> *Unofficial fan guide. Not affiliated with Rockstar Games or Take-Two Interactive.*

---

## Jak przebudować PDF po zmianach

```bash
cd gta6-guide/tools && npm install && cd .. && node tools/build.js
```

PDF pojawi się w `dist/`, a podglądy dla strony w `site/img/`.
