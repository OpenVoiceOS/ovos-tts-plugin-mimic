# TODO

## Open issues

- [ ] #21 Dependency Dashboard (Renovate)

## Gaps

- [ ] No standard gh-automations CI: missing `build-tests`, `coverage`, `license-check`, and the shared `release_workflow` / `publish_stable` reusable jobs. Current workflows are hand-rolled (`build_tests.yml`, `unit_tests.yml`, `license_tests.yml`) and reference `TigreGotico/gh-automations@master` instead of `OpenVoiceOS/gh-automations@dev`.
- [ ] No opm-check despite declaring OVOS/OPM plugin entry points (`mycroft.plugin.tts`, `ovos.plugin.g2p`).
- [ ] Only test (`test/unittests/test_something.py`) is integration-style: requires the real `mimic` binary and asserts exact phoneme durations; no mocked/unit coverage.
- [ ] Stale packaging: uses `setup.py` (no `pyproject.toml`); classifiers claim Python 2.7 / 3.0–3.6 support.
- [ ] `distutils.spawn.find_executable` import breaks on Python 3.12+ (distutils removed).
- [ ] Committed build artifact `ovos_tts_plugin_mimic.egg-info/`.
- [ ] `build_tests.yml` has broken YAML indentation in the "Build Source Packages" step (`run:` over-indented).

## Code TODOs

None found.
