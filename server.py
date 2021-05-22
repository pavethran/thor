import socket
import pyaudio
import wave

# Socket
HOST = socket.gethostname()
PORT = 5000

# Audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
frames = []

with socket.socket() as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("Connection from " + address[0] + ":" + str(address[1]))
    while True:
        try:
            data = conn.recv(2048)
            print(type(data))
            frames.append(data)
        except socket.error as error_message:
            break

print(frames)

with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))