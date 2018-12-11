
wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	find pullenti -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info