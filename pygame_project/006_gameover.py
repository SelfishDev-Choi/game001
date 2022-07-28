import os
import pygame
#########################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
from random import *

pygame.init()       #초기화 (반드시 필요)

# 화면크기 설정

screen_width = 1380     # 가로크기
screen_height = 845     # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption("Nado Pang")

#fps
clock = pygame.time.Clock()
#########################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도 폰트 등)

currnet_path = os.path.dirname(__file__)    # 현재 파일의 위치를 반환
image_path = os.path.join(currnet_path, "images")   # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background1.jpg"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]    #스테이지 높이위에 캐릭터를 놓기 위해

# 캐릭터 만들기 
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]

character_x_pos = (screen_width - character_width)/2
character_y_pos = screen_height - stage_height - character_height

character_move_speed = 0.5
character_to_x = 0

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

weapon_count = 1
# 무기 이동 속도
weapons_move_speed = 5

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공의 속도가 다르다. 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3에 해당하는 값

# 공들
balls = []

# 최초 방생하는 큰 공 추가
balls.append({
    "pos_x" : 50,       # 공의 x 좌표
    "pos_y" : 50,       # 공의 y 좌표
    "img_idx" : 0,      # 공의 이미지 인덱스
    "to_x" : 3,         # x축 이동방향 -3 이면 왼쪽으로, 3 이면 오른쪽으로
    "to_y" : -6,        # y축 이동방향
    "init_spe_y" : ball_speed_y[0]     # y 최초 속도
})


# 사라질 무기와 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메세지 Time Over, Mission Complete, Game Over
game_result = "Game Over"

# 이벤트 루프
running = True              # 게임이 진행중인가?
# 시간 초가로 종료하는 경우 딜레이 
delay_timeout = False


while running:
    dt = clock.tick(30)             #게임 화면의 초당 프레임 수를 설정

    #print("fps : " + str(clock.get_fps())) # 프레임 속도를 출력해 볼 수 있음

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_move_speed
            if event.key == pygame.K_RIGHT:
                character_to_x += character_move_speed
            if event.key == pygame.K_SPACE:
                weapon_x_pos = (character_x_pos + (character_width / 2)) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x * dt

    # 캐릭터가 밖으로 나가는 것 방지
    if character_x_pos <= 0:
        character_x_pos = 0
    if character_x_pos >= (screen_width - character_width):
        character_x_pos = (screen_width - character_width)


    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1] - weapons_move_speed] for w in weapons if w[1] > 0]
    
    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapons_move_speed] for w in weapons]

    # 공 위치 정의 [01:57:55]
    for ball_idx, ball_val in enumerate(balls):     #balls에 있는 인덱스와 값을 출력해 줌
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동이 바뀌는 효과
        if ball_pos_x <= 0 or ball_pos_x >= (screen_width - ball_width):
            ball_val["to_x"] = ball_val["to_x"] * -1


        if ball_pos_y >= (screen_height - stage_height - ball_height):
            ball_val["to_y"] = ball_val["init_spe_y"]
        else:
            ball_val["to_y"] += 0.5    #점점 느리게 올라가고 빠르게 내려오는 효과를 준다.

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    # 캐릭터 위치 수정
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 4. 충돌 처리
    
    # 캐릭터 rect 정보 업데이트
    for ball_idx, ball_val in enumerate(balls):     #balls에 있는 인덱스와 값을 출력해 줌
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공하고 캐릭터가 충돌
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공들하고 무기들 충돌
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # 가장 작은 공이 아니라면 둘로 나누어 준다.
                if ball_img_idx < 3:
                    #현재 볼 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),       # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),       # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1,      # 공의 이미지 인덱스
                        "to_x" : -3,         # x축 이동방향 -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y" : -6,        # y축 이동방향
                        "init_spe_y" : ball_speed_y[ball_img_idx + 1]     # y 최초 속도
                    })

                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),       # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),       # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1,      # 공의 이미지 인덱스
                        "to_x" : 3,         # x축 이동방향 -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y" : -6,        # y축 이동방향
                        "init_spe_y" : ball_speed_y[ball_img_idx + 1]     # y 최초 속도
                    })
                break
        else:           # for문에 대해서도 else 문이 적용되는 경우, 계속 게임을 진행
            continue    # 안쪽 for 문 조건이 맞지 않으면 continue, 바깥 for 문 계속 수행
        break           # 안쪽 for 문에서 break를 만나면 여기로 진입 가능, 2중 for 문을 한번에 탈출
            # if weapon_to_remove > -1:
            #     break
    
    # 충돌된 공  or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        # game_result = "Mission Complete"
        # running = False
        weapon_count += 1
        for c in range(weapon_count):
            start_x = randint(0, screen_width - 160)

            if start_x < (screen_width/2):
                to_x = 3
            else:
                to_x = -3


            balls.append({
                "pos_x" : start_x,       # 공의 x 좌표
                "pos_y" : 50,       # 공의 y 좌표
                "img_idx" : 0,      # 공의 이미지 인덱스
                "to_x" : 3,         # x축 이동방향 -3 이면 왼쪽으로, 3 이면 오른쪽으로
                "to_y" : -6,        # y축 이동방향
                "init_spe_y" : ball_speed_y[0]     # y 최초 속도
            })

    # 5. 화면에 그리기
    
    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10,10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()             # 게임 화면을 다시 그리기 (계속 그려야 함)

game_over_msg = game_font.render(game_result, True, (255, 255, 0))
game_over_rect = game_over_msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(game_over_msg, game_over_rect)
# game_over_rect = game_over_msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2))).size
# game_over_width = game_over_rect[0]
# game_over_height = game_over_rect[1]
# screen.blit(game_over_msg, ((screen_width - game_over_width)/2, (screen_height - game_over_height)/2))

pygame.display.update()
#시간이 초과되어 종료 되는 경우 2초 지연 후 종료
pygame.time.delay(2*1000) # 종료 하기 전 2초 정도 대기

pygame.quit()       #pygame 종료

# pyinstaller -F -w <파이썬 파일명>  -> 실행파일 만들기