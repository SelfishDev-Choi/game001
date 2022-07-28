# 01:03:08 
import pygame
#########################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
from random import *

pygame.init()       #초기화 (반드시 필요)

# 화면크기 설정

screen_width = 1500     # 가로크기
screen_height = 800     # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption("나도 old game")

#fps
clock = pygame.time.Clock()
#########################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도 폰트 등)

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

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기
    
    pygame.display.update()             # 게임 화면을 다시 그리기 (계속 그려야 함)

#시간이 초과되어 종료 되는 경우 2초 지연 후 종료
if delay_timeout:
    pygame.time.delay(2*1000) # 종료 하기 전 2초 정도 대기

pygame.quit()       #pygame 종료

# pyinstaller -F -w <파이썬 파일명>  -> 실행파일 만들기