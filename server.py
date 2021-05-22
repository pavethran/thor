import socket
import os
import wave
import pyaudio
from traceback import print_exc

from speech_text import convert_byte_to_text

# Socket
HOST = socket.gethostbyname('localhost')
PORT = 5000
print(HOST)

# Audio
CHANNELS = 1
RATE = 44100
FORMAT = pyaudio.paInt16

WAVE_OUTPUT_FILENAME = "output.wav"
frames = []
p = pyaudio.PyAudio()


def write_file(file_path, data):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def convert_file_to_text(file_path):
    with open(file_path, 'rb') as read_file:
        _text = convert_byte_to_text(read_file)
    return _text


def bootstrapping_process():
    try:
        os.removedirs('./audio_chunks')
        os.mkdir('./audio_chunks')
    except FileExistsError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


def establish_connection():
    with socket.socket() as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        conn, address = server_socket.accept()
        print("Connection from " + address[0] + ":" + str(address[1]))
        i = 1
        file_iterator = 1
        bootstrapping_process()
        audio_bytes = b''
        while True:
            try:
                data = conn.recv(2048)
                if i % 100 == 0:
                    file_name = f'./audio_chunks/chunk{file_iterator}.wav'
                    write_file(file_name, audio_bytes)
                    audio_bytes = b''
                    text = convert_file_to_text(file_name)
                    print(text)
                    os.remove(file_name)
                    file_iterator += 1
                audio_bytes += data
                frames.append(data)
                i += 1

            except socket.error as error_message:
                print(print_exc())
                print(error_message)
                break


establish_connection()
