# Grapher

Graph redactor for:
1. Finding absolute center in graph or many absolute centers for given lower boundary
2. Finding point with maximal supply in graph or many point with summary maximal supply for given lower boundary

### Development
#### Debian based linux
```shell script
sudo apt install `cat ./requirements/requirements.apt.txt ./requirements/requirements_dev.apt.txt`
pip3 install virtualenv virtualenvwrapper
source `whereis virtualenvwrapper | awk '{print $2}'`
mkvirtualenv grapher -p `which python3`
pip3 install -r requirements/requirements.txt -r requirements/requirements_dev.txt
```

### Packaging
#### Debian based linux
```shell script
./scripts/pyUIconvert.sh
./scripts/translate.sh
./setup.py build
./setup.py bdist_msi
```

#### Windows
TODO