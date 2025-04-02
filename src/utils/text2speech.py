import os
import time
try:
    from TTS.api import TTS
    tts_available = True
except ImportError:
    tts_available = False
    print("TTS module not found. Text-to-speech functionality will be disabled.")
    print("To enable TTS, install it with: pip install TTS")


class TTSTalker():
    def __init__(self):
        if not tts_available:
            self.model = None
            return
            
        # List available 🐸TTS models
        # print(TTS().list_models())
        """
        | Model Name | Language | Dataset | Vocoder | 
        | 'tts_models/de/thorsten/tacotron2-DDC' | de | thorsten | hifigan_v2 |
        | 'tts_models/de/thorsten/vits' | de | thorsten | None |
        | 'tts_models/en/ljspeech/tacotron2-DDC' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/ljspeech/glow-tts' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/ljspeech/speedy-speech' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/ljspeech/tacotron2-DCA' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/ljspeech/vits' | en | ljspeech | None |
        | 'tts_models/en/ljspeech/vits--neon' | en | ljspeech | None |
        | 'tts_models/en/ljspeech/fast_pitch' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/ljspeech/overflow' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/ljspeech/neural_hmm' | en | ljspeech | hifigan_v2 |
        | 'tts_models/en/vctk/vits' | en | vctk | None |
        | 'tts_models/en/vctk/fast_pitch' | en | vctk | hifigan_v2 |
        | 'tts_models/en/sam/tacotron-DDC' | en | sam | hifigan_v2 |
        | 'tts_models/en/blizzard2013/capacitron-t2-c50' | en | blizzard2013 | hifigan_v2 |
        | 'tts_models/es/mai/tacotron2-DDC' | es | mai | hifigan_v2 |
        | 'tts_models/fr/mai/tacotron2-DDC' | fr | mai | hifigan_v2 |
        | 'tts_models/uk/mai/glow-tts' | uk | mai | hifigan_v2 |
        | 'tts_models/zh-CN/baker/tacotron2-DDC-GST' | zh-CN | baker | hifigan_v2 |
        | 'tts_models/nl/mai/tacotron2-DDC' | nl | mai | hifigan_v2 |
        | 'tts_models/it/mai_female/glow-tts' | it | mai_female | hifigan_v2 |
        | 'tts_models/it/mai_male/glow-tts' | it | mai_male | hifigan_v2 |
        | 'tts_models/it/mai_female/vits' | it | mai_female | None |
        | 'tts_models/it/mai_male/vits' | it | mai_male | None |
        | 'tts_models/ja/kokoro/tacotron2-DDC' | ja | kokoro | hifigan_v2 |
        | 'tts_models/tr/common-voice/glow-tts' | tr | common-voice | hifigan_v2 |
        | 'tts_models/ja/kokoro/glow-tts' | ja | kokoro | hifigan_v2 |
        | 'tts_models/be/common-voice/glow-tts' | be | common-voice | hifigan_v2 |
        | 'tts_models/fa/common-voice/glow-tts' | fa | common-voice | hifigan_v2 |
        | 'tts_models/bg/common-voice/glow-tts' | bg | common-voice | hifigan_v2 |
        | 'tts_models/ka/common-voice/glow-tts' | ka | common-voice | hifigan_v2 |
        | 'tts_models/el/cv/glow-tts' | el | cv | hifigan_v2 |
        | 'tts_models/hr/common-voice/glow-tts' | hr | common-voice | hifigan_v2 |
        | 'tts_models/hu/common-voice/glow-tts' | hu | common-voice | hifigan_v2 |
        | 'tts_models/fi/common-voice/glow-tts' | fi | common-voice | hifigan_v2 |
        | 'tts_models/kk/common-voice/glow-tts' | kk | common-voice | hifigan_v2 |
        | 'tts_models/ru/common-voice/glow-tts' | ru | common-voice | hifigan_v2 |
        | 'tts_models/tt/common-voice/glow-tts' | tt | common-voice | hifigan_v2 |
        | 'tts_models/ca/custom/nar-44100' | ca | custom | hifigan_v2 |
        | 'tts_models/cs/cv/vits' | cs | cv | None |
        | 'vocoder_models/en/ljspeech/multiband-melgan' | None | None | None |
        | 'vocoder_models/en/ljspeech/hifigan_v2' | None | None | None |
        | 'vocoder_models/en/ljspeech/univnet' | None | None | None |
        | 'vocoder_models/en/blizzard2013/hifigan_v2' | None | None | None |
        | 'vocoder_models/en/vctk/hifigan_v2' | None | None | None |
        | 'vocoder_models/en/sam/hifigan_v2' | None | None | None |
        | 'vocoder_models/nl/mai/parallel-wavegan' | None | None | None |
        | 'vocoder_models/de/thorsten/hifigan_v2' | None | None | None |
        | 'vocoder_models/ja/kokoro/hifigan_v2' | None | None | None |
        | 'vocoder_models/uk/mai/multiband-melgan' | None | None | None |
        | 'vocoder_models/tr/common-voice/hifigan_v2' | None | None | None |
        | 'vocoder_models/zh-CN/baker/hifigan_v2' | None | None | None |
        | 'vocoder_models/be/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/fa/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/fa/common-voice/fullband-melgan' | None | None | None |
        | 'vocoder_models/bg/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/ka/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/el/cv/multiband-melgan' | None | None | None |
        | 'vocoder_models/hr/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/hu/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/fi/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/kk/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/ru/common-voice/multiband-melgan' | None | None | None |
        | 'vocoder_models/tt/common-voice/multiband-melgan' | None | None | None |
        | 'voice_conversion_models/multilingual/vctk/freevc24' | None | None | None |
        | 'voice_conversion_models/autovc/ljspeech/autovc' | None | None | None |
        | 'voice_conversion_models/freevc/vctk/freevc' | None | None | None |
        | 'voice_conversion_models/universal/libri_tts/uni_pc' | None | None | None |
        """

        # Init TTS with the target model name
        #self.model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        self.model = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST")
    
    def test(self, text="你好，欢迎使用SadTalker"):
        if not tts_available:
            print("TTS module not available. Cannot generate audio from text.")
            return None
            
        # Running from the directory, the path should be below:
        wav_path =  f'./generated_{str(time.time())}.wav'
        self.model.tts_to_file(text=text, file_path=wav_path)  

        return wav_path
