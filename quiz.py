import pygame

from random import *

pygame.init()       #초기화 (반드시 필요)

# 화면크기 설정

screen_width = 1500
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀
pygame.display.set_caption("나도 old game")

#fps
clock = pygame.time.Clock()

#배경 이미지 불러오기
background = pygame.image.load("/Users/choiair/Documents/100_Develop/game001/background.png")

#캐릭터 불러오기
character = pygame.image.load("/Users/choiair/Documents/100_Develop/game001/character.png")

character_size = character.get_rect().size  # 이미지의 크기를 구해 옴
character_width =character_size[0]          # 캐릭터의 가로 크기
character_height =character_size[1]         # 캐릭터의 세로 크기
character_x_pos = (screen_width - character_width) /2
character_y_pos = screen_height - character_height 

# 이동 할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.6

# 적 enemy 캐릭터
enemy = pygame.image.load("/Users/choiair/Documents/100_Develop/game001/enemy.png")        
enemy_size = enemy.get_rect().size  # 이미지의 크기를 구해 옴
enemy_width =enemy_size[0]          # 캐릭터의 가로 크기
enemy_height =enemy_size[1]         # 캐릭터의 세로 크기
# enemy_x_pos = (screen_width - enemy_width) / 2
# enemy_y_pos = (screen_height - enemy_height) / 2
enemy_x_pos = randint(5, screen_width-enemy_width-5)
enemy_y_pos = -enemy_height
enemy_speed = 10


# 폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체를 생성 (폰트, 크기)

# 총 게임시간
total_time = 10

# 시작시간 정보
start_ticks = pygame.time.get_ticks()  # 시작 tick 정보를 받아옴

# 이벤트 루프
running = True              # 게임이 진행중인가?

# 시간 초가로 종료하는 경우 딜레이 
delay_timeout = False

while running:
    dt = clock.tick(30)             #게임 화면의 초당 프레임 수를 설정

# 키보드 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # pass
                to_x -= character_speed
            if event.key == pygame.K_RIGHT:
                # pass
                to_x += character_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

# 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt        # 프레임 속도에 따라 속도를 유지하기 위해 dt를 곱해준다.
    character_y_pos += to_y * dt

    
    # 캐릭터가 화면 밖으로 나가지 않도록 경계값 처리
    if character_x_pos <= 0: 
        character_x_pos = 0
    if character_x_pos >= (screen_width - character_width): 
        character_x_pos = screen_width - character_width

    # Enemy 위치 변경
    if enemy_y_pos >= (screen_height - enemy_height):
        enemy_x_pos = randint(5, screen_width-enemy_width-5)
        enemy_y_pos = -enemy_height
    else:
        enemy_y_pos += enemy_speed

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌 했어요")
        running = False

    screen.blit(background, (0, 0))     # 배경 이미지를 (0,0) 위치에 넣는다. 
    # screen.fill(255,0,0)

    screen.blit(character, (character_x_pos, character_y_pos))

    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

# 타이머 집어 넣기
# 경과 시간 계산 
    # elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간을 1000으로 나누어서 초단위로 변경

# game_font.render 를 통해서 출력할 글자를 만들어 준다.
    # if int(total_time - elapsed_time)  == 0:
    #     time_text = game_font.render("GAME OVER", True, (255, 255, 255))
    #     running = False
    #     delay_timeout = True
# elif int(total_time - elapsed_time)  < 0:
    #     running = False
    #     dalay_timeout = True
    # else:
    #     time_text = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    
    # screen.blit(time_text, (10, 10))

    pygame.display.update()             # 게임 화면을 다시 그리기 (계속 그려야 함)

#시간이 초과되어 종료 되는 경우 2초 지연 후 종료
# if delay_timeout:
#     pygame.time.delay(2*1000) # 종료 하기 전 2초 정도 대기

pygame.quit()       #pygame 종료

# pyinstaller -F -w <파이썬 파일명>  -> 실행파일 만들기