g++ -std=c++0x main.cpp -O3 -pipe -pthread -o main -DORDERED=$1 -DN=$2 && time ./main $*
