ROOT_COMP:=`root-config --cflags` `root-config --libs --glibs`
PYTHIA_COMP:=-I$(PYTHIA)/include -L$(PYTHIA)/lib -lpythia8

all: generate_z_events.exe

%.exe: %.cpp
	g++ -std=c++17 -Wall -ldl $(ROOT_COMP) $(PYTHIA_COMP) $^ -o $@
