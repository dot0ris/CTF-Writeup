CXX = g++-9
PROT = -fPIE -fstack-protector-strong -Wl,-z,relro,-z,now #-s
CXXFLAGS = -std=c++11 -Wall -Wextra -O0
DEBUGFLAGS = -g
TARGET = deploy

.PHONY : all deploy

all : $(TARGET)

deploy : terpsichore

debug : terpsichore_debug

terpsichore : main.cc movement.cc util.cc
	$(CXX) -o terpsichore $(CXXFLAGS) $(PROT) main.cc movement.cc util.cc

terpsichore_debug : main.cc movement.cc util.cc
	$(CXX) -o terpsichore_debug $(CXXFLAGS) $(DEBUGFLAGS) main.cc movement.cc util.cc

clean :
	rm -f terpsichore terpsichore_debug
