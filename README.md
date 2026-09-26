## Description

This plugin connects [Mimic 1](https://github.com/MycroftAI/mimic1) to OpenVoiceOS through
[OVOS Plugin Manager](https://github.com/OpenVoiceOS/ovos-plugin-manager). Mimic 1 is an
offline, festvox-based text-to-speech engine. The plugin calls the local `mimic` binary and
returns the synthesized audio to OVOS.

## Install

```bash
pip install ovos-tts-plugin-mimic
```

The plugin needs the `mimic` binary. [Compile it from source](https://github.com/MycroftAI/mycroft-core/blob/dev/scripts/install-mimic.sh),
or install a prebuilt package from [forslund's repo](https://forslund.github.io/mycroft-desktop-repo/).

## Configuration

If `mimic` is on the system path, set only a voice:

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic",
    "ovos-tts-plugin-mimic": {
      "voice": "ap"
    }
  }
```

### Advanced config

A voice can be a URL, a file path, or one of the voices built into `mimic`. You can find
compatible festvox voices on the [festvox flite voice page](http://www.festvox.org/flite/packed/flite-2.0/voices/).

Set the path to the `mimic` binary if it is not on the system path:

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic",
    "ovos-tts-plugin-mimic": {
      "voice": "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_fem.flitevox",
      "binary": "~/mimic1/mimic"
    }
  }
```

Mycroft premium subscribers get a female voice called `trinity`. This voice is a
precompiled `mimic` binary with the voice built in. The plugin detects this binary and
uses it, but you can also set the path directly. For a subscriber, the voice binary is
usually at `/opt/mycroft/voices/mimic_tn`:

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic",
    "ovos-tts-plugin-mimic": {
      "voice": "trinity",
      "binary": "/opt/mycroft/voices/mimic_tn"
    }
  }
```

## Docker (ovos-tts-server)

A container image runs the plugin as an [`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server)
(ElevenLabs-compatible API). CI builds this image and pushes it to GHCR on every push to
`dev` or `master`. The image compiles Mimic 1 from source with its bundled voices, so the
container runs fully offline:

```bash
docker run -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-mimic:latest
curl "http://localhost:9666/synthesize/hello%20world?lang=en-US" --output hello.wav
```

The `MIMIC_VOICE` build arg sets the voice baked into the image. The default is `ap`
(Alan Pope). The image also includes `slt`, `kal`, `awb`, and `rms` (all en-US). Rebuild
the image to change the voice, for example:

```bash
docker build --build-arg MIMIC_VOICE=slt -t mimic-tts .
```

See the bundled `docker-compose.yml` for a ready-to-run example.

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) — the plugin framework this package extends
- [OpenVoiceOS/ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) — the HTTP server the Docker image runs
- [MycroftAI/mimic1](https://github.com/MycroftAI/mimic1) — the text-to-speech engine this plugin wraps

## License

Apache-2.0
