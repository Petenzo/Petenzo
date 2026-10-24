import { useEffect, useState } from "react";
import {
  Check,
  ChevronRight,
  Menu,
  Minus,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  Star,
  Truck,
  X,
} from "lucide-react";

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

import {
  animations,
  PRICE,
  PRICE_OLD,
  PRODUCT_NAME,
  bundleItems,
  compareColumns,
  compareRows,
  faqs,
  footerLinks,
  heroBadges,
  heroBenefits,
  offerTabs,
  pains,
  reliefs,
  reviews,
  steps,
  variants,
} from "./content";
import { Bullet, Card, Eyebrow, GradientButton, Pill, Section, SectionTitle } from "./ui";

const LOGO = "[LOGO PRODUKTU]";
const CONTACT_EMAIL = "[EMAIL]";

const gallery = [
  { src: "/images/hero.jpg", alt: "Elektryczna odśnieżarka 3000 W na zaśnieżonym podjeździe", label: "[FOTO 1]" },
  { src: "/images/studio.jpg", alt: "Odśnieżarka elektryczna na białym tle", label: "[FOTO 2]" },
  { src: "/images/detal.jpg", alt: "Zbliżenie na ślimak odśnieżarki zbierający śnieg", label: "[FOTO 3]" },
  { src: "/images/proces.jpg", alt: "Odśnieżarka wyrzuca śnieg i zostawia czysty chodnik", label: "[FOTO 4]" },
];

function MicroTrust() {
  return (
    <p className="text-muted-foreground mt-3 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs">
      <span className="inline-flex items-center gap-1">
        <Truck className="size-3.5" aria-hidden /> [MIKROZAUFANIE — darmowa wysyłka]
      </span>
      <span className="inline-flex items-center gap-1">
        <ShieldCheck className="size-3.5" aria-hidden /> [MIKROZAUFANIE — 14 dni na zwrot]
      </span>
    </p>
  );
}

// Zapętlona, wyciszona animacja (zachowuje się jak GIF), z plakatem jako fallback.
function LoopClip({
  src,
  poster,
  label,
  width,
  height,
  className,
}: {
  src: string;
  poster: string;
  label: string;
  width: number;
  height: number;
  className?: string;
}) {
  return (
    <video
      src={src}
      poster={poster}
      width={width}
      height={height}
      autoPlay
      muted
      loop
      playsInline
      preload="metadata"
      aria-label={label}
      className={cn("shadow-soft aspect-[4/3] w-full rounded-[20px] object-cover", className)}
    />
  );
}

function Logo({ className }: { className?: string }) {
  return (
    <span
      className={cn("text-brand text-lg tracking-wide sm:text-xl", className)}
      style={{ fontFamily: "var(--font-logo)" }}
    >
      {LOGO}
    </span>
  );
}

function Stars() {
  return (
    <div className="text-primary flex gap-0.5" aria-label="Ocena 5 na 5">
      {Array.from({ length: 5 }).map((_, i) => (
        <Star key={i} className="size-4 fill-current" aria-hidden />
      ))}
    </div>
  );
}

function KlarnaIcon() {
  return (
    <svg viewBox="0 0 24 24" className="text-primary size-5 shrink-0" fill="none" aria-hidden>
      <rect x="2" y="5" width="20" height="14" rx="3" stroke="currentColor" strokeWidth="1.8" />
      <path d="M2 10h20" stroke="currentColor" strokeWidth="1.8" />
      <rect x="5" y="13.5" width="5" height="2" rx="1" fill="currentColor" />
    </svg>
  );
}

