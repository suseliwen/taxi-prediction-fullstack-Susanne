#!/usr/bin/env bash
# Enkel rutin: bygger och kör din Docker-image (OBS! Kod kopierad rakt från ChatGPT...)

IMAGE_NAME="taxi-lab"
PORT="8501"

echo "🚧 Bygger Docker-image: $IMAGE_NAME ..."
docker build -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
  echo "✅ Build klar, startar container..."
  docker run --rm -p $PORT:$PORT $IMAGE_NAME
else
  echo "❌ Build misslyckades!"
fi