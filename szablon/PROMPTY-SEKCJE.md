# Prompty do każdej sekcji sklepu (ogólne)

Jak używać: otwórz nowy czat w Claude Code i wklej **najpierw PROMPT 0**, potem kolejne prompty po kolei (albo wszystkie naraz). Na początku dopisz swoje dane, np.: „Marka: …, produkt: …, kolor przewodni: …, ceny: …, e-mail: …” – Claude podmieni kolor w tokenach :root i teksty w [NAWIASACH]. Kod w każdym prompcie to WZÓR wyglądu i działania – Claude ma go odtworzyć 1:1 w strukturze i zachowaniu, a treści, zdjęcia i kolor dopasować do mojego produktu.

Dopisek do każdego promptu (już jest wliczony): *teksty sprzedażowe po polsku, psychologiczne, bez nawiasów [ ] w wersji końcowej; zdjęcia moje albo wygenerowane; wszystko ma działać na telefonie.*

---

## PROMPT 0. FUNDAMENT (wklej jako pierwszy)

```text
Zbuduj jednostronicowy sklep z jednym produktem jako JEDEN plik index.html (HTML + CSS + czysty JS, bez frameworków). Wszystkie kolory, cienie i zaokrąglenia trzymaj w tokenach CSS w :root (prefiks --sk-), żeby zmiana koloru marki była w jednym miejscu – kolor podam osobno, na razie użyj tego niebieskiego. Czcionki: Poppins (tekst) + Russo One (nagłówki, logo). Mobile-first, max szerokość treści ok. 1200 px, sekcje z dużym oddechem, karty z miękkim cieniem i zaokrągleniem 20 px, przyciski CTA z gradientem i cieniem. Strona ma dwa „widoki”: #skHome (strona produktu) i #skPages (podstrony polityk) przełączane funkcją skShow(). Poniżej: <head>, bazowy CSS (tokeny, reset, przyciski, kontenery, animacje, wersja mobilna) i początek skryptu (zdjęcia, galeria). Kolejne prompty dokładają po jednej sekcji – wstawiaj je w tej kolejności.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>[NAZWA SKLEPU] – [NAZWA PRODUKTU]</title>
<meta name="description" content="[OPIS SEO – 1–2 zdania z korzyścią]">
<meta property="og:title" content="[NAZWA SKLEPU] – [OBIETNICA]">
<meta property="og:description" content="[OPIS DO UDOSTĘPNIEŃ]">
<meta property="og:type" content="product">
<meta property="og:image" content="{{IMG}}/foto-4.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Russo+One&display=swap" rel="stylesheet">
```

**CSS**

```css
:root{
  --sk-bg:#FFFFFF;
  --sk-surface:#F6F8FC;
  --sk-surface-2:#EAF0FB;
  --sk-fg:#1B2333;
  --sk-muted:#5E6878;
  --sk-border:#E2E8F2;
  --sk-primary:#2F5BD8;
  --sk-primary-dark:#1D3A8A;
  --sk-primary-soft:#E8EEFC;
  --sk-gold:#2F5BD8;
  --sk-gold-soft:#E8EEFC;
  --sk-sale:#B8323A;
  --sk-sale-soft:#FBE9EA;
  --sk-ok:#2E8B57;
  --sk-gradient:linear-gradient(135deg,#4A74EC 0%,#2448B8 100%);
  --sk-gradient-gold:linear-gradient(135deg,#2448B8 0%,#1D3A8A 100%);
  --sk-shadow-card:0 6px 28px -10px rgba(47,91,216,.18);
  --sk-shadow-cta:0 12px 30px -10px rgba(47,91,216,.45);
  --sk-radius:20px;
  --sk-font:'Poppins',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  --sk-logo:'Russo One','Poppins',sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--sk-font);color:var(--sk-fg);background:var(--sk-bg);-webkit-font-smoothing:antialiased;line-height:1.55}
img{max-width:100%;display:block}
a{color:inherit}
button{font-family:inherit;cursor:pointer}
.sk-container{width:100%;max-width:1120px;margin:0 auto;padding:0 16px}
.sk-section{padding:56px 0}
@media(min-width:768px){.sk-section{padding:84px 0}}
.sk-alt{background:var(--sk-surface)}
.sk-eyebrow{display:block;text-align:center;font-size:12px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--sk-gold);margin-bottom:10px}
.sk-eyebrow.left{text-align:left}
.sk-h2{font-size:28px;line-height:1.2;font-weight:800;margin:0 0 12px;text-align:center;letter-spacing:-.01em}
@media(min-width:768px){.sk-h2{font-size:38px}}
.sk-h2.left{text-align:left}
.sk-lead{color:var(--sk-muted);text-align:center;max-width:640px;margin:0 auto 36px;font-size:15.5px}
.sk-lead.left{text-align:left;margin-left:0}
.sk-accent{color:var(--sk-primary);background:var(--sk-gradient);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.sk-gold{color:var(--sk-gold)}
.sk-card{background:#fff;border:1px solid var(--sk-border);border-radius:var(--sk-radius);box-shadow:var(--sk-shadow-card)}
.sk-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:0;border-radius:16px;padding:17px 26px;font-size:15.5px;font-weight:700;color:#fff;background:var(--sk-gradient);box-shadow:var(--sk-shadow-cta);transition:transform .15s,box-shadow .15s;text-decoration:none}
.sk-btn:hover{transform:scale(1.02)}
.sk-btn.full{width:100%}
.sk-btn.small{padding:11px 16px;font-size:13.5px;border-radius:12px}
.sk-pill{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:700;background:var(--sk-primary-soft);color:var(--sk-primary)}
.sk-pill.gold{background:var(--sk-gold-soft);color:#8A6015}
.sk-pill.sale{background:var(--sk-sale);color:#fff}
.sk-stars{color:#F2B33D;letter-spacing:1px}
.sk-check{flex:0 0 22px;width:22px;height:22px;border-radius:50%;background:var(--sk-gradient);display:inline-flex;align-items:center;justify-content:center;margin-top:1px}
.sk-check svg{width:12px;height:12px}
.sk-x{flex:0 0 22px;width:22px;height:22px;border-radius:50%;background:var(--sk-sale-soft);color:var(--sk-sale);display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;margin-top:1px}
.sk-list{list-style:none;padding:0;margin:0;display:grid;gap:12px}
.sk-list li{display:flex;gap:12px;align-items:flex-start;font-size:15px}
.sk-list b{font-weight:700}
.sk-photo{border-radius:var(--sk-radius);overflow:hidden;box-shadow:var(--sk-shadow-card)}
.sk-photo img{width:100%;height:100%;object-fit:cover}

/* animacje i telefon */
@media(min-width:960px){.sk-sticky{display:none}}
.sk-toast{position:fixed;left:50%;bottom:90px;transform:translateX(-50%) translateY(20px);background:var(--sk-primary-dark);color:#fff;padding:12px 18px;border-radius:12px;font-size:14px;font-weight:600;opacity:0;transition:all .25s;z-index:130;pointer-events:none}
.sk-toast.on{opacity:1;transform:translateX(-50%)}
img[width][height]{height:auto}
@media(min-width:960px){.sk-hero-grid>div:first-child{position:sticky;top:84px}}
.sk-use img,.sk-step img{aspect-ratio:16/10!important;height:auto}
.sk-photo img{aspect-ratio:4/3;height:auto}
.sk-gallery-main img{height:100%!important;width:100%}
.sk-thumbs img{height:100%!important}
.sk-deal{display:grid;max-width:980px;margin:0 auto;background:#fff;border:1px solid var(--sk-border);border-radius:28px;overflow:hidden;box-shadow:0 20px 60px -24px rgba(18,56,38,.35)}
@media(min-width:768px){.sk-deal{grid-template-columns:.85fr 1.15fr}}
.sk-deal-img{position:relative;background:linear-gradient(135deg,#E8F1EA 0%,#FBF1DC 100%);display:grid;place-items:center;padding:36px;min-height:260px}
.sk-deal-img img{width:72%;max-width:280px;aspect-ratio:1;object-fit:cover;border-radius:22px;box-shadow:0 22px 40px -16px rgba(18,56,38,.45);height:auto}
.sk-float{animation:sk-float 3.2s ease-in-out infinite}
@keyframes sk-float{0%,100%{transform:translateY(0) rotate(-1.5deg)}50%{transform:translateY(-16px) rotate(1.5deg)}}
.sk-spark{position:absolute;width:26px;height:26px;background:radial-gradient(circle,var(--sk-gold) 2px,transparent 3px) 50% 0/4px 10px no-repeat,radial-gradient(circle,var(--sk-gold) 2px,transparent 3px);opacity:.8;animation:sk-tw 2.4s ease-in-out infinite}
.sk-spark.s1{top:28px;right:34px}.sk-spark.s2{bottom:30px;left:30px;animation-delay:1.2s}
@keyframes sk-tw{0%,100%{transform:scale(.6);opacity:.3}50%{transform:scale(1.1);opacity:1}}
.sk-deal-body{padding:30px 24px;text-align:center}
@media(min-width:768px){.sk-deal-body{padding:36px 40px}}
.sk-deal-body h2{margin:0;font-size:32px;font-weight:800;color:var(--sk-primary)}
.sk-deal-badge{display:flex;align-items:center;justify-content:center;gap:10px;color:var(--sk-sale);margin:6px 0 4px}
.sk-deal-badge b{font-size:34px;font-weight:800}
.sk-deal-body p{color:var(--sk-muted);font-size:14.5px;margin:0 0 20px}
.sk-deal-timer{display:flex;justify-content:center;align-items:center;gap:10px;margin-bottom:22px}
.sk-deal-timer div{width:96px;padding:14px 0 10px;border-radius:18px;background:#fff;border:1px solid var(--sk-border);box-shadow:var(--sk-shadow-card)}
.sk-deal-timer b{display:block;font-size:40px;line-height:1;font-weight:800;color:var(--sk-primary);font-variant-numeric:tabular-nums}
.sk-deal-timer small{display:block;margin-top:6px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--sk-muted)}
.sk-deal-timer i{font-style:normal;font-size:30px;font-weight:800;color:var(--sk-gold)}
@media(max-width:420px){.sk-deal-timer div{width:78px}.sk-deal-timer b{font-size:32px}}
.sk-rev-row{padding-left:32px}
@media(max-width:767px){.sk-strip-in{gap:16px 10px}.sk-strip-item{font-size:12px;max-width:210px}}
.sk-ring{transform-origin:50% 20%;animation:sk-ring 2.4s ease-in-out infinite}
@keyframes sk-ring{0%,60%,100%{transform:rotate(0)}5%{transform:rotate(18deg)}10%{transform:rotate(-16deg)}15%{transform:rotate(14deg)}20%{transform:rotate(-12deg)}25%{transform:rotate(8deg)}30%{transform:rotate(-6deg)}35%{transform:rotate(0)}}
.sk-pulse{display:inline-block;animation:sk-pulse 1.6s ease-in-out infinite}
@keyframes sk-pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
.sk-deal-timer div b.tick{animation:sk-tick .35s ease}
@keyframes sk-tick{0%{transform:translateY(-6px);opacity:.3}100%{transform:none;opacity:1}}
.sk-deal .sk-btn{animation:sk-glow 2.2s ease-in-out infinite}
@keyframes sk-glow{0%,100%{box-shadow:var(--sk-shadow-cta)}50%{box-shadow:0 12px 34px -6px rgba(201,150,58,.75)}}
.sk-shine{background:linear-gradient(100deg,var(--sk-primary) 0%,var(--sk-primary) 40%,#E2B866 50%,var(--sk-primary) 60%,var(--sk-primary) 100%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:sk-shine 1.5s linear infinite,sk-bob 3.2s ease-in-out infinite;display:inline-block}
@keyframes sk-shine{0%{background-position:120% 0}100%{background-position:-120% 0}}
@keyframes sk-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.sk-nudge{animation:sk-nudge 2s ease-in-out infinite}
@keyframes sk-nudge{0%,60%,100%{transform:translateX(0)}68%{transform:translateX(-5px)}76%{transform:translateX(5px)}84%{transform:translateX(-3px)}92%{transform:translateX(2px)}}
.sk-beat{display:inline-block;animation:sk-pulse 1s ease-in-out infinite}
.sk-strip-item b{font-size:13px}.sk-strip-item small{font-size:11.5px}.sk-strip-item>span{font-size:18px!important}
@media(max-width:767px){.sk-strip-in{max-width:none;padding:10px 16px;column-gap:48px;row-gap:10px}}
.sk-gallery-caption{white-space:nowrap;max-width:calc(100% - 28px);overflow:hidden;text-overflow:ellipsis}
@media(max-width:959px){body{padding-bottom:84px}}
.sk-limit{display:inline-block;margin-top:8px;font-weight:800;color:var(--sk-sale);}
.sk-pills{display:flex;gap:6px;flex-wrap:nowrap;white-space:nowrap}
@media(max-width:400px){.sk-pills .sk-pill{font-size:10.5px;padding:5px 9px}}
.sk-gallery-main{touch-action:pan-y}
.sk-gallery-arrow{display:none!important}
html.sk-exp #skDealSec{display:none!important}
.sk-hero-grid>*{min-width:0}
.sk-pills{flex-wrap:wrap!important;white-space:normal!important}
```

**JS**

