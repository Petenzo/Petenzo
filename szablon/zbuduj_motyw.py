"""Robi JEDEN plik: gotowy motyw Shopify .zip (strona + zdjęcia + koszyk).
Użycie:  python3 zbuduj_motyw.py ../kwiatora/src.html ../kwiatora/img Kwiatora kalendarz-adwentowy-kwiatora
          (html)                  (folder zdjęć)     (nazwa)   (uchwyt produktu w Shopify)
Wynik:   szablon/Kwiatora_motyw.zip  → Shopify: Sklep online → Motywy → Dodaj motyw → Prześlij plik zip
"""
import json, os, re, sys, zipfile

src, imgdir, name, handle = (sys.argv[1:5] + ['../kwiatora/src.html', '../kwiatora/img', 'Kwiatora', 'kalendarz-adwentowy-kwiatora'][len(sys.argv)-1:])[:4]
html = open(src, encoding='utf-8').read()
if '{%' in html or re.search(r'\{\{(?!IMG\}\})', html):
    sys.exit('Błąd: w HTML są znaczniki {{ lub {% inne niż {{IMG}}.')
head = html.split('<head>', 1)[1].split('</head>', 1)[0]
style = head.split('<style>', 1)[1].split('</style>', 1)[0]
links = '\n'.join(l for l in head.splitlines() if l.strip().startswith('<link'))
body = html.split('<body>', 1)[1].split('</body>', 1)[0].replace('{{IMG}}', '{{ kw_img }}')
old = 'window.kwGoCheckout=function(){window.location.href=CHECKOUT_URL};'
assert old in body, 'brak kwGoCheckout'
body = body.replace(old, '''window.kwGoCheckout=function(){
  var q=cart.reduce(function(s,i){return s+i.qty},0);
  if(!window.KW_VARIANT||!q){window.location.href="/cart";return}
  fetch("/cart/clear.js",{method:"POST"})
   .then(function(){return fetch("/cart/add.js",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({items:[{id:window.KW_VARIANT,quantity:q}]})})})
   .then(function(){try{localStorage.removeItem("kwCart2")}catch(e){};window.location.href="/checkout"})
   .catch(function(){window.location.href="/cart"})};''')

F = {}
F['layout/theme.liquid'] = ('<!doctype html>\n<html lang="pl">\n<head>\n<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{{ page_title }}</title>\n'
  '{%- if page_description -%}<meta name="description" content="{{ page_description | escape }}">{%- endif -%}\n'
  '<meta property="og:title" content="{{ page_title | escape }}">\n<meta name="twitter:card" content="summary_large_image">\n'
  + links + '\n{{ content_for_header }}\n</head>\n<body>\n{{ content_for_layout }}\n</body>\n</html>\n')

F['sections/landing.liquid'] = (
  "{%- assign kw_img = 'logo-ikona.png' | asset_url | split: 'logo-ikona.png' | first | remove_last: '/' -%}\n"
  "{%- liquid\n  assign kw_p = product\n  if kw_p == blank\n    assign kw_p = all_products[section.settings.handle]\n  endif\n"
  "  assign kw_variant = kw_p.selected_or_first_available_variant.id\n-%}\n"
  "<style>" + style + "</style>\n<script>window.KW_VARIANT={{ kw_variant | json }};</script>\n" + body +
  "\n{% schema %}\n" + json.dumps({"name": "Landing produktu", "settings": [
    {"type": "text", "id": "handle", "label": "Uchwyt produktu (na stronie głównej)", "default": handle}],
    "presets": [{"name": "Landing produktu"}]}, ensure_ascii=False, indent=2) + "\n{% endschema %}\n")

