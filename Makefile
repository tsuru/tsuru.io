deps:
	@pip install -r requirements.txt

test: deps
	@python test_app.py
