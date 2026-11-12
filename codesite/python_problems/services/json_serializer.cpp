// Serialize C++ values in the JSON-like format expected by response validation.
#include <iostream>
#include <string>
#include <vector>

using namespace std;


template <typename T>
void print(const T& value) {
   cout << value;
}


void print_escaped_string(const string& value) {
   cout << '"';

   for (unsigned char character : value) {
      switch (character) {
      case '"':
         cout << "\\\"";
         break;
      case '\\':
         cout << "\\\\";
         break;
      case '\b':
         cout << "\\b";
         break;
      case '\f':
         cout << "\\f";
         break;
      case '\n':
         cout << "\\n";
         break;
      case '\r':
         cout << "\\r";
         break;
      case '\t':
         cout << "\\t";
         break;
      default:
         if (character < 0x20) {
            const char hex_digits[] = "0123456789abcdef";
            cout << "\\u00" << hex_digits[character >> 4]
               << hex_digits[character & 0x0f];
         }
         else {
            cout << character;
         }
      }
   }

   cout << '"';
}


void print(const string& value) {
   print_escaped_string(value);
}


void print(const char& value) {
   print_escaped_string(string(1, value));
}


template <typename T>
void print(const vector<T>& values) {
   cout << "[";

   for (size_t idx = 0; idx < values.size(); ++idx) {
      if (idx > 0) {
         cout << ", ";
      }
      print(values[idx]);
   }

   cout << "]";
}


template <typename T>
void println(const T& value) {
   print(value);
   cout << endl;
}
