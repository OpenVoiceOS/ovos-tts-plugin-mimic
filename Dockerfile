# Mimic 1 served through ovos-tts-server's ElevenLabs-compatible API. A self-contained,
# fully offline image: Mimic 1 is built from source with its bundled US-English voices
# compiled in, so no network or model download is needed at runtime. Any client that
# speaks the ovos-tts-server / ElevenLabs API can hit it, and it can be A/B-tested against
# other ovos-tts-server voices by pointing at a different port.

# --- build stage: compile Mimic 1 from source ---
FROM python:3.11-slim AS mimic-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        git wget unzip ca-certificates make gcc build-essential pkg-config automake libtool \
        libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/MycroftAI/mimic1 /tmp/mimic1 \
    && cd /tmp/mimic1 \
    && ./dependencies.sh --prefix=/usr/local \
    && ./autogen.sh \
    && ./configure --prefix=/usr/local \
    && make \
    && make install

# --- runtime stage ---
FROM python:3.11-slim

# libasound2 is the only shared runtime lib Mimic links against.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libasound2 \
    && rm -rf /var/lib/apt/lists/*

# the compiled mimic binary + its data files (voices are compiled in).
COPY --from=mimic-builder /usr/local/ /usr/local/
RUN ldconfig

WORKDIR /app
COPY . /app

# the plugin + the OVOS TTS server. setuptools<81 keeps ovos-plugin-manager's
# pkg_resources usage working. Mimic emits WAV, so no ffmpeg transcode is needed;
# the ovos-tts-server>=1.13.5a1 alpha floor lets pip resolve the prerelease without --pre.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# Default voice, overridable with the MIMIC_VOICE build arg. "ap" (Alan Pope, en-GB)
# is Mimic's classic default; "slt", "kal", "awb", "rms" (en-US) are also compiled in.
ARG MIMIC_VOICE=ap
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "tts": {\n    "module": "ovos-tts-plugin-mimic",\n    "ovos-tts-plugin-mimic": {\n      "voice": "%s"\n    }\n  }\n}\n' "${MIMIC_VOICE}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config
USER 1000

EXPOSE 9666
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-mimic", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
