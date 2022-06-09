from typing import Callable

import tensorflow as tf
from tensorflow_tts.inference import AutoProcessor, TFAutoModel


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


def text_to_speech(text, processor, model, mb_melgan, language="ko"):
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

    return audio
