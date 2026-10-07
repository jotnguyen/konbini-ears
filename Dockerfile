# Konbini Ears build image: speech-kit (Kokoro TTS + Japanese reading check) plus genanki.
#   docker build -t konbini-ears:local .     (needs speech-kit:local, see README)
FROM speech-kit:local
RUN pip install --no-cache-dir "genanki==0.13.1"
WORKDIR /work
ENTRYPOINT ["python", "-m", "ears"]
