"""Unit tests for the Mimic TTS plugin.

These exercise the real `mimic` binary: they instantiate the plugin, locate
the binary, synthesise audio to disk and assert a non-empty WAV plus
well-formed phoneme output. The `mimic` binary must be installed and on PATH
(the CI unit_tests workflow installs it from the mycroft-desktop .deb).
"""
import os
import tempfile
import unittest

from ovos_tts_plugin_mimic import MimicTTSPlugin


class TestMimicTTSPlugin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mimic = MimicTTSPlugin()

    def test_binary_resolved(self):
        # the binary must be discoverable, otherwise get_tts would pass None
        # to a subprocess/path call and crash
        self.assertTrue(self.mimic.mimic_bin, "mimic binary was not resolved")

    def test_has_voice(self):
        # a voice must always be set so get_tts never passes an empty -voice
        self.assertTrue(self.mimic.voice)

    def test_get_tts_writes_wav_and_phonemes(self):
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        os.remove(path)
        try:
            audio, phonemes = self.mimic.get_tts("hello world", path)
            self.assertEqual(audio, path)
            self.assertTrue(os.path.isfile(path), "no wav file was written")
            self.assertGreater(os.path.getsize(path), 0, "wav file is empty")
            # phonemes: list of [phone, duration] pairs with monotonic durations
            self.assertTrue(phonemes, "no phonemes returned")
            for pair in phonemes:
                self.assertEqual(len(pair), 2)
                float(pair[1])  # duration must be parseable as float
        finally:
            if os.path.isfile(path):
                os.remove(path)

    def test_visemes_from_phonemes(self):
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        os.remove(path)
        try:
            _, phonemes = self.mimic.get_tts("hello", path)
            visemes = self.mimic.viseme(phonemes)
            self.assertEqual(len(visemes), len(phonemes))
            for viseme, dur in visemes:
                self.assertIsInstance(dur, float)
        finally:
            if os.path.isfile(path):
                os.remove(path)

    def test_available_languages(self):
        langs = MimicTTSPlugin.available_languages
        self.assertIn("en-gb", langs)
        self.assertIn("en-us", langs)


if __name__ == "__main__":
    unittest.main()
