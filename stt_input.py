import speech_recognition as sr

def listen_to_voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... (say 'roll the dice')")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("[ERROR] Could not understand audio.")
    except sr.RequestError:
        print("[ERROR] Could not reach STT service.")
    
    return ""
