default:
  @killall -9 gunicorn
  @gunicorn --bind 0.0.0.0:80 --workers 3 --daemon app:app

.PHONY: default
