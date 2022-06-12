from typing import Callable

import tensorflow as tf
from playsound import playsound
from tensorflow_tts.inference import AutoProcessor, TFAutoModel


# 음성 합성 모델 불러오기
async def load_voice_model(language: str = "ko") -> None or Callable:
    if language == "ko":
        model_name = "tensorspeech/tts-tacotron2-kss-ko"
        processor_name = "tensorspeech/tts-tacotron2-kss-ko"
        mb_melgan_name = "tensorspeech/tts-mb_melgan-kss-ko"

    elif language == "en":
        model_name = "tensorspeech/tts-fastspeech2-ljspeech-en"
        processor_name = "tensorspeech/tts-fastspeech2-ljspeech-en"
        mb_melgan_name = "tensorspeech/tts-mb_melgan-ljspeech-en"

    elif language == "ch":
        model_name = "tensorspeech/tts-fastspeech2-baker-ch"
        processor_name = "tensorspeech/tts-fastspeech2-baker-ch"
        mb_melgan_name = "tensorspeech/tts-mb_melgan-baker-ch"

    try:
        processor = AutoProcessor.from_pretrained(model_name)
        model = TFAutoModel.from_pretrained(processor_name)
        mb_melgan = TFAutoModel.from_pretrained(mb_melgan_name)
        return processor, model, mb_melgan
    except:
        return None


# 텍스트를 음성으로 변환
def text_to_speech(
    text: str,
    processor: Callable,
    model: Callable,
    mb_melgan: Callable,
    language="ko",
    display_streamlit: bool = True,
):
    """음성 변환 추론
    언어에 따라 모델이 상이하기 때문에 모델 추론 함수를 부를 때 파라미터가 달라짐으로 구분하며 음성 변환 실행

    Args:
        test (str): 음성 변환 할 텍스트
        processor (Callable): 음성 변환 전처리 프로세서 모델
        model (Callable): mel spectrogram 추론 모델
        mb_melgan: mel spectrogram에서 waveform으로 합성 및 변환하는 모델
        language (str): 음성 변환 시 사용할 언어
        display_streamlit (bool): streamlit에서 오디오 파일 재생할 것인지 여부, False일 시 프로그램 작동 기기에서 오디오 재생
    """
    # inference
    if language == "ch":
        input_ids = processor.text_to_sequence(text, inference=True)
    else:
        input_ids = processor.text_to_sequence(text)

    if language == "ko":
        _, mel_outputs, _, _ = model.inference(
            input_ids=tf.expand_dims(
                tf.convert_to_tensor(input_ids, dtype=tf.int32), 0
            ),
            input_lengths=tf.convert_to_tensor([len(input_ids)], tf.int32),
            speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
        )
    elif language == "en" or language == "ch":
        _, mel_outputs, _, _, _ = model.inference(
            input_ids=tf.expand_dims(
                tf.convert_to_tensor(input_ids, dtype=tf.int32), 0
            ),
            speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
            speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        )

    # melgan inference (mel-to-wav)
    audio = mb_melgan.inference(mel_outputs)[0, :, 0]
    if display_streamlit:
        print(type(audio))
        return audio
    else:
        sf.write("temp.wav", audio, 22050, "PCM_16", format="wav")
        playsound("temp.wav")
