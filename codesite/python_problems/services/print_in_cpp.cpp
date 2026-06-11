// Serialize for C++ like json.dumps or JSON.stringify.
#include <iostream>
#include <string>
#include <vector>
using namespace std;


void print(const string& value) {
   cout << '"' << value << '"' << endl;
   // The line above transforms to the line below
   // it should raise an error but somehow in judge0 env it works
   // cout << \'"\' << value << \'"\' << endl;
}

// void print(const string& value) {
//    cout << "\"" << value << "\"" << endl;
// }

void print(const vector<string>& values) {
   cout << "[";

   for (int idx = 0; idx < values.size(); idx++) {
      cout << '"' << values[idx] << '"';

      if (idx < values.size() - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}

void print(const vector<vector<string>>& values) {
   cout << "[";

   for (int idx = 0; idx < values.size(); idx++) {
      print(values[idx]);

      if (idx < values.size() - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}

void print(int value) {
   cout << value << endl;
}

void print(const vector<int>& values) {
   cout << "[";

   for (int idx = 0; idx < values.size(); idx++) {
      cout << values[idx];

      if (idx < values.size() - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}

void print(const vector<vector<int>>& values) {
   cout << "[";

   for (int idx = 0; idx < values.size(); idx++) {
      print(values[idx]);

      if (idx < values.size() - 1) {
         cout << ", ";
      }
   }

   cout << "]" << endl;
}
