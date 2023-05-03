import pygame
from pygame.locals import *
import sys
import random
import time

FIELD_H = 10
FIELD_W = 10
field = []  # bom→1, nothing→0
openlist = []  # opened→1, unopened→0
flaglist = []  # put→1, nothing→0
GRAY = (204, 204, 204)
LBLUE = (0, 192, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
phase = -1
times = 0

def initialization():
    """
    フィールド等の必要な初期化処理を行う
    Returns:
    mine_counter, auto_open_counter
    """
    # field setting
    for x in range(FIELD_H):
        field.append([0] * FIELD_W)

    # openlist setting
    for x in range(FIELD_H):
        openlist.append([0] * FIELD_W)

    # flaglist setting
    for x in range(FIELD_H):
        flaglist.append(([0] * FIELD_W))

    # set mine
    mine_counter = 0
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            m = random.randint(1, 100)
            if 1 <= m <= 25:
                field[y][x] = 1
                mine_counter += 1

    # init field
    auto_open_counter = 0
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            if field[y][x] == 0 and openlist[y][x] == 0:
                m = random.randint(1, 100)
                if 1 <= m <= 20:
                    openlist[y][x] = 1
                    auto_open_counter += 1

    return mine_counter, auto_open_counter


def re_init():
    """
    2回目以降の初期化処理を行う
    Returns:
    mine_counter, auto_open_counter
    """

    # field setting
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            field[y][x] = 0

    # openlist setting
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            openlist[y][x] = 0

    # flaglist setting
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            flaglist[y][x] = 0

    # set mine
    mine_counter = 0
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            m = random.randint(1, 100)
            if 1 <= m <= 25:
                field[y][x] = 1
                mine_counter += 1

    # init field
    auto_open_counter = 0
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            if field[y][x] == 0 and openlist[y][x] == 0:
                m = random.randint(1, 100)
                if 1 <= m <= 20:
                    openlist[y][x] = 1
                    auto_open_counter += 1

    return mine_counter, auto_open_counter

def retry(re_init):
    """
    phaseを0に戻し, ゲームオーバーorクリア後にリトライする
    Returns:
    counter_tup (= (mine_counter, auto_open_counter))
    """

    global phase
    phase = 0
    counter_tup = re_init()

    return counter_tup


def explosion(se):
    """
    mouseXとmouseYからポインターがどのマスを選択したかを調べて、そのマスに爆発の画像と音を出力する
    Returns:
    None
    """

    # global
    global phase
    # play SE
    for x in range(FIELD_W):
        for y in range(FIELD_H):
            if openlist[y][x] == 1 and field[y][x] == 1:
                se.play()
                phase = 1

    return None


def blit_bom_num(font2, screen):
    """
    fieldの値が0かつopenlistが1のマスに、checklistから値を得ていくつの爆弾があるかを描画する
    openlistを参照して、opened(1)ならblit,unopened(0)ならblitしない
    Returns:
    None
    """

    for y in range(FIELD_H):
        for x in range(FIELD_W):
            r = random.randint(1, 100)
            # 周りのfieldの値を調べて, 足してbom_numとする
            # 角
            if (y, x) == (0, 0):
                bom_num = str(field[0][1] + field[1][1] + field[1][0])
            elif (y, x) == (0, FIELD_W - 1):
                bom_num = str(field[0][FIELD_W - 2] + field[1][FIELD_W - 2] + field[1][FIELD_W - 1])
            elif (y, x) == (FIELD_H - 1, 0):
                bom_num = str(field[FIELD_H - 2][0] + field[FIELD_H - 2][1] + field[FIELD_H - 1][1])
            elif (y, x) == (FIELD_H - 1, FIELD_W - 1):
                bom_num = str(
                    field[FIELD_H - 2][FIELD_W - 1] + field[FIELD_H - 2][FIELD_W - 2] + field[FIELD_H - 1][FIELD_W - 2])
            # 端　(上端→下端→左端→右端)
            elif y == 0 and x != 0 and x != FIELD_W - 1:
                bom_num = str(
                    field[y][x - 1] + field[y][x + 1] + field[y + 1][x - 1] + field[y + 1][x] + field[y + 1][x + 1])
            elif y == FIELD_H - 1 and x != 0 and x != FIELD_W - 1:
                bom_num = str(
                    field[y][x - 1] + field[y][x + 1] + field[y - 1][x - 1] + field[y - 1][x] + field[y - 1][x + 1])
            elif x == 0 and y != 0 and y != FIELD_H - 1:
                bom_num = str(
                    field[y - 1][x] + field[y + 1][x] + field[y - 1][x + 1] + field[y][x + 1] + field[y + 1][x + 1])
            elif x == FIELD_W - 1 and y != 0 and y != FIELD_H - 1:
                bom_num = str(
                    field[y - 1][x] + field[y + 1][x] + field[y - 1][x - 1] + field[y][x - 1] + field[y + 1][x - 1])
            # 内側 左上→真上→右上→右→右下→真下→左下→左
            else:
                bom_num = str(field[y - 1][x - 1] + field[y - 1][x] + field[y - 1][x + 1] + field[y][x + 1] +
                              field[y + 1][x + 1] + field[y + 1][x] + field[y + 1][x - 1] + field[y][x - 1])

            bom_num_txt = font2.render(bom_num, True, BLACK)
            if field[y][x] == 0 and openlist[y][x] == 1:
                screen.blit(bom_num_txt, [x * 50 + 15, y * 50 + 10])
            else:
                pass

    return None


def open(mouseX, mouseY):
    """
    マウスで選択されたマスを開く。（openlistで該当のマスの値を1に変える, 色変更はdraw関数に任せる）
    Returns:
    None
    """

    # X, Yはopenlistのインデックス
    X = mouseX // 50
    Y = mouseY // 50
    openlist[Y][X] = 1

    return None


def put_warning(mouseX, mouseY):
    """
    マウスで右クリックされたマスに"危"と描く
    macの右クリックは2本指でクリック
    Returns:
    None
    """

    X = mouseX // 50
    Y = mouseY // 50
    if flaglist[Y][X] == 0:
        flaglist[Y][X] = 1
        time.sleep(0.2)
    else:
        flaglist[Y][X] = 0
        time.sleep(0.2)

    return None


def draw(screen, font1, font2, ja_font1, start_time, counter_tup, open_count):
    """
    種々の描画処理を行う
    Returns:
    None
    """
    screen.fill(BLACK)
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            if openlist[y][x] == 1:
                pygame.draw.rect(screen, LBLUE, [x * 50, y * 50, 50, 50])
            else:
                pygame.draw.rect(screen, GRAY, [x * 50, y * 50, 50, 50])
                if flaglist[y][x] == 1:
                    # blit "危"
                    danger = "危"
                    danger_txt = ja_font1.render(danger, True, RED)
                    screen.blit(danger_txt, [x * 50 + 15, y * 50 + 15])

    for y in range(FIELD_H + 1):
        pygame.draw.line(screen, BLACK, [0, 50 * y], [500, 50 * y])
    for x in range(FIELD_W + 1):
        pygame.draw.line(screen, BLACK, [50 * x, 0], [50 * x, 500])

    # blit how to
    to_open = "Open:Click"
    warning = "Put warning:Right-click"
    restart = "Restart:Space"
    to_open_txt = font1.render(to_open, True, WHITE)
    warning_txt = font1.render(warning, True, WHITE)
    restart_txt = font1.render(restart, True, WHITE)
    screen.blit(to_open_txt, [175, 510])
    screen.blit(warning_txt, [85, 550])
    screen.blit(restart_txt, [150, 590])

    # blit score
    score = str(100 * (open_count - counter_tup[1]))
    score_txt = font2.render(score, True, WHITE)
    screen.blit(score_txt, [90, 630])

    # blit timer
    milli_seconds = (pygame.time.get_ticks() - start_time)  # prepare for timer
    seconds = (milli_seconds // 1000) % 60  # ms → seconds
    minutes = milli_seconds // 60000  # ms → seconds → minutes
    timer = ("%s:%s" % (minutes, seconds))
    txt = font2.render(timer, True, GRAY)
    screen.blit(txt, [340, 630])  # blit the timer

    return None


def main():
    # global
    global phase, times
    # init and return (mine_counter, auto_open_counter)
    counter_tup = initialization()

    pygame.init()
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Mine Sweeping")
    clock = pygame.time.Clock()
    font1 = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 50)
    ja_font1 = pygame.font.SysFont("ヒラキノ明朝pron", 20)
    ja_font2 = pygame.font.SysFont("ヒラキノ明朝pron", 40)

    try:
        img_title = pygame.image.load("image/title2.png")
    except:
        print("pngファイルを発見することができません")

    try:
        pygame.mixer.music.load("music/bgm_maoudamashii_8bit02.ogg")
        pygame.mixer.music.play(-1)
        se = pygame.mixer.Sound("music/bomb1.ogg")
    except:
        print("oggファイルを発見することが出来ないか, オーディオ機器が接続されていません.")

    while True:
        # redo
        key = pygame.key.get_pressed()
        if key[K_SPACE] == 1:
            counter_tup = re_init()

        for event in pygame.event.get():  # exit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # get mouse state
        mouseX, mouseY = pygame.mouse.get_pos()
        pos = ((mouseX // 50) * 50, (mouseY // 50) * 50)
        mouse_Btn1, mouse_Btn2, mouse_Btn3 = pygame.mouse.get_pressed()

        # phase -1:title
        if phase == -1:
            # Remember fill black
            screen.fill(BLACK)
            # blit title and press enter
            screen.blit(img_title, [10, 150])
            direction = "press Enter"
            direction_txt = font2.render(direction, True, LBLUE)
            screen.blit(direction_txt, [150, 400])
            if key[K_RETURN] == 1:
                phase = 0
                # play the bgm
                try:
                    pygame.mixer.music.load("music/game_maoudamashii_8_piano04.ogg")
                    pygame.mixer.music.play(-1)
                except:
                    print("oggファイルを発見することが出来ないか, オーディオ機器が接続されていません.")

                start_time = pygame.time.get_ticks()

        # phase 0:play
        elif phase == 0:
            # calc opened cell
            open_count = 0
            for y in range(FIELD_H):
                for x in range(FIELD_W):
                    if field[y][x] == 0 and openlist[y][x] == 1:
                        open_count += 1
            # draw
            draw(screen, font1, font2, ja_font1, start_time, counter_tup, open_count)
            if mouse_Btn1 == 1 and mouseY <= 500:
                open(mouseX, mouseY)
            elif mouse_Btn3 == 1 and mouseY <= 500:
                put_warning(mouseX, mouseY)

            # explosion
            explosion(se)

            # blit bomb number
            blit_bom_num(font2, screen)

            # change phase
            if (100 - open_count) == counter_tup[0]:
                phase = 2
                end_time = (pygame.time.get_ticks() - start_time)

        # phase 1:gameover
        elif phase == 1:
            surface = pygame.Surface((200, 200), flags=pygame.SRCALPHA)
            surface.fill((255, 0, 0, 128))
            bomb_txt = font2.render("BANG!!", True, BLACK)
            GG_txt = font2.render("Good Game", True, BLACK)
            retry_txt = font2.render("RETRY:ESC", True, BLACK)
            screen.blit(surface, [150, 150])
            screen.blit(bomb_txt, [190, 170])
            screen.blit(GG_txt, [152, 230])
            screen.blit(retry_txt, [152, 310])
            # retry
            if key[K_ESCAPE] == 1:
                counter_tup = retry(re_init)

        # phase 2:clear
        elif phase == 2:
            screen.fill(BLACK)
            # blit texts
            restart = "RESTART:SPACE"
            restart_txt = font2.render(restart, True, WHITE)
            copyright = "BGM:魔王魂"
            bgm_txt = ja_font2.render(copyright, True, RED)
            clear_txt = font2.render("Cleared!!", True, WHITE)
            score_str_txt = font2.render("SCORE", True, WHITE)
            timer_txt = font2.render("TIME", True, WHITE)
            screen.blit(restart_txt, [110, 510])
            screen.blit(bgm_txt, [135, 600])
            screen.blit(clear_txt, [175, 100])
            screen.blit(score_str_txt, [80, 200])
            screen.blit(timer_txt, [310, 200])


            # blit clear_time
            milli_seconds = (end_time - start_time)  # prepare for timer
            seconds = (milli_seconds // 1000) % 60  # ms → seconds(remainder of 60)
            minutes = milli_seconds // 60000  # ms → seconds → minutes
            clear_time = ("%s:%s" % (minutes, seconds))
            clear_time_txt = font2.render(clear_time, True, GRAY)
            screen.blit(clear_time_txt, [315, 245])  # blit the timer

            # blit score(タイムボーナス有)
            if times == 0:
                score = 100 * (open_count - counter_tup[1])
                bonus = 50 * (600 - (60 * minutes + seconds))
            score_txt = font2.render(str(score), True, WHITE)
            bonus_txt = font2.render(str(bonus), True, WHITE)
            bonus_str_txt = font2.render("TIME BONUS", True, WHITE)
            if times == 0:
                screen.blit(score_txt, [90, 245])
                pygame.display.update()
                time.sleep(1)
                times += 1
                continue

            screen.blit(score_txt, [90, 245])
            screen.blit(bonus_txt, [90, 350])
            screen.blit(bonus_str_txt, [40, 310])

            if bonus > 0:
                score += 50
                bonus -= 50

            if key[K_SPACE] == 1:
                counter_tup = retry(re_init)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()