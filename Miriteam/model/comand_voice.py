import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'cmusphinx-ru-5.2'),
    lm=os.path.join(model_path, 'ru.lm'),
    dic=os.path.join(model_path, 'ru1.dic')
)

print("Say something!")

for phrase in speech:
    print(phrase)
