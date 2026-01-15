# #!/bin/bash

# # Generate parser with yacc
# yacc -d -y --debug --verbose 2210xxxx.y
# echo 'Generated the parser C file as well the header file'

# # Compile parser
# g++ -w -c -o y.o y.tab.c
# echo 'Generated the parser object file'

# # Generate scanner with flex
# flex 2210xxxx.l
# echo 'Generated the scanner C file'

# # Compile scanner
# g++ -fpermissive -w -c -o l.o lex.yy.c
# echo 'Generated the scanner object file'

# # Link all together
# g++ y.o l.o -o parser
# echo 'All ready, running'

# # Run the parser
# ./parser input.txt
# echo 'Output written to 2210xxxx_log.txt'

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
./a.exe input.txt