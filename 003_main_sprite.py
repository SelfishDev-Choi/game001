import pygame

pygame.init()       #초기화 (반드시 필요)

# 화면크기 설정

screen_width = 1500
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀
pygame.display.set_caption("나도 old game")

#배경 이미지 불러오기
background = pygame.image.load("/Users/choiair/Documents/100_Develop/game001/background.png")

#캐릭터 불러오기
character = pygame.image.load("/Users/choiair/Documents/100_Develop/game001/character.png")

character_size = character.get_rect().size  # 이미지의 크기를 구해 옴
character_width =character_size[0]          # 캐릭터의 가로 크기
character_height =character_size[1]         # 캐릭터의 세로 크기
character_x_pos = (screen_width - character_width) /2
character_y_pos = screen_height - character_height - 10

# 이벤트 루프
running = True      # 게임이 진행중인가?

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))     # 배경 이미지를 (0,0) 위치에 넣는다. 

    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update()             # 게임 화면을 다시 그리기 (계속 그려야 함)





pygame.quit()       #pygame 종료

