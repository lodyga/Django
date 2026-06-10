// Serialize for C++ like json.dumps or JSON.stringify.
#include <iostream>
#include <string>
#include <vector>
using namespace std;


void print(const int& value) {
   cout << value << endl;
}

void print(const string& value) {
   cout << '"' << value << '"' << endl;
}

// C++ todo
// vecor of strings?
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
