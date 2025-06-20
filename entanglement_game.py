from qiskit import QuantumCircuit
import time
import threading
import queue
import argparse
import sys
from time import sleep

from ibm_qc_interface import noisy_simulator
from llm_interface import query_llm
from wake_word_listener import passive_listen, active_listen

# ========== OUTPUT METHODS ==========
def try_led_output(qubit_a, qubit_b):
    try:
        raise NotImplementedError("Physical LED output not implemented.")
    except Exception as e:
        print(f"[WARNING] LED output unavailable: {e}")
        return False
    return True

def try_hat_emulator(qubit_a, qubit_b):
    try:
        from sense_emu import SenseHat
        hat = SenseHat()
        hat.clear()

        RED = [255, 0, 0]
        GREEN = [0, 255, 0]
        OFF = [0, 0, 0]
        pixels = [OFF[:] for _ in range(64)]

        color_a = GREEN if qubit_a == '1' else RED
        color_b = GREEN if qubit_b == '1' else RED

        for i in [0, 1, 8, 9]:    # Qubit A
            pixels[i] = color_a
        for i in [6, 7, 14, 15]:  # Qubit B
            pixels[i] = color_b

        hat.set_pixels(pixels)
        time.sleep(1.5)
        hat.clear()
        return True
    except Exception as e:
        print(f"[WARNING] Sense HAT emulator failed: {e}")
        return False

def fallback_cli_output(qubit_a, qubit_b):
    print(f"[CLI OUTPUT] Qubit A: {qubit_a}, Qubit B: {qubit_b}")

def display_qubits(qubit_a, qubit_b):
    if try_led_output(qubit_a, qubit_b):
        return
    if try_hat_emulator(qubit_a, qubit_b):
        return
    fallback_cli_output(qubit_a, qubit_b)

# ========== GAME LOGIC ==========
def speak(message):
    print(f"\n {message}")

def get_user_input():
    user_text = input("Please enter your guess for Qubit B (0 or 1): ").strip()
    if '1' in user_text:
        return '1'
    elif '0' in user_text:
        return '0'
    else:
        return None

def entanglement_game_main():
    score = 0
    rounds = 5

    speak("Welcome to the Quantum Entanglement Time Challenge!")
    time.sleep(2)

    for i in range(rounds):
        speak(f"Round {i+1}. Preparing entangled qubits...")

        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        counts = noisy_simulator(qc)[0]
        outcome = list(counts.keys())[0]
        qubit_b, qubit_a = outcome[0], outcome[1]

        display_qubits(qubit_a, '0')
        speak(f"Qubit A is measured as {qubit_a}. Make your prediction for Qubit B (0 or 1).")

        prediction = get_user_input()

        if prediction is None:
            speak(f"No valid input detected. Qubit B was {qubit_b}.")
        elif prediction == qubit_b:
            speak("Correct! As expected from perfect entanglement, Qubit B matches Qubit A.")
            score += 1
        else:
            speak(f"Incorrect. Qubit B was actually {qubit_b}.")

        display_qubits(qubit_a, qubit_b)

    speak(f"Game over. You scored {score} out of {rounds}. Well done!")

# ========== QUEUED EXECUTION ==========
def fallback_worker(command_queue):
    print("[INFO] Running CLI fallback worker. Awaiting commands...")
    while True:
        cmd = command_queue.get()
        if cmd == "roll":
            entanglement_game_main()
        elif cmd == "exit":
            print("Exiting fallback worker.")
            break
        else:
            print(f"[WARNING] Unknown command: {cmd}")

def start_game_thread(command_queue):
    try:
        from dice_game_ui import run_dice_gui_controlled as gui_runner
        gui_runner(command_queue)
    except Exception as e:
        print(f"[INFO] GUI not available or failed: {e}")
        fallback_worker(command_queue)

# ========== WAKE WORD LISTENER ==========
def simulate_chatbot_loop(command_queue):
    while True:
        try:
            passive_listen()
            spoken = active_listen(timeout=5)

            if not spoken:
                print("[INFO] No speech detected.")
                continue

            reply = spoken  # Or query_llm(spoken)
            print("LLM:", reply)

            if any(k in reply.lower() for k in ["roll", "dice", "throw"]):
                command_queue.put("roll")
            elif any(k in reply.lower() for k in ["exit", "stop"]):
                command_queue.put("exit")
                sys.exit()

        except KeyboardInterrupt:
            command_queue.put("exit")
            break

# ========== MAIN ENTRY ==========
if __name__ == "__main__":
    q = queue.Queue()

    game_thread = threading.Thread(target=start_game_thread, args=(q,))
    game_thread.start()

    simulate_chatbot_loop(q)
    game_thread.join()
