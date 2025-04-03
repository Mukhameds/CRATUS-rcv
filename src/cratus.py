"""
CRATUS-rcv Core Module
Author: Mukhameds
Description: This is the core skeleton of the CRATUS decentralized system.
"""
# === Imports ===
import pygame
import sys
import time

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ghost Logic Reflex Demo")

font = pygame.font.SysFont("Arial", 20)

# Цвета
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
RED = (255, 100, 100)
BLACK = (0, 0, 0)

# Блоки
class Block:

    def __init__(self, name, x, y, threshold=0):
        self.name = name
        self.rect = pygame.Rect(x, y, 120, 60)
        self.color = GRAY
        self.activated = False
        self.signals_received = 0
        self.threshold = threshold
        self.targets = []

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        text = font.render(self.name, True, BLACK)
        screen.blit(text, (self.rect.x + 10, self.rect.y + 20))

    def send_signal(self):
        for target in self.targets:
            target.receive_signal()

    def receive_signal(self):
        self.signals_received += 1
        self.color = YELLOW
        if self.threshold == 0 or self.signals_received >= self.threshold:
            self.activate()

    def activate(self):
        if not self.activated:
            self.activated = True
            self.color = RED if self.name == "Muscle" else GREEN
            self.send_signal()

# Создаём блоки
sensor1 = Block("Temperature", 100, 100)
sensor2 = Block("Memory", 100, 200)
sensor3 = Block("Instinct", 100, 300)
muscle = Block("Muscle", 500, 200, threshold=3)

# Соединения
sensor1.targets = [muscle]
sensor2.targets = [muscle]
sensor3.targets = [muscle]

blocks = [sensor1, sensor2, sensor3, muscle]

# Основной цикл
def run_simulation():
    running = True
    triggered = False
    start_time = time.time()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Автоматический запуск сигналов после 1 секунды
        if not triggered and time.time() - start_time > 1:
            sensor1.receive_signal()
            sensor2.receive_signal()
            sensor3.receive_signal()
            triggered = True

        # Рисуем блоки
        for block in blocks:
            block.draw()

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()
    sys.exit()

run_simulation()



