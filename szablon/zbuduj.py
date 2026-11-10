"""Zamienia gotową stronę sklepu (src.html z {{IMG}}) na 3 pliki do Shopify.
Użycie:  python3 zbuduj.py ../kwiatora/src.html
Wynik:   shopify/layout/landing.liquid
         shopify/sections/landing.liquid
         shopify/templates/product.landing.json
"""
import json, os, re, sys

src_path = sys.argv[1] if len(sys.argv) > 1 else '../kwiatora/src.html'
html = open(src_path, encoding='utf-8').read()
if '{%' in html or re.search(r'\{\{(?!IMG\}\})', html):
    sys.exit('Błąd: w HTML są znaczniki {{ lub {% inne niż {{IMG}} – popraw przed budową.')

head = html.split('<head>', 1)[1].split('</head>', 1)[0]
style = head.split('<style>', 1)[1].split('</style>', 1)[0]
links = '\n'.join(l for l in head.splitlines() if l.strip().startswith('<link'))
body = html.split('<body>', 1)[1].split('</body>', 1)[0]

# zdjęcia: Shopify → Treści → Pliki (te same nazwy plików co w folderze img/)
body = body.replace('{{IMG}}', '{{ kw_img }}')

# przycisk "Przejdź do płatności" dodaje kalendarze do koszyka Shopify i otwiera kasę
old = 'window.kwGoCheckout=function(){window.location.href=CHECKOUT_URL};'
if old not in body:
    sys.exit('Błąd: nie znalazłem funkcji kwGoCheckout w HTML.')
body = body.replace(old, '''window.kwGoCheckout=function(){
  var q=cart.reduce(function(s,i){return s+i.qty},0);
  if(!window.KW_VARIANT||!q){window.location.href="/cart";return}
  fetch("/cart/clear.js",{method:"POST"})
   .then(function(){return fetch("/cart/add.js",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({items:[{id:window.KW_VARIANT,quantity:q}]})})})
   .then(function(){try{localStorage.removeItem("kwCart2")}catch(e){};window.location.href="/checkout"})
   .catch(function(){window.location.href="/cart"})};''')

section = (
    "{%- comment -%} Sekcja landing page – wygenerowana przez szablon/zbuduj.py {%- endcomment -%}\n"
    "{%- assign kw_img = 'x.jpg' | file_url | split: 'x.jpg' | first | remove_last: '/' -%}\n"
    "{%- liquid\n"
    "  assign kw_variant = section.settings.variant_id\n"
    "  if product\n"
    "    assign kw_variant = product.selected_or_first_available_variant.id\n"
    "  endif\n"
    "-%}\n"
    "<style>" + style + "</style>\n"
    "<script>window.KW_VARIANT={{ kw_variant | json }};</script>\n"
    + body +
    "\n{% schema %}\n" + json.dumps({
        "name": "Landing produktu",
        "settings": [{"type": "text", "id": "variant_id", "label": "ID wariantu (tylko gdy szablon nie jest na stronie produktu)"}],
        "presets": [{"name": "Landing produktu"}]
    }, ensure_ascii=False, indent=2) + "\n{% endschema %}\n"
)

layout = (
    "<!doctype html>\n<html lang=\"pl\">\n<head>\n"
    "<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
    "<title>{{ page_title }}</title>\n"
    "{%- if page_description -%}<meta name=\"description\" content=\"{{ page_description | escape }}\">{%- endif -%}\n"
    "<meta property=\"og:title\" content=\"{{ page_title | escape }}\">\n"
    "{%- if product and product.featured_image -%}<meta property=\"og:image\" content=\"https:{{ product.featured_image | image_url: width: 1200 }}\">{%- endif -%}\n"
    "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
    + links + "\n{{ content_for_header }}\n</head>\n<body>\n{{ content_for_layout }}\n</body>\n</html>\n"
)

template = {"layout": "landing", "sections": {"main": {"type": "landing", "settings": {}}}, "order": ["main"]}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shopify')
for d in ('layout', 'sections', 'templates'):
    os.makedirs(os.path.join(out, d), exist_ok=True)
open(os.path.join(out, 'layout/landing.liquid'), 'w', encoding='utf-8').write(layout)
open(os.path.join(out, 'sections/landing.liquid'), 'w', encoding='utf-8').write(section)
open(os.path.join(out, 'templates/product.landing.json'), 'w', encoding='utf-8').write(json.dumps(template, indent=2) + '\n')
print('OK:', out, '| sekcja', len(section) // 1024, 'KB')
