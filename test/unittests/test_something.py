# write your first unittest!
import unittest

from ovos_tts_plugin_mimic import MimicTTSPlugin


class TestTTS(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mimic = MimicTTSPlugin()

    def test_something(self):
        path = "/tmp/hello_ap.wav"
        audio, phonemes = self.mimic.get_tts("hello world", path)
        self.assertEqual(audio, path)
        self.assertEqual(phonemes,
                         [['pau', '0.137'],
                          ['hh', '0.236'],
                          ['ax', '0.286'],
                          ['l', '0.375'],
                          ['ow', '0.513'],
                          ['w', '0.673'],
                          ['er', '0.760'],
                          ['l', '0.946'],
                          ['d', '1.050'],
                          ['pau', '1.230']])
