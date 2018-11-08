default:
	git pull | echo
	killall -9 gunicorn | echo
	gunicorn --bind 0.0.0.0:80 --workers 3 --daemon app:app

.PHONY: default
