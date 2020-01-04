CC := g++
FLAGS := -std=c++11 -w
bin/main: build/main.o build/log.o build/AgendaUI.o build/AgendaService.o build/Storage.o build/Meeting.o build/Date.o build/User.o
	@mkdir -p bin
	$(CC) $(FLAGS) -I./include build/main.o build/log.o build/AgendaUI.o build/AgendaService.o build/Storage.o build/Meeting.o build/Date.o build/User.o -o $@
build/log.o:src/log.cpp include/log.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/log.cpp
build/AgendaUI.o:src/AgendaUI.cpp include/AgendaUI.hpp include/log.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/AgendaUI.cpp
build/AgendaService.o:src/AgendaService.cpp include/AgendaService.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/AgendaService.cpp
build/Storage.o:src/Storage.cpp include/Storage.hpp 
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/Storage.cpp
build/Meeting.o:src/Meeting.cpp include/Meeting.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/Meeting.cpp
build/Date.o:src/Date.cpp include/Date.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/Date.cpp
build/User.o:src/User.cpp include/User.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/User.cpp
build/main.o:src/main.cpp include/AgendaUI.hpp
	@mkdir -p build
	$(CC) $(FLAGS) -I./include -c -o $@ src/main.cpp
clean:
	@rm -rf build
	@rm -rf bin