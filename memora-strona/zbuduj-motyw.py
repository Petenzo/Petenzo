# Buduje motyw Shopify (folder motyw-shopify/ + lumorka-motyw.zip) z index.html.
# Uruchom: python3 zbuduj-motyw.py
import os, re, shutil, json, zipfile
d = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(d, 'motyw-shopify')
VARIANTS = {'Biały': 55770552336725, 'Czarny': 55770552369493}
s = open(os.path.join(d, 'index.html'), encoding='utf-8').read()
head = s[s.index('<head>') + 6:s.index('</head>')]
body = s[s.index('<body>') + 6:s.index('</body>')]

# --- prawdziwy koszyk Shopify zamiast demo ---
go = ("async function goCheckout(){ const V=" + json.dumps(VARIANTS, ensure_ascii=False) + ", m={};"
      " cartItems.forEach(i=>i.color.split(', ').forEach(c=>{const v=V[c]||V['Biały']; m[v]=(m[v]||0)+i.qty;}));"
      " try{ await fetch('/cart/clear.js',{method:'POST'});"
      " const r=await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:Object.entries(m).map(([id,quantity])=>({id:+id,quantity}))})});"
      " if(!r.ok) throw 0; location.href='/checkout'; }catch(e){ toast('Coś poszło nie tak, spróbuj ponownie.'); } }\n")
old1 = "$('#shipGo').onclick=()=>{ closeShip(); closeCart(); toast('Podgląd: tu klient przejdzie do kasy Shopify (' + shipMethod + ').'); };"
old2 = "$('#cpOrder').onclick=()=>toast('Podgląd: tu klient przejdzie do kasy Shopify i zapłaci.');"
assert old1 in body and old2 in body
body = body.replace(old1, go + "$('#shipGo').onclick=()=>{ $('#shipGo').textContent='Przechodzę do kasy…'; goCheckout(); };")
body = body.replace(old2, "$('#cpOrder').onclick=goCheckout;")

# --- pliki: zdjęcia i filmy jako assets ---
if os.path.exists(OUT): shutil.rmtree(OUT)
for sub in ['layout', 'templates', 'sections', 'assets', 'config', 'locales', 'snippets']:
    os.makedirs(os.path.join(OUT, sub))
used = set()
def asset(m):
    p = m.group(1); name = os.path.basename(p)
    src = os.path.join(d, p)
    if not os.path.exists(src): return m.group(0)
    shutil.copy(src, os.path.join(OUT, 'assets', name)); used.add(name)
    return '{% endraw %}{{ \'' + name + '\' | asset_url }}{% raw %}'
pat = r'((?:zdjecia|filmy)/[A-Za-z0-9_./-]+\.(?:jpg|png|mp4))'
body = re.sub(pat, asset, body)
head = re.sub(pat, asset, head)

layout = ('<!DOCTYPE html>\n<html lang="pl">\n<head>\n' +
          '{% raw %}' + head.replace('<title>Lumorka</title>', '') + '{% endraw %}\n'
          '<title>{% if template contains "product" %}{{ product.title }}{% else %}Lumorka – świecąca kula wspomnień{% endif %}</title>\n'
          '<link rel="icon" href="{{ \'favicon.png\' | asset_url }}">\n'
          '{{ content_for_header }}\n</head>\n<body>\n{{ content_for_layout }}\n</body>\n</html>\n')
open(os.path.join(OUT, 'layout', 'theme.liquid'), 'w', encoding='utf-8').write(layout)

section = '{% raw %}' + body + '{% endraw %}\n{% schema %}{"name":"Strona Lumorka","settings":[]}{% endschema %}\n'
open(os.path.join(OUT, 'sections', 'lumorka.liquid'), 'w', encoding='utf-8').write(section)

