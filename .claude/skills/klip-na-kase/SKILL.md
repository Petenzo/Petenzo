---
name: klip-na-kase
description: Pełny cykl "klip → YouTube → Content Rewards". Bierze klip z Ssemble (przez MCP), pisze tytuł, opis i hashtagi, wrzuca go jako YouTube Short w przeglądarce użytkownika, a potem zgłasza link do kampanii w Content Rewards (Whop), żeby dostać wypłatę za każde 1000 wyświetleń. Używaj, gdy użytkownik mówi np. "wrzuć klip", "zrób klipa i zgłoś", "klip na kasę", "nowy klip z Ssemble", albo podaje link do kampanii Content Rewards lub do filmu źródłowego.
---

# Klip na kasę: Ssemble → YouTube → Content Rewards

Masz poprowadzić jeden klip (albo kilka po kolei) przez cały proces:

1. **Ssemble (MCP):** zrób albo pobierz gotowy klip.
2. **Opis:** napisz tytuł, opis i hashtagi zgodne z zasadami kampanii.
3. **YouTube:** wrzuć klip jako Short na kanał użytkownika (w jego przeglądarce).
4. **Content Rewards:** zgłoś link do Shorta w wybranej kampanii.
5. **Dziennik:** zapisz wynik w `klipy-log.md`.

Odpowiadaj użytkownikowi po polsku, krótko.

---

## 0. Zanim zaczniesz (sprawdź raz na sesję)

- **Ssemble MCP:** poszukaj narzędzi Ssemble (`ToolSearch` z zapytaniem `ssemble`).
  Nie zgaduj nazw narzędzi. Przeczytaj, co MCP faktycznie udostępnia (tworzenie klipu,
  status zadania, link do pobrania), i używaj tylko tego. Jeśli nie ma ich wcale,
  powiedz użytkownikowi, że MCP Ssemble nie jest podłączony, i się zatrzymaj.
- **Przeglądarka:** potrzebujesz Claude in Chrome (narzędzia `mcp__claude-in-chrome__*`)
  albo wbudowanej przeglądarki aplikacji Claude. Najpierw wczytaj odpowiedni skill
  (`anthropic-skills:chrome-browser` albo `anthropic-skills:built-in-browser`).
  Użytkownik ma być **już zalogowany** w YouTube Studio i Content Rewards (whop.com).
- **Nigdy nie proś o hasła ani ich nie wpisuj.** Jeśli strona wymaga logowania,
  2FA albo captchy, zatrzymaj się i poproś użytkownika, żeby zrobił to sam.
- **Plik ustawień:** wczytaj `klipy-config.md` z katalogu projektu. Jeśli go nie ma,
  zapytaj o brakujące rzeczy i utwórz go (szablon niżej).

### Szablon `klipy-config.md`

```markdown
# Ustawienia klipów
- Kanał YouTube: <nazwa kanału>
- Kampania Content Rewards: <link do kampanii>
- Zasady kampanii (skopiuj z Content Rewards): <wymagane hashtagi, oznaczenia, długość, zakazy>
- Język opisów: polski / angielski
- Widoczność: publiczny
- Tryb: potwierdzaj przed publikacją (tak/nie)
- Limit dzienny: 3 klipy
```

---

## 1. Klip z Ssemble

1. Weź od użytkownika źródło: link do filmu albo ID projektu w Ssemble.
2. Użyj narzędzi MCP Ssemble, żeby utworzyć klip (format pionowy 9:16, do 60 s,
   z napisami, jeśli MCP to obsługuje) albo pobrać gotowy.
3. Jeśli zadanie jest asynchroniczne, sprawdzaj jego status narzędziem MCP,
   aż będzie gotowe. Nie zgaduj wyniku.
4. Pobierz plik MP4 do folderu `klipy/` i zapisz pełną ścieżkę.
5. Sprawdź: plik istnieje, ma więcej niż 0 bajtów i jest pionowy (`ffprobe`, jeśli jest).

## 2. Tytuł, opis, hashtagi

- **Tytuł:** do 70 znaków, haczyk w pierwszych słowach, bez clickbaitu wprowadzającego w błąd.
- **Opis:** 1–3 zdania o treści klipu + wszystko, czego wymaga kampania
  (oznaczenia, link do twórcy, `#shorts`, hashtagi kampanii).
- Zasady kampanii mają pierwszeństwo przed Twoimi pomysłami.
  Jeśli kampania czegoś zakazuje, nie rób tego.
- Pokaż użytkownikowi tytuł i opis. W trybie potwierdzania czekaj na „ok”.

## 3. Wrzucenie na YouTube (przeglądarka)

1. Otwórz `https://studio.youtube.com` w nowej karcie.
2. „Utwórz” → „Prześlij filmy” → wybierz plik z `klipy/`.
   Jeśli narzędzie przeglądarki nie umie wskazać lokalnego pliku, poproś użytkownika,
   żeby przeciągnął plik sam, i przejdź dalej, gdy plik się wgra.
3. Wklej tytuł i opis. „Nie, to nie jest film dla dzieci”.
4. Przejdź kroki do „Widoczność” → „Publiczny” → „Opublikuj”.
5. Skopiuj link do filmu (`https://youtube.com/shorts/<ID>`). Otwórz go i sprawdź,
   że działa i jest publiczny. **Nie przechodź dalej bez działającego linku.**

## 4. Zgłoszenie w Content Rewards

1. Otwórz link kampanii z `klipy-config.md` (whop.com / Content Rewards).
2. Sprawdź, czy kampania jest aktywna i czy ma jeszcze budżet. Jeśli nie, zatrzymaj się
   i powiedz to użytkownikowi.
3. Kliknij przycisk zgłoszenia (np. „Submit”, „Submit clip”), wybierz platformę YouTube,
   wklej link do Shorta i wyślij.
4. Zrób zrzut ekranu potwierdzenia albo spisz status („pending”, „w weryfikacji”).

## 5. Dziennik

Dopisz wiersz do `klipy-log.md`:

```
| data | źródło | tytuł | link YouTube | kampania | status zgłoszenia |
```

Na koniec powiedz użytkownikowi w 2–3 zdaniach: co wrzuciłeś, gdzie, jaki jest status.

---

## Zasady bezpieczeństwa (zawsze)

- Wrzucaj tylko treści, do których użytkownik ma prawo, albo te, które kampania
  wprost pozwala klipować.
- Bez sztucznych wyświetleń, botów, kupowania widzów i wrzucania tego samego klipu
  wiele razy. To łamie zasady YouTube i Content Rewards, grozi banem i brakiem wypłaty.
- Trzymaj się limitu dziennego z `klipy-config.md`. Za dużo identycznych uploadów
  w krótkim czasie YouTube może uznać za spam.
- Przy błędzie (upload nie przeszedł, zgłoszenie odrzucone, strona się zmieniła)
  zatrzymaj się, opisz, co widzisz, i nie klikaj na ślepo.
- Nigdy nie usuwaj filmów ani zgłoszeń bez wyraźnej prośby.
