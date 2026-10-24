// Wszystkie teksty to placeholdery copy: opisują funkcję tekstu, nie są tekstem finalnym.

export const PRODUCT_NAME = "[NAZWA PRODUKTU — odśnieżarka elektryczna 3000 W]";
export const PRICE = "[CENA] zł";
export const PRICE_OLD = "[CENA PRZED] zł";

export const heroBadges = [
  "[BADGE 1 — bestseller / nr 1]",
  "[BADGE 2 — wysyłka 24 h]",
  "[BADGE 3 — gwarancja]",
];

export const heroBenefits = [
  "[KORZYŚĆ 1 — oszczędność czasu: podjazd w minuty, nie w godzinę]",
  "[KORZYŚĆ 2 — moc 3000 W przełożona na efekt, nie na liczbę]",
  "[KORZYŚĆ 3 — koniec z bólem pleców i ramion]",
  "[KORZYŚĆ 4 — start jednym przyciskiem, bez paliwa i szarpania linki]",
  "[KORZYŚĆ 5 — cicha praca, sąsiedzi rano śpią]",
  "[KORZYŚĆ 6 — lekka, mieści się w garażu / komórce]",
];

export const variants = [
  { id: "solo", label: "[WARIANT 1]", hint: "[sam produkt]" },
  { id: "plus", label: "[WARIANT 2]", hint: "[+ akcesorium]" },
  { id: "pro", label: "[WARIANT 3]", hint: "[zestaw pełny]" },
];

export const pains = [
  "[BÓL FIZYCZNY — plecy i barki po godzinie z łopatą]",
  "[BÓL CZASOWY — wstawanie godzinę wcześniej, żeby wyjechać z posesji]",
  "[BÓL FINANSOWY — przepłacanie za firmę odśnieżającą / gorsze alternatywy]",
  "[BÓL SPOŁECZNY — wstyd przed sąsiadami za zasypany chodnik]",
  "[BÓL PRAWNY — odpowiedzialność i mandat za nieodśnieżony chodnik]",
  "[BÓL TECHNICZNY — spalinowa się nie odpala, śmierdzi i hałasuje]",
];

export const reliefs = [
  "[ULGA 1 — odwrócenie bólu fizycznego: idziesz, maszyna pracuje]",
  "[ULGA 2 — odzyskany poranek: kawa zamiast łopaty]",
  "[ULGA 3 — jednorazowy koszt zamiast abonamentu za odśnieżanie]",
  "[ULGA 4 — czysty chodnik jako pierwszy na ulicy]",
  "[ULGA 5 — spokój: obowiązek odśnieżania odhaczony w 10 minut]",
  "[ULGA 6 — zero paliwa, oleju i serwisu silnika]",
];

export const steps = [
  {
    title: "[KROK 1 — usuwa obiekcję „to skomplikowane”: wyjmij i podłącz]",
    body: "[OPIS KROKU 1 — co dokładnie robi klient, ile to trwa]",
  },
  {
    title: "[KROK 2 — usuwa obiekcję „nie będę wiedział jak obsługiwać”]",
    body: "[OPIS KROKU 2 — jeden przycisk, prowadzisz jak kosiarkę]",
  },
  {
    title: "[KROK 3 — pokazuje efekt końcowy: czysty podjazd]",
    body: "[OPIS KROKU 3 — ile metrów, w ile minut, gdzie ląduje śnieg]",
  },
];

export const offerTabs = [
  {
    id: "maszyna",
    label: "[ZAKŁADKA 1]",
    title: "[CO DOSTAJESZ 1 — sama maszyna jako narzędzie transformacji]",
    body: "[OPIS — specyfikacja przetłumaczona na korzyści: 3000 W, szerokość robocza, zasięg wyrzutu]",
    gains: ["[ZYSK 1.1]", "[ZYSK 1.2]", "[ZYSK 1.3]", "[ZYSK 1.4]"],
  },
  {
    id: "w-zestawie",
    label: "[ZAKŁADKA 2]",
    title: "[CO DOSTAJESZ 2 — elementy w pudełku, które podnoszą wartość]",
    body: "[OPIS — co jest w zestawie i dlaczego nie musisz nic dokupować]",
    gains: ["[ZYSK 2.1]", "[ZYSK 2.2]", "[ZYSK 2.3]", "[ZYSK 2.4]"],
  },
  {
    id: "wsparcie",
    label: "[ZAKŁADKA 3]",
    title: "[CO DOSTAJESZ 3 — gwarancja, zwroty, wsparcie po zakupie]",
    body: "[OPIS — odwrócenie ryzyka: co się dzieje, jeśli coś pójdzie nie tak]",
    gains: ["[ZYSK 3.1]", "[ZYSK 3.2]", "[ZYSK 3.3]", "[ZYSK 3.4]"],
  },
];

