ROOT_COMP=`root-config --cflags` `root-config --libs --glibs`
PYTHIA_COMP=-I$(PYTHIA)/include -L$(PYTHIA)/lib

all: findZpeak.exe example.exe

%.exe: %.cpp
	g++ -std=c++17 -Wall -ldl $(ROOT_COMP) $(PYTHIA_COMP) $^ -o $@

clean:
	rm *.exe
