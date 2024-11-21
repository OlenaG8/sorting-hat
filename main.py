import base64
import io
import wave

import pyaudio
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

def main():
    load_dotenv(find_dotenv())

    client = OpenAI()
    pya = pyaudio.PyAudio()

    print("recording...")
    wav_data = record_input(pya)
    print("finished recording")

    print("sending to chatgpt...")
    completion = send_to_ai(client, wav_data)

    print("playing response...")
    play_output(pya, completion)

    pya.terminate()

def record_input(pya):
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

    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        frames.append(input_stream.read(chunk))

    input_stream.stop_stream()
    input_stream.close()

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as file:
        file.setnchannels(channels)
        file.setsampwidth(pya.get_sample_size(format))
        file.setframerate(rate)
        file.writeframes(b''.join(frames))

    return wav_buffer.getvalue()

def send_to_ai(client, wav_data):
    return client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "onyx", "format": "pcm16"},
        messages=[
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

def play_output(pya, completion):
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