test:
	@coverage run --source=cartao,compras,core,orcamento manage.py test
	@coverage html --omit=*/migrations/*,*/wsgi.py,*/tests.py,*/apps.py,*/settings.py -d coverage


ecr-login:
	aws ecr get-login-password --region us-east-1  | docker login --username AWS --password-stdin 215758104365.dkr.ecr.us-east-1.amazonaws.com

build:
	docker buildx build -t us.gcr.io/diegor-infra/orcamento:dev .

clean-storage:
	@python clean-storage.py "orcamento" "orcamento-static"

release:
	./release.sh
