import os
import subprocess
import sys
import wave

import argostranslate
import argostranslate.package
import argostranslate.translate

import vosk

from pydub import AudioSegment


#

from_code = "ru"
to_code = "en"

translatedText = argostranslate.translate.translate("доброго дня, друзья", from_code, to_code)
print(translatedText)


#функция преоброзования видио в аудио
def convert_video_to_audio_ffmpeg(video_file, output_ext="mp3"):
    """Преобразует видео в аудио напрямую с помощью команды `ffmpeg`
    с помощью модуля подпроцесса"""
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

def convert_mp3_to_wav(mp3_file, output_wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(output_wav_file, format="wav")

def audio_to_text(audio_file_path, model_path):
    # Загрузка модели для распознавания речи
    model = vosk.Model(model_path)

    # Создание объекта распознавателя
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Открытие аудиофайла
    wf = wave.open(audio_file_path, 'rb')

    # Чтение данных из аудиофайла по кускам
    while True:
        data = wf.readframes(4000)  # Чтение 4000 фреймов
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            pass

    # Получение результата распознавания
    result = recognizer.FinalResult()

    # Возвращаем текст из распознанной речи
    return result



convert_video_to_audio_ffmpeg(video_file='videos/file_0.mp4')

convert_mp3_to_wav(mp3_file='videos/file_0.mp3', output_wav_file='videos/file_0.waw')

print(audio_to_text(audio_file_path='videos/file_0.waw', model_path='models/vosk-model-ru-0.42')
