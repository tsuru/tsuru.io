deps:
	@pip install -r requirements.txt

test_deps:
	@pip install -r test_requirements.txt

test: test_deps
	@python test_app.py

run: deps
	@python app.py