# prosta sekcja dla innych stron (polityki, strony, 404, wyszukiwanie)
generic = '''<style>.lm-simple{max-width:760px;margin:0 auto;padding:40px 20px 80px;font-family:Poppins,sans-serif;color:#1b1b1f;line-height:1.7}
.lm-simple h1{font-family:"Playfair Display",serif;color:#14325f;font-size:34px;margin:24px 0 18px}.lm-simple h2{color:#14325f;font-size:19px;margin:26px 0 8px}
.lm-top{display:flex;justify-content:center;padding:18px;border-bottom:1px solid #efe8da}.lm-top a{font-family:"Playfair Display",serif;font-weight:600;font-size:32px;color:#14325f;text-decoration:none}
.lm-back{display:inline-block;margin-top:30px;color:#1f5fbf;font-weight:600}</style>
<div class="lm-top"><a href="/">Lumorka</a></div>
<div class="lm-simple">{{ content }}<a class="lm-back" href="/">← Wróć do sklepu</a></div>
'''
open(os.path.join(OUT, 'snippets', 'prosta-strona.liquid'), 'w', encoding='utf-8').write(generic)

def jtpl(name):
    json.dump({"sections": {"main": {"type": "lumorka"}}, "order": ["main"]},
              open(os.path.join(OUT, 'templates', name), 'w'))
jtpl('index.json'); jtpl('product.json')
simple = {
 'page.liquid': "{% capture c %}<h1>{{ page.title }}</h1>{{ page.content }}{% endcapture %}{% render 'prosta-strona', content: c %}",
 '404.liquid': "{% capture c %}<h1>Nie znaleziono strony</h1><p>Ta strona nie istnieje.</p>{% endcapture %}{% render 'prosta-strona', content: c %}",
 'search.liquid': "{% capture c %}<h1>Szukaj</h1><p><a href='/products/kula-wspomnien'>Zobacz Lumorkę – świecącą kulę wspomnień</a></p>{% endcapture %}{% render 'prosta-strona', content: c %}",
 'collection.liquid': "<script>location.replace('/products/kula-wspomnien')</script>",
 'list-collections.liquid': "<script>location.replace('/products/kula-wspomnien')</script>",
 'blog.liquid': "<script>location.replace('/')</script>",
 'article.liquid': "<script>location.replace('/')</script>",
 'cart.liquid': "<script>location.replace({% if cart.item_count > 0 %}'/checkout'{% else %}'/'{% endif %})</script>",
 'password.liquid': "{% capture c %}<h1>Wkrótce otwieramy</h1><p>Sklep Lumorka startuje już niedługo.</p>{% form 'storefront_password' %}{{ form.errors | default_errors }}<p><input type='password' name='password' placeholder='Hasło' style='padding:10px;border:1px solid #ddd;border-radius:8px'> <button type='submit' style='padding:10px 18px;background:#14325f;color:#fff;border-radius:8px;border:0'>Wejdź</button></p>{% endform %}{% endcapture %}{% render 'prosta-strona', content: c %}",
}
for k, v in simple.items():
    open(os.path.join(OUT, 'templates', k), 'w', encoding='utf-8').write(v)

json.dump([{"name": "theme_info", "theme_name": "Lumorka", "theme_version": "1.0.0", "theme_author": "Lumorka",
            "theme_documentation_url": "https://lumorka.pl", "theme_support_url": "https://lumorka.pl"}],
          open(os.path.join(OUT, 'config', 'settings_schema.json'), 'w'))
json.dump({"current": {}}, open(os.path.join(OUT, 'config', 'settings_data.json'), 'w'))
json.dump({}, open(os.path.join(OUT, 'locales', 'pl.default.json'), 'w'))
# favicon z logo
from PIL import Image
Image.open(os.path.join(d, 'logo', 'LUMORKA-LOGO-PROFILOWE-granat.png')).resize((96, 96)).save(os.path.join(OUT, 'assets', 'favicon.png'))

z = os.path.join(d, 'lumorka-motyw.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
    for root, _, files in os.walk(OUT):
        for fn in files:
            p = os.path.join(root, fn); f.write(p, os.path.relpath(p, OUT))
print('assets:', len(used), 'zip MB:', round(os.path.getsize(z) / 1e6, 2))