```js
(function(){
var IMG="{{IMG}}";
var KWI=window.SK_IMG||{};function skSrc(f){return KWI[f]||IMG+"/"+f}
var CHECKOUT_URL="/checkout"; /* Shopify: podmień na link do kasy lub /cart */
var EMAIL="[E-MAIL KONTAKTOWY]";

var gallery=[
 ["foto-1.jpg","⭐ [PODPIS ZDJĘCIA 1 – korzyść]"],
 ["foto-2.jpg","⭐ [PODPIS ZDJĘCIA 2 – korzyść]"],
 ["foto-3.jpg","⭐ [PODPIS ZDJĘCIA 3 – korzyść]"],
 ["foto-4.jpg","⭐ [PODPIS ZDJĘCIA 4 – korzyść]"],
 ["foto-5.jpg","⭐ [PODPIS ZDJĘCIA 5 – korzyść]"],
 ["foto-6.jpg","⭐ [PODPIS ZDJĘCIA 6 – korzyść]"]
];
var gi=0,main=document.getElementById("skMain"),cap=document.getElementById("skCaption"),dots=document.getElementById("skDots"),th=document.getElementById("skThumbs");
gallery.forEach(function(g,i){
  var d=document.createElement("button");d.setAttribute("aria-label","Zdjęcie "+(i+1));d.onclick=function(){setG(i)};dots.appendChild(d);
  var t=document.createElement("button");t.innerHTML='<img src="'+skSrc(g[0])+'" width="200" height="200" loading="lazy" alt="">';t.onclick=function(){setG(i)};th.appendChild(t);
});
function setG(i){gi=(i+gallery.length)%gallery.length;main.style.opacity=.3;setTimeout(function(){main.src=skSrc(gallery[gi][0]);main.style.opacity=1},120);cap.textContent=gallery[gi][1];
  [].forEach.call(dots.children,function(b,k){b.classList.toggle("on",k===gi)});[].forEach.call(th.children,function(b,k){b.classList.toggle("on",k===gi)});}
window.skGal=function(s){setG(gi+s)};setG(0);
(function(){var g=document.querySelector(".sk-gallery-main"),x0=null,y0=null;
 g.addEventListener("touchstart",function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
 g.addEventListener("touchend",function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;
  if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy))setG(gi+(dx<0?1:-1));x0=null},{passive:true});})();
```

---

## PROMPT 1. PASEK PROMOCJI + MENU Z LOGO

```text
Na samej górze cienki pasek w kolorze marki z napisami przesuwającymi się płynnie od prawej do lewej w nieskończoność (np. darmowa dostawa, zwroty, promocja, hasło marki – teksty powielone 3×, żeby nie było przerwy). Pod nim biały, przyklejony nagłówek: po lewej logo (mała ikona produktu ok. 46 px + nazwa sklepu i mały podpis wersalikami), na środku menu z kotwicami do sekcji, po prawej ikona koszyka z licznikiem. Na telefonie menu chowa się pod „hamburgerem” i wysuwa na pełny ekran.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<div class="sk-topbar" aria-label="Promocje">
  <div class="sk-marquee">
    <span>[KORZYŚĆ 1 – np. Darmowa wysyłka]</span><span>[KORZYŚĆ 2 – np. 14 dni na zwrot]</span><span>[PROMOCJA]</span><span>[HASŁO MARKI]</span>
    <span>[KORZYŚĆ 1 – np. Darmowa wysyłka]</span><span>[KORZYŚĆ 2 – np. 14 dni na zwrot]</span><span>[PROMOCJA]</span><span>[HASŁO MARKI]</span>
    <span>[KORZYŚĆ 1 – np. Darmowa wysyłka]</span><span>[KORZYŚĆ 2 – np. 14 dni na zwrot]</span><span>[PROMOCJA]</span><span>[HASŁO MARKI]</span>
  </div>
</div>

<header class="sk-nav">
  <div class="sk-container sk-nav-in">
    <button class="sk-icon-btn sk-burger" aria-label="Otwórz menu" onclick="skMenu(true)">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <a href="#" class="sk-logo" onclick="skShow('home');return false">
      <img src="{{IMG}}/logo.png" width="26" height="46" alt=""><div><span>[NAZWA]</span><small>[PODPIS POD LOGO]</small></div>
    </a>
    <nav class="sk-menu">
      <a href="#zastosowania" onclick="skShow('home')">[MENU 1 – zastosowania]</a>
      <a href="#jak-dziala" onclick="skShow('home')">[MENU 2 – jak działa]</a>
      <a href="#zestaw" onclick="skShow('home')">[MENU 3 – zestaw]</a>
      <a href="#porownanie" onclick="skShow('home')">[MENU 4 – porównanie]</a>
      <a href="#opinie" onclick="skShow('home')">[MENU 5 – opinie]</a>
      <a href="#faq" onclick="skShow('home')">[MENU 6 – FAQ]</a>
    </nav>
    <button class="sk-icon-btn" aria-label="Koszyk" onclick="skCart(true)">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>
      <span class="sk-cart-count" id="skCount" hidden>0</span>
    </button>
  </div>
</header>

<div class="sk-mobile-menu" id="skMobile">
  <div class="sk-mm-top">
    <span class="sk-logo"><img src="{{IMG}}/logo.png" width="26" height="46" alt=""><div><span>[NAZWA]</span><small>[PODPIS POD LOGO]</small></div></span>
    <button class="sk-icon-btn" aria-label="Zamknij menu" onclick="skMenu(false)">✕</button>
  </div>
  <nav>
    <a href="#hero" onclick="skMenu(false);skShow('home')">[NAZWA PRODUKTU]</a>
    <a href="#jak-dziala" onclick="skMenu(false);skShow('home')">Jak to działa</a>
    <a href="#opinie" onclick="skMenu(false);skShow('home')">Opinie</a>
    <a href="#faq" onclick="skMenu(false);skShow('home')">FAQ</a>
    <a href="#" onclick="skMenu(false);skShow('kontakt');return false">Kontakt</a>
  </nav>
  <button class="sk-mm-close" onclick="skMenu(false)">Zamknij menu.</button>
</div>
```

**CSS**

```css
.sk-topbar{background:var(--sk-primary-dark);color:#fff;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;overflow:hidden;white-space:nowrap;padding:9px 0}
.sk-marquee{display:inline-flex;gap:42px;animation:sk-scroll 40s linear infinite;padding-left:42px}
.sk-marquee span{display:inline-flex;align-items:center;gap:42px}
.sk-marquee span::after{content:"✦";color:var(--sk-gold)}
@keyframes sk-scroll{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
.sk-nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--sk-border)}
.sk-nav-in{display:flex;align-items:center;justify-content:space-between;height:64px;gap:16px}
.sk-logo{display:flex;align-items:center;gap:9px;text-decoration:none;font-family:var(--sk-logo);font-size:24px;color:var(--sk-primary-dark);letter-spacing:.01em}
.sk-logo img{height:46px!important;width:auto!important;max-width:none}
.sk-logo span{font-family:var(--sk-logo);font-size:26px;line-height:1;color:var(--sk-primary-dark)}
.sk-logo small{display:block;font-family:var(--sk-font);font-size:9px;font-weight:700;letter-spacing:.24em;color:var(--sk-gold);margin-top:3px}
.sk-salebar{background:var(--sk-sale);color:#fff;text-align:center;padding:8px 12px;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}
.sk-salebar .sk-timer span{background:#fff;color:var(--sk-sale);border-radius:7px;padding:3px 7px;font-weight:800;font-variant-numeric:tabular-nums;min-width:30px;display:inline-block}
.sk-salebar .sk-timer i{font-style:normal;font-size:10px;font-weight:600;opacity:.85;margin:0 4px 0 2px}
.sk-pay span{display:inline-flex;align-items:center;gap:4px;height:28px;border-radius:7px;padding:0 10px;font-size:12px;font-weight:800;color:#fff;border:0;letter-spacing:.01em}
.pay-blik{background:#111}.pay-visa{background:#1A1F71;font-style:italic;letter-spacing:.04em!important}.pay-mc{background:#2B2B33}.pay-apple{background:#000}.pay-google{background:#3C4043}.pay-p24{background:#D13239}
.sk-rev .pfp{width:38px;height:38px;border-radius:50%;object-fit:cover;flex:0 0 38px;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.15)}
.sk-menu{display:none;gap:22px;font-size:13.5px;font-weight:500}
.sk-menu a{text-decoration:none;color:var(--sk-muted)}
.sk-menu a:hover{color:var(--sk-primary)}
@media(min-width:960px){.sk-menu{display:flex}}
.sk-icon-btn{width:42px;height:42px;border-radius:12px;border:1px solid var(--sk-border);background:#fff;display:grid;place-items:center;position:relative}
.sk-cart-count[hidden]{display:none}
.sk-cart-count{position:absolute;top:-6px;right:-6px;min-width:20px;height:20px;border-radius:10px;background:var(--sk-sale);color:#fff;font-size:11px;font-weight:700;display:grid;place-items:center;padding:0 5px}
.sk-burger{display:grid}
@media(min-width:960px){.sk-burger{display:none}}
.sk-mobile-menu{position:fixed;inset:0;z-index:100;background:#fff;display:none;flex-direction:column}
.sk-mobile-menu.open{display:flex}
.sk-mobile-menu .sk-mm-top{display:flex;justify-content:space-between;align-items:center;height:64px;padding:0 16px;border-bottom:1px solid var(--sk-border)}
.sk-mobile-menu nav{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px}
.sk-mobile-menu nav a{font-size:24px;font-weight:700;text-decoration:none}
.sk-mobile-menu .sk-mm-close{margin:0 auto 40px;background:none;border:0;text-decoration:underline;color:var(--sk-muted);font-size:15px}
```

---

## PROMPT 2. HERO: GALERIA, CENA, ZESTAWY + PASEK KORZYŚCI

```text
Pierwszy ekran sprzedażowy w dwóch kolumnach. Lewa: galeria (duże zdjęcie z podpisem na dole + miniatury), na komputerze przyklejona (sticky) podczas przewijania, na telefonie przesuwana palcem (swipe), bez strzałek. Pierwsze zdjęcie = ludzie używający produktu. Prawa: plakietki („Hit…” + „Liczba sztuk ograniczona”), nazwa, gwiazdki z liczbą opinii i „X osób ogląda teraz”, cena + cena przekreślona + procent rabatu, lista 6 korzyści z ikonami „✓”, wybór zestawu 1/2/3 sztuki jako karty z radiem (plakietki „Najczęściej wybierany”, „Najlepsza cena”) – po kliknięciu zestawu pod nim pojawia się wybór wariantu dla każdej sztuki (dwa małe przyciski A/B na każdą sztukę), duży przycisk „Dodaj do koszyka · cena”, linijka zaufania i kolorowe logotypy płatności. Cena w nagłówku, przycisku i pasku na dole zmienia się po wyborze zestawu. Pod hero pełnoszeroki pasek w kolorze marki z 4 kafelkami (dostawa, zwroty, płatności, ocena) – na telefonie 2×2.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- HERO -->
<section class="sk-hero" id="hero">
  <div class="sk-container sk-hero-grid">
    <div>
      <div class="sk-gallery-main">
        <img id="skMain" src="{{IMG}}/foto-1.jpg" width="1200" height="1200" alt="[OPIS ZDJĘCIA 1]">
        <button class="sk-gallery-arrow prev" aria-label="Poprzednie zdjęcie" onclick="skGal(-1)">‹</button>
        <button class="sk-gallery-arrow next" aria-label="Następne zdjęcie" onclick="skGal(1)">›</button>
        <div class="sk-gallery-caption" id="skCaption">⭐ [PODPIS ZDJĘCIA 1 – korzyść]</div>
      </div>
      <div class="sk-dots" id="skDots"></div>
      <div class="sk-thumbs" id="skThumbs"></div>
    </div>

    <div class="sk-buy">
      <div class="sk-pills"><span class="sk-pill gold">★ [PLAKIETKA – np. Bestseller 2026]</span><span class="sk-pill sale">⚠️ [PILNOŚĆ – np. Liczba sztuk ograniczona]</span></div>
      <h1>[NAGŁÓWEK GŁÓWNY – problem klienta + obietnica] <span class="sk-accent">[EFEKT KOŃCOWY]</span></h1>
      <p class="sk-sub">[PODTYTUŁ – jak produkt zmienia dzień klienta, 1–2 zdania]</p>
      <div class="sk-rating"><span class="sk-stars">★★★★★</span><b>[OCENA]</b> · [LICZBA] opinii · <span style="color:var(--sk-ok);font-weight:600">● [LICZBA] osób ogląda teraz</span></div>
      <div class="sk-price-row">
        <span class="sk-price" id="skPrice">199,99 zł</span>
        <span class="sk-old" id="skOld">299,99 zł</span>
        <span class="sk-save" id="skSave">−33%</span>
      </div>
      <ul class="sk-list">
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[KORZYŚĆ 1]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[KORZYŚĆ 2]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[KORZYŚĆ 3]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[KORZYŚĆ 4]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[KORZYŚĆ 5]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[KORZYŚĆ 6]</b> [dopowiedzenie]</span></li>
      </ul>

      <div class="sk-bundles" id="skBundles">
        <div class="sk-bundles-title">[WYBIERZ ZESTAW]</div>
      </div>

      <button class="sk-btn full" onclick="skAddBundle()">Dodaj do koszyka · <span id="skCtaPrice">199,99 zł</span>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></button>
      <div class="sk-pay"><span class="pay-blik">blik</span><span class="pay-visa">VISA</span><span class="pay-mc"><svg width="22" height="14" viewBox="0 0 22 14"><circle cx="7" cy="7" r="7" fill="#EB001B"/><circle cx="15" cy="7" r="7" fill="#F79E1B" fill-opacity=".9"/></svg>mastercard</span><span class="pay-apple"><svg width="12" height="14" viewBox="0 0 17 20" fill="#fff"><path d="M14.1 10.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9C3.6 4.8 2 5.8 1.1 7.4c-1.8 3.2-.5 7.9 1.3 10.5.9 1.3 1.9 2.7 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.6 1-1.5 1.4-2.9 1.4-3-.1 0-2.7-1-2.7-4.3zM11.6 3c.7-.9 1.2-2 1-3.2-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.1 1.2.1 2.3-.6 3.1-1.5z"/></svg>Pay</span><span class="pay-google"><svg width="13" height="13" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>Pay</span><span class="pay-p24">P24</span></div>
      <p class="sk-micro">🔒 [MIKROZAUFANIE – płatność · zwroty · kontakt]</p>
    </div>
  </div>
</section>

<div class="sk-strip">
  <div class="sk-container sk-strip-in">
    <div class="sk-strip-item"><span style="font-size:22px">🚚</span><div><b>[DOSTAWA]</b><small>[sposób dostawy]</small></div></div>
    <div class="sk-strip-item"><span style="font-size:22px">↩️</span><div><b>[ZWROTY]</b><small>[krótki dopisek]</small></div></div>
    <div class="sk-strip-item"><span style="font-size:22px">🔒</span><div><b>[PŁATNOŚCI]</b><small>[metody płatności]</small></div></div>
    <div class="sk-strip-item"><span style="font-size:22px">⭐</span><div><b>[OCENA]</b><small>[liczba zadowolonych]</small></div></div>
  </div>
</div>
```

