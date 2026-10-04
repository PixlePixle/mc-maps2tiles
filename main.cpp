#include "parser.h"

#include <iostream>
#include <string>
#include <variant>

using namespace Parser;

void printNBT(const NBT& nbt, int indent = 0);

void printIndent(int indent)
{
    for (int i = 0; i < indent; ++i)
        std::cout << "  ";
}

void printList(const List& list, int indent)
{
    std::cout << "[\n";

    for (const NBT& element : list)
    {
        printIndent(indent + 1);
        printNBT(element, indent + 1);
        std::cout << '\n';
    }

    printIndent(indent);
    std::cout << "]";
}

void printCompound(const Compound& compound, int indent)
{
    std::cout << "{\n";

    for (const auto& [key, value] : compound)
    {
        printIndent(indent + 1);
        std::cout << '"' << key << "\": ";

        printNBT(value, indent + 1);
        std::cout << '\n';
    }

    printIndent(indent);
    std::cout << "}";
}

void printNBT(const NBT& nbt, int indent)
{
    std::visit(
        [&](const auto& value)
        {
            using T = std::decay_t<decltype(value)>;

            if constexpr (std::is_same_v<T, Parser::Byte>)
            {
                std::cout << "Byte(" << static_cast<int>(value) << ")";
            }
            else if constexpr (std::is_same_v<T, Short>)
            {
                std::cout << "Short(" << value << ")";
            }
            else if constexpr (std::is_same_v<T, Int>)
            {
                std::cout << "Int(" << value << ")";
            }
            else if constexpr (std::is_same_v<T, Long>)
            {
                std::cout << "Long(" << value << ")";
            }
            else if constexpr (std::is_same_v<T, Float>)
            {
                std::cout << "Float(" << value << ")";
            }
            else if constexpr (std::is_same_v<T, Double>)
            {
                std::cout << "Double(" << value << ")";
            }
            else if constexpr (std::is_same_v<T, String>)
            {
                std::cout << "String(\"" << value << "\")";
            }
            else if constexpr (std::is_same_v<T, List>)
            {
                printList(value, indent);
            }
            else if constexpr (std::is_same_v<T, Compound>)
            {
                printCompound(value, indent);
            }
            else if constexpr (std::is_same_v<T, Parser::ByteArray>)
            {
                std::cout << "ByteArray[";

                for (size_t i = 0; i < value.size(); ++i)
                {
                    if (i > 0)
                        std::cout << ", ";

                    std::cout << static_cast<int>(value[i]);
                }

                std::cout << "]";
            }
            else if constexpr (std::is_same_v<T, Parser::IntArray>)
            {
                std::cout << "IntArray[";

                for (size_t i = 0; i < value.size(); ++i)
                {
                    if (i > 0)
                        std::cout << ", ";

                    std::cout << value[i];
                }

                std::cout << "]";
            }
            else if constexpr (std::is_same_v<T, Parser::LongArray>)
            {
                std::cout << "LongArray[";

                for (size_t i = 0; i < value.size(); ++i)
                {
                    if (i > 0)
                        std::cout << ", ";

                    std::cout << value[i];
                }

                std::cout << "]";
            }
        },
        nbt.data
    );
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <file.nbt>\n";
        return 1;
    }

    try
    {
        Compound root = Parser::parse(argv[1]);

        printCompound(root, 0);
        std::cout << '\n';
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }

    return 0;
}
