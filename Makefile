.PHONY: all install dist clean
all: install dist

install:
	pip3 install -e .
reinstall:
	- yes | pip3 uninstall pyapa
	pip3 install -e .
dist:
	python setup.py sdist
	python setup.py bdist_wheel
clean:
	- rm -r build/ dist/ *.egg-info



