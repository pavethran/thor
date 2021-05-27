from aiohttp import web
import redis
import socketio
import eventlet
import wave
import base64
CHANNELS = 1
RATE = 44100
SAMPLE_WIDTH = 2


# sio = socketio.AsyncServer(cors_allowed_origins='*')
# app = web.Application()
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# sio.attach(app)
redis_client = redis.Redis()

i = 1
file_iterator = 1

@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
def chat_message(sid, data):
    print("message ", data)

@sio.on('message')
def userAdded(sid, message):
    audio_bytes = message.get('audio')
    sio.emit('rec_message', message)
    print(type(message.get('audio')))
    write_file("./output.wav", audio_bytes)
    # print(message)


@sio.on('audio')
def recive_audio(sid, data):
    print('hello data ....................------------->')
    print(base64.b64decode(data))
    data = base64.b64decode(data)
    write_file("./output.wav", data)
    redis_client.lpush('audio_chunk', data)

def write_file(file_path, data):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLE_WIDTH)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


if __name__ == '__main__':
    # web.run_app(app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