**CSS**

```css
.sk-hero{padding:28px 0 56px}
.sk-hero-grid{display:grid;gap:28px}
@media(min-width:960px){.sk-hero-grid{grid-template-columns:1.05fr 1fr;gap:44px;align-items:start}}
.sk-gallery-main{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:1/1;background:var(--sk-surface);box-shadow:var(--sk-shadow-card)}
.sk-gallery-main img{width:100%;height:100%;object-fit:cover;transition:opacity .25s}
.sk-gallery-caption{position:absolute;left:14px;bottom:14px;background:rgba(255,255,255,.94);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:600;display:flex;gap:6px;align-items:center;box-shadow:0 4px 14px rgba(0,0,0,.12)}
.sk-gallery-arrow{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.92);display:grid;place-items:center;box-shadow:0 4px 14px rgba(0,0,0,.15)}
.sk-gallery-arrow.prev{left:12px}.sk-gallery-arrow.next{right:12px}
.sk-dots{display:flex;justify-content:center;gap:6px;margin:12px 0}
.sk-dots button{width:8px;height:8px;border-radius:4px;border:0;background:#D8D0C2;padding:0;transition:width .2s}
.sk-dots button.on{width:24px;background:var(--sk-primary)}
.sk-thumbs{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.sk-thumbs button{border:2px solid transparent;border-radius:12px;overflow:hidden;padding:0;aspect-ratio:1/1;background:none}
.sk-thumbs button.on{border-color:var(--sk-primary)}
.sk-thumbs img{width:100%;height:100%;object-fit:cover}
.sk-trust-tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}
.sk-trust-tile{display:flex;gap:10px;align-items:center;border:1px solid var(--sk-border);border-radius:14px;padding:12px;background:#fff}
.sk-trust-tile .ic{width:36px;height:36px;border-radius:10px;background:var(--sk-primary-soft);display:grid;place-items:center;flex:0 0 36px}
.sk-trust-tile b{display:block;font-size:13px}
.sk-trust-tile small{color:var(--sk-muted);font-size:11.5px;line-height:1.35;display:block}

.sk-buy h1{font-size:28px;line-height:1.18;font-weight:800;margin:12px 0 10px;letter-spacing:-.015em}
@media(min-width:768px){.sk-buy h1{font-size:36px}}
.sk-sub{color:var(--sk-muted);font-size:15px;margin:0 0 14px}
.sk-rating{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--sk-muted);margin-bottom:16px;flex-wrap:wrap}
.sk-rating b{color:var(--sk-fg)}
.sk-price-row{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.sk-price{font-size:34px;font-weight:800;color:var(--sk-primary)}
.sk-old{font-size:18px;color:var(--sk-muted);text-decoration:line-through}
.sk-save{background:var(--sk-sale);color:#fff;border-radius:8px;padding:3px 9px;font-size:12.5px;font-weight:700}
.sk-klarna{display:flex;align-items:center;gap:10px;border:1px solid rgba(30,91,61,.25);background:rgba(30,91,61,.05);border-radius:12px;padding:10px 12px;font-size:13px;margin:12px 0 18px}
.sk-countdown{display:flex;align-items:center;justify-content:space-between;gap:10px;background:var(--sk-sale-soft);border:1px dashed rgba(184,50,58,.4);border-radius:14px;padding:10px 14px;margin:18px 0;font-size:13px;font-weight:600;color:var(--sk-sale)}
.sk-timer{display:flex;gap:6px}
.sk-timer span{background:#fff;border-radius:8px;padding:4px 7px;font-weight:800;font-variant-numeric:tabular-nums;color:var(--sk-fg);min-width:34px;text-align:center}
.sk-bundles{display:grid;gap:12px;margin:18px 0}
.sk-bundles-title{text-align:center;font-size:12px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--sk-muted);display:flex;align-items:center;gap:12px}
.sk-bundles-title::before,.sk-bundles-title::after{content:"";flex:1;height:1px;background:var(--sk-border)}
.sk-flower{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;border:2px solid var(--sk-border);border-radius:12px;padding:8px 6px;background:#fff;font:inherit;font-weight:600;font-size:14px;color:var(--sk-fg);cursor:pointer;transition:border-color .15s,background .15s,transform .15s}.sk-flower span{font-size:18px;line-height:1}.sk-flower.on{border-color:var(--sk-primary);background:var(--sk-primary-soft);transform:translateY(-1px)}
.sk-bundle{position:relative;border:2px solid var(--sk-border);border-radius:18px;padding:14px 16px;cursor:pointer;background:#fff;transition:border-color .15s,background .15s}
.sk-bundle.on{border-color:var(--sk-primary);background:var(--sk-primary-soft)}
.sk-bundle-head{display:flex;align-items:center;gap:12px}
.sk-radio{width:20px;height:20px;border-radius:50%;border:2px solid #C9C0B0;flex:0 0 20px;display:grid;place-items:center}
.sk-bundle.on .sk-radio{border-color:var(--sk-primary)}
.sk-bundle.on .sk-radio::after{content:"";width:10px;height:10px;border-radius:50%;background:var(--sk-primary)}
.sk-bundle-name{font-weight:700;font-size:15px}
.sk-bundle-desc{font-size:12.5px;color:var(--sk-muted)}
.sk-bundle-price{margin-left:auto;text-align:right}
.sk-bundle-price b{display:block;font-size:17px;color:var(--sk-primary)}
.sk-bundle-price s{font-size:12.5px;color:var(--sk-muted)}
.sk-bundle-tag{position:absolute;top:-11px;right:14px;font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:4px 10px;color:#fff;background:var(--sk-gradient)}
.sk-bundle-tag.gold{background:var(--sk-gradient-gold)}
.sk-variants{display:none;margin-top:12px;padding-top:12px;border-top:1px dashed rgba(30,91,61,.25)}
.sk-bundle.on .sk-variants{display:grid;gap:10px}
.sk-var-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:12.5px}
.sk-var-row .lbl{color:var(--sk-muted);min-width:92px;font-weight:600}.sk-var-row{flex-wrap:nowrap!important}.sk-bundle-price b{white-space:nowrap}.sk-var-row .sk-flower{padding:6px 4px;font-size:13px}
.sk-var-row .lbl b{color:var(--sk-primary)}
.sk-swatch{width:38px;height:38px;border-radius:50%;border:2px solid #fff;outline:2px solid var(--sk-border);padding:0;overflow:hidden;background:#fff}
.sk-swatch.on{outline-color:var(--sk-primary)}
.sk-swatch img{width:100%;height:100%;object-fit:cover}
.sk-ship-box{display:flex;gap:10px;align-items:flex-start;background:var(--sk-surface);border-radius:14px;padding:12px 14px;font-size:13px;margin:14px 0}
.sk-pay{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:12px}
.sk-micro{text-align:center;font-size:12.5px;color:var(--sk-muted);margin-top:10px}
.sk-strip{background:var(--sk-primary-dark);color:#fff}
.sk-strip-in{display:grid;grid-template-columns:1fr 1fr;gap:10px 48px;padding:10px 0;max-width:1120px}
@media(min-width:768px){.sk-strip-in{grid-template-columns:repeat(4,1fr)}}
.sk-strip-item{display:flex;gap:10px;align-items:center;justify-content:flex-start;font-size:13px;justify-self:center;width:100%;max-width:300px}
.sk-strip-item b{display:block;font-size:14px}
.sk-strip-item small{opacity:.75}
.sk-upsell{display:grid;gap:0;overflow:hidden}
@media(min-width:768px){.sk-upsell{grid-template-columns:1fr 1fr}}
.sk-upsell img{width:100%;height:100%;object-fit:cover;aspect-ratio:1/1}
.sk-upsell .b{padding:28px}
.sk-pill{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:700;background:var(--sk-primary-soft);color:var(--sk-primary)}
.sk-pill.gold{background:var(--sk-gold-soft);color:#8A6015}
.sk-pill.sale{background:var(--sk-sale);color:#fff}
.sk-gallery-main{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:1/1;background:var(--sk-surface);box-shadow:var(--sk-shadow-card)}
.sk-gallery-main img{width:100%;height:100%;object-fit:cover;transition:opacity .25s}
.sk-gallery-caption{position:absolute;left:14px;bottom:14px;background:rgba(255,255,255,.94);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:600;display:flex;gap:6px;align-items:center;box-shadow:0 4px 14px rgba(0,0,0,.12)}
.sk-gallery-arrow{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.92);display:grid;place-items:center;box-shadow:0 4px 14px rgba(0,0,0,.15)}
.sk-gallery-arrow.prev{left:12px}.sk-gallery-arrow.next{right:12px}
.sk-flower{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;border:2px solid var(--sk-border);border-radius:12px;padding:8px 6px;background:#fff;font:inherit;font-weight:600;font-size:14px;color:var(--sk-fg);cursor:pointer;transition:border-color .15s,background .15s,transform .15s}.sk-flower span{font-size:18px;line-height:1}.sk-flower.on{border-color:var(--sk-primary);background:var(--sk-primary-soft);transform:translateY(-1px)}
.sk-variants{display:none;margin-top:12px;padding-top:12px;border-top:1px dashed rgba(30,91,61,.25)}
.sk-bundle.on .sk-variants{display:grid;gap:10px}
.sk-var-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:12.5px}
.sk-var-row .lbl{color:var(--sk-muted);min-width:92px;font-weight:600}.sk-var-row{flex-wrap:nowrap!important}.sk-bundle-price b{white-space:nowrap}.sk-var-row .sk-flower{padding:6px 4px;font-size:13px}
.sk-var-row .lbl b{color:var(--sk-primary)}
.sk-gallery-main img{height:100%!important;width:100%}
.sk-gallery-caption{white-space:nowrap;max-width:calc(100% - 28px);overflow:hidden;text-overflow:ellipsis}
.sk-pills{display:flex;gap:6px;flex-wrap:nowrap;white-space:nowrap}
@media(max-width:400px){.sk-pills .sk-pill{font-size:10.5px;padding:5px 9px}}
.sk-gallery-main{touch-action:pan-y}
.sk-gallery-arrow{display:none!important}
.sk-pills{flex-wrap:wrap!important;white-space:normal!important}
```

**JS**

```js
/* BUNDLES */
/* PROMO 48h: liczona od pierwszej wizyty na tym urządzeniu */
var SK_END;try{SK_END=+localStorage.getItem("skDealEnd")}catch(e){}
if(!SK_END){SK_END=Date.now()+48*3600*1000;try{localStorage.setItem("skDealEnd",SK_END)}catch(e){}}
var SK_EXP=Date.now()>=SK_END;if(SK_EXP)document.documentElement.classList.add("sk-exp");
var BUNDLES=[
 {q:1,name:"[Kup 1]",desc:"[Pakiet startowy]",price:99.99,old:149.99},
 {q:2,name:"[Kup 2]",desc:"[Oszczędzasz X zł · cena za szt.]",price:179.98,old:299.98,tag:"[NAJCZĘŚCIEJ WYBIERANY]"},
 {q:3,name:"[Kup 3]",desc:"[Najlepsza cena za szt.]",price:239.97,old:449.97,tag:"[NAJLEPSZA CENA]",gold:true}
];
var sel=0;
function zl(n){return n.toFixed(2).replace(".",",").replace(/\B(?=(\d{3})+(?!\d))/g," ")+" zł"}
var bw=document.getElementById("skBundles");
var CH=BUNDLES.map(function(b){var a=[];for(var k=0;k<b.q;k++)a.push("[WARIANT A]");return a});
BUNDLES.forEach(function(b,i){
  var el=document.createElement("div");el.className="sk-bundle";el.onclick=function(){pick(i)};
  el.innerHTML=(b.tag?'<span class="sk-bundle-tag'+(b.gold?' gold':'')+'">'+b.tag+'</span>':'')+
   '<div class="sk-bundle-head"><span class="sk-radio"></span><div><div class="sk-bundle-name">'+b.name+'</div><div class="sk-bundle-desc">'+b.desc+'</div></div><div class="sk-bundle-price"><b>'+zl(b.price)+'</b><s>'+zl(b.old)+'</s></div></div>'+
   '<div class="sk-variants">'+CH[i].map(function(f,k){return '<div class="sk-var-row"><span class="lbl">'+(b.q>1?'Sztuka '+(k+1)+':':'Wybierz wariant:')+'</span><button type="button" class="sk-flower'+(f==="[WARIANT A]"?' on':'')+'" data-i="'+i+'" data-k="'+k+'" data-f="[WARIANT A]"><span>🅰️</span>[WARIANT A]</button><button type="button" class="sk-flower'+(f==="[WARIANT B]"?' on':'')+'" data-i="'+i+'" data-k="'+k+'" data-f="[WARIANT B]"><span>🅱️</span>[WARIANT B]</button></div>'}).join('')+'</div>';
  el.querySelectorAll('.sk-flower').forEach(function(btn){btn.onclick=function(e){e.stopPropagation();var ii=+btn.dataset.i,kk=+btn.dataset.k;CH[ii][kk]=btn.dataset.f;btn.parentNode.querySelectorAll('.sk-flower').forEach(function(x){x.classList.toggle('on',x===btn)});pick(ii)}});
  bw.appendChild(el);
});
function pick(i){sel=i;render()}
function render(){
  [].forEach.call(bw.querySelectorAll(".sk-bundle"),function(el,i){el.classList.toggle("on",i===sel);});
  var b=BUNDLES[sel];
  document.getElementById("skPrice").textContent=zl(b.price);document.getElementById("skOld").textContent=zl(b.old);
  document.getElementById("skSave").textContent="−"+Math.round((1-b.price/b.old)*100)+"%";
  document.getElementById("skCtaPrice").textContent=zl(b.price);
  document.getElementById("skStickyPrice").innerHTML=zl(b.price)+' <s style="color:var(--sk-muted);font-weight:400">'+zl(b.old)+'</s>';
}
render();
```

