.PHONY: clean publish

clean:
	rm -rf build dist

publish:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
