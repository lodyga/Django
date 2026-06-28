// Serialize for C++ like json.dumps or JSON.stringify.
#include <tuple>
#include <iostream>
#include <string>
#include <vector>
using namespace std;


void println(const string& value) {
   cout << char(34) << value << char(34) << endl;
}

void print(const vector<string>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      cout << char(34) << values[idx] << char(34);

      if (idx < N - 1) {
         cout << ", ";
      }
   }

   cout << "]";
}

void println(const vector<string>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      cout << char(34) << values[idx] << char(34);

      if (idx < N - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}

void println(const vector<vector<string>>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      print(values[idx]);

      if (idx < N - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}

void println(int value) {
   cout << value << endl;
}

void println(const vector<int>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      cout << values[idx];

      if (idx < N - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}

void print(const vector<int>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      cout << values[idx];

      if (idx < N - 1) {
         cout << ", ";
      }
   }

   cout << "]";
}

void println(const vector<vector<int>>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      print(values[idx]);

      if (idx < N - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}
