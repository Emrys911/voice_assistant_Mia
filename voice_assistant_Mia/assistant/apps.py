import sys
import json
import queue
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from django.apps import AppConfig
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from tasks_func import *
import manage

# Initialize a queue to communicate between the callback and main thread
q = queue.Queue()

# Load Vosk model
model = Model('model_small')

# Set default input and output devices
device = sd.default.device = (0, 4)  # sd.default.device = 1, 3    /////input, output [1, 4]
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
#48000

def recognize_speech(vectorizer, clf):
    def callback(indata):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16', channels=1,
                           callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                recognize(text, vectorizer, clf)


def recognize(data, vectorizer, clf):
    trg = manage.TRIGGERS.intersection(data.split())
    if not trg:
        return
    data = data.replace(list(trg)[0], '').strip()
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    func_name = answer.split()[0]
    speaker(answer.replace(func_name, ''))
    exec(func_name + '()')


def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(manage.data_set.keys()))
    clf = LogisticRegression()
    clf.fit(vectors, list(manage.data_set.values()))

    # Start recognizing speech
    recognize_speech(vectorizer, clf)


class AssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'My_assistant_Mia'

    def ready(self):
        from .tasks import start_scheduler
        start_scheduler()


if __name__ == '__main__':
    main()
