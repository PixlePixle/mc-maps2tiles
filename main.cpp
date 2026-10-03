#include "parser.h"
#include <iostream>

int main()
{
    std::cout << "Hello World" << std::endl;
    std::string filePath = "./data/map_0.dat";
    Parser::Compound root = Parser::parse(filePath);
    return 0;
}