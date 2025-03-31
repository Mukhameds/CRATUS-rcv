# Cratus RCV v0.1 — Симуляция каскадных зон с маяком и копиями
import time
import threading
import random
from collections import deque

# === Параметры системы ===
MAX_COPIES_PER_ZONE = 50
COPIES_PER_CALL = 2
LEVELS = 3

# === Класс копии блока ===
class BlockCopy:
    def __init__(self, block_type, timer):
        self.block_type = block_type
        self.timer = timer  # время до активации
        self.age = 0
        self.active = False

    def tick(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.active = True

    def mutate_type(self, new_type):
        self.block_type = new_type

# === Зона (может быть и красной, и зелёной в зависимости от уровня) ===
class Zone:
    def __init__(self, level):
        self.level = level
        self.copies = deque()
        self.lock = threading.Lock()

    def add_copy(self, block_copy):
        with self.lock:
            if len(self.copies) < MAX_COPIES_PER_ZONE:
                self.copies.append(block_copy)

    def tick_all(self):
        with self.lock:
            for copy in self.copies:
                copy.tick()

    def get_active_copies(self, block_type):
        with self.lock:
            return [c for c in self.copies if c.active and c.block_type == block_type]

    def remove_copy(self, copy):
        with self.lock:
            if copy in self.copies:
                self.copies.remove(copy)

# === Маяк ===
class Beacon:
    def __init__(self):
        self.signal = None
        self.lock = threading.Lock()

    def flash(self, block_type):
        with self.lock:
            self.signal = block_type

    def read(self):
        with self.lock:
            return self.signal

    def reset(self):
        with self.lock:
            self.signal = None

# === Инициализация ===
zones = [Zone(level=i) for i in range(LEVELS)]
beacon = Beacon()

# === Функция цикла смерти в верхнем уровне ===
def death_and_summon():
    while True:
        time.sleep(5)
        beacon.flash("A")  # Блок типа A умер в зелёной зоне
        print("[!] Beacon flash: A")
        time.sleep(1)
        beacon.reset()

# === Основной цикл Cratus ===
def cratus_cycle():
    while True:
        for zone in zones:
            zone.tick_all()

        signal = beacon.read()
        if signal:
            for zone in reversed(zones):  # от глубины к поверхности
                active = zone.get_active_copies(signal)
                if active:
                    selected = random.sample(active, min(COPIES_PER_CALL, len(active)))
                    for copy in selected:
                        print(f"[+] Copy {copy.block_type} from level {zone.level} responding to beacon")
                        copy.active = False
                        copy.timer = random.randint(5, 15)  # сброс таймера
                        zones[0].add_copy(copy)  # переместили в зелёную зону верхнего уровня
                        zone.remove_copy(copy)
                    break

        time.sleep(1)

# === Инициализация системы ===
def seed_system():
    for i, zone in enumerate(zones):
        for _ in range(random.randint(20, MAX_COPIES_PER_ZONE)):
            delay = random.randint(3, 30 * (i + 1))
            block = BlockCopy(block_type="A", timer=delay)
            zone.add_copy(block)

seed_system()

# === Запуск ===
threading.Thread(target=death_and_summon, daemon=True).start()
cratus_cycle()
