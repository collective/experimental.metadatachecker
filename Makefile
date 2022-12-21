.PHONY: all
all: .installed.cfg

py3/bin/pip3:
	python3.8 -m venv py3


py3/bin/buildout: py3/bin/pip3 requirements.txt
	./py3/bin/pip3 uninstall -qy setuptools
	./py3/bin/pip3 install -IUr requirements.txt

buildout_cfgs := $(wildcard *.cfg config/*.cfg profiles/*.cfg)
.installed.cfg: py3/bin/buildout $(buildout_cfgs)
	./py3/bin/buildout

.PHONY: test
test: all
	./bin/test

.PHONY: clean
clean:
	rm -rf ./py3
