#include "parser.h"

#include <fstream>
#include <cstring>

// Delete this
#include <iostream>

namespace Parser {
    uint8_t readByte(gzFile fileStream)
    {
        uint8_t ret;
        if ( gzread(fileStream, &ret, 1) != 1 )
            throw std::runtime_error("Unexpected EOF");
        
        return ret;
    }

    Compound parse(std::string filePath)
    {
        gzFile fileStream = gzopen(filePath.c_str(), "rb");
        if ( !fileStream )
            throw std::runtime_error("Failed to open NBT file");

        // Consume a byte here because it represents the compound root
        readByte(fileStream);
        // Burn two more for some reason.
        readByte(fileStream);
        readByte(fileStream);
        Compound ret = parseCompound(fileStream);

        gzclose(fileStream);
        return ret;
    }

    Byte parseByte(gzFile fileStream)
    {
        uint8_t ret = readByte(fileStream);
        return static_cast<Byte>(ret);
    }

    Short parseShort(gzFile fileStream)
    {
        uint16_t ret = readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        return static_cast<Short>(ret);
    }

    Int parseInt(gzFile fileStream)
    {
        uint32_t ret = readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        return static_cast<Int>(ret);
    }

    Long parseLong(gzFile fileStream)
    {
        uint64_t ret = readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        ret = (ret << 8) | readByte(fileStream);
        return static_cast<Long>(ret);
    }

    Float parseFloat(gzFile fileStream)
    {
        uint32_t bits = parseInt(fileStream);
        Float ret;
        std::memcpy(&ret, &bits, sizeof(ret));
        return ret;
    }

    Double parseDouble(gzFile fileStream)
    {
        uint64_t bits = parseLong(fileStream);
        double ret;
        std::memcpy(&ret, &bits, sizeof(ret));
        return ret;
    }

    String parseString(gzFile fileStream)
    {
        uint16_t length = static_cast<uint16_t>(parseShort(fileStream));
        String ret(length, '\0');
        int bytesRead ;
        if ( bytesRead = gzread(fileStream, ret.data(), length) != length )
            throw std::runtime_error("Unexpected EOF");
        
        std::cout << "length: " << length << '\n';
        std::cout << "bytesRead: " << bytesRead << '\n';
        return ret;
    }

    List parseList(gzFile fileStream)
    {
        List ret;
        uint8_t tag = static_cast<uint8_t>(readByte(fileStream));
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

    Compound parseCompound(gzFile fileStream)
    {
        Compound ret;
        while ( true )
        {
            // Reads the tag id
            uint8_t tag = static_cast<uint8_t>(readByte(fileStream));
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

    ByteArray parseByteArray(gzFile fileStream) 
    {
        ByteArray ret;
        Int length = parseInt(fileStream);
        for (Int i = 0; i < length; i++)
        {
            ret.push_back(parseByte(fileStream));
        }
        
        return ret;
    }

    IntArray parseIntArray(gzFile fileStream) 
    {
        IntArray ret;
        Int length = parseInt(fileStream);
        for (Int i = 0; i < length; i++)
        {
            ret.push_back(parseInt(fileStream));
        }
        return ret;
    }

    LongArray parseLongArray(gzFile fileStream) 
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
