
#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

#include <stdlib.h>
#include <stdint.h>

int main(int count, char ** arguments) {

	if(count != 2) {
		cout << "Error: you must provide a number of bytes" << endl;
		cout << endl;
	}

	int bytesInSlice = 2000000000;

	vector<char*> pointers;

	uint64_t totalBytes = 0;

	istringstream input(arguments[1]);

	input >> totalBytes;

	uint64_t allocatedBytes = 0;

	cout << "Bytes to allocate: " << totalBytes << endl;

	while(allocatedBytes < totalBytes) {

		int bytes = bytesInSlice;

		uint64_t remainingBytes = totalBytes - allocatedBytes;

		if(remainingBytes < (uint64_t) bytes) {
			bytes = remainingBytes;
		}

		char * memory = (char *) malloc(bytes * sizeof(char));

		if(memory == NULL) {
			cout << "Warning, could not allocate memory !" << endl;
			break;
		}

		for(int j = 0 ; j < bytes ; ++j) {
			memory[j] = 42;
		}

		pointers.push_back(memory);

		allocatedBytes += bytes;

		cout << "Bytes allocated so far: " << allocatedBytes << " / ";
		cout << totalBytes << " (" << (0.0+allocatedBytes) / totalBytes * 100.00;
		cout << "%)" << endl;
	}

	for(int i = 0 ; i < (int) pointers.size() ; ++i) {

		free(pointers[i]);
	}

	pointers.clear();

	return 0;
}
