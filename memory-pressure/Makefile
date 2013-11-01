all: ApplyPressure

ApplyPressure: ApplyPressure.cpp
	g++ ApplyPressure.cpp -O3 -Wall -std=c++98 -o ApplyPressure

# 132038812 KiB
# irb(main):001:0> 132038812*1024
# => 135207743488
ls28:
	./ApplyPressure 115207743488

clean:
	rm ApplyPressure
