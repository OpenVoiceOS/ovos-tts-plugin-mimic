"""The plugin must not call helpers their owners have deprecated.

`find_premium_mimic` and the plugin constructors run on every start, so a
DeprecationWarning there is printed on every start, and the helper goes
away with the next major release of its library. The test records every
warning raised from inside this package and fails on the first one.
"""
import unittest
import warnings

import ovos_tts_plugin_mimic
from ovos_tts_plugin_mimic import MimicPhonemesPlugin, MimicTTSPlugin


def _package_deprecations(func):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        func()
    return [w for w in caught
            if issubclass(w.category, DeprecationWarning)
            and w.filename == ovos_tts_plugin_mimic.__file__]


class TestNoDeprecatedHelpers(unittest.TestCase):
    def test_find_premium_mimic_raises_no_deprecation(self):
        found = _package_deprecations(MimicTTSPlugin.find_premium_mimic)
        self.assertEqual([], [str(w.message) for w in found])

    def test_phonemes_plugin_init_raises_no_deprecation(self):
        found = _package_deprecations(lambda: MimicPhonemesPlugin({}))
        self.assertEqual([], [str(w.message) for w in found])
