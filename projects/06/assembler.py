import re
import sys

def main():
    #file = open("06/pong/Pong.asm", "r")
    #outFile = open("06/pong/Pong.hack", "w+")
    file = open(sys.argv[1], "r")
    outFile = open(str(sys.argv[1])+"_parsed.hack", "w+")
    lines = file.readlines()
    outLines = []
    #init vars
    lnCnt = 0
    varStartAdr = 16

    #compile steps loop
    for i in range(1,5):
        print("-----------------------RUN: "+ str(i) + " -----------------------\n")
        for idx, line  in enumerate(lines):
            #if re.
            #ignore whitespaces and comments
            if i is 1:
                line = clearTrash(line)
                if line:
                    outLines.append(line)

            #check for symbols and add into dict
            if i is 2:
                res = re.search("\((.*)\)", line)
                if res:
                    symbolDict[res.group(1)] = lnCnt
                    print("Added LBL " + res.group(1) + " to SymbolDict: " + str(symbolDict[res.group(1)]) )
                else:
                    outLines.append(line)
                    lnCnt = lnCnt + 1
            
            #replace symbols in code
            if i is 3:
                res = re.search("@(\d*)(.*)", line)
                if res:
                    #only replace non digit A-commands
                    if res.group(2):
                        #check for value in dict
                        if res.group(2) in symbolDict.keys():
                            #replace lable
                            print("LBL Line: "+ line, end="")
                            line = re.sub("@(\d*)(.*)", "@"+str(symbolDict[res.group(2)]), line)
                            print("| Replaced: " + line +" | DictVal:"+ str(symbolDict[res.group(2)])) 
                        else:
                            #variable requestes --> allocate in RAM
                            symbolDict[res.group(2)] = varStartAdr
                            varStartAdr = varStartAdr +1 #increment address
                            print("Added VAR " + str(res.group(2)) + " to SymbolDict: " + str(symbolDict[res.group(2)]) )#
                            print("VAR Line: "+ line, end="")
                            line = re.sub("@(\d*)(.*)", "@"+str(symbolDict[res.group(2)]), line)
                            print("| Replaced: " + line ) 
                        lines[idx] = line

            #parse to binary
            if i is 4:
                res = re.search("@(.*)", line)
                # A-Type instruction
                if res:
                    #check if it is as symbol by checking the table
                    #if res.group(1) in symbolDict:
                    #    outLines.append('0'+format(symbolDict[res.group(1)], '015b'))
                    #else:
                        outLines.append('0'+format(int(res.group(1)), '015b'))
                else: #else its C-Type instruction
                    resC = re.search("([AMD]*)=*([01\-\+\&\|\!AMD]+);*([JGTEQLNMP]*)", line)
                    outBinary = "111"
                    #if comp always treu --> always comp needed
                    if resC.group(2):
                        outBinary = outBinary + compDict[resC.group(2)]
                    #if destination given
                    if resC.group(1):
                        outBinary = outBinary + destDict[resC.group(1)]
                    else:
                        outBinary = outBinary + "000"

                    #if  jump
                    if resC.group(3):
                        outBinary = outBinary + jumpDict[resC.group(3)]
                    else:
                        outBinary = outBinary + "000"
                    outLines.append(outBinary)

        # replace the old lines with new after every compile step
        if outLines:
            lines = outLines[:]
        
        #print(symbolDict)
        #print(lines)
        outLines.clear()
    #print(symbolDict)

    for line in lines:
        outFile.write(line + "\n")

    #DBG
    #symbolFile = open("06/pong/SymbolList.txt", "w+")
    #for symbol in symbolDict:
    #    symbolFile.write(str(symbol) + " = " + str(symbolDict[symbol]) + "\n")

            
#hack symbols
symbolDict = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,   
    "R6": 6,
    "R7": 7,  
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
}

compDict = {
    #a=0 half
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    #a=1 half
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

destDict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jumpDict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def clearTrash(line):
    line = re.sub('\/\/.*','', line)
    line = re.sub('\n','', line)
    line = re.sub(' ','', line)
    return line

def checkSymbols(line):
    return re.search("\(.*\)", line)

if __name__ == "__main__":
    main()
    pass

