import librosa
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

model_name = "openai/whisper-large-v3-turbo"
model = WhisperForConditionalGeneration.from_pretrained(model_name)
processor = WhisperProcessor.from_pretrained(model_name)


def voice2text_function(file_path):
    model_name = "openai/whisper-large-v3-turbo"
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    processor = WhisperProcessor.from_pretrained(model_name)

    def load_audio(file_path):
        audio, sample_rate = librosa.load(file_path, sr=16000)
        return audio, sample_rate

    def preprocess_audio(audio, sample_rate):
        inputs = processor(
            audio, sampling_rate=sample_rate, return_tensors="pt"
        )
        return inputs

    def recognize_speech(file_path, segment_length=30):
        audio, sample_rate = load_audio(file_path)
        duration = librosa.get_duration(y=audio, sr=sample_rate)
        transcriptions = []

        for start in range(0, int(duration), segment_length):
            end = min(start + segment_length, int(duration))
            segment = audio[
                int(start * sample_rate) : int(end * sample_rate)  # noqa
            ]  # noqa
            inputs = preprocess_audio(segment, sample_rate)

            with torch.no_grad():
                generated_ids = model.generate(inputs["input_features"])

            transcription = processor.batch_decode(
                generated_ids, skip_special_tokens=True
            )
            transcriptions.append(transcription[0])

        return " ".join(transcriptions)

    transcription = recognize_speech(file_path)
    return transcription
