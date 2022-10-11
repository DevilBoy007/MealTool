app: venv/bin/activate
	python3 food_bot.py
venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/pip3 install -r requirements.txt
clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete
