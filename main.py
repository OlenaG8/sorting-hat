import base64

import pyaudio
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

client = OpenAI()

with open('sup.wav', mode='rb') as file:
    wav_data = file.read()

# encoded_string = base64.b64encode(wav_data).decode('utf-8')

completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "echo", "format": "pcm16"},
    messages=[
        {
            "role": "user",
            "content": "Panie kierowniku, da pan piątaka",
            # "content": [
            #     {
            #         "type": "input_audio",
            #         "input_audio": {
            #             "data": encoded_string,
            #             "format": "wav"
            #         }
            #     }
            # ]
        }
    ],
    stream=True,
)

# wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
# with open("sup.wav", "wb") as f:
#     f.write(wav_bytes)

pya = pyaudio.PyAudio()
stream = pya.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=24000,
    output=True,
)

for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, 'audio'):
        audio = delta.audio
        if 'transcript' in audio:
            print(audio['transcript'], end='')
        if 'data' in audio:
            raw = base64.b64decode(audio['data'])
            stream.write(raw)

stream.stop_stream()
stream.close()
pya.terminate()