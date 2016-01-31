import sys
import struct

fr = open(sys.argv[1], "rb")
f = open('utf8encoder_out.txt', 'w+')

try:
    byte = fr.read(2)
    while byte != "":
        print "1"
        intstr = struct.unpack('bb', byte)
        if(intstr[0]== 0 and intstr[1]>=int("00",16) and intstr[1]<=int("7F",16)):
            binstr=""
            for i in xrange(7):
                binstr += str((intstr[1] >> i) & 1)
            binstr = binstr[::-1]
            output = int("0"+binstr, 2) 
            newFileBytes =[output]
            newFileByteArray = bytearray(newFileBytes)
            f.write(newFileByteArray)
            print 'first range'
        elif(intstr[0]>=int("00",16) and intstr[0]<= int("07",16)):
            binstr = ""
            for i in xrange(8):
                binstr += str((intstr[1] >> i) & 1)
            binstr = binstr[::-1]
            print binstr
            binstr2 = ""
            for i in xrange(3):
                binstr2 += str((intstr[0] >> i) & 1)
            binstr2 = binstr2[::-1]
            binstr2=binstr2+binstr
            print bin
            output1 = int("110"+binstr2[:5], 2)
            output2 = int("10"+binstr2[5:], 2)
            newFileBytes =[output1, output2]
            newFileByteArray = bytearray(newFileBytes)
            f.write(newFileByteArray);
            print 'second range'
        else:
            binstr = ""
            for i in xrange(8):
                binstr += str((intstr[1] >> i) & 1)
            binstr = binstr[::-1]
           
            binstr2 = ""
            for i in xrange(8):
                binstr2 += str((intstr[0] >> i) & 1)
            binstr2 = binstr2[::-1]
            binstr2=binstr2+binstr
           
            output1 = int("1110"+binstr2[:4],2)
            output2 = int("10"+binstr2[4:10],2)
            output3 = int("10" + binstr2[10:], 2)
            newFileBytes =[output1, output2, output3]
            newFileByteArray = bytearray(newFileBytes)
            f.write(newFileByteArray);

        byte = fr.read(2)   
finally:
    fr.close()