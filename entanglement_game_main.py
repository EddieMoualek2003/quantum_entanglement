from qiskit import QuantumCircuit
import time
import threading
import queue
import sys
from time import sleep

from ibm_qc_interface import noisy_simulator
# from wake_word_listener import passive_listen
# from watson_stt import *

# ========== OUTPUT METHODS ==========
def fallback_cli_output(qubit_a, qubit_b):
    print(f"[CLI OUTPUT] Qubit A: {qubit_a}, Qubit B: {qubit_b}")

def display_qubits(qubit_a, qubit_b):
    fallback_cli_output(qubit_a, qubit_b)

# ========== GAME LOGIC ==========
def speak(message):
    print(f"\n {message}")

def get_user_input():
    user_text = input("Please enter your guess for Qubit B (0 or 1): ").strip()
    return '1' if '1' in user_text else '0' if '0' in user_text else None

def entanglement_game():
    score = 0
    rounds = 5
    speak("Welcome to the Quantum Entanglement Time Challenge!")
    time.sleep(1)
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
            speak("Correct! Qubit B matches Qubit A.")
            score += 1
        else:
            speak(f"Incorrect. Qubit B was actually {qubit_b}.")

        display_qubits(qubit_a, qubit_b)

    speak(f"Game over. You scored {score} out of {rounds}. Well done!")

# ========== CLI WORKER ==========
def game_command_worker(command_queue, game_running_flag):
    while True:
        cmd = command_queue.get()
        if cmd == "roll":
            game_running_flag.set()
            entanglement_game()
            game_running_flag.clear()
        elif cmd == "exit":
            print("[INFO] Exiting game.")
            break

# ========== WAKE WORD LISTENER ==========
def simulate_chatbot_loop(command_queue, game_running_flag):
    awaiting_command = True
    print("[INFO] Say 'Hey Watson' to start.")
    while True:
        if game_running_flag.is_set():
            sleep(1)
            continue

        # passive_listen()

        # record_audio("test.wav", duration=5)
        spoken = "play" # input("Enter Command (In place of Watson): ") # transcribe_ibm("test.wav")

        # spoken = active_listen(timeout=5)
        print(f"SPOKEN {spoken}")
        if not spoken:
            continue

        reply = spoken.lower()
        # if "hey watson" in reply:
        #     print("[WAKE] Wake word detected. Say 'play' or 'entanglement' to begin.")
        #     awaiting_command = True
        #     continue

        if not awaiting_command:
            continue

        if any(k in reply for k in ["play", "entanglement", "game"]):
            awaiting_command = False
            command_queue.put("roll")
            print("Successfully Triggered")
            awaiting_command = True
        elif any(k in reply for k in ["exit", "stop", "quit"]):
            command_queue.put("exit")
            break

def entanglement_game_main():
    command_queue = queue.Queue()
    game_flag = threading.Event()

    worker_thread = threading.Thread(target=game_command_worker, args=(command_queue, game_flag))
    worker_thread.start()

    simulate_chatbot_loop(command_queue, game_flag)
    worker_thread.join()

# # ========== MAIN ==========
# if __name__ == "__main__":
#     #print("Hello world")
#    entanglement_game_main()    
entanglement_game_main()