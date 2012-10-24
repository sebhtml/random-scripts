#!/usr/bin/env python
# encoding: UTF-8
# Sébastien Boisvert

class IndexedFile:
	def __init__(self,inputFile):
		self.inputFile=inputFile
		self.indexedColumn=0
		self.lines=[]
		stream=open(inputFile)
		self.index={}
		self.columns=[]

		for line in stream:
			if line.strip()=="":
				continue

			columns=line.split()
			key=columns[self.indexedColumn]

			row=len(self.lines)

			if key in self.index:
				print("Error: key "+key+" already in index")

			self.index[key]=row
			self.lines.append(line)
			self.columns.append(columns)
			
		stream.close()

		print("Loaded "+str(len(self.lines))+" from file "+inputFile)

	def getNumberOfLines(self):
		return len(self.lines)

	def getNumberOfColumns(self):
		if self.getNumberOfLines()>0:
			return len(self.columns[0])

		return 0

	def getLineWithNumber(self,lineNumber):
		return self.lines[lineNumber]

	def getLineWithKey(self,key):
		lineNumber=self.searchKey(key)

		if lineNumber>=0:
			return self.getLineWithNumber(lineNumber)

		return None

	def searchKey(self,key):
		if key in self.index:
			return self.index[key]

		return -1

	def getColumnContent(self,lineNumber,columnNumber):
		#print("Getting cell ("+str(lineNumber)+","+str(columnNumber)+") in "+self.inputFile)
		return self.columns[lineNumber][columnNumber]

	def printRow(self,lineNumber):
		print("File: "+self.inputFile)
		print("Row: "+str(lineNumber))
		print("Key: "+self.columns[lineNumber][0])
		print("Content: "+self.lines[lineNumber])

ncbiFile=IndexedFile("NCBI_File")
pttFile=IndexedFile("PTT_File")
readCountFile=IndexedFile("ReadCount_File")

readCountFileEntryNumber=0
numberOfLines=readCountFile.getNumberOfLines()

while readCountFileEntryNumber<numberOfLines:

	ncbiHandle=readCountFile.getColumnContent(readCountFileEntryNumber,0)
	ncbiFileEntryNumber=ncbiFile.searchKey(ncbiHandle)

	if ncbiFileEntryNumber<0:
		print("Handle "+ncbiHandle+" was not found")

	position=ncbiFile.getColumnContent(ncbiFileEntryNumber,1)
	pttFileEntryNumber=pttFile.searchKey(position)

	print("***Result")
	readCountFile.printRow(readCountFileEntryNumber)
	ncbiFile.printRow(ncbiFileEntryNumber)
	pttFile.printRow(pttFileEntryNumber)

	readCountFileEntryNumber+=1
