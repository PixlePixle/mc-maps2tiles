#include "parser.h"

#include <fstream>
#include <cstring>

namespace Parser {

    Compound parse(std::string filePath)
    {
        std::ifstream fileStream(filePath , std::ios_base::binary);
        Compound ret = parseCompound(fileStream);
        return ret;
    }

    Byte parseByte(std::ifstream& fileStream)
    {
        uint8_t ret = fileStream.get();
        return static_cast<Byte>(ret);
    }

    Short parseShort(std::ifstream& fileStream)
    {
        uint16_t ret = fileStream.get();
        ret = ret << 8 | fileStream.get();
        return static_cast<Short>(ret);
    }

    Int parseInt(std::ifstream& fileStream)
    {
        uint32_t ret = fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        return static_cast<Int>(ret);
    }

    Long parseLong(std::ifstream& fileStream)
    {
        uint64_t ret = fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        ret = ret << 8 | fileStream.get();
        return static_cast<Long>(ret);
    }

    Float parseFloat(std::ifstream& fileStream)
    {
        uint32_t bits = parseInt(fileStream);
        Float ret;
        std::memcpy(&ret, &bits, sizeof(ret));
        return ret;
    }

    Double parseDouble(std::ifstream& fileStream)
    {
        uint64_t bits = parseLong(fileStream);
        double ret;
        std::memcpy(&ret, &bits, sizeof(ret));
        return ret;
    }

    String parseString(std::ifstream& fileStream)
    {
        uint16_t length = static_cast<uint16_t>(parseShort(fileStream));
        String ret(length, '\0');
        fileStream.read(ret.data(), length);
        return ret;
    }

    List parseList(std::ifstream& fileStream)
    {
        List ret;
        uint8_t tag = static_cast<uint8_t>(fileStream.get());
        if ( tag < 0 || ID::ID_LAST <= tag )
        {
            exit(EXIT_FAILURE);
        }
        Int length = parseInt(fileStream);
        for (Int i = 0; i < length; i++)
        {
            switch (tag)
            {
                case ID::BYTE:
                    ret.push_back(parseByte(fileStream));
                    break;
                case ID::SHORT:
                    ret.push_back(parseShort(fileStream));
                    break;
                case ID::INT:
                    ret.push_back(parseInt(fileStream));
                    break;
                case ID::LONG:
                    ret.push_back(parseLong(fileStream));
                    break;
                case ID::FLOAT:
                    ret.push_back(parseFloat(fileStream));
                    break;
                case ID::DOUBLE:
                    ret.push_back(parseDouble(fileStream));
                    break;
                case ID::STRING:
                    ret.push_back(parseString(fileStream));
                    break;
                case ID::LIST:
                    ret.push_back(parseList(fileStream));
                    break;
                case ID::COMPOUND:
                    ret.push_back(parseCompound(fileStream));
                    break;
                case ID::BYTE_ARRAY:
                    ret.push_back(parseByteArray(fileStream));
                    break;
                case ID::INT_ARRAY:
                    ret.push_back(parseIntArray(fileStream));
                    break;
                case ID::LONG_ARRAY:
                    ret.push_back(parseLongArray(fileStream));
                    break;
            }
        }
        return ret;
    }

    Compound parseCompound(std::ifstream& fileStream)
    {
        Compound ret;
        while ( true )
        {
            // Reads the tag id
            uint8_t tag = static_cast<uint8_t>(fileStream.get());
            if ( tag < 0 || ID::ID_LAST <= tag )
            {
                exit(EXIT_FAILURE);
            } else if ( tag == ID::END ) return ret; // Retuns if END is read
            String key = parseString(fileStream);
            
            switch (tag)
            {
                case ID::BYTE:
                    ret[key] = parseByte(fileStream);
                    break;
                case ID::SHORT:
                    ret[key] = parseShort(fileStream);
                    break;
                case ID::INT:
                    ret[key] = parseInt(fileStream);
                    break;
                case ID::LONG:
                    ret[key] = parseLong(fileStream);
                    break;
                case ID::FLOAT:
                    ret[key] = parseFloat(fileStream);
                    break;
                case ID::DOUBLE:
                    ret[key] = parseDouble(fileStream);
                    break;
                case ID::STRING:
                    ret[key] = parseString(fileStream);
                    break;
                case ID::LIST:
                    ret[key] = parseList(fileStream);
                    break;
                case ID::COMPOUND:
                    ret[key] = parseCompound(fileStream);
                    break;
                case ID::BYTE_ARRAY:
                    ret[key] = parseByteArray(fileStream);
                    break;
                case ID::INT_ARRAY:
                    ret[key] = parseIntArray(fileStream);
                    break;
                case ID::LONG_ARRAY:
                    ret[key] = parseLongArray(fileStream);
                    break;
            }
        }
        return ret;
    }

    ByteArray parseByteArray(std::ifstream& fileStream) 
    {
        ByteArray ret;
        Int length = parseInt(fileStream);
        for (Int i = 0; i < length; i++)
        {
            ret.push_back(parseByte(fileStream));
        }
        
        return ret;
    }

    IntArray parseIntArray(std::ifstream& fileStream) 
    {
        IntArray ret;
        Int length = parseInt(fileStream);
        for (Int i = 0; i < length; i++)
        {
            ret.push_back(parseInt(fileStream));
        }
        return ret;
    }

    LongArray parseLongArray(std::ifstream& fileStream) 
    {
        LongArray ret;
        Int length = parseInt(fileStream);
        for (Int i = 0; i < length; i++)
        {
            ret.push_back(parseLong(fileStream));
        }
        return ret;
    }
}
