# import pygame
import random
# from pygame.locals import *


def collision(player_pos, enemy_pos):
    return not (player_pos[0]+56 < enemy_pos[0] or player_pos[0] > enemy_pos[0]+56 or player_pos[1] > enemy_pos[1]+122 or player_pos[1]+122 < enemy_pos[1])


class Simulate():

    def __init__(self, score=0, alive=True, observations=None, time=0, numSpawns=1, spawnTimer=5.0, enemies=None, reward=0):
        class EnemyOne:
            def __init__(self, pos):
                self.pos = pos
                # self.enemyImg = enemyImg
                # elf.screen = screen
                # super(EnemyOne, self).__init__()
                # self.original_image = self.enemyImg
                # self.image = self.original_image
                # self.rect = self.image.get_rect()
                # self.rect.center = pos

            def move(self):
                list(self.pos)
                self.pos = [self.pos[0], self.pos[1] + 0.5]
                tuple(self.pos)
                # self.rect.center = self.pos

            def draw(self):
                # self.screen.blit(self.enemyImg, self.pos)
                pass
        class Car:
            def __init__(self, pos, y_change, x_change, alive):
                self.pos = pos
                # self.carImg = carImg
                # self.screen = screen
                self.x_change = x_change
                self.y_change = y_change
                self.alive = alive
                # self.original_image = self.carImg
                # self.image = self.original_image
                # self.rect = self.image.get_rect()
                # self.rect.center = pos

            def draw(self):
                if self.alive:
                    # self.screen.blit(self.carImg, self.pos)
                    pass

            def move(self):
                if self.alive:
                    self.pos = (self.pos[0] - self.x_change, self.pos[1] - self.y_change)
                    # self.rect.center = self.pos
        if enemies is None:
            enemies = [EnemyOne((-10000, -10000))]
        if observations is None:
            observations = [100.00, 1000.0, 1000.00, 1000.0, 1000.00]
        self.reward = reward
        self.score = score
        self.alive = alive
        self.observations = observations
        self.time = time
        self.numSpawns = numSpawns
        self.spawnTimer = spawnTimer
        self.enemies = enemies
        self.player = Car((0, 400), 0, 0, self.alive)
        """self.screen_width = 500
        self.screen_height = 500

        # Create the self.screen

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption('Car game')

        # load images

        self.carImg = pygame.image.load("C:\\Users\\ben\\Pictures\\Car_better.png").convert_alpha()
        self.carImg = pygame.transform.scale(self.carImg, (56, 122))

        self.enemyImg = pygame.image.load("C:\\Users\\ben\\Pictures\\enemy_car.png").convert_alpha()
        self.enemyImg = pygame.transform.scale(self.enemyImg, (56, 122))

        pygame.init()"""

    def run(self, input_net, width=500, height=500):
        class EnemyOne:
            def __init__(self, pos, numSpawns):
                self.pos = pos
                # self.enemyImg = enemyImg
                # elf.screen = screen
                # super(EnemyOne, self).__init__()
                # self.original_image = self.enemyImg
                # self.image = self.original_image
                # self.rect = self.image.get_rect()
                # self.rect.center = pos
                self.numSpawns = numSpawns

            def move(self):
                list(self.pos)
                self.pos = [self.pos[0], self.pos[1] + (0.5 + self.numSpawns/1000)]
                tuple(self.pos)
                # self.rect.center = self.pos

            def draw(self):
                # self.screen.blit(self.enemyImg, self.pos)
                pass
        if self.alive:
            """for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.name(event.key))
                    self.alive = False"""

            x_change_outer = 0
            y_change_outer = 0
            spawnPos = [width / 2 + 95, width / 2 - 140, width / 2 - 75, width / 2 + 19]
            if input_net == "a":
                x_change_outer = height / 1250
            if input_net == "d":
                x_change_outer = -(height / 1250)
            if input_net == "w":
                y_change_outer = (height / 1250)
            if input_net == "s":
                y_change_outer = -(height / 1250)

                """if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    elif event.key == K_a:
                        left = True
                    elif event.key == K_d:
                        right = True
                    elif event.key == K_w:
                        forward = True
                    elif event.key == K_s:
                        backward = True
    
                if event.type == KEYUP:
                    if event.key == K_a:
                        left = False
                    elif event.key == K_d:
                        right = False
                    elif event.key == K_w:
                        forward = False
                    elif event.key == K_s:
                        backward = False"""
            self.player.pos = list(self.player.pos)
            if self.player.pos[1] < 0:
                y_change_outer = 0
                self.player.pos[1] = 0
            elif self.player.pos[1] + 122 > height:
                y_change_outer = 0
                self.player.pos[1] = height - 122
            if self.player.pos[0] < width / 2 - 150:
                x_change_outer = 0
                self.player.pos[0] = width / 2 - 150
            elif self.player.pos[0] + 56 > (width / 2) + 150:
                x_change_outer = 0
                self.player.pos[0] = width / 2 + 94
            tuple(self.player.pos)
            for enemy in self.enemies:
                collide = collision(self.player.pos, enemy.pos)
                if collide:
                    self.alive = False
            self.player.x_change = x_change_outer
            self.player.y_change = y_change_outer
            # self.screen.fill((000, 000, 000))
            # pygame.draw.rect(self.screen, (175, 167, 169), pygame.Rect(width / 2 - 150, 0, 300, height))
            if self.spawnTimer >= 5.0:
                spawnPosOne = random.choice(spawnPos)
                self.enemies.append(EnemyOne((spawnPosOne, 0), self.numSpawns))
                spawnPos.remove(spawnPosOne)
                self.spawnTimer = 0.0
                self.numSpawns += 1
                if self.numSpawns > 5 and random.choice((True, False)):
                    spawnPosTwo = random.choice(spawnPos)
                    spawnPos.remove(spawnPosTwo)
                    self.enemies.append(EnemyOne((spawnPosTwo, 0), self.numSpawns))
                    """if self.numSpawns > 40 and random.choice((True, False)):
                        spawnPosThree = random.choice(spawnPos)
                        spawnPos.remove(spawnPosThree)
                        self.enemies.append(EnemyOne((spawnPosThree, 0), self.numSpawns))"""
            self.observations = []
            self.observations.append(self.player.pos[0])
            saved_y = 500
            saved_x = 500
            closest = ""
            for enemy in self.enemies:
                if not enemy.pos[1] > 500:
                    y_distance = self.player.pos[1] - enemy.pos[1]
                    x_distance = self.player.pos[0] - enemy.pos[0]
                    if abs(x_distance) < abs(saved_x):
                        saved_x = x_distance
                        if y_distance < saved_y:
                            saved_y = y_distance
                            closest = enemy
            self.observations.append(saved_x)
            self.observations.append(saved_y)
            if abs(saved_x) > 75.0:
                saved_x = 75.0
            elif 60 < abs(saved_x) < 75.0:
                saved_x = 100.0
            self.reward = abs(saved_x)/10000
            saved_y = 500
            saved_x = 500
            second_closest = ""
            for enemy in self.enemies:
                if not enemy.pos[1] > 500 and not enemy == closest:
                    y_distance = self.player.pos[1] - enemy.pos[1]
                    x_distance = self.player.pos[0] - enemy.pos[0]
                    if abs(x_distance) < abs(saved_x):
                        saved_x = x_distance
                        if y_distance < saved_y:
                            saved_y = y_distance
                            second_closest = enemy
            if second_closest == "":
                self.observations.append(10000.00)
                self.observations.append(10000.00)
            else:
                self.observations.append(saved_x)
                self.observations.append(saved_y)
                self.reward += abs(saved_x)/10000

            for enemy in self.enemies:
                enemy.move()
                enemy.draw()

            self.player.move()
            self.player.draw()
            if self.alive:
                self.score += 0.001
            # pygame.display.update()
            self.time += 0.001
            self.spawnTimer += (0.5 + self.numSpawns/1000)/100
