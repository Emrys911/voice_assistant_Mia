import speech_recognition
import speech_recognition as sr

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите что-нибудь:")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-ENG")
            print("Вы сказали: " + text)
            return text
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи; {e}")

    return None
