// Serialize for C++ like json.dumps or JSON.stringify.
#include <tuple>
#include <iostream>
#include <string>
#include <vector>
using namespace std;


void println(const string& value) {
   cout << char(34) << value << char(34) << endl;
}


// print in void println(const vector<vector<string>>& values) {
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

void println(const vector<char>& values) {
   cout << "[";
   for (size_t idx = 0; idx < values.size(); ++idx) {
      // need to be '"' because json.loads() in get_output_data in response_validation.py
      cout << '"' << values[idx] << '"';
      // or this and use [ast.literal_eval(line) for line in output_serialized_data]
      // cout << "'" << values[idx] << "'";

      if (idx + 1 < values.size()) {
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


// print in void println(const vector<vector<int>>& values) {
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
