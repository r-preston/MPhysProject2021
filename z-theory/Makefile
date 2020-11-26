PYTHIA:=/home/epp/phuswg/pythia8302
ROOT_COMP:=`root-config --cflags` `root-config --libs --glibs`
PYTHIA_COMP:=-I$(PYTHIA)/include -L$(PYTHIA)/lib -Wl,-rpath,$(PYTHIA)/lib -lpythia8

all: analyse

%.exe: %.cpp
	g++ $^ -o $@ $(PYTHIA_COMP) $(ROOT_COMP) -O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC  -ldl

zmuons.root: generate_z_events.exe
	./generate_z_events.exe

analyse: zmuons.root crosssections.py
	python crosssections.py