---

## PROMPT 3. PROBLEM

```text
Sekcja „ból klienta”: dwie kolumny – zdjęcie (na telefonie nad tekstem) i tekst: mały nadtytuł wersalikami, mocny nagłówek nazywający problem, 2 krótkie akapity budujące emocję i lista 3–4 punktów z czerwonym „✕”. Tło jasne, zdjęcie z zaokrągleniem i cieniem.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- PROBLEM -->
<section class="sk-section sk-alt" id="problem">
  <div class="sk-container sk-two">
    <div>
      <span class="sk-eyebrow left">[NADTYTUŁ – np. Brzmi znajomo?]</span>
      <h2 class="sk-h2 left">[NAGŁÓWEK PROBLEMU – frustracja klienta] <span class="sk-accent">[SŁOWO KLUCZ]</span></h2>
      <p class="sk-lead left">[ZDANIE WYJAŚNIAJĄCE PROBLEM]</p>
      <ul class="sk-list sk-pain">
        <li><span class="sk-x">✕</span><span>[PROBLEM 1]</span></li>
        <li><span class="sk-x">✕</span><span>[PROBLEM 2]</span></li>
        <li><span class="sk-x">✕</span><span>[PROBLEM 3]</span></li>
        <li><span class="sk-x">✕</span><span>[PROBLEM 4]</span></li>
        <li><span class="sk-x">✕</span><span>[PROBLEM 5]</span></li>
        <li><span class="sk-x">✕</span><span>[PROBLEM 6]</span></li>
      </ul>
      <div class="sk-bridge">[PODSUMOWANIE – skutek problemów w 1 zdaniu, pytanie „a gdyby…”]</div>
    </div>
    <div class="sk-photo" style="aspect-ratio:4/3"><img src="{{IMG}}/problem.jpg" width="1200" height="900" loading="lazy" alt="[OPIS ZDJĘCIA]"></div>
  </div>
</section>
```

**CSS**

```css
.sk-two{display:grid;gap:32px;align-items:center}
@media(min-width:900px){.sk-two{grid-template-columns:1fr 1fr;gap:56px}}
.sk-pain{display:grid;gap:10px}
.sk-pain li{background:#fff;border:1px solid var(--sk-border);border-radius:14px;padding:12px 14px}
.sk-bridge{margin-top:18px;border-radius:16px;background:var(--sk-primary-soft);padding:16px 18px;font-size:15px;font-weight:600;color:var(--sk-primary-dark)}
```

---

## PROMPT 4. KOMU SPRAWISZ RADOŚĆ (3 KARTY)

```text
Wyśrodkowany nagłówek + podtytuł, pod spodem 3 karty obok siebie (na telefonie jedna pod drugą): zdjęcie u góry, krótki tytuł i 1–2 zdania. Karty lekko unoszą się po najechaniu.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- USES -->
<section class="sk-section" id="zastosowania">
  <div class="sk-container">
    <span class="sk-eyebrow">[NADTYTUŁ – np. Gdzie się przydaje]</span>
    <h2 class="sk-h2">[NAGŁÓWEK ZASTOSOWAŃ] <span class="sk-accent">[SŁOWO KLUCZ]</span></h2>
    <p class="sk-lead">[PODTYTUŁ ZASTOSOWAŃ]</p>
    <div class="sk-uses">
      <article class="sk-card sk-use"><img src="{{IMG}}/foto-6.jpg" width="1200" height="1200" loading="lazy" alt="[ZASTOSOWANIE 1]"><div><h3>[ZASTOSOWANIE 1]</h3><p>[OPIS – 1 zdanie]</p></div></article>
      <article class="sk-card sk-use"><img src="{{IMG}}/zastosowanie-2.jpg" width="1200" height="900" loading="lazy" alt="[ZASTOSOWANIE 2]"><div><h3>[ZASTOSOWANIE 2]</h3><p>[OPIS – 1 zdanie]</p></div></article>
      <article class="sk-card sk-use"><img src="{{IMG}}/zastosowanie-3.jpg" width="1200" height="675" loading="lazy" alt="[ZASTOSOWANIE 3]"><div><h3>[ZASTOSOWANIE 3]</h3><p>[OPIS – 1 zdanie]</p></div></article>
    </div>
  </div>
</section>
```

**CSS**

```css
.sk-uses{display:grid;gap:18px}
@media(min-width:768px){.sk-uses{grid-template-columns:repeat(3,1fr)}}
.sk-use{overflow:hidden}
.sk-use img{aspect-ratio:4/3;object-fit:cover;width:100%}
.sk-use div{padding:18px 20px 22px}
.sk-use h3{margin:0 0 6px;font-size:17px}
.sk-use p{margin:0;color:var(--sk-muted);font-size:14px}
```

---

## PROMPT 5. ROZWIĄZANIE

```text
Lustrzane odbicie sekcji „Problem”: tekst po lewej, zdjęcie po prawej. Nadtytuł, nagłówek przedstawiający produkt jako rozwiązanie, akapit i lista korzyści z zielonym „✓”, na końcu przycisk CTA przewijający do wyboru zestawu.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- SOLUTION -->
<section class="sk-section sk-alt">
  <div class="sk-container sk-two">
    <div class="sk-photo" style="aspect-ratio:4/3"><img src="{{IMG}}/rozwiazanie.jpg" width="1200" height="900" loading="lazy" alt="[OPIS ZDJĘCIA]"></div>
    <div>
      <span class="sk-eyebrow left">[NADTYTUŁ – np. Dlatego powstał produkt]</span>
      <h2 class="sk-h2 left">[NAGŁÓWEK ROZWIĄZANIA – jak produkt rozwiązuje problem] <span class="sk-accent">[SŁOWO KLUCZ]</span></h2>
      <p class="sk-lead left">[ZDANIE O ROZWIĄZANIU]</p>
      <ul class="sk-list">
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[ULGA 1]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[ULGA 2]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[ULGA 3]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[ULGA 4]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[ULGA 5]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[ULGA 6]</b> [dopowiedzenie]</span></li>
      </ul>
    </div>
  </div>
</section>
```

**CSS**

```css
.sk-two{display:grid;gap:32px;align-items:center}
@media(min-width:900px){.sk-two{grid-template-columns:1fr 1fr;gap:56px}}
.sk-pain{display:grid;gap:10px}
.sk-pain li{background:#fff;border:1px solid var(--sk-border);border-radius:14px;padding:12px 14px}
.sk-bridge{margin-top:18px;border-radius:16px;background:var(--sk-primary-soft);padding:16px 18px;font-size:15px;font-weight:600;color:var(--sk-primary-dark)}
```

---

## PROMPT 6. W 3 KROKACH

```text
Nagłówek „Jak to działa” + 3 kroki w rzędzie (na telefonie w kolumnie): duży numer w kółku w kolorze marki, zdjęcie, tytuł kroku i jedno zdanie. Między krokami subtelna linia/strzałka.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- HOW IT WORKS -->
<section class="sk-section" id="jak-dziala">
  <div class="sk-container">
    <span class="sk-eyebrow">[NADTYTUŁ – np. Proste jak 1-2-3]</span>
    <h2 class="sk-h2">[EFEKT] <span class="sk-accent">w 3 krokach</span></h2>
    <p class="sk-lead">[PODTYTUŁ – co jest proste]</p>
    <ol class="sk-steps" style="list-style:none;padding:0;margin:0">
      <li class="sk-card sk-step"><span class="num">01</span><img src="{{IMG}}/krok-1.jpg" width="1200" height="900" loading="lazy" alt="[KROK 1]"><div class="t"><h3>[KROK 1]</h3><p>[OPIS KROKU 1]</p></div></li>
      <li class="sk-card sk-step"><span class="num">02</span><img src="{{IMG}}/krok-2.jpg" width="1200" height="900" loading="lazy" alt="[KROK 2]"><div class="t"><h3>[KROK 2]</h3><p>[OPIS KROKU 2]</p></div></li>
      <li class="sk-card sk-step"><span class="num">03</span><img src="{{IMG}}/krok-3.jpg" width="1200" height="900" loading="lazy" alt="[KROK 3]"><div class="t"><h3>[KROK 3]</h3><p>[OPIS KROKU 3]</p></div></li>
    </ol>
    <p class="sk-steps-foot">[ZDANIE PODSUMOWANIA KROKÓW]</p>
  </div>
</section>
```

**CSS**

```css
.sk-steps{display:grid;gap:18px}
@media(min-width:768px){.sk-steps{grid-template-columns:repeat(3,1fr)}}
.sk-step{overflow:hidden;position:relative}
.sk-step img{aspect-ratio:4/3;object-fit:cover;width:100%}
.sk-step .num{position:absolute;top:14px;left:14px;width:44px;height:44px;border-radius:14px;background:var(--sk-gradient);color:#fff;font-weight:800;display:grid;place-items:center;box-shadow:var(--sk-shadow-cta)}
.sk-step div.t{padding:18px 20px 22px}
.sk-step h3{margin:0 0 6px;font-size:17px}
.sk-step p{margin:0;color:var(--sk-muted);font-size:14px}
.sk-steps-foot{text-align:center;margin-top:26px;color:var(--sk-muted);font-size:14.5px}
```

---

## PROMPT 7. CO DOSTAJESZ (ZAKŁADKI)

```text
Sekcja z 3 zakładkami (np. „W zestawie”, „Specyfikacja”, „Dla kogo”): przyciski-pigułki u góry, aktywna wypełniona kolorem marki; treść zakładki to lista lub krótki tekst obok zdjęcia. Przełączanie bez przeładowania.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- WHAT YOU GET -->
<section class="sk-section sk-alt" id="zestaw">
  <div class="sk-container">
    <span class="sk-eyebrow">[NADTYTUŁ – np. W paczce]</span>
    <h2 class="sk-h2">Co dokładnie <span class="sk-accent">dostajesz</span></h2>
    <p class="sk-lead">[PODTYTUŁ ZESTAWU]</p>
    <div class="sk-tabs-list" role="tablist">
      <button class="on" onclick="skTab(0)">[ZAKŁADKA 1]</button>
      <button onclick="skTab(1)">[ZAKŁADKA 2]</button>
      <button onclick="skTab(2)">[ZAKŁADKA 3]</button>
    </div>
    <div class="sk-card sk-tab on">
      <div><h3>[NAZWA PRODUKTU / ZAKŁADKA 1]</h3><p>[OPIS ZESTAWU – 1–2 zdania]</p></div>
      <div class="sk-tab-panel"><small>[ZAWARTOŚĆ]</small><ul class="sk-list"><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 1]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 2]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 3]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 4]</li></ul></div>
    </div>
    <div class="sk-card sk-tab">
      <div><h3>[NAZWA PRODUKTU / ZAKŁADKA 2]</h3><p>[OPIS ZESTAWU – 1–2 zdania]</p></div>
      <div class="sk-tab-panel"><small>[ZAWARTOŚĆ]</small><ul class="sk-list"><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 1]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 2]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 3]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 4]</li></ul></div>
    </div>
    <div class="sk-card sk-tab">
      <div><h3>[NAZWA PRODUKTU / ZAKŁADKA 3]</h3><p>[OPIS ZESTAWU – 1–2 zdania]</p></div>
      <div class="sk-tab-panel"><small>[ZAWARTOŚĆ]</small><ul class="sk-list"><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 1]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 2]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 3]</li><li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>[ELEMENT 4]</li></ul></div>
    </div>
  </div>
</section>
```

**CSS**

```css
.sk-tabs-list{display:flex;justify-content:center;gap:6px;background:var(--sk-surface);border-radius:999px;padding:6px;width:max-content;max-width:100%;margin:0 auto 22px;overflow-x:auto}
.sk-tabs-list button{border:0;background:none;border-radius:999px;padding:10px 18px;font-weight:600;font-size:14px;color:var(--sk-muted);white-space:nowrap}
.sk-tabs-list button.on{background:#fff;color:var(--sk-primary);box-shadow:0 2px 10px rgba(0,0,0,.08)}
.sk-tab{display:none;padding:24px;gap:24px}
.sk-tab.on{display:grid}
@media(min-width:768px){.sk-tab{grid-template-columns:1fr 1fr;padding:32px}}
.sk-tab h3{margin:0 0 8px;font-size:20px}
.sk-tab p{margin:0;color:var(--sk-muted);font-size:14.5px}
.sk-tab-panel{background:var(--sk-surface);border-radius:16px;padding:18px 20px}
.sk-tab-panel small{display:block;font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--sk-gold);margin-bottom:10px}
```

**JS**

```js
/* TABS */
window.skTab=function(i){document.querySelectorAll(".sk-tabs-list button").forEach(function(b,k){b.classList.toggle("on",k===i)});document.querySelectorAll(".sk-tab").forEach(function(t,k){t.classList.toggle("on",k===i)})};
```

---

## PROMPT 8. TABELA PORÓWNAWCZA (MY vs INNI)

