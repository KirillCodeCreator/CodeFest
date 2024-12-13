import numpy as np
import torch
from pydub import AudioSegment
from transformers import WhisperForConditionalGeneration, WhisperProcessor

# Загрузка модели и процессора
model_name = "openai/whisper-large-v3-turbo"
model = WhisperForConditionalGeneration.from_pretrained(model_name)
processor = WhisperProcessor.from_pretrained(model_name)


# Загрузка аудиофайла с использованием pydub
def load_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = audio.get_array_of_samples()
    audio_np = np.array(samples).astype(np.float32) / 32768.0  # Нормализация
    return audio_np, 16000


# Преобразование аудио в формат, пригодный для модели
def preprocess_audio(audio, sample_rate):
    inputs = processor(audio, sampling_rate=sample_rate, return_tensors="pt")
    return inputs


# Распознавание речи
def recognize_speech(file_path, segment_length=30):
    audio, sample_rate = load_audio(file_path)
    duration = len(audio) / sample_rate
    transcriptions = []

    for start in range(0, int(duration), segment_length):
        end = min(start + segment_length, int(duration))
        segment = audio[int(start * sample_rate) : int(end * sample_rate)]
        inputs = preprocess_audio(segment, sample_rate)

        # Генерация текста
        with torch.no_grad():
            generated_ids = model.generate(inputs["input_features"])

        transcription = processor.batch_decode(
            generated_ids, skip_special_tokens=True
        )
        transcriptions.append(transcription[0])

    return " ".join(transcriptions)


# Пример использования
file_path = "Запись.wav"
transcription = recognize_speech(file_path)
print("Распознанный текст:", transcription)
