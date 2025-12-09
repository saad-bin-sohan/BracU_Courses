#!/bin/bash

yacc -d -y --debug --verbose 2210xxxx.y
echo 'Generated the parser C file as well the header file'
g++ -w -c -o y.o y.tab.c
echo 'Generated the parser object file'
flex 2210xxxx.l
echo 'Generated the scanner C file'
g++ -fpermissive -w -c -o l.o lex.yy.c
# if the above command doesn't work try g++ -fpermissive -w -c -o l.o lex.yy.c
echo 'Generated the scanner object file'
g++ y.o l.o
echo 'All ready, running'
#i am using linux so i have to use ./a.out to run the file. please change it to a.exe if you are using windows
./a.out input.c
./a.exe input.c
echo 'logfile'
cat 2210xxxx.txt
