import socket
import pyaudio
import hashlib

# Socket
HOST = socket.gethostbyname('localhost')
PORT = 5000

# Audio
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording")
with socket.socket() as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.setblocking(0)
    while True:
        data = stream.read(CHUNK)
        client_socket.send(data)
        try:
            value = client_socket.recv(1024)
        except socket.error as e:
            h = hashlib.sha256(str(e).encode('utf-8'))
            resource_temp_available_error = '61a62fe839e6cc26eedd3ab2075ed4aedc6580414fa1b7140005c89a2ac5d3f6'
            if resource_temp_available_error == h.hexdigest():
                continue
            print(e)