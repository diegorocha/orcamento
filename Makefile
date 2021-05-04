test:
	@coverage run --source=cartao,compras,core,orcamento manage.py test
	@coverage html --omit=*/migrations/*,*/wsgi.py,*/tests.py,*/apps.py,*/settings.py -d coverage


ecr-login:
	aws ecr get-login-password --region us-east-1  | docker login --username AWS --password-stdin 215758104365.dkr.ecr.us-east-1.amazonaws.com

build:
	docker build -t 215758104365.dkr.ecr.us-east-1.amazonaws.com/orcamento:dev .

release: ecr-login
	./release.sh
