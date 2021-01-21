
all: plot_MC_comparison.exe plot_W_dist.exe W_background.exe

%.exe: scripts/%.cpp
	g++ -std=c++17 -Wall -ldl `root-config --cflags` `root-config --libs --glibs` $^ -o $@

clean:
	rm *.exe
