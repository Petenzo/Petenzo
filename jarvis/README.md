# Jarvis

Lokalny asystent głosowy: mówisz polecenie, Claude je wykonuje na Twoim komputerze i odpowiada na głos.

## Uruchomienie

Potrzebujesz Node.js 18+ oraz Chrome lub Edge.

```
git clone https://github.com/petenzo/petenzo.git
cd petenzo
git checkout claude/jarvis-ai-assistant-8szv6m
cd jarvis
npm install
npm start
```

Potem otwórz http://localhost:7777 i zezwól na mikrofon.

Jarvis korzysta z Twojego logowania do Claude Code (`npm i -g @anthropic-ai/claude-code`, potem `claude` i zaloguj się)
albo z klucza API w zmiennej `ANTHROPIC_API_KEY`.

## Głos ElevenLabs (opcjonalnie)

W folderze `jarvis` utwórz plik `.env` i wpisz w nim:

```
ELEVENLABS_API_KEY=tu_wklej_swój_klucz
ELEVENLABS_VOICE_ID=id_głosu_z_ElevenLabs
```

Klucz weźmiesz na elevenlabs.io w ustawieniach konta (API Keys), a ID głosu w bibliotece głosów.
Drugą linię możesz pominąć — wtedy Jarvis użyje domyślnego męskiego głosu. Bez pliku `.env` mówi głosem systemowym.
Po zmianie pliku uruchom Jarvisa ponownie.

## Sterowanie

- **MÓW** – jedno polecenie głosem.
- **NASŁUCH** – ciągłe czuwanie: powiedz „Jarvis, …" od razu z poleceniem, albo klaśnij dwa razy (lub powiedz samo „Jarvis") – odpowie „Jestem, do usług" i czeka na polecenie.
- Pole tekstowe – polecenie z klawiatury.
- „Stop" albo przycisk STOP – przerywa pracę. Kliknięcie w kulę ucisza głos.
- Gdy Jarvis chce zrobić coś poza swoim katalogiem roboczym (polecenie systemowe, mail, publikacja),
  pyta o zgodę: powiedz „tak" / „nie" albo kliknij.

## Gdzie co jest

- `workspace/` – katalog roboczy Jarvisa; tu tworzy pliki i strony.
- `workspace/memory.md` – trwała pamięć o Tobie; możesz ją edytować ręcznie.
- `server.mjs` – mózg (Claude Agent SDK). `public/index.html` – ekran, mikrofon i głos.

## Ustawienia (zmienne środowiskowe)

- `JARVIS_PORT` – port (domyślnie 7777).
- `JARVIS_TITLE` – jak Jarvis się do Ciebie zwraca (domyślnie „szefie").
- `JARVIS_MODEL` – model Claude; tańszy i szybszy model obniża koszt i skraca czas odpowiedzi.

Narzędzia (Gmail, Netlify itd.) Jarvis bierze z serwerów MCP skonfigurowanych w Twoim Claude Code (`claude mcp add …`).
