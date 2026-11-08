import base64,io,os,re,sys
from PIL import Image
src=open('src.html',encoding='utf-8').read()
# 1) wersja lokalna i Shopify
open('kwiatora-shopify.html','w',encoding='utf-8').write(src.replace('{{IMG}}','https://raw.githubusercontent.com/Petenzo/Petenzo/claude/gracious-bell-yojazo/kwiatora/img'))
# 2) index.html: zdjęcia wbudowane (działa wszędzie, także w podglądzie)
cache={}
def data(f):
    if f in cache: return cache[f]
    p='img/'+f; im=Image.open(p)
    if f.endswith('.png'):
        b=io.BytesIO(); im.save(b,'PNG',optimize=True); u='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
    else:
        im=im.convert('RGB'); im.thumbnail((720,720)); b=io.BytesIO(); im.save(b,'WEBP',quality=68,method=6); u='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    cache[f]=u; return u
names=sorted(f for f in os.listdir('img') if f.endswith(('.jpg','.png')))
out=src.replace('<meta property="og:image" content="{{IMG}}/04-prezent.jpg">','')
ids={f:'kwi%d'%i for i,f in enumerate(names)}
# statyczne <img src="{{IMG}}/x"> -> data-kw, wypełniane z mapy (bez duplikatów)
HERO=('00-hero-stol.jpg','logo-ikona.png')
out=re.sub(r'src="\{\{IMG\}\}/([^"]+)"',lambda m:('src="%s"'%data(m.group(1))) if m.group(1) in HERO else 'src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" data-kw="%s"'%m.group(1),out)
mp='<script>window.KW_IMG={'+','.join('"%s":"%s"'%(f,data(f)) for f in names)+'};document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll("img[data-kw]").forEach(function(i){i.src=window.KW_IMG[i.dataset.kw]})});</script>'
out=out.replace('<script>\n(function(){',mp+'\n<script>\n(function(){',1)
out=out.replace('{{IMG}}','img')
open('index.html','w',encoding='utf-8').write(out)
print('index.html',len(out)//1024,'KB')
