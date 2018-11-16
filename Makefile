default:
	git pull | echo
	killall -9 gunicorn | echo
	gunicorn --bind 0.0.0.0:80 --workers 3 --daemon app:app

ssh:
        @ssh root@207.148.17.93

.PHONY: default
