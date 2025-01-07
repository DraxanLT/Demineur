import pygame
import csv
from game import start_game

pygame.init()

widthscreen = 1920
heightscreen = 1080
screen = pygame.display.set_mode((widthscreen, heightscreen))
colorfill = (136, 162, 193)
screen.fill(colorfill)
font = pygame.font.Font("font/Super Sense.ttf", 100)

# Images
boutton_play = pygame.image.load("image/play.png").convert_alpha()
boutton_score = pygame.image.load("image/score.png").convert_alpha()
boutton_exit = pygame.image.load("image/exit.png").convert_alpha()
boutton_back = pygame.image.load("image/back.png").convert_alpha()
boutton_load = pygame.image.load("image/load.png").convert_alpha()
boutton_playpressed = pygame.image.load("image/playpressed.png").convert_alpha()
boutton_scorepressed = pygame.image.load("image/scorepressed.png").convert_alpha()
boutton_exitpressed = pygame.image.load("image/exitpressed.png").convert_alpha()
boutton_backpressed = pygame.image.load("image/backpressed.png").convert_alpha()
difficulty_pad = pygame.image.load("image/difficultypad.png").convert_alpha()
titleimage = pygame.image.load("image/title.png").convert_alpha()
titleresized = pygame.transform.scale(titleimage, (1000, 150))

# Images positions
play_position = (800, 300)
load_position = (800, 500)
score_position = (800, 700)
back_position = (25, 925)
play_position2 = (1590, 925)
exit_position = (800, 900)

# interactions with the images
rect_play = boutton_play.get_rect(topleft=play_position)
rect_score = boutton_score.get_rect(topleft=score_position)
rect_exit = boutton_exit.get_rect(topleft=exit_position)
rect_back = boutton_back.get_rect(topleft=back_position)
rect_play2 = boutton_play.get_rect(topleft=play_position2)
rect_load = boutton_load.get_rect(topleft=load_position)

class Menu:
    screenw = widthscreen
    screenh = heightscreen
    gcolorfill = colorfill
    gtitle = titleresized

    def __init__(self):
        self.main_menu = True
        self.score_menu = False
        self.load_menu = False
        self.difficulties = {"Easy": (9, 9, 10), "Medium": (16, 16, 40), "Hard": (30, 16, 99)}  # Difficulty levels (w/h/mines)
        self.radio_positions = [(115, 400), (115, 500), (115, 600)]  # Difficulty buttons positions
        self.selected_difficulty = 0
        self.difficulty_name = None

    def display(self, screen):
        ingame = True
        while ingame:
            mouse = pygame.mouse.get_pos()
            screen.fill(colorfill)
            screen.blit(titleresized, (475, 20))

            if self.main_menu:  # Show main menu
                screen.blit(boutton_play, play_position)
                screen.blit(boutton_load, load_position)
                screen.blit(boutton_score, score_position)
                screen.blit(boutton_exit, exit_position)

            elif self.score_menu: # Show score page
                screen.blit(boutton_back, back_position)
                font = pygame.font.Font("font/Super Sense.ttf", 50)
                i = 1
                y = 200
                with open('stats.csv', 'r') as file:
                    reader = csv.reader(file, delimiter=',',quotechar='"')
                    for row in reader:
                        y += 100

                        if not row or all(cell == '' for cell in row):
                            continue
                        screen.blit(font.render(f"{row[0]}", 1, (255, 255, 255)), (100, y))
                        screen.blit(font.render(f"{row[1]}", 1, (255, 255, 255)), (700, y))
                        screen.blit(font.render(f"{row[2]}", 1, (255, 255, 255)), (950, y))
            elif self.load_menu:
                y=200
                fontheader = pygame.font.Font("font/Super Sense.ttf", 40)
                font = pygame.font.Font("font/Super Sense.ttf", 20)
                i = 0


                with open('stats.csv', 'r') as file:
                    reader = csv.reader(file, delimiter=',',quotechar='"')


                    for row in reader:
                        y = y + 100
                        if not row or all(cell == '' for cell in row):
                            continue
                        if i ==0:
                            screen.blit(fontheader.render(f"{row[0]}", 1, (255, 255, 255)), (50, y))
                            screen.blit(fontheader.render(f"{row[1]}", 1, (255, 255, 255)), (290, y))
                            screen.blit(fontheader.render(f"{row[2]}", 1, (255, 255, 255)), (500, y))
                            screen.blit(fontheader.render(f"{row[3]}", 1, (255, 255, 255)), (800, y))
                            i+=1
                        else:
                            screen.blit(font.render(f"{row[0]}", 1, (255, 255, 255)), (50, y))
                            screen.blit(font.render(f"{row[1]}", 1, (255, 255, 255)), (290, y))
                            screen.blit(font.render(f"{row[2]}", 1, (255, 255, 255)), (500, y))
                            screen.blit(font.render(f"{row[3]}", 1, (255, 255, 255)), (800, y))
                screen.blit(boutton_back, back_position)




                screen.blit(boutton_back, back_position)

            else:  # Show start menu
                screen.blit(difficulty_pad, (50, 160))

                for i, (difficulty, pos) in enumerate(zip(self.difficulties.keys(), self.radio_positions)):
                    font = pygame.font.Font("font/Super Sense.ttf", 70)

                    pygame.draw.circle(screen, (255, 255, 255), pos, 15)
                    if i == self.selected_difficulty:
                        pygame.draw.circle(screen, (0, 255, 0), pos, 10)

                    label = font.render(difficulty, True, (255, 255, 255))
                    screen.blit(label, (pos[0] + 30, pos[1] - 30))

                font = pygame.font.Font("font/Super Sense.ttf", 50)
                screen.blit(font.render("Difficulty :", True, (255, 255, 255)), (115, 250))
                w, h, mines = list(self.difficulties.values())[self.selected_difficulty]
                font = pygame.font.Font("font/Super Sense.ttf", 70)
                screen.blit(font.render(f"W = {w}", True, (255, 255, 255)), (600, 250))
                screen.blit(font.render(f"H = {h}", True, (255, 255, 255)), (900, 250))
                screen.blit(font.render(f"Mines = {mines}", True, (255, 255, 255)), (1200, 250))

                screen.blit(boutton_back, back_position)
                screen.blit(boutton_play, play_position2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.main_menu:
                        if rect_play.collidepoint(mouse):
                            self.main_menu = False
                        elif rect_score.collidepoint(mouse):
                            self.main_menu = False
                            self.score_menu = True
                        elif rect_load.collidepoint(mouse):
                            self.main_menu = False
                            self.load_menu = True
                        elif rect_exit.collidepoint(mouse):
                            ingame = False

                    else:
                        if rect_back.collidepoint(mouse):
                            self.main_menu = True
                            self.score_menu = False
                            self.load_menu = False
                        elif rect_play2.collidepoint(mouse):
                            self.difficulty_name = list(self.difficulties.keys())[self.selected_difficulty]
                            w, h, mines = self.difficulties[self.difficulty_name]
                            start_game(w, h, mines, self.difficulty_name)

                        for i, pos in enumerate(self.radio_positions):
                            distance = ((mouse[0] - pos[0]) ** 2 + (mouse[1] - pos[1]) ** 2) ** 0.5
                            if distance <= 15:
                                self.selected_difficulty = i
                                print(f"Difficulty selected: {list(self.difficulties.keys())[i]}")

            pygame.display.flip()
        pygame.quit()


menu = Menu()
menu.display(screen)