```text
Tabela 3 kolumny: cecha | nasz produkt (kolumna wyróżniona kolorem marki, z logo) | „zwykłe rozwiązanie”. Wiersze z „✓” i „✕”/„–”, pod tabelą krótka legenda co znaczy „–”. Na telefonie tabela mieści się bez przewijania w bok.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- COMPARE -->
<section class="sk-section" id="porownanie">
  <div class="sk-container">
    <span class="sk-eyebrow">[NADTYTUŁ – np. Porównanie]</span>
    <h2 class="sk-h2">Dlaczego <span class="sk-accent">[TWÓJ PRODUKT]</span>, a nie [ALTERNATYWA]?</h2>
    <p class="sk-lead">[PODTYTUŁ PORÓWNANIA]</p>
    <div class="sk-table-wrap">
      <table class="sk-table">
        <thead><tr><th>Cecha</th><th class="us">[TWÓJ PRODUKT]</th><th>[ALTERNATYWA 1]</th><th>[ALTERNATYWA 2]</th><th>[ALTERNATYWA 3]</th></tr></thead>
        <tbody>
          <tr><td>[CECHA 1]</td><td class="us"><span class="sk-yes">✓</span></td><td><span class="sk-yes" style="color:#9DB3A6">✓</span></td><td><span class="sk-no">✕</span></td><td><span class="sk-no">✕</span></td></tr>
          <tr><td>[CECHA 2]</td><td class="us"><span class="sk-yes">✓</span></td><td><span class="sk-no">✕</span></td><td><span class="sk-mid">–</span></td><td><span class="sk-no">✕</span></td></tr>
          <tr><td>[CECHA 3]</td><td class="us"><span class="sk-yes">✓</span></td><td><span class="sk-no">✕</span></td><td><span class="sk-yes" style="color:#9DB3A6">✓</span></td><td><span class="sk-yes" style="color:#9DB3A6">✓</span></td></tr>
          <tr><td>[CECHA 4]</td><td class="us"><span class="sk-yes">✓</span></td><td><span class="sk-no">✕</span></td><td><span class="sk-mid">–</span></td><td><span class="sk-no">✕</span></td></tr>
          <tr><td>[CECHA 5]</td><td class="us"><span class="sk-yes">✓</span></td><td><span class="sk-no">✕</span></td><td><span class="sk-no">✕</span></td><td><span class="sk-mid">–</span></td></tr>
          <tr><td>[CECHA 6]</td><td class="us"><span class="sk-yes">✓</span></td><td><span class="sk-mid">–</span></td><td><span class="sk-mid">–</span></td><td><span class="sk-mid">–</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
```

**CSS**

```css
.sk-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.sk-table{width:100%;min-width:680px;border-collapse:separate;border-spacing:0;font-size:14px;background:#fff;border-radius:20px;overflow:hidden;border:1px solid var(--sk-border)}
.sk-table th,.sk-table td{padding:15px 14px;text-align:center;border-bottom:1px solid var(--sk-border)}
.sk-table tr:last-child td{border-bottom:0}
.sk-table th{font-size:12.5px;font-weight:700;color:var(--sk-muted);background:var(--sk-surface)}
.sk-table td:first-child,.sk-table th:first-child{text-align:left;font-weight:600;color:var(--sk-fg)}
.sk-table .us{background:var(--sk-primary-soft)}
.sk-table th.us{background:var(--sk-primary);color:#fff}
.sk-yes{color:var(--sk-primary);font-weight:800;font-size:17px}
.sk-no{color:#C3BBAF;font-weight:700;font-size:17px}
.sk-mid{color:#C3BBAF;font-weight:800}
```

---

## PROMPT 9. OPINIE (JEDEN PASEK PRZEWIJANY W LEWO)

```text
Nagłówek z oceną (np. 4,9/5 i liczba opinii). Pod spodem JEDEN rząd kart opinii, który sam płynnie przesuwa się w lewo w pętli (animacja startuje, gdy sekcja pojawi się na ekranie, translate3d, bez zacięć; pauza po najechaniu tylko na komputerze). Karta: awatar w kółku (zdjęcie krajobrazu, nie twarz), imię + miasto, 5 gwiazdek, „Zweryfikowany zakup”, tekst opinii – wszystkie opinie podobnej długości, bez dat. 12 opinii z polskimi imionami.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- REVIEWS -->
<section class="sk-section sk-alt" id="opinie">
  <div class="sk-container">
    <span class="sk-eyebrow">[NADTYTUŁ – np. Opinie klientów]</span>
    <h2 class="sk-h2">Zobacz, co mówią <span class="sk-accent">[KLIENCI]</span></h2>
    <div class="sk-rev-head">
      <div class="sk-rev-score"><b>[OCENA]</b><span class="sk-stars" style="font-size:20px">★★★★★</span></div>
      <div style="font-size:13.5px;color:var(--sk-muted)">Na podstawie [LICZBA] zweryfikowanych zakupów</div>
    </div>
  </div>
  <div class="sk-rev-track"><div class="sk-rev-row" id="skRev1"></div></div>
</section>
```

**CSS**

```css
.sk-rev-head{display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:28px}
.sk-rev-score{display:flex;align-items:center;gap:10px;font-size:15px}
.sk-rev-score b{font-size:28px}
.sk-rev-track{overflow:hidden;mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.sk-rev-row{display:flex;gap:16px;width:max-content;animation:sk-scroll 90s linear infinite;padding:6px 0}
.sk-rev-row{animation-play-state:paused;will-change:transform;transform:translate3d(0,0,0);backface-visibility:hidden}
.sk-rev-row.run{animation-play-state:running}
@media(hover:hover){.sk-rev-track:hover .sk-rev-row.run{animation-play-state:paused}}
.sk-rev{contain:layout paint}
.sk-rev{width:290px;flex:0 0 290px;overflow:hidden;display:flex;flex-direction:column}
.sk-rev img{width:100%;aspect-ratio:4/3;object-fit:cover}
.sk-rev .b{padding:16px 18px 18px;display:flex;flex-direction:column;gap:8px;flex:1}
.sk-rev p{margin:0;font-size:13.5px;color:#36433B;min-height:84px}
.sk-rev .who{display:flex;align-items:center;gap:10px;margin-top:auto}
.sk-avatar{width:34px;height:34px;border-radius:50%;background:var(--sk-gradient);color:#fff;font-weight:700;font-size:13px;display:grid;place-items:center}
.sk-rev .who b{font-size:13.5px;display:block}
.sk-rev .who small{font-size:11.5px;color:var(--sk-ok);font-weight:600}
.sk-rev .var{font-size:11.5px;color:var(--sk-muted)}
```

**JS**

```js
/* REVIEWS */
var R=[
 ["Amelia","Kraków","opinia-1.jpg","","[TREŚĆ OPINII 1 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Piotr","Wrocław","opinia-2.jpg","","[TREŚĆ OPINII 2 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Julia","Gdańsk","opinia-3.jpg","","[TREŚĆ OPINII 3 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Aleksander","Poznań","opinia-4.jpg","","[TREŚĆ OPINII 4 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Natalia","Łódź","opinia-5.jpg","","[TREŚĆ OPINII 5 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Zofia","Lublin","opinia-6.jpg","","[TREŚĆ OPINII 6 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Kacper","Katowice","opinia-1.jpg","","[TREŚĆ OPINII 7 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Maja","Szczecin","opinia-2.jpg","","[TREŚĆ OPINII 8 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Oliwia","Bydgoszcz","opinia-3.jpg","","[TREŚĆ OPINII 9 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Szymon","Rzeszów","opinia-4.jpg","","[TREŚĆ OPINII 10 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Hanna","Toruń","opinia-5.jpg","","[TREŚĆ OPINII 11 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"],
 ["Mateusz","Białystok","opinia-6.jpg","","[TREŚĆ OPINII 12 – 2–3 zdania, konkretna korzyść, ok. 25 słów]"]
];
function card(r){return '<article class="sk-card sk-rev"><img src="'+skSrc(r[2])+'" width="400" height="300" alt="Zdjęcie od klienta"><div class="b"><span class="sk-stars">★★★★★</span><p>'+r[4]+'</p><div class="who"><img class="pfp" src="'+skSrc('av'+(R.indexOf(r)%12+1)+'.jpg')+'" alt=""><div><b>'+r[0]+', '+r[1]+'</b><small>✓ Zweryfikowany zakup</small></div></div></div></article>'}
document.getElementById("skRev1").innerHTML=(R.concat(R)).map(card).join("");
(function(){var row=document.getElementById("skRev1");row.querySelectorAll("img").forEach(function(i){i.decoding="async"});
 if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){row.classList.add("run");io.disconnect()}},{threshold:.05});io.observe(row)}else{row.classList.add("run")}})();
```

---

## PROMPT 10. SEKCJA Z 4 PUNKTAMI (DLA KOGO / DLACZEGO)

```text
Dwie kolumny: duże zdjęcie i blok tekstu z nagłówkiem oraz 4 punktami z ikonami w kółkach (każdy punkt w jednej linijce: pogrubiony początek + dopowiedzenie). Na końcu przycisk CTA.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- ADULT -->
<section class="sk-section sk-adult">
  <div class="sk-container sk-two">
    <div class="sk-photo" style="aspect-ratio:4/3"><img src="{{IMG}}/sekcja-4.jpg" width="1200" height="900" loading="lazy" alt="[OPIS ZDJĘCIA]"></div>
    <div>
      <span class="sk-eyebrow left">[NADTYTUŁ – np. Nie tylko dla…]</span>
      <h2 class="sk-h2 left">[NAGŁÓWEK – obalenie obiekcji] <span class="sk-accent">[SŁOWO KLUCZ]</span></h2>
      <p class="sk-lead left">[ZDANIE ROZWIJAJĄCE]</p>
      <ul class="sk-list">
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[PUNKT 1]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[PUNKT 2]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[PUNKT 3]</b> [dopowiedzenie]</span></li>
        <li><span class="sk-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span><span><b>[PUNKT 4]</b> [dopowiedzenie]</span></li>
      </ul>
      
    </div>
  </div>
</section>
```

**CSS**

```css
.sk-adult{background:var(--sk-gold-soft)}
```

---

## PROMPT 11. KARTA PROMOCJI 48 H Z ANIMACJAMI

```text
Duża karta w kolorze marki: po lewej zdjęcie produktu, które delikatnie unosi się w górę i w dół (float) z iskierkami; po prawej nazwa z przelatującym połyskiem co 1,5 s, plakietka z dzwoniącym zegarem, tekst „cena promocyjna tylko przez 48 godzin” + „Liczba sztuk ograniczona”, licznik GG:MM:SS (sekundy „tykają”) i przycisk CTA z lekkim drganiem co 2 s. Licznik liczony od PIERWSZEJ wizyty na danym urządzeniu (koniec zapisany w localStorage) – przy kolejnej wizycie czas leci dalej. Po upływie 48 h cała ta sekcja znika (ceny zostają bez zmian).
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- FINAL CTA: 48h -->
<section class="sk-section sk-alt" id="skDealSec">
  <div class="sk-container">
    <div class="sk-deal">
      <div class="sk-deal-img">
        <span class="sk-spark s1"></span><span class="sk-spark s2"></span>
        <img class="sk-float" src="{{IMG}}/foto-2.jpg" width="1200" height="1200" loading="lazy" alt="[NAZWA PRODUKTU]">
      </div>
      <div class="sk-deal-body">
        <h2 class="sk-shine">[NAZWA PRODUKTU]</h2>
        <div class="sk-deal-badge"><svg class="sk-ring" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="7"/><path d="M12 10v3l2 2M5 4 2.5 6.5M19 4l2.5 2.5"/></svg><b class="sk-pulse">48h!</b></div>
        <p class="sk-nudge">Nie przegap – [CENA PROMOCYJNA tylko przez 48 godzin]!<br><span class="sk-limit">⚠️ [PILNOŚĆ – np. Liczba sztuk ograniczona]</span> <span class="sk-gold sk-beat">♡</span></p>
        <div class="sk-deal-timer">
          <div><b id="skDH">48</b><small>godzin</small></div><i>:</i>
          <div><b id="skDM">00</b><small>minut</small></div><i>:</i>
          <div><b id="skDS">00</b><small>sekund</small></div>
        </div>
        <button class="sk-btn full" onclick="skScrollBuy()">[CTA – np. Kup teraz i skorzystaj z rabatu!] →</button>
      </div>
    </div>
  </div>
</section>
```

**CSS**

