.PHONY: all install dist clean
all: install dist

install:
	pip3 install -e .
reinstall:
	- yes | pip3 uninstall pyapa
	pip3 install -e .
dist:
	python3 setup.py sdist
	python3 setup.py bdist_wheel
clean:
	- rm -r build/ dist/ *.egg-info



