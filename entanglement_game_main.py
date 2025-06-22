# from qiskit import QuantumCircuit
# from time import sleep
# import threading
# import queue
# import sys

# from ibm_qc_interface import noisy_simulator


# # ========== OUTPUT METHODS ==========
# def fallback_cli_output(qubit_a, qubit_b):
#     print(f"[CLI OUTPUT] Qubit A: {qubit_a}, Qubit B: {qubit_b}")


# def display_qubits(qubit_a, qubit_b):
#     fallback_cli_output(qubit_a, qubit_b)


# # ========== GAME LOGIC ==========
# def speak(message):
#     print(f"\n{message}")


# def get_user_input():
#     try:
#         user_text = input("Please enter your guess for Qubit B (0 or 1): ").strip()
#         return '1' if '1' in user_text else '0' if '0' in user_text else None
#     except EOFError:
#         print("[ERROR] Input failed. This game requires interactive mode.")
#         return None


# def entanglement_game():
#     score = 0
#     rounds = 5
#     speak("Welcome to the Quantum Entanglement Time Challenge!")
#     sleep(1)

#     for i in range(rounds):
#         speak(f"\nRound {i + 1}: Preparing entangled qubits...")

#         qc = QuantumCircuit(2, 2)
#         qc.h(0)
#         qc.cx(0, 1)
#         qc.measure([0, 1], [0, 1])

#         counts = noisy_simulator(qc)[0]
#         outcome = list(counts.keys())[0]
#         qubit_b, qubit_a = outcome[0], outcome[1]

#         display_qubits(qubit_a, '0')
#         speak(f"Qubit A is measured as {qubit_a}. Make your prediction for Qubit B (0 or 1).")
#         prediction = get_user_input()

#         if prediction is None:
#             speak(f"No valid input detected. Qubit B was {qubit_b}.")
#         elif prediction == qubit_b:
#             speak("Correct. Qubit B matches Qubit A.")
#             score += 1
#         else:
#             speak(f"Incorrect. Qubit B was actually {qubit_b}.")

#         display_qubits(qubit_a, qubit_b)

#     speak(f"\nGame over. You scored {score} out of {rounds}.")


# # ========== GAME THREAD WORKER ==========
# def game_command_worker(command_queue, game_flag):
#     while True:
#         cmd = command_queue.get()
#         if cmd == "roll":
#             game_flag.set()
#             entanglement_game()
#             game_flag.clear()
#         elif cmd == "exit":
#             print("[INFO] Exiting game.")
#             break


# # ========== CONSOLE LOOP ==========
# def simulate_cli_loop(command_queue, game_flag):
#     print("\n[Quantum Entanglement Game CLI]")
#     print("Type 'roll' to play or 'exit' to quit.\n")
#     while True:
#         if game_flag.is_set():
#             sleep(1)
#             continue

#         try:
#             cmd = input(">> ").strip().lower()
#         except EOFError:
#             print("[ERROR] EOF received. Exiting.")
#             break

#         if cmd in ["play", "roll", "start"]:
#             command_queue.put("roll")
#         elif cmd in ["exit", "quit", "q"]:
#             command_queue.put("exit")
#             break


# # ========== MAIN ==========
# def entanglement_game_main():
#     command_queue = queue.Queue()
#     game_flag = threading.Event()

#     worker_thread = threading.Thread(target=game_command_worker, args=(command_queue, game_flag))
#     worker_thread.start()

#     simulate_cli_loop(command_queue, game_flag)
#     worker_thread.join()


# if __name__ == "__main__":
#     entanglement_game_main()

name = input("What is your name: ")
print(f"Hello {name}")