```css
.sk-final{text-align:center;max-width:680px;margin:0 auto;padding:36px 24px}
.sk-final .ic{width:56px;height:56px;border-radius:16px;background:var(--sk-gradient);display:grid;place-items:center;margin:0 auto 16px}
@keyframes sk-scroll{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
.sk-deal{display:grid;max-width:980px;margin:0 auto;background:#fff;border:1px solid var(--sk-border);border-radius:28px;overflow:hidden;box-shadow:0 20px 60px -24px rgba(18,56,38,.35)}
@media(min-width:768px){.sk-deal{grid-template-columns:.85fr 1.15fr}}
.sk-deal-img{position:relative;background:linear-gradient(135deg,#E8F1EA 0%,#FBF1DC 100%);display:grid;place-items:center;padding:36px;min-height:260px}
.sk-deal-img img{width:72%;max-width:280px;aspect-ratio:1;object-fit:cover;border-radius:22px;box-shadow:0 22px 40px -16px rgba(18,56,38,.45);height:auto}
.sk-float{animation:sk-float 3.2s ease-in-out infinite}
@keyframes sk-float{0%,100%{transform:translateY(0) rotate(-1.5deg)}50%{transform:translateY(-16px) rotate(1.5deg)}}
.sk-spark{position:absolute;width:26px;height:26px;background:radial-gradient(circle,var(--sk-gold) 2px,transparent 3px) 50% 0/4px 10px no-repeat,radial-gradient(circle,var(--sk-gold) 2px,transparent 3px);opacity:.8;animation:sk-tw 2.4s ease-in-out infinite}
.sk-spark.s1{top:28px;right:34px}.sk-spark.s2{bottom:30px;left:30px;animation-delay:1.2s}
@keyframes sk-tw{0%,100%{transform:scale(.6);opacity:.3}50%{transform:scale(1.1);opacity:1}}
.sk-deal-body{padding:30px 24px;text-align:center}
@media(min-width:768px){.sk-deal-body{padding:36px 40px}}
.sk-deal-body h2{margin:0;font-size:32px;font-weight:800;color:var(--sk-primary)}
.sk-deal-badge{display:flex;align-items:center;justify-content:center;gap:10px;color:var(--sk-sale);margin:6px 0 4px}
.sk-deal-badge b{font-size:34px;font-weight:800}
.sk-deal-body p{color:var(--sk-muted);font-size:14.5px;margin:0 0 20px}
.sk-deal-timer{display:flex;justify-content:center;align-items:center;gap:10px;margin-bottom:22px}
.sk-deal-timer div{width:96px;padding:14px 0 10px;border-radius:18px;background:#fff;border:1px solid var(--sk-border);box-shadow:var(--sk-shadow-card)}
.sk-deal-timer b{display:block;font-size:40px;line-height:1;font-weight:800;color:var(--sk-primary);font-variant-numeric:tabular-nums}
.sk-deal-timer small{display:block;margin-top:6px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--sk-muted)}
.sk-deal-timer i{font-style:normal;font-size:30px;font-weight:800;color:var(--sk-gold)}
@media(max-width:420px){.sk-deal-timer div{width:78px}.sk-deal-timer b{font-size:32px}}
.sk-ring{transform-origin:50% 20%;animation:sk-ring 2.4s ease-in-out infinite}
@keyframes sk-ring{0%,60%,100%{transform:rotate(0)}5%{transform:rotate(18deg)}10%{transform:rotate(-16deg)}15%{transform:rotate(14deg)}20%{transform:rotate(-12deg)}25%{transform:rotate(8deg)}30%{transform:rotate(-6deg)}35%{transform:rotate(0)}}
@keyframes sk-pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
.sk-deal-timer div b.tick{animation:sk-tick .35s ease}
@keyframes sk-tick{0%{transform:translateY(-6px);opacity:.3}100%{transform:none;opacity:1}}
.sk-deal .sk-btn{animation:sk-glow 2.2s ease-in-out infinite}
@keyframes sk-glow{0%,100%{box-shadow:var(--sk-shadow-cta)}50%{box-shadow:0 12px 34px -6px rgba(201,150,58,.75)}}
.sk-shine{background:linear-gradient(100deg,var(--sk-primary) 0%,var(--sk-primary) 40%,#E2B866 50%,var(--sk-primary) 60%,var(--sk-primary) 100%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:sk-shine 1.5s linear infinite,sk-bob 3.2s ease-in-out infinite;display:inline-block}
@keyframes sk-shine{0%{background-position:120% 0}100%{background-position:-120% 0}}
@keyframes sk-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.sk-nudge{animation:sk-nudge 2s ease-in-out infinite}
@keyframes sk-nudge{0%,60%,100%{transform:translateX(0)}68%{transform:translateX(-5px)}76%{transform:translateX(5px)}84%{transform:translateX(-3px)}92%{transform:translateX(2px)}}
.sk-beat{display:inline-block;animation:sk-pulse 1s ease-in-out infinite}
.sk-limit{display:inline-block;margin-top:8px;font-weight:800;color:var(--sk-sale);}
```

**JS**

```js
/* PROMO 48h: liczona od pierwszej wizyty na tym urządzeniu */
var SK_END;try{SK_END=+localStorage.getItem("skDealEnd")}catch(e){}
if(!SK_END){SK_END=Date.now()+48*3600*1000;try{localStorage.setItem("skDealEnd",SK_END)}catch(e){}}
var SK_EXP=Date.now()>=SK_END;if(SK_EXP)document.documentElement.classList.add("sk-exp");

/* 48h licznik w sekcji promocji */
var skDEnd=SK_END;
function dtick(){var s=Math.max(0,Math.ceil((skDEnd-Date.now())/1000));
  document.getElementById("skDH").textContent=String(Math.floor(s/3600)).padStart(2,"0");document.getElementById("skDM").textContent=String(Math.floor(s%3600/60)).padStart(2,"0");var ds=document.getElementById("skDS");ds.textContent=String(s%60).padStart(2,"0");ds.classList.remove("tick");void ds.offsetWidth;ds.classList.add("tick")}
dtick();var skDT=setInterval(function(){dtick();if(!SK_EXP&&Date.now()>=SK_END){clearInterval(skDT);location.reload()}},1000);
```

---

## PROMPT 12. FAQ (NAJCZĘŚCIEJ ZADAWANE PYTANIA)

```text
Wyśrodkowany nagłówek + mail kontaktowy pod spodem. Lista 8 pytań jako akordeon, wyśrodkowana, wąska kolumna: każde pytanie w jednej linijce z numerem (01, 02…) po lewej i plusem po prawej, który obraca się w „×”; odpowiedź rozwija się płynnie. Otwarte jest jedno pytanie naraz.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- FAQ -->
<section class="sk-section" id="faq">
  <div class="sk-container">
    <span class="sk-eyebrow">FAQ</span>
    <h2 class="sk-h2">Najczęściej zadawane <span class="sk-accent">pytania</span></h2>
    <p class="sk-lead" style="margin-bottom:8px">Nie ma tu Twojego pytania? Napisz:</p>
    <p style="text-align:center;margin:0 0 36px"><a href="mailto:[E-MAIL KONTAKTOWY]" style="font-weight:700;text-decoration:none">[E-MAIL KONTAKTOWY]</a></p>
    <div id="skFaq" class="sk-faq-list"></div>
  </div>
</section>
```

**CSS**

```css
.sk-faq-grid{display:grid;gap:28px}
@media(min-width:900px){.sk-faq-grid{grid-template-columns:minmax(0,1fr) 1.4fr;gap:48px}}
.sk-faq-list{max-width:760px;margin:0 auto}
.sk-acc .q{display:flex;align-items:center;gap:14px;flex:1;min-width:0}
.sk-acc .n{flex:0 0 34px;height:34px;border-radius:10px;background:var(--sk-primary-soft);color:var(--sk-primary);font-size:13px;font-weight:800;display:grid;place-items:center}
.sk-acc.open .n{background:var(--sk-gradient);color:#fff}
.sk-acc{border-bottom:1px solid var(--sk-border);background:none}
.sk-acc button{width:100%;background:none;border:0;text-align:left;padding:28px 4px;font-weight:700;font-size:16px;display:flex;justify-content:space-between;gap:12px;align-items:center;color:var(--sk-fg)}
.sk-acc button::after{content:"+";font-size:22px;font-weight:400;color:var(--sk-primary);transition:transform .2s}
.sk-acc.open button::after{transform:rotate(45deg)}
.sk-acc .a{display:none;padding:0 4px 24px;color:var(--sk-muted);font-size:14.5px}
.sk-acc.open .a{display:block}
```

**JS**

```js
/* FAQ */
var F=[
 ["[PYTANIE 1]","[ODPOWIEDŹ 1]"],
 ["[PYTANIE 2]","[ODPOWIEDŹ 2]"],
 ["[PYTANIE 3]","[ODPOWIEDŹ 3]"],
 ["[PYTANIE 4]","[ODPOWIEDŹ 4]"],
 ["[PYTANIE 5]","[ODPOWIEDŹ 5]"],
 ["[PYTANIE 6]","[ODPOWIEDŹ 6]"],
 ["[PYTANIE 7]","[ODPOWIEDŹ 7]"],
 ["[PYTANIE 8]","[ODPOWIEDŹ 8]"]
];
document.getElementById("skFaq").innerHTML=F.map(function(f,i){return '<div class="sk-acc"><button><span class="q"><span class="n">'+String(i+1).padStart(2,'0')+'</span>'+f[0]+'</span></button><div class="a">'+f[1]+'</div></div>'}).join("");
document.querySelectorAll("#skFaq .sk-acc button").forEach(function(b){b.onclick=function(){var p=b.parentNode,o=p.classList.contains("open");document.querySelectorAll("#skFaq .sk-acc").forEach(function(x){x.classList.remove("open")});if(!o)p.classList.add("open")}});
```

---

## PROMPT 13. STOPKA + WSZYSTKIE POLITYKI (REGULAMIN, PRYWATNOŚĆ, WYSYŁKA, ZWROTY, KONTAKT)

```text
Stopka od logo do samego dołu: po lewej logo + nazwa, krótki opis sklepu, mail i informacja o kontakcie; po prawej kolumna „Informacje” z linkami: Regulamin, Polityka prywatności, Polityka wysyłki, Zwroty i reklamacje, Kontakt. Na dole pasek z „© rok” i skrótem zaufania. Kliknięcie linku NIE przeładowuje strony – pokazuje podstronę (widok #skPages) w tym samym stylu: nagłówek, punkty numerowane z tytułem i akapitem, przycisk „← Wróć do sklepu”, a pod treścią każdej polityki formularz „Skontaktuj się z nami” (imię, e-mail, wiadomość → otwiera mail do sklepu). Teksty polityk ogólne, trochę dłuższe, bez ryzykownych obietnic (bez „wysyłamy w 24 h”, bez konkretnych godzin odpowiedzi; terminy reklamacji/zwrotu pieniędzy „w terminie przewidzianym przepisami prawa”, 14 dni na odstąpienie). Sklep prowadzi [NAZWA SKLEPU], kontakt tylko przez [E-MAIL], BEZ imienia, nazwiska i adresu.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- POLICY PAGES -->
<main id="skPages"></main>

<footer class="sk-footer">
  <div class="sk-container">
    <div class="sk-footer-grid">
      <div>
        <span class="sk-logo"><img src="{{IMG}}/logo.png" width="26" height="46" alt=""><div><span>[NAZWA]</span><small>[PODPIS POD LOGO]</small></div></span>
        <p style="color:var(--sk-muted);font-size:14px;max-width:360px">[OPIS SKLEPU – 1–2 zdania]</p>
        <div class="sk-foot-contact">
          <div><span class="ic">✉️</span><a href="mailto:[E-MAIL KONTAKTOWY]">[E-MAIL KONTAKTOWY]</a></div>
          <div><span class="ic">🕘</span>[GODZINY ODPOWIEDZI]</div>
        </div>
      </div>
      <div>
        <h4>Informacje</h4>
        <ul>
          <li><a href="#" onclick="skShow('regulamin');return false">Regulamin</a></li>
          <li><a href="#" onclick="skShow('prywatnosc');return false">Polityka prywatności</a></li>
          <li><a href="#" onclick="skShow('wysylka');return false">Polityka wysyłki</a></li>
          <li><a href="#" onclick="skShow('zwroty');return false">Zwroty i reklamacje</a></li>
          <li><a href="#" onclick="skShow('kontakt');return false">Kontakt</a></li>
        </ul>
      </div>
    </div>
    <div class="sk-foot-bottom"><span>[NAZWA SKLEPU] © [ROK]</span><span>🔒 Bezpieczne płatności SSL · Dane chronione RODO</span></div>
  </div>
</footer>

<!-- CONTACT MODAL -->
<div class="sk-modal" id="skContact" onclick="if(event.target===this)this.classList.remove('on')">
  <div class="sk-modal-box" style="text-align:center">
    <div class="sk-modal-head"><h3>Kontakt</h3><button class="sk-close" onclick="document.getElementById('skContact').classList.remove('on')">✕</button></div>
    <p>Skontaktuj się tutaj z nami: <a href="mailto:[E-MAIL KONTAKTOWY]" style="color:var(--sk-primary);font-weight:700">[E-MAIL KONTAKTOWY]</a></p>
  </div>
</div>
```

**CSS**

```css
.sk-footer{background:var(--sk-surface);padding:52px 0 26px;border-top:1px solid var(--sk-border)}
.sk-footer-grid{display:grid;gap:30px}
@media(min-width:768px){.sk-footer-grid{grid-template-columns:1.3fr 1fr}}
.sk-footer h4{font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--sk-muted);margin:0 0 14px}
.sk-footer ul{list-style:none;padding:0;margin:0;display:grid;gap:10px;font-size:14px}
.sk-footer ul a{text-decoration:none}
.sk-footer ul a:hover{color:var(--sk-primary)}
.sk-foot-contact{display:grid;gap:10px;margin-top:16px;font-size:13.5px}
.sk-foot-contact div{display:flex;gap:10px;align-items:center}
.sk-foot-contact .ic{width:32px;height:32px;border-radius:9px;border:1px solid rgba(30,91,61,.3);display:grid;place-items:center}
.sk-foot-bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;border-top:1px solid var(--sk-border);margin-top:34px;padding-top:18px;font-size:12px;color:var(--sk-muted)}
.sk-page{display:none}
.sk-page.on{display:block}
.sk-policy{max-width:720px;margin:0 auto;padding:48px 16px 24px}
.sk-policy h1{text-align:center;font-size:34px;margin:0 0 28px}
.sk-policy h2{font-size:18px;margin:28px 0 8px}
.sk-policy p,.sk-policy li{color:#3B4740;font-size:14.5px}
.sk-back{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;color:var(--sk-primary);text-decoration:none;font-weight:600;margin-bottom:12px}
.sk-form{max-width:560px;margin:48px auto 64px;padding:0 16px}
.sk-form h2{text-align:center;font-size:26px;margin:0 0 20px}
.sk-form input,.sk-form textarea{width:100%;border:1px solid var(--sk-border);border-radius:14px;padding:14px 16px;font-family:inherit;font-size:14.5px;margin-bottom:12px;background:#fff}
.sk-form input:focus,.sk-form textarea:focus{outline:2px solid var(--sk-primary-soft);border-color:var(--sk-primary)}
.sk-form textarea{min-height:120px;resize:vertical}
.sk-form-ok{display:none;text-align:center;background:var(--sk-primary-soft);color:var(--sk-primary-dark);border-radius:14px;padding:14px;font-weight:600;margin-top:12px}
.sk-modal{position:fixed;inset:0;z-index:120;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(15,25,20,.55)}
.sk-modal.on{display:flex}
.sk-modal-box{background:#fff;border-radius:22px;width:100%;max-width:440px;padding:24px;box-shadow:0 30px 80px -20px rgba(0,0,0,.35)}
.sk-modal-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.sk-modal-head h3{margin:0;font-size:22px}
.sk-close{width:36px;height:36px;border-radius:50%;border:0;background:var(--sk-surface);font-size:18px}
.sk-ship-opt{display:flex;justify-content:space-between;align-items:center;gap:12px;width:100%;border:2px solid var(--sk-border);border-radius:16px;padding:16px 18px;background:#fff;margin-bottom:10px;font-size:15px;font-weight:700;text-align:left;color:var(--sk-fg)}
.sk-ship-opt small{display:block;font-weight:500;color:var(--sk-muted);font-size:12px}
.sk-ship-opt .p{color:var(--sk-ok);font-size:14px;white-space:nowrap}
.sk-ship-opt.on{background:var(--sk-primary-dark);color:#fff;border-color:var(--sk-primary-dark)}
.sk-ship-opt.on small{color:rgba(255,255,255,.75)}
.sk-ship-opt.on .p{color:#9FE0B8}
```

