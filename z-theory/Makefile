PYTHIA:=/home/epp/phuswg/pythia8302
ROOT_COMP:=`root-config --cflags` `root-config --libs --glibs`
PYTHIA_COMP:=-I$(PYTHIA)/include -L$(PYTHIA)/lib -Wl,-rpath,$(PYTHIA)/lib -lpythia8

all: generate_z_events.exe

%.exe: %.cpp
	g++ $^ -o $@ $(PYTHIA_COMP) $(ROOT_COMP) -O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC  -ldl

