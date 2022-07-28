# 01:03:08 
import os
import pygame
#########################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
from random import *

pygame.init()       #초기화 (반드시 필요)

# 화면크기 설정

screen_width = 640     # 가로크기
screen_height = 480     # 세로 크기
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
background = pygame.image.load(os.path.join(image_path, "background.png"))

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

character_move_tab = 0.5

# 이벤트 루프
running = True              # 게임이 진행중인가?
# 시간 초가로 종료하는 경우 딜레이 
delay_timeout = False

to_x = 0

while running:
    dt = clock.tick(30)             #게임 화면의 초당 프레임 수를 설정

    #print("fps : " + str(clock.get_fps())) # 프레임 속도를 출력해 볼 수 있음

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_move_tab
            if event.key == pygame.K_RIGHT:
                to_x += character_move_tab
            if event.key == pygame.K_SPACE:
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt

    # 캐릭터가 밖으로 나가는 것 방지
    if character_x_pos <= 0:
        character_x_pos = 0
    if character_x_pos >= (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    # 캐릭터 위치 수정
    character_rect = character.get_rect()
    character_rect.left = character_x_pos

    # 4. 충돌 처리

    # 5. 화면에 그리기
    
    screen.blit(background, (0,0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))


    pygame.display.update()             # 게임 화면을 다시 그리기 (계속 그려야 함)

#시간이 초과되어 종료 되는 경우 2초 지연 후 종료
if delay_timeout:
    pygame.time.delay(2*1000) # 종료 하기 전 2초 정도 대기

pygame.quit()       #pygame 종료

# pyinstaller -F -w <파이썬 파일명>  -> 실행파일 만들기