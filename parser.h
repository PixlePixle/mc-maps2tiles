#pragma once
#include <vector>
#include <unordered_map>
#include <variant>
#include <string>  
#include <cstdint>
#include <zlib.h>

namespace Parser
{
    enum ID {
        END,
        BYTE,
        SHORT,
        INT,
        LONG,
        FLOAT,
        DOUBLE,
        BYTE_ARRAY,
        STRING,
        LIST,
        COMPOUND,
        INT_ARRAY,
        LONG_ARRAY,
        ID_LAST
    };

    typedef int8_t Byte;
    typedef int16_t Short;
    typedef int32_t Int;
    typedef int64_t Long;
    typedef float Float;
    typedef double Double;
    typedef std::string String;
    typedef std::vector<Byte> ByteArray;
    typedef std::vector<Int> IntArray;
    typedef std::vector<Long> LongArray;

    struct NBT;

    typedef std::vector<NBT> List;
    typedef std::unordered_map<std::string, NBT> Compound;
    
    struct NBT
    {
        std::variant<Byte, Short, Int, Long, Float, Double, String, List, Compound, ByteArray, IntArray, LongArray> data;

        // Constructors
        NBT() = default;

        template<typename T>
        NBT(T value) : data(std::move(value)) {};


        // Getters
        template<typename T>
        T& get()
        {
            return std::get<T>(data);
        }

        template<typename T>
        const T& get() const
        {
            return std::get<T>(data);
        }
    };

    // Since the root is always a Compound, return a compound

    /**
     * @brief Given a filePath, parses the file. Assumes it's properly formatted NBT data.
     * 
     * @param filePath The path of the NBT file
     * 
     * @return A Compound object which is the root of the NBT object.
     */
    Compound parse(std::string filePath);

    /**
     * @brief Reads a Byte from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Byte Object (uint8_t)
     */
    Byte parseByte(gzFile fileStream);
    
    /**
     * @brief Reads a Short from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Short Object (uint16_t)
     */
    Short parseShort(gzFile fileStream);

    /**
     * @brief Reads a Int from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Int Object (uint32_t)
     */
    Int parseInt(gzFile fileStream);

    /**
     * @brief Reads a Long from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Long Object (uint64_t)
     */
    Long parseLong(gzFile fileStream);

    /**
     * @brief Reads a Float from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Float Object (float)
     */
    Float parseFloat(gzFile fileStream);

    /**
     * @brief Reads a Double from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Double Object (double)
     */
    Double parseDouble(gzFile fileStream);

    /**
     * @brief Reads a String from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return String Object (std::string)
     */
    String parseString(gzFile fileStream);
    
    /**
     * @brief Reads a List from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return List Object (std::vector<NBT>)
     */
    List parseList(gzFile fileStream);

    /**
     * @brief Reads a Compound from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return Compound Object (std::unordered_map<NBT>)
     */
    Compound parseCompound(gzFile fileStream);

    /**
     * @brief Reads a Byte Array from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return ByteArray Object (std::vector<Byte>)
     */
    ByteArray parseByteArray(gzFile fileStream);

    /**
     * @brief Reads a Int Array from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return IntArray Object (std::vector<Int>)
     */
    IntArray parseIntArray(gzFile fileStream);

    /**
     * @brief Reads a Long Array from the file
     * 
     * @param fileStream The filestream first obtained from parse
     * 
     * @return LongArray Object (std::vector<Long>)
     */
    LongArray parseLongArray(gzFile fileStream);

}