**JS**

```js
/* POLICY PAGES */
var SELLER="[NAZWA SKLEPU]";
var L=function(k,t){return "<a href='#' onclick=\"skShow('"+k+"');return false\" style='color:var(--sk-primary)'>"+t+"</a>"};
var P={
 regulamin:["Regulamin",[
  ["1. Postanowienia ogólne","Niniejszy regulamin określa zasady korzystania ze sklepu internetowego <b>[NAZWA SKLEPU]</b>, składania zamówień, dostawy, płatności, odstąpienia od umowy oraz składania reklamacji. Sklep prowadzi sprzedaż na odległość za pośrednictwem tej strony. Kontakt ze sklepem: <b>"+EMAIL+"</b>."],
  ["2. Wymagania techniczne","Do korzystania ze sklepu potrzebne jest urządzenie z dostępem do internetu, aktualna przeglądarka internetowa oraz aktywny adres e-mail. Zabronione jest dostarczanie przez Klienta treści o charakterze bezprawnym."],
  ["3. Produkty i ceny","Informacje o produktach zamieszczone w sklepie stanowią zaproszenie do zawarcia umowy. Ceny podane są w złotych polskich i zawierają podatki. Zdjęcia produktów mają charakter poglądowy – drobne różnice w odcieniach kolorów mogą wynikać z ustawień ekranu. Sklep zastrzega sobie prawo do zmiany cen oraz prowadzenia promocji; zmiany nie dotyczą zamówień złożonych przed ich wprowadzeniem."],
  ["4. Składanie zamówień","Zamówienie można złożyć przez stronę sklepu. Po złożeniu zamówienia Klient otrzymuje e-mail z jego potwierdzeniem – z tą chwilą zostaje zawarta umowa sprzedaży. Klient odpowiada za podanie prawidłowych danych do wysyłki i kontaktu."],
  ["5. Płatności","Dostępne metody płatności są wyświetlane w kasie podczas składania zamówienia. Płatności obsługują zewnętrzni operatorzy płatności. Realizacja zamówienia rozpoczyna się po zaksięgowaniu płatności."],
  ["6. Dostawa","Dostawa odbywa się na terenie Polski i jest bezpłatna. Czas dostawy wynosi zwykle <b>6–10 dni roboczych</b> od zaksięgowania płatności. W wyjątkowych sytuacjach, np. w okresach wzmożonych zamówień lub z przyczyn leżących po stronie przewoźnika, czas ten może się wydłużyć. Szczegóły w "+L('wysylka','Polityce wysyłki')+"."],
  ["7. Prawo odstąpienia od umowy","Konsument może odstąpić od umowy bez podawania przyczyny w terminie <b>14 dni</b> od dnia otrzymania produktu. Zasady i sposób zwrotu opisuje strona "+L('zwroty','Zwroty i reklamacje')+"."],
  ["8. Reklamacje","Sklep odpowiada wobec Klienta za zgodność produktu z umową na zasadach określonych w przepisach prawa. Reklamację można złożyć, pisząc na <b>"+EMAIL+"</b>. Reklamacje rozpatrywane są w terminie przewidzianym przepisami prawa."],
  ["9. Pozasądowe rozwiązywanie sporów","Konsument może skorzystać z pozasądowych sposobów rozpatrywania reklamacji i dochodzenia roszczeń, m.in. z pomocy miejskiego lub powiatowego rzecznika konsumentów, Wojewódzkiego Inspektoratu Inspekcji Handlowej lub organizacji konsumenckich."],
  ["10. Postanowienia końcowe","W sprawach nieuregulowanych regulaminem stosuje się przepisy prawa polskiego, w szczególności Kodeksu cywilnego oraz ustawy o prawach konsumenta. Regulamin nie wyłącza ani nie ogranicza praw przysługujących konsumentom na mocy przepisów prawa. Zasady przetwarzania danych osobowych opisuje "+L('prywatnosc','Polityka prywatności')+"."]]],
 prywatnosc:["Polityka prywatności",[
  ["1. Administrator danych","Administratorem danych osobowych Klientów jest sklep <b>[NAZWA SKLEPU]</b>. W sprawach dotyczących danych osobowych można kontaktować się pod adresem <b>"+EMAIL+"</b>."],
  ["2. Jakie dane przetwarzamy","Przetwarzamy dane podane podczas składania zamówienia lub kontaktu z nami, w szczególności: imię i nazwisko, adres dostawy, adres e-mail, numer telefonu oraz informacje niezbędne do realizacji płatności i zamówienia."],
  ["3. Cele i podstawy przetwarzania","Dane przetwarzamy w celu: realizacji zamówień i umowy sprzedaży, obsługi zwrotów i reklamacji, kontaktu z Klientem, wypełnienia obowiązków wynikających z przepisów prawa (np. podatkowych i rachunkowych), a za zgodą Klienta – w celach statystycznych i marketingowych."],
  ["4. Odbiorcy danych","Dane mogą być przekazywane wyłącznie podmiotom, które pomagają nam w realizacji zamówień, takim jak firmy kurierskie, operatorzy płatności, dostawcy towaru, dostawca platformy sklepu oraz podmioty świadczące usługi IT i księgowe – w zakresie niezbędnym do realizacji ich zadań."],
  ["5. Okres przechowywania","Dane przechowujemy przez czas niezbędny do realizacji zamówienia oraz przez okres wymagany przepisami prawa lub potrzebny do dochodzenia ewentualnych roszczeń. Dane przetwarzane na podstawie zgody przechowujemy do czasu jej wycofania."],
  ["6. Prawa Klienta","Klient ma prawo do dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia danych, wniesienia sprzeciwu oraz wycofania zgody w dowolnym momencie. Klient ma również prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych."],
  ["7. Pliki cookies","Sklep korzysta z plików cookies, aby zapewnić prawidłowe działanie strony (np. koszyka), a także w celach statystycznych i reklamowych. Ustawienia cookies można w każdej chwili zmienić w przeglądarce internetowej."],
  ["8. Zmiany polityki","Polityka prywatności może być aktualizowana. Aktualna wersja jest zawsze dostępna na tej stronie."]]],
 wysylka:["Polityka wysyłki",[
  ["1. Obszar dostawy","Realizujemy dostawy na terenie Polski: do paczkomatów InPost oraz kurierem pod wskazany adres."],
  ["2. Koszt dostawy","Dostawa jest <b>bezpłatna</b> przy każdym zamówieniu."],
  ["3. Czas dostawy","Czas dostawy wynosi zwykle <b>6–10 dni roboczych</b> od zaksięgowania płatności. W okresach wzmożonych zamówień (np. przed Świętami) lub w przypadku opóźnień po stronie przewoźnika czas dostawy może się wydłużyć – w takiej sytuacji poinformujemy o tym Klienta."],
  ["4. Śledzenie przesyłki","Po nadaniu przesyłki Klient otrzymuje wiadomość e-mail z informacją o wysyłce. Informacje o statusie przesyłki mogą być udostępniane przez przewoźnika."],
  ["5. Odbiór przesyłki","Prosimy o sprawdzenie stanu przesyłki przy odbiorze. Jeśli opakowanie jest uszkodzone, warto sporządzić z przewoźnikiem protokół szkody lub zrobić zdjęcia i skontaktować się z nami pod adresem <b>"+EMAIL+"</b>."],
  ["6. Kontakt","W sprawach dotyczących dostawy prosimy o kontakt: <b>"+EMAIL+"</b>."]]],
 zwroty:["Zwroty i reklamacje",[
  ["1. Prawo do zwrotu","Konsument ma prawo odstąpić od umowy bez podawania przyczyny w terminie <b>14 dni</b> od dnia otrzymania produktu. Do zachowania terminu wystarczy wysłanie oświadczenia przed jego upływem."],
  ["2. Jak zgłosić zwrot","Aby odstąpić od umowy, wyślij wiadomość na <b>"+EMAIL+"</b>, podając numer zamówienia oraz informację, że chcesz zwrócić produkt. W odpowiedzi otrzymasz dalsze instrukcje, w tym adres do odesłania."],
  ["3. Odesłanie produktu","Produkt należy odesłać nie później niż w terminie 14 dni od dnia odstąpienia od umowy. Bezpośredni koszt odesłania produktu ponosi Klient. Prosimy o odpowiednie zabezpieczenie przesyłki na czas transportu."],
  ["4. Zwrot pieniędzy","Zwrot płatności następuje w terminie przewidzianym przepisami prawa, przy użyciu tej samej metody płatności, chyba że Klient zgodzi się na inną. Sklep może wstrzymać się ze zwrotem do chwili otrzymania produktu lub dowodu jego odesłania."],
  ["5. Stan zwracanego produktu","Klient odpowiada za zmniejszenie wartości produktu wynikające z korzystania z niego w sposób wykraczający poza konieczny do stwierdzenia jego charakteru, cech i funkcjonowania."],
  ["6. Reklamacje","Jeśli produkt jest niezgodny z umową lub uszkodzony, napisz na <b>"+EMAIL+"</b>, podając numer zamówienia, opis problemu i – jeśli to możliwe – zdjęcia. Reklamacja zostanie rozpatrzona w terminie przewidzianym przepisami prawa. Klientowi przysługują uprawnienia wynikające z przepisów prawa, w tym prawo żądania naprawy lub wymiany produktu, a w określonych przypadkach obniżenia ceny lub odstąpienia od umowy."],
  ["7. Anulowanie zamówienia","Zamówienie można anulować do momentu jego wysłania – w tym celu prosimy o jak najszybszy kontakt z numerem zamówienia."]]],
 kontakt:["Kontakt",[
  ["Napisz do nas","Masz pytanie o zamówienie, wysyłkę albo zwrot? Napisz na <b>"+EMAIL+"</b> albo skorzystaj z formularza poniżej.</p><p>Na wiadomości odpowiadamy najszybciej, jak to możliwe. W okresach wzmożonego ruchu czas odpowiedzi może się wydłużyć."]]]
};
var pages=document.getElementById("skPages");
Object.keys(P).forEach(function(k){
  var d=document.createElement("section");d.className="sk-page";d.id="kwp-"+k;
  d.innerHTML='<div class="sk-policy"><a href="#" class="sk-back" onclick="skShow(\'home\');return false">← Wróć do sklepu</a><h1>'+P[k][0]+'</h1>'+P[k][1].map(function(s){return '<h2>'+s[0]+'</h2><p>'+s[1]+'</p>'}).join("")+'</div>'+
  '<form class="sk-form" onsubmit="return skSend(this)"><h2>Skontaktuj się <span class="sk-accent">z nami</span></h2><input name="imie" placeholder="Imię" required><input name="email" type="email" placeholder="E-mail" required><input name="tel" placeholder="Numer telefonu"><textarea name="msg" placeholder="Wiadomość" required></textarea><button class="sk-btn full" type="submit">Wyślij</button><div class="sk-form-ok">Dziękujemy! Otworzyliśmy Twoją pocztę z gotową wiadomością.</div></form>';
  pages.appendChild(d);
});
window.skSend=function(f){var b="Imię: "+f.imie.value+"%0D%0AE-mail: "+f.email.value+"%0D%0ATelefon: "+f.tel.value+"%0D%0A%0D%0A"+encodeURIComponent(f.msg.value);
  window.location.href="mailto:"+EMAIL+"?subject="+encodeURIComponent("Wiadomość ze sklepu [NAZWA SKLEPU]")+"&body="+b;f.querySelector(".sk-form-ok").style.display="block";return false};
window.skShow=function(k){var home=k==="home";document.getElementById("skHome").classList.toggle("on",home);
  document.querySelectorAll("#skPages .sk-page").forEach(function(p){p.classList.toggle("on",p.id==="kwp-"+k)});
  if(!home){window.scrollTo(0,0);document.getElementById("skSticky").classList.remove("on")}};
})();
```

---

## PROMPT 14. KOSZYK, OKNO DOSTAWY, PASEK NA DOLE TELEFONU

