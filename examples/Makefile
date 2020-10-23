
all: findZpeak.exe example.exe

%.exe: %.cpp
	g++ -std=c++17 -Wall -ldl `root-config --cflags` `root-config --libs --glibs` $^ -o $@

clean:
	rm *.exe
