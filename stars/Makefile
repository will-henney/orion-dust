
CLOUDY=cloudy.exe
SRC = $(wildcard *.in)
OBJ = $(SRC:.in=.out)

all: $(OBJ)

%.out: %.in
	$(CLOUDY) < $< > $@
