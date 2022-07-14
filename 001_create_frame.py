import pygame

pygame.init()       #초기화 (반드시 필요)

# 화면크기 설정

screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀

pygame.display.set_caption("나도 old game")

# 이벤트 루프
running = True      # 게임이 진행중인가?

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False





pygame.quit()       #pygame 종료

