import speech_recognition as sr


def convert_byte_to_text(file_obj):
    r = sr.Recognizer()
    with sr.AudioFile(file_obj) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
    return text