simple_css = '<style>body{font-family:Poppins,system-ui,sans-serif;margin:0;color:#18241D}.w{max-width:760px;margin:0 auto;padding:40px 16px}a{color:#1E5B3D}.b{display:inline-block;background:#1E5B3D;color:#fff;padding:14px 24px;border-radius:14px;text-decoration:none;font-weight:700;border:0;font-size:15px;cursor:pointer}</style>'
back = '<p><a href="{{ routes.root_url }}">← Wróć do sklepu</a></p>'
F['sections/simple.liquid'] = (simple_css + '<div class="w">' + back + '''
{%- case template.name -%}
{%- when 'cart' -%}<h1>Koszyk</h1>{%- if cart.item_count > 0 -%}<form action="{{ routes.cart_url }}" method="post">{%- for item in cart.items -%}<p>{{ item.product.title }} × <input type="number" name="updates[]" value="{{ item.quantity }}" min="0" style="width:60px"> – {{ item.final_line_price | money }}</p>{%- endfor -%}<p><b>Razem: {{ cart.total_price | money }}</b></p><button class="b" name="checkout">Przejdź do płatności</button></form>{%- else -%}<p>Koszyk jest pusty.</p>{%- endif -%}
{%- when 'page' -%}<h1>{{ page.title }}</h1>{{ page.content }}
{%- when 'collection' -%}<h1>{{ collection.title }}</h1>{%- for p in collection.products -%}<p><a href="{{ p.url }}">{{ p.title }}</a> – {{ p.price | money }}</p>{%- endfor -%}
{%- when 'list-collections' -%}<h1>Kolekcje</h1>{%- for c in collections -%}<p><a href="{{ c.url }}">{{ c.title }}</a></p>{%- endfor -%}
{%- when 'search' -%}<h1>Szukaj</h1><form action="{{ routes.search_url }}"><input name="q" value="{{ search.terms | escape }}"> <button class="b">Szukaj</button></form>{%- for r in search.results -%}<p><a href="{{ r.url }}">{{ r.title }}</a></p>{%- endfor -%}
{%- when 'blog' -%}<h1>{{ blog.title }}</h1>{%- for a in blog.articles -%}<p><a href="{{ a.url }}">{{ a.title }}</a></p>{%- endfor -%}
{%- when 'article' -%}<h1>{{ article.title }}</h1>{{ article.content }}
{%- when 'password' -%}<h1>{{ shop.name }}</h1><p>Sklep wkrótce ruszy.</p><form action="/password" method="post"><input type="password" name="password" placeholder="Hasło"> <button class="b">Wejdź</button></form>
{%- else -%}<h1>Nie znaleziono strony</h1><p><a class="b" href="{{ routes.root_url }}">Wróć do sklepu</a></p>
{%- endcase -%}
</div>
{% schema %}
{"name":"Prosta strona","settings":[]}
{% endschema %}
''')
landing = {"sections": {"main": {"type": "landing", "settings": {"handle": handle}}}, "order": ["main"]}
simple = {"sections": {"main": {"type": "simple", "settings": {}}}, "order": ["main"]}
F['templates/index.json'] = json.dumps(landing, indent=2)
F['templates/product.json'] = json.dumps(landing, indent=2)
for t in ['cart', 'page', 'collection', 'list-collections', 'search', 'blog', 'article', '404', 'password']:
    F['templates/%s.json' % t] = json.dumps(simple, indent=2)
F['config/settings_schema.json'] = json.dumps([{"name": "theme_info", "theme_name": name, "theme_version": "1.0.0",
    "theme_author": "Kwiatora", "theme_documentation_url": "https://kwiatora.pl", "theme_support_url": "https://kwiatora.pl"}], indent=2)
F['config/settings_data.json'] = json.dumps({"current": "Default", "presets": {"Default": {}}}, indent=2)
F['locales/pl.default.json'] = '{}'

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), name + '_motyw.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for k, v in F.items():
        z.writestr(k, v)
    for f in sorted(os.listdir(imgdir)):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            z.write(os.path.join(imgdir, f), 'assets/' + f)
print('OK', out, os.path.getsize(out) // 1024, 'KB')
