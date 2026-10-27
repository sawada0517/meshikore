# LP（index.html）で使っている文字だけを含むフォントを Google Fonts に作ってもらうよう、<link> の URL を書き直す。
# 日本語のフォントは、文字を細かく分けた数百のファイルで届くので、全部の文字を指定すると、
# 最初の表示で設定の CSS（約170KB）と80本ほどのフォントを読み込んでいた。text= で使う文字だけにすると、太さごとに1本になる。
#
# LP の文を変えたら、必ずこれを流す（新しい文字がフォントに無いと、その字だけ別の字体で出る）：
#   python3 -I tools/font-url.py
import re, sys, urllib.parse, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
page = root / 'index.html'
html = page.read_text(encoding='utf-8')

FAMILIES = 'family=Zen+Maru+Gothic:wght@700;900&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Klee+One:wght@600'

# ページの中の文字（画面の文・JS の中の文言・aria-label など全部）。<link> の URL 自体は数えない
body = re.sub(r'<link[^>]+fonts\.googleapis\.com/css2[^>]+>', '', html)
chars = set(body)
# 英数字・記号はいつでも出せるように全部入れる
chars |= set(chr(c) for c in range(0x20, 0x7f))
chars |= set('０１２３４５６７８９、。・「」『』（）！？ー〜…％')
chars = ''.join(sorted(c for c in chars if c.isprintable() and c not in '\n\r\t'))

url = 'https://fonts.googleapis.com/css2?' + FAMILIES + '&display=swap&text=' + urllib.parse.quote(chars, safe='')
link = f'<link rel="stylesheet" href="{url}">'

new, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]+">', lambda m: link, html)
if n != 1:
    sys.exit('index.html の Google Fonts の <link> が見つかりません')
page.write_text(new, encoding='utf-8')
print(f'{len(chars)} 文字・URL {len(url)} 文字')
