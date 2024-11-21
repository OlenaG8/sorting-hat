import base64
import io
import wave

import pyaudio
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from pyaudio import PyAudio


def main():
    load_dotenv(find_dotenv())

    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    client = OpenAI()
    pya = pyaudio.PyAudio()

    print("recording...")
    wav_data = record_input(pya)
    print("finished recording")

    print("sending to chatgpt...")
    completion = send_to_ai(client, system_prompt, wav_data)

    print("playing response...")
    play_output(pya, completion)

    pya.terminate()

def send_to_ai(client: OpenAI, system_prompt: str, wav_data: bytes):
    return client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "onyx", "format": "pcm16"},
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt,
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": base64.b64encode(wav_data).decode('utf-8'),
                            "format": "wav"
                        }
                    }
                ]
            }
        ],
        stream=True,
    )

def record_input(pya: PyAudio):
    format = pyaudio.paInt16
    channels = 2
    rate = 24000
    chunk = 1024
    record_seconds = 5

    input_stream = pya.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as f:
        f.setnchannels(channels)
        f.setsampwidth(pya.get_sample_size(format))
        f.setframerate(rate)
        for i in range(0, int(rate / chunk * record_seconds)):
            f.writeframes(input_stream.read(chunk))

    input_stream.stop_stream()
    input_stream.close()

    return wav_buffer.getvalue()

def play_output(pya: PyAudio, completion):
    output_stream = pya.open(
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
                output_stream.write(raw)

    output_stream.stop_stream()
    output_stream.close()

if __name__ == '__main__':
    main()