export function LandingPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [contactOpen, setContactOpen] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);
  const [variant, setVariant] = useState(variants[0].id);
  const [photo, setPhoto] = useState(0);
  const [cart, setCart] = useState<string[]>([]);
  const [showSticky, setShowSticky] = useState(false);

  useEffect(() => {
    const onScroll = () => setShowSticky(window.scrollY > 700);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const addToCart = (item: string) => {
    setCart((c) => [...c, item]);
    setCartOpen(true);
  };

  const selectedVariant = variants.find((v) => v.id === variant) ?? variants[0];
  const addMain = () => addToCart(`${PRODUCT_NAME} · ${selectedVariant.label}`);
  const current = gallery[photo];

  return (
    <div className="flex min-h-screen flex-col">
      {/* 1. Top bar */}
      <div className="bg-brand text-primary-foreground px-4 py-2 text-center text-xs font-semibold sm:text-sm">
        [BADGE PROMOCYJNY — pilność / nowość]
      </div>

      {/* 2. Nawigacja */}
      <header className="bg-background/90 border-border sticky top-0 z-40 border-b backdrop-blur">
        <div className="relative mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4">
          <button
            type="button"
            onClick={() => setMenuOpen((o) => !o)}
            aria-label={menuOpen ? "Zamknij menu" : "Otwórz menu"}
            aria-expanded={menuOpen}
            className="border-border hover:bg-accent inline-flex size-10 items-center justify-center rounded-xl border transition-colors"
          >
            {menuOpen ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
          <a href="#hero" className="absolute left-1/2 -translate-x-1/2">
            <Logo />
          </a>
          <button
            type="button"
            onClick={() => setCartOpen(true)}
            aria-label="Koszyk"
            className="hover:bg-accent relative inline-flex size-10 items-center justify-center rounded-xl transition-colors"
          >
            <ShoppingBag className="size-5" />
            {cart.length > 0 && (
              <span className="bg-brand text-primary-foreground absolute -top-0.5 -right-0.5 inline-flex size-5 items-center justify-center rounded-full text-[10px] font-bold">
                {cart.length}
              </span>
            )}
          </button>
        </div>
      </header>

      {menuOpen && (
        <div className="bg-background fixed inset-0 z-[100] flex flex-col" role="dialog" aria-modal="true" aria-label="Menu">
          <div className="border-border relative flex h-16 items-center justify-center border-b px-4">
            <Logo />
            <button
              type="button"
              onClick={() => setMenuOpen(false)}
              aria-label="Zamknij menu"
              className="border-border hover:bg-accent absolute right-4 inline-flex size-10 items-center justify-center rounded-xl border"
            >
              <X className="size-5" />
            </button>
          </div>
          <nav className="flex flex-1 flex-col items-center justify-center gap-8">
            <a href="#hero" onClick={() => setMenuOpen(false)} className="hover:text-primary text-2xl font-semibold">
              Ambiente
            </a>
            <button
              type="button"
              onClick={() => {
                setMenuOpen(false);
                setContactOpen(true);
              }}
              className="hover:text-primary text-2xl font-semibold"
            >
              Kontakt
            </button>
            <button
              type="button"
              onClick={() => setMenuOpen(false)}
              className="text-muted-foreground mt-4 text-sm underline underline-offset-4"
            >
              Zamknij menu
            </button>
          </nav>
        </div>
      )}

      <main className="flex-1">
        {/* 3. Hero */}
        <Section id="hero" className="pt-8 sm:pt-12">
          <div className="flex justify-center">
            <Pill>
              <Star className="size-3.5 fill-current" aria-hidden /> [BADGE ZAUFANIA — ocena / liczba klientów]
            </Pill>
          </div>
          <h1 className="mx-auto mt-5 max-w-3xl text-center text-3xl leading-tight font-extrabold tracking-tight sm:text-5xl">
            [NAGŁÓWEK GŁÓWNY — obietnica transformacji end-state,{" "}
            <span className="text-brand">nie funkcji produktu</span>]
          </h1>
          <p className="text-muted-foreground mx-auto mt-4 max-w-2xl text-center text-base sm:text-lg">
            [PODNAGŁÓWEK — dla kogo, jaki ból znika i w jakim czasie]
          </p>

          <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-2 lg:gap-10">
            <Card className="p-3 sm:p-4">
              <div className="bg-surface aspect-square overflow-hidden rounded-2xl">
                {current.src ? (
                  <img
                    src={current.src}
                    alt={current.alt}
                    width={1200}
                    height={1200}
                    loading="lazy"
                    className="size-full object-cover"
                  />
                ) : (
                  <div className="text-muted-foreground flex size-full items-center justify-center text-sm font-semibold">
                    {current.label}
                  </div>
                )}
              </div>
              <div className="mt-3 grid grid-cols-4 gap-2 sm:gap-3">
                {gallery.map((g, i) => (
                  <button
                    key={g.label}
                    type="button"
                    onClick={() => setPhoto(i)}
                    aria-label={`Pokaż ${g.label}`}
                    className={cn(
                      "bg-surface aspect-square overflow-hidden rounded-xl border-2 transition-colors",
                      i === photo ? "border-primary" : "border-transparent hover:border-border",
                    )}
                  >
                    {g.src ? (
                      <img src={g.src} alt={g.alt} width={300} height={300} loading="lazy" className="size-full object-cover" />
                    ) : (
                      <span className="text-muted-foreground text-[10px] font-semibold sm:text-xs">{g.label}</span>
                    )}
                  </button>
                ))}
              </div>
            </Card>

            <Card>
              <div className="flex flex-wrap gap-2">
                {heroBadges.map((b) => (
                  <Badge key={b} variant="secondary" className="bg-accent text-accent-foreground rounded-full px-3 py-1">
                    {b}
                  </Badge>
                ))}
              </div>
              <h2 className="mt-4 text-xl font-bold sm:text-2xl">{PRODUCT_NAME}</h2>
              <p className="text-muted-foreground mt-2 text-sm">
                [OPIS KRÓTKI — jedno zdanie: co robi + dla kogo + główny wynik]
              </p>
              <div className="mt-5 flex items-end gap-3">
                <span className="text-brand text-3xl font-extrabold sm:text-4xl">{PRICE}</span>
                <span className="text-muted-foreground pb-1 text-base line-through">{PRICE_OLD}</span>
              </div>

              <div className="border-primary/25 bg-primary/5 mt-4 flex items-center gap-3 rounded-xl border px-4 py-3 text-sm">
                <KlarnaIcon />
                <span>lub 3 × XX zł bez odsetek · Klarna</span>
              </div>

              <ul className="mt-6 space-y-3">
                {heroBenefits.map((b) => (
                  <Bullet key={b}>{b}</Bullet>
                ))}
              </ul>

              <div className="mt-6">
                <p className="text-sm font-semibold">[ETYKIETA WYBORU WARIANTU]</p>
                <div className="mt-2 grid grid-cols-3 gap-2">
                  {variants.map((v) => (
                    <button
                      key={v.id}
                      type="button"
                      onClick={() => setVariant(v.id)}
                      aria-pressed={variant === v.id}
                      className={cn(
                        "rounded-xl border px-2 py-3 text-center text-xs transition-colors sm:text-sm",
                        variant === v.id ? "border-primary bg-accent" : "border-border hover:bg-surface",
                      )}
                    >
                      <span className="block font-semibold">{v.label}</span>
                      <span className="text-muted-foreground block text-[11px]">{v.hint}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="border-border mt-5 flex items-center gap-3 rounded-xl border border-dashed p-3">
                <img
                  src="/images/przedluzacz.jpg"
                  alt="Przedłużacz zimowy na bębnie"
                  width={64}
                  height={64}
                  loading="lazy"
                  className="size-16 shrink-0 rounded-lg object-cover"
                />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold">[CROSS-SELL — dodatek, bez którego produkt działa gorzej]</p>
                  <p className="text-muted-foreground text-xs">+ [CENA DODATKU] zł</p>
                </div>
                <button
                  type="button"
                  onClick={() => addToCart("[DODATEK — przedłużacz zimowy 20 m]")}
                  className="border-primary text-primary hover:bg-accent shrink-0 rounded-lg border px-3 py-1.5 text-xs font-semibold"
                >
                  Dodaj
                </button>
              </div>

              <div className="mt-6">
                <GradientButton full onClick={addMain}>
                  [CTA GŁÓWNE — działanie + korzyść] <ChevronRight className="size-4" aria-hidden />
                </GradientButton>
                <MicroTrust />
              </div>
            </Card>
          </div>
        </Section>

        {/* 4. Problem */}
        <Section id="problem" alt>
          <Eyebrow>[EYEBROW — nazwanie problemu]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK PROBLEMU — czytelnik rozpoznaje swoją sytuację]</SectionTitle>
          <div className="mt-10 grid grid-cols-1 items-center gap-8 lg:grid-cols-2">
            <div>
              <ul className="grid grid-cols-1 gap-3">
                {pains.map((p) => (
                  <li key={p} className="shadow-soft border-border bg-card flex items-start gap-3 rounded-2xl border p-4 text-sm">
                    <span className="bg-destructive/10 text-destructive inline-flex size-6 shrink-0 items-center justify-center rounded-full">
                      <X className="size-3.5" strokeWidth={3} aria-hidden />
                    </span>
                    {p}
                  </li>
                ))}
              </ul>
              <p className="bg-accent text-accent-foreground mt-5 rounded-2xl p-5 text-sm font-medium">
                [ZDANIE-MOST — „to nie twoja wina, to kwestia narzędzia” → przejście do rozwiązania]
              </p>
            </div>
            <img
              src="/images/problem.jpg"
              alt="Zmęczony mężczyzna z łopatą przed zasypanym podjazdem"
              width={1200}
              height={896}
              loading="lazy"
              className="shadow-soft aspect-[4/3] w-full rounded-[20px] object-cover"
            />
          </div>
        </Section>

        {/* 5. Rozwiązanie */}
        <Section id="rozwiazanie">
          <div className="grid grid-cols-1 items-center gap-8 lg:grid-cols-2">
            <LoopClip
              src={animations.detal}
              poster="/images/detal.jpg"
              label="Animacja: ślimak odśnieżarki wgryza się w śnieg i wyrzuca go kominem"
              width={768}
              height={768}
              className="order-1 lg:order-1"
            />
            <div className="order-2">
              <Eyebrow className="lg:text-left">[EYEBROW — rozwiązanie]</Eyebrow>
              <SectionTitle className="lg:text-left">
                [NAGŁÓWEK ROZWIĄZANIA — produkt jako <span className="text-brand">most do nowego stanu</span>]
              </SectionTitle>
              <p className="text-muted-foreground mt-4 text-sm sm:text-base">
                [LEAD — mechanizm: dlaczego to działa tam, gdzie inne sposoby zawodzą]
              </p>
              <ul className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
                {reliefs.map((r) => (
                  <Bullet key={r}>{r}</Bullet>
                ))}
              </ul>
            </div>
          </div>
        </Section>

        {/* 6. Jak to działa */}
        <Section id="jak-to-dziala" alt>
          <Eyebrow>[EYEBROW — jak to działa]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK — „3 kroki do czystego podjazdu”: prostota]</SectionTitle>
          <div className="mt-10 grid grid-cols-1 items-center gap-8 lg:grid-cols-2">
            <LoopClip
              src={animations.proces}
              poster="/images/proces.jpg"
              label="Animacja: odśnieżarka wyrzuca śnieg i zostawia czysty chodnik"
              width={1024}
              height={768}
            />
            <ol className="grid grid-cols-1 gap-4">
              {steps.map((s, i) => (
                <li key={s.title}>
                  <Card className="flex items-start gap-4 p-5 sm:p-6">
                    <span className="text-brand text-3xl leading-none font-extrabold">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <div>
                      <h3 className="font-semibold">{s.title}</h3>
                      <p className="text-muted-foreground mt-1 text-sm">{s.body}</p>
                    </div>
                  </Card>
                </li>
              ))}
            </ol>
          </div>
        </Section>

        {/* 7. Co dostajesz */}
        <Section id="co-dostajesz">
          <Eyebrow>[EYEBROW — co dostajesz]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK — wartość pakietu większa niż cena]</SectionTitle>
          <Tabs defaultValue={offerTabs[0].id} className="mt-8 items-center gap-6">
            <TabsList className="bg-surface h-auto w-full max-w-xl rounded-full p-1">
              {offerTabs.map((t) => (
                <TabsTrigger
                  key={t.id}
                  value={t.id}
                  className="data-[state=active]:bg-card rounded-full px-3 py-2 text-xs sm:text-sm"
                >
                  {t.label}
                </TabsTrigger>
              ))}
            </TabsList>
            {offerTabs.map((t) => (
              <TabsContent key={t.id} value={t.id} className="w-full">
                <Card>
                  <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:gap-10">
                    <div>
                      <h3 className="text-lg font-bold sm:text-xl">{t.title}</h3>
                      <p className="text-muted-foreground mt-3 text-sm sm:text-base">{t.body}</p>
                    </div>
                    <div className="bg-surface rounded-2xl p-5">
                      <ul className="space-y-3">
                        {t.gains.map((g) => (
                          <Bullet key={g}>{g}</Bullet>
                        ))}
                      </ul>
                    </div>
                  </div>
                </Card>
              </TabsContent>
            ))}
          </Tabs>
        </Section>

        {/* 8. Tabela porównawcza */}
        <Section id="porownanie" alt>
          <Eyebrow>[EYEBROW — porównanie]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK — dlaczego to lepsze niż to, co robisz teraz]</SectionTitle>
          <div className="shadow-soft border-border bg-card mt-10 overflow-x-auto rounded-[20px] border">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead>
                <tr className="border-border border-b">
                  <th className="p-4 font-semibold">[KRYTERIUM]</th>
                  {compareColumns.map((c, i) => (
                    <th
                      key={c}
                      className={cn(
                        "p-4 text-center font-semibold",
                        i === 0 ? "bg-accent text-accent-foreground" : "text-muted-foreground",
                      )}
                    >
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {compareRows.map((row) => (
                  <tr key={row.label} className="border-border border-b last:border-b-0">
                    <td className="p-4 font-medium">{row.label}</td>
                    <td className="bg-accent/60 p-4 text-center">
                      <Check className="text-primary mx-auto size-5" strokeWidth={3} aria-label="Tak" />
                    </td>
                    {row.marks.map((m, i) => (
                      <td key={i} className="text-muted-foreground/60 p-4 text-center">
                        {m === "yes" ? (
                          <Check className="mx-auto size-5" aria-label="Tak" />
                        ) : m === "partial" ? (
                          <Minus className="mx-auto size-5" aria-label="Częściowo" />
                        ) : (
                          <X className="mx-auto size-5" aria-label="Nie" />
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>

        {/* 9. Opinie */}
        <Section id="opinie">
          <Eyebrow>[EYEBROW — opinie]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK — dowód społeczny: ludzie jak ty już to mają]</SectionTitle>
          <div className="mt-10 grid grid-cols-1 gap-5 md:grid-cols-2">
            {reviews.map((r, i) => (
              <Card key={i}>
                <Stars />
                <p className="mt-4 text-sm leading-relaxed sm:text-base">„{r.text}”</p>
                <div className="mt-5 flex items-center gap-3">
                  <span className="bg-brand inline-block size-10 shrink-0 rounded-full" aria-hidden />
                  <span className="text-sm font-semibold">{r.author}</span>
                </div>
              </Card>
            ))}
          </div>
        </Section>

        {/* 10. CTA powtórzone */}
        <Section id="cta" alt>
          <Card className="mx-auto max-w-2xl text-center">
            <span className="bg-brand shadow-glow text-primary-foreground mx-auto inline-flex size-12 items-center justify-center rounded-2xl">
              <Sparkles className="size-6" aria-hidden />
            </span>
            <h2 className="mt-5 text-2xl font-extrabold sm:text-3xl">
              [NAGŁÓWEK CTA — przypomnienie end-state + <span className="text-brand">pilność</span>]
            </h2>
            <p className="text-muted-foreground mt-3 text-sm sm:text-base">
              [LEAD CTA — co tracisz, czekając do pierwszego śniegu]
            </p>
            <div className="mt-6">
              <GradientButton full onClick={addMain}>
                [CTA POWTÓRZONE] <ChevronRight className="size-4" aria-hidden />
              </GradientButton>
              <MicroTrust />
            </div>
          </Card>
        </Section>

        {/* 11. Upsell */}
        <Section id="upsell">
          <Eyebrow>[EYEBROW — polecany dodatek]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK UPSELL — „uzupełnij zestaw”]</SectionTitle>
          <Card className="mt-10">
            <div className="grid grid-cols-1 items-center gap-6 lg:grid-cols-2 lg:gap-10">
              <img
                src="/images/przedluzacz.jpg"
                alt="Przedłużacz zimowy 20 m na bębnie"
                width={1200}
                height={896}
                loading="lazy"
                className="aspect-[4/3] w-full rounded-2xl object-cover"
              />
              <div>
                <h3 className="text-xl font-bold sm:text-2xl">[NAZWA DODATKU — przedłużacz zimowy 20 m]</h3>
                <ul className="mt-5 space-y-3">
                  <Bullet>[KORZYŚĆ DODATKU 1 — zasięg całej posesji]</Bullet>
                  <Bullet>[KORZYŚĆ DODATKU 2 — elastyczny na mrozie]</Bullet>
                  <Bullet>[KORZYŚĆ DODATKU 3 — bezpieczeństwo, IP44]</Bullet>
                </ul>
                <p className="text-brand mt-5 text-3xl font-extrabold">[CENA DODATKU] zł</p>
                <div className="mt-5">
                  <GradientButton onClick={() => addToCart("[DODATEK — przedłużacz zimowy 20 m]")}>
                    [CTA UPSELL — dodaj do zamówienia] <ChevronRight className="size-4" aria-hidden />
                  </GradientButton>
                </div>
              </div>
            </div>
          </Card>
        </Section>

        {/* 12. Bundle */}
        <Section id="zestaw" alt>
          <Eyebrow>[EYEBROW — zestaw]</Eyebrow>
          <SectionTitle>[NAGŁÓWEK BUNDLE — wszystko na zimę w jednym zamówieniu]</SectionTitle>
          <Card className="mx-auto mt-10 max-w-4xl">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {bundleItems.map((b) => (
                <div key={b.name} className="border-border bg-background rounded-2xl border p-4 text-center">
                  <div className="bg-surface mx-auto aspect-square w-full max-w-40 overflow-hidden rounded-xl">
                    <img
                      src={b.image}
                      alt={b.alt}
                      width={300}
                      height={300}
                      loading="lazy"
                      className="size-full object-cover"
                    />
                  </div>
                  <p className="mt-3 text-sm font-semibold">{b.name}</p>
                  <p className="text-muted-foreground text-xs">{b.price}</p>
                </div>
              ))}
            </div>
            <div className="mt-8 flex flex-col items-center text-center">
              <Pill>[OSZCZĘDNOŚĆ — „oszczędzasz XX zł”]</Pill>
              <div className="mt-4 flex items-end gap-3">
                <span className="text-brand text-4xl font-extrabold">[CENA ZESTAWU] zł</span>
                <span className="text-muted-foreground pb-1 line-through">[SUMA OSOBNO] zł</span>
              </div>
              <div className="mt-6 w-full max-w-md">
                <GradientButton full onClick={() => addToCart("[ZESTAW ZIMOWY]")}>
                  [CTA BUNDLE — biorę cały zestaw] <ChevronRight className="size-4" aria-hidden />
                </GradientButton>
              </div>
            </div>
          </Card>
        </Section>

        {/* 13. FAQ */}
        <Section id="faq">
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1fr)_1.4fr] lg:gap-12">
            <div>
              <Eyebrow className="lg:text-left">[EYEBROW — FAQ]</Eyebrow>
              <SectionTitle className="lg:text-left">[NAGŁÓWEK FAQ — „masz pytania? mamy odpowiedzi”]</SectionTitle>
              <p className="text-muted-foreground mt-4 text-center text-sm sm:text-base lg:text-left">
                [LEAD FAQ — zaproszenie do kontaktu, jeśli czegoś brakuje]
              </p>
            </div>
            <Accordion type="single" collapsible className="w-full">
              {faqs.map((f, i) => (
                <AccordionItem key={f.q} value={`faq-${i}`}>
                  <AccordionTrigger className="text-sm font-semibold sm:text-base">{f.q}</AccordionTrigger>
                  <AccordionContent className="text-muted-foreground">{f.a}</AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </Section>
      </main>

      {/* 14. Stopka */}
      <footer className="bg-surface border-border border-t px-4 py-10 pb-28 lg:pb-10">
        <div className="mx-auto flex w-full max-w-6xl flex-col items-center gap-5 text-center">
          <Logo />
          <nav className="text-muted-foreground flex flex-wrap justify-center gap-x-5 gap-y-2 text-sm">
            {footerLinks.map((l) => (
              <a key={l} href="#" className="hover:text-foreground">
                {l}
              </a>
            ))}
          </nav>
          <p className="text-muted-foreground text-xs">© {new Date().getFullYear()} [NAZWA FIRMY]. Wszelkie prawa zastrzeżone.</p>
        </div>
      </footer>

      {/* Sticky CTA na mobile */}
      <div
        className={cn(
          "bg-background/95 border-border fixed inset-x-0 bottom-0 z-30 border-t px-4 py-3 backdrop-blur transition-transform duration-300 lg:hidden",
          showSticky ? "translate-y-0" : "translate-y-full",
        )}
        aria-hidden={!showSticky}
      >
        <div className="mx-auto flex max-w-6xl items-center gap-3">
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-semibold">{PRODUCT_NAME}</p>
            <p className="text-brand text-sm font-extrabold">{PRICE}</p>
          </div>
          <button
            type="button"
            onClick={addMain}
            tabIndex={showSticky ? 0 : -1}
            className="bg-brand shadow-glow text-primary-foreground shrink-0 rounded-xl px-4 py-2.5 text-xs font-semibold"
          >
            [CTA KRÓTKIE]
          </button>
        </div>
      </div>

      {/* Koszyk (drawer) */}
      <Sheet open={cartOpen} onOpenChange={setCartOpen}>
        <SheetContent side="right" className="w-[88vw] sm:max-w-sm">
          <SheetHeader>
            <SheetTitle>Koszyk</SheetTitle>
            <SheetDescription>[MIKROCOPY KOSZYKA — darmowa wysyłka od XX zł]</SheetDescription>
          </SheetHeader>
          <div className="flex-1 overflow-y-auto px-4">
            {cart.length === 0 ? (
              <p className="text-muted-foreground text-sm">[KOSZYK PUSTY — zachęta do powrotu do produktu]</p>
            ) : (
              <ul className="space-y-3">
                {cart.map((item, i) => (
                  <li key={i} className="border-border flex items-start justify-between gap-3 rounded-xl border p-3 text-sm">
                    <span>{item}</span>
                    <button
                      type="button"
                      onClick={() => setCart((c) => c.filter((_, j) => j !== i))}
                      aria-label="Usuń z koszyka"
                      className="text-muted-foreground hover:text-foreground"
                    >
                      <X className="size-4" />
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <SheetFooter>
            <GradientButton full disabled={cart.length === 0}>
              [CTA KASA — przejdź do płatności] <ChevronRight className="size-4" aria-hidden />
            </GradientButton>
          </SheetFooter>
        </SheetContent>
      </Sheet>

      {/* Modal Kontakt */}
      <Dialog open={contactOpen} onOpenChange={setContactOpen}>
        <DialogContent className="max-w-[92vw] rounded-[20px] sm:max-w-md">
          <DialogTitle>Kontakt</DialogTitle>
          <DialogDescription className="text-foreground text-base">
            Skontaktuj się tutaj z nami:{" "}
            <a href={`mailto:${CONTACT_EMAIL}`} className="text-primary font-semibold underline underline-offset-4">
              {CONTACT_EMAIL}
            </a>
          </DialogDescription>
          <GradientButton full onClick={() => setContactOpen(false)}>
            Zamknij
          </GradientButton>
        </DialogContent>
      </Dialog>
    </div>
  );
}
