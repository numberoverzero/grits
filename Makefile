.PHONY: clean publish test

clean:
	rm -rf build dist

test:
	rm -rf tests/output
	grits-build --src tests/sample --dst tests/output

publish:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