export const compareColumns = [
  "[NASZ PRODUKT]",
  "[ALTERNATYWA 1 — łopata]",
  "[ALTERNATYWA 2 — spalinowa]",
  "[ALTERNATYWA 3 — firma odśnieżająca]",
];

type Mark = "yes" | "no" | "partial";

export const compareRows: { label: string; marks: [Mark, Mark, Mark] }[] = [
  { label: "[KRYTERIUM 1 — czas odśnieżania]", marks: ["no", "yes", "partial"] },
  { label: "[KRYTERIUM 2 — wysiłek fizyczny]", marks: ["no", "partial", "yes"] },
  { label: "[KRYTERIUM 3 — koszt w sezonie]", marks: ["yes", "no", "no"] },
  { label: "[KRYTERIUM 4 — brak paliwa i spalin]", marks: ["yes", "no", "partial"] },
  { label: "[KRYTERIUM 5 — dostępność od ręki o 6:00]", marks: ["yes", "partial", "no"] },
  { label: "[KRYTERIUM 6 — cicha praca]", marks: ["yes", "no", "partial"] },
];

export const reviews = [
  {
    text: "[OPINIA 1 — przed/po: konkretny problem rozwiązany, liczby, czas]",
    author: "[IMIĘ / MIASTO]",
  },
  {
    text: "[OPINIA 2 — przełamanie sceptycyzmu: „myślałem, że elektryczna nie da rady”]",
    author: "[IMIĘ / MIASTO]",
  },
  {
    text: "[OPINIA 3 — łatwość obsługi: senior / osoba bez doświadczenia]",
    author: "[IMIĘ / MIASTO]",
  },
  {
    text: "[OPINIA 4 — obsługa sklepu: szybka wysyłka, kontakt, gwarancja]",
    author: "[IMIĘ / MIASTO]",
  },
];

export const bundleItems = [
  { name: "[PRODUKT 1 — odśnieżarka 3000 W]", price: "[CENA 1] zł" },
  { name: "[PRODUKT 2 — przedłużacz zimowy 20 m]", price: "[CENA 2] zł" },
  { name: "[PRODUKT 3 — pokrowiec / skrobak]", price: "[CENA 3] zł" },
];

export const faqs = [
  {
    q: "[OBIEKCJA 1 — „Czy 3000 W poradzi sobie z mokrym, ciężkim śniegiem?”]",
    a: "[ODPOWIEDŹ 1 — dowód + konkretna grubość warstwy]",
  },
  {
    q: "[OBIEKCJA 2 — „Czy kabel nie będzie przeszkadzał?”]",
    a: "[ODPOWIEDŹ 2 — sposób prowadzenia kabla, zalecany przedłużacz]",
  },
  {
    q: "[OBIEKCJA 3 — „Czy poradzę sobie z obsługą?”]",
    a: "[ODPOWIEDŹ 3 — prostota, jeden przycisk, instrukcja PL]",
  },
  {
    q: "[OBIEKCJA 4 — „Czy to się opłaca vs. łopata / firma?”]",
    a: "[ODPOWIEDŹ 4 — rachunek kosztu w sezonie]",
  },
  {
    q: "[OBIEKCJA 5 — „Ile trwa dostawa? Zdążę przed śniegiem?”]",
    a: "[ODPOWIEDŹ 5 — czas wysyłki i dostawy]",
  },
  {
    q: "[OBIEKCJA 6 — „Co jeśli się zepsuje?”]",
    a: "[ODPOWIEDŹ 6 — gwarancja, serwis, części]",
  },
  {
    q: "[OBIEKCJA 7 — „Mogę zwrócić, jeśli nie spełni oczekiwań?”]",
    a: "[ODPOWIEDŹ 7 — zasady zwrotu, 14 dni, kto płaci za odesłanie]",
  },
];

export const footerLinks = [
  "[REGULAMIN]",
  "[POLITYKA PRYWATNOŚCI]",
  "[DOSTAWA]",
  "[ZWROTY I REKLAMACJE]",
  "[KONTAKT]",
];
