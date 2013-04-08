deps:
	@pip install -qr requirements.txt

test_deps:
	@pip install -qr test_requirements.txt

test: test_deps
	@nosetests -s --with-coverage --cover-erase --cover-package=app --cover-package=forms --cover-min-percentage=100 --cover-branches
	@flake8 .

run: deps
	@python app.py

extract: deps
	@pybabel extract -F babel.cfg -o messages.pot .

catalog-pt: deps
	@pybabel init -i messages.pot -d translations -l pt
