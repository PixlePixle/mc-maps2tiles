#include "map_creator.h"
#include "parser.h"


#include <iostream>

void Map_Creator::generateImage(std::string filePath)
{
    Parser::Compound temp = Parser::parse(filePath);
    Parser::Compound root = temp.at("data").get<Parser::Compound>();
    Parser::ByteArray colors = root.at("colors").get<Parser::ByteArray>();
    std::vector<uint8_t> mapColors;
    for (auto &&i : colors)
    {
        for (int j = 0; j < allColors[i].size(); j++)
        {
            mapColors.push_back(allColors[i][j]);
        }
        
    }
    std::string newFilepath = filePath.substr(0, filePath.length()-3) + "png";
    stbi_write_png(newFilepath.data(), 128, 128, 4, mapColors.data(), 128*4);
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <file.nbt>\n";
        return 1;
    }
    Map_Creator generator;
    generator.generateImage(argv[1]);
}