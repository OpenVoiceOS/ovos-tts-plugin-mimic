# ovos-tts-plugin-mimic

OVOS TTS plugin wrapping the [Mimic 1](https://github.com/MycroftAI/mimic1) flite-based CLI synthesizer. Also ships a G2P (grapheme-to-phoneme / viseme) plugin driven by the same binary.

## Setup

```bash
pip install .
```

Requires the `mimic` binary on `PATH` (or a configured `binary` path). Install it by compiling mimic1 or via forslund's apt repo. Only runtime Python dep is `ovos-plugin-manager`.

## Test

```bash
pip install pytest pytest-cov
pytest test/unittests
```

License audit (uses `lichecker`):

```bash
pytest test/license_tests.py
```

Note: `test/unittests/test_something.py` calls the real `mimic` binary and asserts exact phoneme/duration output for the `ap` voice. It is an integration test, not a unit test, and fails if `mimic` is absent or produces different durations.

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_mimic/__init__.py` — all logic:
  - `MimicTTSPlugin(TTS)` — synth via `mimic -voice <v> -psdur -ssml`; SSML rate mapping in `modify_tag`; premium "trinity" binary autodetect in `find_premium_mimic`.
  - `MimicTTSValidator(TTSValidator)` — checks voice is a URL, path, or in `mimic -lv` builtin list.
  - `MimicPhonemesPlugin(Grapheme2PhonemePlugin)` — `get_arpa`, `utterance2visemes`, phoneme parsing.
  - `MimicTTSPluginConfig` — voice catalog (en-gb `ap`; en-us `slt`/`kal`/`awb`/`rms`, plus `trinity` if premium binary found).
- `ovos_tts_plugin_mimic/version.py` — version block (do not edit).
- `ovos_tts_plugin_mimic/locale/en-US/phonetic_spellings.txt` — pronunciation overrides.
- `compile_mimic.sh`, `generate_samples.py` — helper scripts (not packaged).
- `setup.py` — packaging (no pyproject.toml).

Entry-point groups: `mycroft.plugin.tts` -> `MimicTTSPlugin`; `mycroft.plugin.tts.config` -> `MimicTTSPluginConfig`; `ovos.plugin.g2p` -> `MimicPhonemesPlugin`.

## Conventions

- Branches: `dev` (work) / `master` (stable). NEVER `main`.
- Never edit `version.py`; gh-automations bumps semver from conventional-commit prefixes (`feat:` / `fix:` / `feat!:`).
- New repos private by default.
- Commit identity: JarbasAi <jarbasai@mailfence.com>.
- Reference `OpenVoiceOS/gh-automations` reusable workflows at `@dev`.
- No Neon / `neon-*` references.
- No meta-commentary (no history, no dates) in code, docs, commits, or PRs.
- CI is provided by OpenVoiceOS/gh-automations.

## Gotchas

- The only test invokes the real `mimic` binary and asserts exact float durations — brittle and environment-dependent.
- `setup.py` still lists Python 2.7 / 3.0–3.6 classifiers; runtime uses f-strings and 3.7+ syntax.
- `find_executable` from `distutils.spawn` is used; `distutils` is removed in Python 3.12+.
- `MimicTTSPluginConfig` mutates at import time when a premium binary exists, so `available_languages` / the config entry point can differ per host.
- Release/CI workflows are hand-rolled and reference `TigreGotico/gh-automations@master` rather than the standard `OpenVoiceOS/gh-automations@dev` build-tests/coverage/license-check set.
- `ovos_tts_plugin_mimic.egg-info/` is committed.
