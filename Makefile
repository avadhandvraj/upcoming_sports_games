.SILENT: 
	clean
	setup
	run
clean:
	rm -rf __pycache__
	rm -rf venv
setup:
	python3 -m venv venv
	pip install -r requirements.txt
text:
	. venv/bin/activate
	python3 text_myself.py
collect: 
	. venv/bin/activate
	python3 basketball_data_collection.py
	python3 football_data_collection.py
	python3 international_soccer_data_collection.py
	python3 league_soccer_data_collection.py
run: 
	make setup
	make text

	
	