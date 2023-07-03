#!/bin/sh
echo "Launching commands into pod-dev"
until nc -z pod-front 8080; do echo waiting for pod-front; sleep 10; done;
# Serveur d'encodage
celery -A pod.video_encode_transcript.transcripting_tasks worker -l INFO -Q transcripting
sleep infinity
