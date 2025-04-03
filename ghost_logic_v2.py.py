
import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ghost Logic v2 – Stateless Reflex")

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FONT = pygame.font.SysFont("Arial", 16)

class Block:
    def __init__(self, name, x, y, rule, targets=None, self_destruct=False):
        self.name = name
        self.rect = pygame.Rect(x, y, 100, 60)
        self.rule = rule  # function: signal -> bool
        self.targets = targets if targets else []
        self.color = GREY
        self.self_destruct = self_destruct
        self.alive = True  # becomes False if self-destructed

    def receive_signal(self, signal=None):
        if not self.alive:
            return
        if self.rule(signal):
            self.react(signal)

    def react(self, signal):
        self.color = GREEN if self.name != "Muscle" else RED
        new_signal = self.emit_signal(signal)
        for target in self.targets:
            target.receive_signal(new_signal)
        if self.self_destruct:
            self.alive = False

    def emit_signal(self, incoming_signal):
        # Optionally modify signal
        return random.randint(1, 10)

    def draw(self):
        if not self.alive:
            return
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text = FONT.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 10, self.rect.y + 20))


# Define stateless rule functions
def always_true(signal): return True
def greater_than_5(signal): return signal and signal > 5
def even_signal(signal): return signal and signal % 2 == 0

# Create blocks (stateless, ghost logic)
sensor1 = Block("Sensor-Temp", 50, 50, rule=always_true, self_destruct=True)
sensor2 = Block("Sensor-Mem", 50, 150, rule=always_true, self_destruct=True)
sensor3 = Block("Sensor-Inst", 50, 250, rule=always_true, self_destruct=True)

muscle = Block("Muscle", 500, 150, rule=greater_than_5)

# Connect targets
sensor1.targets = [muscle]
sensor2.targets = [muscle]
sensor3.targets = [muscle]

blocks = [sensor1, sensor2, sensor3, muscle]

clock = pygame.time.Clock()
timer = 0
triggered = False

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Trigger once after short delay
    if not triggered and timer > 30:
        sensor1.receive_signal()
        sensor2.receive_signal()
        sensor3.receive_signal()
        triggered = True

    for block in blocks:
        block.draw()

    pygame.display.flip()
    clock.tick(30)
    timer += 1

pygame.quit()
sys.exit()