```text
Koszyk jako panel wysuwany z prawej (z przyciemnieniem tła): pozycje ze zdjęciem, nazwą, wybranym wariantem, licznikiem –/+ i koszem; pasek postępu „Dodaj jeszcze 1 szt. i zapłać mniej”; podsumowanie (cena regularna, łączny rabat, razem); przycisk „Realizuj zakup” i logotypy płatności. Koszyk zapisuje się w localStorage. „Realizuj zakup” otwiera małe okno wyboru dostawy (np. „📦 Paczkomat – GRATIS”, „🚚 Kurier pod adres – GRATIS”, dopisek, że adres poda się w kasie) i przycisk „Przejdź do płatności”, który od razu przenosi do kasy (w Shopify: link /cart/IDwariantu:ilość,… – bez czekania). Na telefonie przy przewijaniu pojawia się przyklejony dolny pasek z nazwą, ceną i przyciskiem „Do koszyka”; po dodaniu wyskakuje mały komunikat „Dodano do koszyka ✓”.
Wzoruj się dokładnie na poniższym kodzie (HTML/CSS/JS). Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści dopasuj do mojego produktu.
```

**HTML**

```html
<!-- CART DRAWER -->
<div class="sk-overlay" id="skOverlay" onclick="skCart(false)"></div>
<aside class="sk-drawer" id="skDrawer" aria-label="Koszyk">
  <div class="sk-dr-head"><h3>Koszyk · <span id="skDrCount">0</span></h3><button class="sk-close" aria-label="Zamknij koszyk" onclick="skCart(false)">✕</button></div>
  <div class="sk-dr-bar">🚚 [DOSTAWA] · ↩️ [ZWROTY]</div>
  <div class="sk-dr-progress" id="skProgress"></div>
  <div class="sk-dr-items" id="skItems"></div>
  <div class="sk-dr-foot">
    <div class="sk-dr-line disc"><span>Łączny rabat</span><span id="skDisc">−0,00 zł</span></div>
    <div class="sk-dr-line total"><span>Łączna kwota</span><span id="skTotal">0,00 zł</span></div>
    <div class="sk-dr-line" style="color:var(--sk-muted)"><span>Dostawa</span><span id="skShipLine">Wybierzesz w następnym kroku</span></div>
    <button class="sk-btn full" id="skCheckout" onclick="skShipModal(true)">Realizuj zakup</button>
    <div class="sk-pay"><span class="pay-blik">blik</span><span class="pay-visa">VISA</span><span class="pay-mc"><svg width="22" height="14" viewBox="0 0 22 14"><circle cx="7" cy="7" r="7" fill="#EB001B"/><circle cx="15" cy="7" r="7" fill="#F79E1B" fill-opacity=".9"/></svg>mastercard</span><span class="pay-apple"><svg width="12" height="14" viewBox="0 0 17 20" fill="#fff"><path d="M14.1 10.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9C3.6 4.8 2 5.8 1.1 7.4c-1.8 3.2-.5 7.9 1.3 10.5.9 1.3 1.9 2.7 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.6 1-1.5 1.4-2.9 1.4-3-.1 0-2.7-1-2.7-4.3zM11.6 3c.7-.9 1.2-2 1-3.2-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.1 1.2.1 2.3-.6 3.1-1.5z"/></svg>Pay</span><span class="pay-google"><svg width="13" height="13" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>Pay</span><span class="pay-p24">P24</span></div>
  </div>
</aside>

<!-- SHIPPING MODAL -->
<div class="sk-modal" id="skShip" onclick="if(event.target===this)skShipModal(false)">
  <div class="sk-modal-box">
    <div class="sk-modal-head"><h3>Wybierz dostawę</h3><button class="sk-close" onclick="skShipModal(false)">✕</button></div>
    <button class="sk-ship-opt on" data-ship="paczkomat" onclick="skPickShip(this)"><span>📦 Paczkomat InPost</span><span class="p">GRATIS</span></button>
    <button class="sk-ship-opt" data-ship="kurier" onclick="skPickShip(this)"><span>🚚 Kurier pod adres</span><span class="p">GRATIS</span></button>
    <button class="sk-btn full" style="margin-top:6px" onclick="skGoCheckout()">Przejdź do płatności</button>
    <p class="sk-micro">Adres i punkt odbioru wskażesz w kasie na następnym ekranie.</p>
  </div>
</div>

<div class="sk-sticky" id="skSticky">
  <div><div class="n">[NAZWA PRODUKTU]</div><div class="p" id="skStickyPrice">199,99 zł <s style="color:var(--sk-muted);font-weight:400">299,99 zł</s></div></div>
  <button class="sk-btn small" onclick="skAddBundle()">Do koszyka</button>
</div>
<div class="sk-toast" id="skToast">Dodano do koszyka ✓</div>
```

**CSS**

```css
.sk-overlay{position:fixed;inset:0;background:rgba(15,25,20,.55);z-index:90;opacity:0;pointer-events:none;transition:opacity .2s}
.sk-overlay.on{opacity:1;pointer-events:auto}
.sk-drawer{position:fixed;top:0;right:0;height:100%;width:100%;max-width:440px;background:#fff;z-index:95;transform:translateX(100%);transition:transform .28s ease;display:flex;flex-direction:column}
.sk-drawer.on{transform:none}
.sk-dr-head{display:flex;justify-content:space-between;align-items:center;padding:18px 20px}
.sk-dr-head h3{margin:0;font-size:22px}
.sk-dr-bar{background:var(--sk-primary-dark);color:#fff;text-align:center;font-size:13px;font-weight:600;padding:10px}
.sk-dr-progress{padding:14px 20px 0;font-size:12.5px;color:var(--sk-muted)}
.sk-dr-progress .bar{height:7px;border-radius:4px;background:var(--sk-surface-2);margin-top:6px;overflow:hidden}
.sk-dr-progress .bar i{display:block;height:100%;background:var(--sk-gradient);transition:width .3s}
.sk-dr-items{flex:1;overflow:auto;padding:16px 20px;display:grid;gap:14px;align-content:start}
.sk-item{display:grid;grid-template-columns:72px 1fr;gap:12px;align-items:start}
.sk-item img{width:72px;height:72px;border-radius:12px;object-fit:cover}
.sk-item-top{display:flex;justify-content:space-between;gap:8px}
.sk-item-top b{font-size:14px}
.sk-item small{color:var(--sk-muted);font-size:12px;display:block}
.sk-item-bot{display:flex;justify-content:space-between;align-items:center;margin-top:8px}
.sk-qty{display:inline-flex;border:1px solid var(--sk-border);border-radius:10px;overflow:hidden}
.sk-qty button{width:30px;height:30px;border:0;background:#fff;font-size:16px}
.sk-qty span{width:30px;display:grid;place-items:center;font-size:13px;font-weight:600}
.sk-item-price{text-align:right;font-size:14px;font-weight:700;color:var(--sk-primary)}
.sk-item-price s{font-weight:400;color:var(--sk-muted);font-size:12px;margin-right:4px}
.sk-trash{border:0;background:none;color:var(--sk-muted);padding:2px}
.sk-upsell-mini{border:2px dashed rgba(30,91,61,.3);border-radius:16px;padding:12px;display:flex;gap:12px;align-items:center;font-size:13px}
.sk-upsell-mini img{width:56px;height:56px;border-radius:10px;object-fit:cover}
.sk-dr-foot{border-top:1px solid var(--sk-border);padding:16px 20px 20px;display:grid;gap:8px;background:var(--sk-surface)}
.sk-dr-line{display:flex;justify-content:space-between;font-size:14px}
.sk-dr-line.disc{color:var(--sk-ok);font-weight:700}
.sk-dr-line.total{font-size:19px;font-weight:800}
.sk-empty{text-align:center;color:var(--sk-muted);padding:40px 0}
.sk-modal{position:fixed;inset:0;z-index:120;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(15,25,20,.55)}
.sk-modal.on{display:flex}
.sk-modal-box{background:#fff;border-radius:22px;width:100%;max-width:440px;padding:24px;box-shadow:0 30px 80px -20px rgba(0,0,0,.35)}
.sk-modal-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.sk-modal-head h3{margin:0;font-size:22px}
.sk-close{width:36px;height:36px;border-radius:50%;border:0;background:var(--sk-surface);font-size:18px}
.sk-ship-opt{display:flex;justify-content:space-between;align-items:center;gap:12px;width:100%;border:2px solid var(--sk-border);border-radius:16px;padding:16px 18px;background:#fff;margin-bottom:10px;font-size:15px;font-weight:700;text-align:left;color:var(--sk-fg)}
.sk-ship-opt small{display:block;font-weight:500;color:var(--sk-muted);font-size:12px}
.sk-ship-opt .p{color:var(--sk-ok);font-size:14px;white-space:nowrap}
.sk-ship-opt.on{background:var(--sk-primary-dark);color:#fff;border-color:var(--sk-primary-dark)}
.sk-ship-opt.on small{color:rgba(255,255,255,.75)}
.sk-ship-opt.on .p{color:#9FE0B8}
.sk-sticky{position:fixed;left:0;right:0;bottom:0;z-index:60;background:#fff;border-top:1px solid var(--sk-border);padding:10px 16px;display:flex;align-items:center;gap:12px;transform:translateY(110%);transition:transform .25s;box-shadow:0 -8px 24px rgba(0,0,0,.08)}
.sk-sticky.on{transform:none}
.sk-sticky .n{font-size:13px;font-weight:700;line-height:1.2}
.sk-sticky .p{font-size:13px;color:var(--sk-primary);font-weight:700}
.sk-sticky .sk-btn{margin-left:auto}
```

**JS**

```js
/* CART */
var cart=[];
function save(){try{localStorage.setItem("skCart2",JSON.stringify(cart))}catch(e){}}
try{cart=JSON.parse(localStorage.getItem("skCart2")||"[]")}catch(e){cart=[]}
function unitFor(q){return q>=3?BUNDLES[2].price/3:q===2?BUNDLES[1].price/2:BUNDLES[0].price}
function calCount(){return cart.reduce(function(s,i){return s+i.qty},0)}
function addItem(it){var f=cart.find(function(c){return c.key===it.key});if(f)f.qty+=it.qty;else cart.push(it);save();drawCart();toast()}
window.skAddBundle=function(){var c={};CH[sel].forEach(function(f){c[f]=(c[f]||0)+1});Object.keys(c).forEach(function(f){addItem({key:"kal-"+f,f:f,name:"[NAZWA PRODUKTU]",variant:"Wariant: "+f,img:"foto-4.jpg",qty:c[f],old:BUNDLES[0].old})});skCart(true)};
function drawCart(){
  var n=calCount(),u=unitFor(n),items=document.getElementById("skItems"),tot=0,old=0,cnt=0;
  items.innerHTML="";
  if(!cart.length){items.innerHTML='<div class="sk-empty">Twój koszyk jest pusty 🌷<br><br><button class="sk-btn small" onclick="skCart(false);skScrollBuy()">Wybierz zestaw</button></div>'}
  cart.forEach(function(it,idx){
    var p=u;tot+=p*it.qty;old+=it.old*it.qty;cnt+=it.qty;
    var d=document.createElement("div");d.className="sk-item";
    d.innerHTML='<img src="'+skSrc(it.img)+'" alt=""><div><div class="sk-item-top"><div><b>'+it.name+'</b><small>'+it.variant+'</small></div><button class="sk-trash" aria-label="Usuń">🗑</button></div><div class="sk-item-bot"><div class="sk-qty"><button aria-label="Mniej">−</button><span>'+it.qty+'</span><button aria-label="Więcej">+</button></div><div class="sk-item-price"><s>'+zl(it.old*it.qty)+'</s>'+zl(p*it.qty)+'<small style="color:var(--sk-ok)">Oszczędzasz '+zl((it.old-p)*it.qty)+'</small></div></div></div>';
    var bs=d.querySelectorAll("button");
    bs[0].onclick=function(){cart.splice(idx,1);save();drawCart()};
    bs[1].onclick=function(){it.qty--;if(it.qty<1)cart.splice(idx,1);save();drawCart()};
    bs[2].onclick=function(){it.qty++;save();drawCart()};
    items.appendChild(d);
  });
  var pr=document.getElementById("skProgress");
  if(n===0)pr.innerHTML="";else if(n<3)pr.innerHTML='Dodaj jeszcze <b>1 szt.</b> i zapłać tylko <b>'+zl(unitFor(n+1))+'</b> za sztukę<div class="bar"><i style="width:'+(n/3*100)+'%"></i></div>';else pr.innerHTML='🎉 Masz najniższą cenę: <b>'+zl(unitFor(3))+'</b> za sztukę<div class="bar"><i style="width:100%"></i></div>';
  document.getElementById("skTotal").textContent=zl(tot);document.getElementById("skDisc").textContent="−"+zl(old-tot);
  document.getElementById("skDrCount").textContent=cnt;var c=document.getElementById("skCount");c.textContent=cnt;c.hidden=!cnt;
  document.getElementById("skCheckout").disabled=!cnt;document.getElementById("skCheckout").style.opacity=cnt?1:.5;
}
drawCart();
function toast(){var t=document.getElementById("skToast");t.classList.add("on");setTimeout(function(){t.classList.remove("on")},1600)}
window.skCart=function(o){document.getElementById("skDrawer").classList.toggle("on",o);document.getElementById("skOverlay").classList.toggle("on",o);document.body.style.overflow=o?"hidden":""};
window.skShipModal=function(o){document.getElementById("skShip").classList.toggle("on",o)};
window.skPickShip=function(b){document.querySelectorAll(".sk-ship-opt").forEach(function(x){x.classList.toggle("on",x===b)});document.getElementById("skShipLine").textContent=b.dataset.ship==="kurier"?"Kurier pod adres · GRATIS":"Paczkomat InPost · GRATIS"};
window.skGoCheckout=function(){window.location.href=CHECKOUT_URL};
window.skMenu=function(o){document.getElementById("skMobile").classList.toggle("open",o);document.body.style.overflow=o?"hidden":""};
window.skScrollBuy=function(){skShow("home");document.getElementById("skBundles").scrollIntoView({behavior:"smooth",block:"center"})};

/* STICKY */
window.addEventListener("scroll",function(){document.getElementById("skSticky").classList.toggle("on",window.scrollY>700&&document.getElementById("skHome").classList.contains("on"))},{passive:true});
```
