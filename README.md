## Description

OVOS TTS plugin for [Mimic](https://github.com/MycroftAI/mimic1)

## Install

`pip install ovos-tts-plugin-mimic`

you can either [compile](https://github.com/MycroftAI/mycroft-core/blob/dev/scripts/install-mimic.sh) [mimic](https://github.com/MycroftAI/mimic1) or use [forslund's repo](https://forslund.github.io/mycroft-desktop-repo/)

## Configuration

if mimic is available system wide you just need to specify a voice

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic",
    "ovos-tts-plugin-mimic": {
      "voice": "ap",
    }
  }
```


### Advanced config

voices can be urls, file paths, or included voices, you can find compatible festvox voices [here](http://www.festvox.org/flite/packed/flite-2.0/voices/)

You can also specify the mimic binary location

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic",
    "ovos-tts-plugin-mimic": {
      "voice": "http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_fem.flitevox",
      "binary": "~/mimic1/mimic"
    }
  }
        
```

## Docker (ovos-tts-server)

A container image runs the plugin as an
[`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server) (ElevenLabs-compatible
API), built and pushed to GHCR by CI on every push to `dev`/`master`. Mimic 1 is compiled
from source inside the image with its bundled voices, so the container is fully offline:

```bash
docker run -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-mimic:latest
curl "http://localhost:9666/synthesize/hello%20world?lang=en-US" --output hello.wav
```

The served voice is baked in via the `MIMIC_VOICE` build arg (default `ap`, Alan Pope);
`slt`, `kal`, `awb` and `rms` (en-US) are also compiled in. Rebuild to change it, e.g.
`docker build --build-arg MIMIC_VOICE=slt -t mimic-tts .`. See the bundled
`docker-compose.yml`.

Mycroft premium subscribers have access to a female voice called trinity
This voice is actually a pre compiled mimic binary with the voice included

The plugin should automatically detect this binary and use it, but you can 
also specify the binary location directly

If you are a subscriber the voice should have been downloaded to `/opt/mycroft/voices/mimic_tn`

```json
  "tts": {
    "module": "ovos-tts-plugin-mimic",
    "ovos-tts-plugin-mimic": {
      "voice": "trinity",
      "binary": "/opt/mycroft/voices/mimic_tn"
    }
  }
        
```