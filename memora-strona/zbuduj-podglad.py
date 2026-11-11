# Tworzy podglad.html: jeden plik z filmami w środku (do otwarcia jednym kliknięciem).
# Uruchom: python3 zbuduj-podglad.py
import base64, re, os

d = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(d, 'index.html'), encoding='utf-8').read()


def emb(m):
    p = os.path.join(d, m.group(1))
    if not os.path.exists(p):
        return m.group(0)
    return 'plik: "data:video/mp4;base64,' + base64.b64encode(open(p, 'rb').read()).decode() + '"'


s = re.sub(r'plik: "(filmy/[^"]+)"', emb, s)
open(os.path.join(d, 'podglad.html'), 'w', encoding='utf-8').write(s)
print(round(len(s) / 1e6, 2), 'MB')
