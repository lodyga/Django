#include <iostream>
#include <tuple>
using namespace std;

template<typename Method, typename Inputs>
void runTests(
   Solution& solution,
   Method method,
   Inputs& inputs)
{
   for (auto& data : inputs) {
      apply(
         [&](auto&... args) {
            (solution.*method)(args...);
         },
         data
      );

      apply(
         [&](const auto&... args) {
            (println(args), ...);
         },
         data
      );
   }
}
