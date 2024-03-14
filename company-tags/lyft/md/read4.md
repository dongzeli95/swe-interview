```cpp
// Given a file and assume that you can only read the file using a given method read4, implement a method read to read n characters.Your method read may be called multiple times.

// Method read4 :

// The API read4 reads four consecutive characters from file, then writes those characters into the buffer array buf4.

// The return value is the number of actual characters read.

// Note that read4() has its own file pointer, much like FILE* fp in C.

// Definition of read4 :

// Parameter:  char[] buf4
// Returns : int

// buf4[] is a destination, not a source.The results from read4 will be copied to buf4[].
// Below is a high - level example of how read4 works :

// File file("abcde"); // File is "abcde", initially file pointer (fp) points to 'a'
// char[] buf4 = new char[4]; // Create buffer with enough space to store characters
// read4(buf4); // read4 returns 4. Now buf4 = "abcd", fp points to 'e'
// read4(buf4); // read4 returns 1. Now buf4 = "e", fp points to end of file
// read4(buf4); // read4 returns 0. Now buf4 = "", fp points to end of file


// Method read :

// By using the read4 method, implement the method read that reads n characters from file and store it in the buffer array buf.Consider that you cannot manipulate file directly.

// The return value is the number of actual characters read.

// Definition of read :

// Parameters:	char[] buf, int n
// Returns : int

// buf[] is a destination, not a source.You will need to write the results to buf[].
// Note :

//     Consider that you cannot manipulate the file directly.The file is only accessible for read4 but not for read.
//     The read function may be called multiple times.
//     Please remember to RESET your class variables declared in Solution, as static / class variables are persisted across multiple test cases.Please see here for more details.
//     You may assume the destination buffer array, buf, is guaranteed to have enough space for storing n characters.
//     It is guaranteed that in a given test case the same buffer buf is called by read.


/**
 * The read4 API is defined in the parent class Reader4.
 *     int read4(char *buf4);
 */

// buf = "ab", [read(1),read(2)]，返回 ["a","b"]

// 那么第一次调用 read(1) 后，从 buf 中读出一个字符，就是第一个字符a，然后又调用了一个 read(2)，想取出两个字符，但是 buf 中只剩一个b了，所以就把取出的结果就是b。再来看一个例子：

// buf = "a", [read(0),read(1),read(2)]，返回 ["","a",""]

// 第一次调用 read(0)，不取任何字符，返回空，第二次调用 read(1)，取一个字符，buf 中只有一个字符，取出为a，然后再调用 read(2)，想取出两个字符，但是 buf 中没有字符了，所以取出为空。

// 但是这道题我不太懂的地方是明明函数返回的是 int 类型啊，为啥 OJ 的 output 都是 vector 类的，
// 然后我就在网上找了下面两种能通过OJ的解法，大概看了看，也是看的个一知半解，
// 貌似是用两个变量 readPos 和 writePos 来记录读取和写的位置，i从0到n开始循环，
// 如果此时读和写的位置相同，那么调用 read4 函数，将结果赋给 writePos，把 readPos 置零，
// 如果 writePos 为零的话，说明 buf 中没有东西了，返回当前的坐标i。
// 然后用内置的 buff 变量的 readPos 位置覆盖输入字符串 buf 的i位置，如果完成遍历，返回n，参见代码如下：


class Solution {
public:
    /**
     * @param buf Destination buffer
     * @param n   Number of characters to read
     * @return    The number of actual characters read
     */
    int read(char* buf, int n) {
        for (int i = 0; i < n; ++i) {
            if (readPos == writePos) {
                writePos = read4(buff);
                readPos = 0;
                if (writePos == 0) return i;
            }
            buf[i] = buff[readPos++];
        }
        return n;
    }

    int readPos = 0, writePos = 0;
    char buff[4];
};```
