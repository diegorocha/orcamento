test:
	@coverage run --source=cartao,compras,core,orcamento manage.py test
	@coverage html --omit=*/migrations/*,*/wsgi.py,*/tests.py,*/apps.py,*/settings.py -d coverage
