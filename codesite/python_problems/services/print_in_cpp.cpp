// Serialize for C++ like json.dumps or JSON.stringify.
#include <iostream>
#include <string>
#include <vector>
using namespace std;


void println(const string& value) {
   cout << '"' << value << '"' << endl;
   // The line above transforms to the line below
   // it should raise an error but somehow in judge0 env it works
   // cout << \'"\' << value << \'"\' << endl;
}

// void println(const string& value) {
//    cout << "\"" << value << "\"" << endl;
// }

void print(const vector<string>& values) {
   size_t N = values.size();
   cout << "[";

   for (int idx = 0; idx < N; idx++) {
      cout << '"' << values[idx] << '"';

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
      cout << '"' << values[idx] << '"';

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
