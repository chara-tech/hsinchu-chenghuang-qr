from PIL import Image, ImageDraw
import random

BASE = '/Users/pink_chara/Documents/claude/projects/新竹城隍廟/'

# ── 假 QR Code 樣稿 ────────────────────────────────────────────────
FINDER = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],
]
def make_qr():
    g = [[0]*21 for _ in range(21)]
    def fp(r,c):
        for i in range(7):
            for j in range(7): g[r+i][c+j] = FINDER[i][j]
    fp(0,0); fp(0,14); fp(14,0)
    for k in range(8,13): g[6][k]=k%2; g[k][6]=k%2
    rng = random.Random(77)
    for r in range(21):
        for c in range(21):
            if r<9 and c<9: continue
            if r<9 and c>12: continue
            if r>12 and c<9: continue
            if r==6 or c==6: continue
            g[r][c] = rng.randint(0,1)
    return g
QR = make_qr()

def draw_qr_card(img, cx, cy):
    IW, IH = img.size
    card = int(min(IW,IH)*0.092)
    pad  = card//7
    mod  = (card-pad*2)//21
    inner= mod*21
    cw   = inner+pad*2; ch = inner+pad*2
    x0   = cx-cw//2;    y0 = cy-ch//2
    ov   = Image.new('RGBA',(IW,IH),(0,0,0,0))
    d    = ImageDraw.Draw(ov)
    sh   = max(3,card//28)
    d.rectangle([x0+sh,y0+sh,x0+cw+sh,y0+ch+sh], fill=(0,0,0,70))
    d.rectangle([x0,y0,x0+cw,y0+ch], fill=(255,255,255,248))
    for r in range(21):
        for c in range(21):
            if QR[r][c]!=1: continue
            mx=x0+pad+c*mod; my=y0+pad+r*mod
            is_f=((r<7 and c<7)or(r<7 and c>13)or(r>13 and c<7))
            if is_f: d.rectangle([mx+1,my+1,mx+mod-1,my+mod-1],fill=(20,20,20,255))
            else:    d.ellipse([mx+1,my+1,mx+mod-1,my+mod-1],fill=(20,20,20,255))
    return Image.alpha_composite(img.convert('RGBA'),ov)

def annotate_photo(src, out, positions, rotate_cw=False, darken=0.42):
    img = Image.open(BASE+src).convert('RGBA')
    if rotate_cw: img = img.transpose(Image.Transpose.ROTATE_270)
    IW,IH = img.size
    dark = Image.new('RGBA',(IW,IH),(0,0,0,int(255*darken)))
    img  = Image.alpha_composite(img,dark)
    for (cx,cy) in positions: img = draw_qr_card(img,cx,cy)
    img.convert('RGB').save(BASE+out, quality=92)
    print(f'✓ {out}')

W,H = 4032,3024

# ── 6 張位置照片（乾淨原圖）────────────────────────────────────────
# 01 廟前廣場：IMG_0066（乾淨，需旋轉 CW）4284×5712 後
annotate_photo('IMG_0066.JPG','loc01_廟前廣場.jpg',
               [(int(4284*0.28), int(5712*0.40))], rotate_cw=True)

# 02 廟宇入口：IMG_0056，左門板圈圈位置
annotate_photo('IMG_0056.JPG','loc02_入口.jpg',
               [(int(W*0.25), int(H*0.54))])

# 03 公爺殿點香處：IMG_0074（乾淨）
annotate_photo('IMG_0074.JPG','loc03_點香處.jpg',
               [(int(W*0.49), int(H*0.50))])

# 04 奶奶殿：IMG_0079，拱門右側紅板
annotate_photo('IMG_0079.JPG','loc04_奶奶殿側門.jpg',
               [(int(W*0.60), int(H*0.48))])

# 05 彌勒殿：IMG_0082（乾淨），右門左邊框
annotate_photo('IMG_0082.JPG','loc05_彌勒殿.jpg',
               [(int(W*0.38), int(H*0.52))])

# 06 法蓮寺：IMG_0086（乾淨），左牆+折疊桌牆
annotate_photo('IMG_0086.JPG','loc06_法蓮寺.jpg',
               [(int(W*0.24), int(H*0.50)),
                (int(W*0.83), int(H*0.50))])

# ── 可標注.png：加上 01–06 號碼標籤 ──────────────────────────────
def annotate_map():
    MW, MH = 1550, 1806
    img = Image.open(BASE+'可標注.png').convert('RGBA')
    d   = ImageDraw.Draw(img)
    CORAL = (243,100,88)
    WHITE = (255,255,255)

    # 6 個 QR 點位置（依 可標注_參考.png 對應）
    # (x, y, label)
    locations = [
        (195, 1540, '01'),   # B0  廟前廣場
        (220, 1430, '02'),   # A+W1 廟宇入口
        ( 70, 1135, '03'),   # B1  公爺殿點香處
        ( 55,  895, '04'),   # C   奶奶殿側門
        (580,  660, '05'),   # E+W3 彌勒殿
        (425, 1290, '06'),   # F+W6 法蓮寺
    ]

    r_dot = 18   # 小圓點半徑
    for (x, y, lbl) in locations:
        # coral 實心圓
        d.ellipse([x-r_dot, y-r_dot, x+r_dot, y+r_dot], fill=CORAL+(255,))
        # 白色數字（用基本字型）
        d.text((x-12, y-10), lbl, fill=WHITE+(255,))

    img.convert('RGB').save(BASE+'可標注_標注.png', quality=95)
    print('✓ 可標注_標注.png')

annotate_map()
print('\n全部完成')
