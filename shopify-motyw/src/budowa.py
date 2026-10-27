import re
src=open('/home/user/Petenzo/lulavi-strona.html').read()
CDN='https://cdn.shopify.com/s/files/1/1123/3876/4114/files/'
head=src[:src.index('</head>')]
head=head.replace('<title>Lulavi</title>','<title>{{ page_title }}</title>\n<link rel="canonical" href="{{ canonical_url }}">')
layout=head+'{{ content_for_header }}\n</head>\n<body>\n{{ content_for_layout }}\n</body>\n</html>\n'
body=src[src.index('<body>')+6:src.index('</body>')]
body=re.sub(r'(?:src|href)="zdjecia/(?:lulavi|opinie)/([\w-]+)\.jpg"',lambda m:m.group(0).split('=')[0]+'="'+CDN+m.group(1)+'.jpg?width=1200"' if 'opinie' not in m.group(0) else m.group(0).split('=')[0]+'="'+CDN+m.group(1)+'.jpg?width=120"',body)
body=body.replace(' decoding="sync"','')
body=re.sub(r'src="zdjecia/warianty/mini-([\w-]+)\.jpg"',lambda m:'src="'+CDN+m.group(1)+'.jpg?width=120"',body)
assert 'zdjecia/lulavi' not in body and 'zdjecia/opinie' not in body
# linki
body=body.replace('<a class="logo" href="#" aria-label','<a class="logo" href="/" aria-label')
body=body.replace('<a class="cart" href="#kup" aria-label="Koszyk">','<a class="cart" href="/cart" aria-label="Koszyk">')
body=body.replace('<a class="logo" href="#">lulavi</a>','<a class="logo" href="/">lulavi</a>')
body=body.replace('<a href="#">Regulamin</a>','<a href="/policies/terms-of-service">Regulamin</a>')
body=body.replace('<a href="#">Polityka prywatności</a>','<a href="/policies/privacy-policy">Polityka prywatności</a>')
body=body.replace('<a href="#">Zwroty i reklamacje</a>','<a href="/policies/refund-policy">Zwroty i reklamacje</a>')
body=body.replace('<a href="#">Kontakt</a>','<a href="mailto:kontakt@lulavi.pl">Kontakt</a>')
# warianty z Shopify
old_w=body[body.index('  var WZORY = ['):body.index('];',body.index('  var WZORY = ['))+2]
body=body.replace(old_w,'''  var WZORY = [{% for v in product.variants %}
    { vid: {{ v.id }}, nazwa: {{ v.title | json }}, img: {{ v.featured_image | image_url: width: 200 | json }}, ok: {{ v.available | json }} }{% unless forloop.last %},{% endunless %}{% endfor %}
  ];''')
body=body.replace("obraz('zdjecia/warianty/mini-' + w.id + '.jpg')","w.img")
body=body.replace("b.setAttribute('aria-label', w.nazwa);","b.setAttribute('aria-label', w.nazwa);\n          b.dataset.vid = w.vid;")
# koszyk
body=body.replace('</script>','</script>\n'+open('/home/user/Petenzo/shopify-motyw/src/koszyk.html').read(),1)
section="{%- if product == blank -%}{%- assign product = all_products['lulavi-opaska-ze-sluchawkami-dla-dzieci'] -%}{%- endif -%}\n"+body+'\n{% schema %}\n{"name": "Lulavi – strona produktu", "settings": []}\n{% endschema %}\n'
tpl='{\n  "layout": "lulavi",\n  "sections": { "main": { "type": "lulavi-strona", "settings": {} } },\n  "order": ["main"]\n}\n'
d='/home/user/Petenzo/shopify-motyw/'
open(d+'layout/lulavi.liquid','w').write(layout)
open(d+'sections/lulavi-strona.liquid','w').write(section)
for t in ['product.lulavi','index','collection','list-collections','search']: open(d+'templates/'+t+'.json','w').write(tpl)
print(len(layout),len(section))
