import pygame
import sys
from time import sleep
from qiskit import QuantumCircuit
from random import choice

# Simulated quantum circuit result for local testing
def noisy_simulator(qc):
    outcomes = ['00', '11']  # Entangled pairs only
    return [{choice(outcomes): 1}]

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Entanglement Game")
FONT = pygame.font.SysFont("Arial", 28)
BIG_FONT = pygame.font.SysFont("Arial", 38)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, rect)

def entanglement_round():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    counts = noisy_simulator(qc)[0]
    outcome = list(counts.keys())[0]
    qubit_b, qubit_a = outcome[0], outcome[1]
    return qubit_a, qubit_b

def run_entanglement_game():
    score = 0
    rounds = 5
    current_round = 1
    waiting_for_input = True
    input_result = None
    qubit_a, qubit_b = entanglement_round()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Quantum Entanglement Game", BIG_FONT, BLACK, screen, WIDTH // 2, 50)

        if current_round <= rounds:
            draw_text(f"Round {current_round} of {rounds}", FONT, BLACK, screen, WIDTH // 2, 120)
            draw_text(f"Qubit A is measured as: {qubit_a}", FONT, BLACK, screen, WIDTH // 2, 170)
            draw_text("Press 0 or 1 to guess Qubit B", FONT, BLACK, screen, WIDTH // 2, 230)

            if input_result is not None:
                if input_result == qubit_b:
                    draw_text("Correct!", FONT, BLACK, screen, WIDTH // 2, 300)
                    score += 1
                else:
                    draw_text(f"Incorrect. Qubit B was {qubit_b}", FONT, BLACK, screen, WIDTH // 2, 300)
                pygame.display.flip()
                sleep(2)
                current_round += 1
                if current_round <= rounds:
                    qubit_a, qubit_b = entanglement_round()
                    input_result = None
                    waiting_for_input = True
        else:
            draw_text(f"Game Over! Final Score: {score}/{rounds}", BIG_FONT, BLACK, screen, WIDTH // 2, HEIGHT // 2)
            draw_text("Press ESC to exit", FONT, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if waiting_for_input and event.key in [pygame.K_0, pygame.K_1]:
                    input_result = '0' if event.key == pygame.K_0 else '1'
                    waiting_for_input = False
                elif current_round > rounds and event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_entanglement_game()
