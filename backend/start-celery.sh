/usr/local/bin/wait-for-it.sh localhost:8000 -t 10 --

celery -q -A config worker -E -B --loglevel=ERROR &

until timeout 10s celery -A config inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'
celery -q -A config flower --port=5555 -P eventlet