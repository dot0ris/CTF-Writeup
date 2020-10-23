all:
	docker build . -t tpu
	docker run --detach --name tpu --publish 1337:1337 --restart always tpu