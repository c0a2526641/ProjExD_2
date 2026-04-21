import os
import sys
import random
import time
import pygame as pg


DELTA = {
    pg.K_UP: (0, -5), #上
    pg.K_DOWN: (0, 5), #下
    pg.K_LEFT: (-5, 0), #左
    pg.K_RIGHT: (5, 0), #右
}


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect 
    戻り値：横方向，縦方向判定結果（True：画面内、False：画面外） 
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    演習1: ゲームオーバー画面を表示 
    """
    #ブラックアウト
    black_out = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_out, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_out.set_alpha(150)# 透明度 
    #Game Overの文字列
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    #泣いてるこうかとん画像
    kk_img1 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5)
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5)

    screen.blit(black_out, [0, 0])
    screen.blit(txt, [400, 300])
    screen.blit(kk_img1, [300, 260])
    screen.blit(kk_img2, [740, 260])
    pg.display.update()
    time.sleep(5) #5秒表示


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    演習3：移動方向に応じたこうかとん画像の辞書を返す 
    """
    base_img = pg.image.load("fig/3.png")
    flip_img = pg.transform.flip(base_img, True, False)
    
    kk_dict = {
        (0, 0): pg.transform.rotozoom(base_img, 0, 0.9),      #静止
        (0, -5): pg.transform.rotozoom(flip_img, 90, 0.9),    #上
        (5, -5): pg.transform.rotozoom(flip_img, 45, 0.9),    #右上
        (5, 0): pg.transform.rotozoom(flip_img, 0, 0.9),      #右
        (5, 5): pg.transform.rotozoom(flip_img, -45, 0.9),    #右下
        (0, 5): pg.transform.rotozoom(flip_img, -90, 0.9),    #下
        (-5, 5): pg.transform.rotozoom(base_img, 45, 0.9),    #左下
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),     #左
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),  #左上
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20)) #爆弾用の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #爆弾円を描く
    bb_img.set_colorkey((0, 0, 0)) 
    bb_rct = bb_img.get_rect() #爆弾Rectを取得する
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #爆弾の初期座標を設定する
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    kk_imgs = get_kk_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            gameover(screen) #ゲームオーバーの画面表示  
            return #ゲームオーバーの意味でmain関数から出る
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): 
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx , vy) #爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向の判定
            vx *= -1
        if not tate: #縦方向の判定
            vy *= -1
        
        screen.blit(bb_img, bb_rct) #爆弾を表示させる
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()