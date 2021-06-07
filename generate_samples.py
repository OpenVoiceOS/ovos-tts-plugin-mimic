from ovos_tts_plugin_mimic import MimicTTSPlugin

mimic = MimicTTSPlugin(
    config={
        "voice": "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_fem.flitevox",
        "binary": "/opt/mycroft/voices/mimic_tn"})
print(mimic.get_builtin_voices())
mimic.get_tts("hello world", wav_file="hello_world.wav")
