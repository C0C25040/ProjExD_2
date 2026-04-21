import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    """ゲームオーバーを表示する関数"""
    shikaku_img = pg.Surface((WIDTH, HEIGHT))#ゲームオーバー用の四角形surfaceを作成
    pg.draw.rect(shikaku_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))#四角形を描く
    shikaku_img.set_alpha(200)#四角形の透明度を設定
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GAME OVER", True, (255, 255, 255))#ゲームオーバーの文字を描く
    txt_rct = txt.get_rect(center=(WIDTH/2, HEIGHT/2))#ゲームオーバーの文字のrectを取得

    gg_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gg_rct = gg_img.get_rect(center=(WIDTH/2, HEIGHT/2))#ゲームオーバーの画像のrectを取得

    shikaku_img.blit(txt, txt_rct)#四角形を画面に貼り付ける
    shikaku_img.blit(gg_img, (gg_rct.left + 200, gg_rct.top))#ゲームオーバーの画像を画面に貼り付ける
    shikaku_img.blit(gg_img, (gg_rct.left - 200, gg_rct.top))#ゲームオーバーの画像を画面に貼り付ける
    screen.blit(shikaku_img, [0, 0])#四角形を画面に貼り付ける

    pg.display.update()
    time.sleep(5) #5秒待つ

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """時間とともに爆弾が拡大、加速する"""
    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))#爆弾用の空のsurfaceを作成
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)#爆弾円を描く
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]#加速のリストを作成
        
    return bb_imgs, bb_accs



def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル(横方向判定結果、縦方向判定結果)
    画面内ならTure,画面外ならFalse
    """
    yoko,tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))#爆弾用の空のsurfaceを作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)#爆弾円を描く
    bb_rct = bb_img.get_rect()#爆弾のrectを取得
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)#爆弾の初期座標をランダムに設定
    bb_img.set_colorkey((0, 0, 0))#爆弾の初期座標設定
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = init_bb_imgs()#爆弾の大きさと加速度のリストを取得


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾が重なったら
            print("ゲームオーバー")
            gameover(screen) #ゲームオーバーの関数を呼び出す
            return #ゲームオーバーの意味でmain関数から出る

        screen.blit(bg_img, [0, 0]) 
        DELTA = {
            pg.K_UP: (0, -5),
            pg.K_DOWN: (0, +5),
            pg.K_LEFT: (-5, 0),
            pg.K_RIGHT: (+5, 0),
        }
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko : #横方向に画面外ならば
            vx *= -1 #速度の向きを反転させる
        if not tate : #縦方向に画面外ならば
            vy *= -1 #速度の向きを反転させる
        avx = vx*bb_accs[min(tmr//500, 9)]#爆弾の加速度を設定
        avy = vy*bb_accs[min(tmr//500, 9)]#爆弾の加速度を設定
        bb_img = bb_imgs[min(tmr//500, 9)]#爆弾の大きさを設定
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy) #爆弾の移動

        screen.blit(bb_img, bb_rct) #爆弾の表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
