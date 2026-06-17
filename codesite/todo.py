# default tests for two sum, min stack, reverse linked list, rev binary tree
# Remove duplicases from search
# Unique paths no input variable name under Test Cases.
# Priority Queue; Cannot use import statement outside a module, K Closest Points to Origin attach import only to pQ problems
# Binary Search Tree Iterator is class and binary tree problem
# Island Perimeter
# fix all redirect, redirect after adding new problem/solution
# add/remove tags privliges
# fix all back
# fordbid run and validate if no test cases.
# remove problem type, method name, argument names,  comparison type fields or meaby not
# fix next slug # get_adjacent_slugs(problem, language)
# add js heap to metadata
# case ComparisonType.EXACT | "equal" | "exact":
# Python 3.8 doesn't support match / case statements.
# setup cursor with proper method name
# edit only own solutions
# validate all test cases
# in progress... preview based on data type:  (grid, matrix) preview veritcal preview for heights [1, 4, 6, 7, 6, 7]
# wrap build_binary_tree and other around bt methods
# for later
# problem add, focus on that problem, exclude Problem, Language, Order fields
# + soultion, hide problem & language fields
# stop <pre></pre> in README.md => test cases
# fix all redirects / back
# import needed only get_heap_utils(language) + get_binary_tree_utils(language) + get_linked_list_utils(language) + source_code
# better light mode
# hints to buttons
# color code output badge greee/red for pass/fail
# code mode/browse mode
# submit/ >> append, > overwrite
# user dashboard
# in detail view back button with filters precerved
# move the screen to 'show solution' if run from prbolem view
# reverse search for order by, difficulty
# Edit/info/settings tab
# dev opts for update|delete
# search bar AND OR
# chanege python to code_problems...
# selenium for testing darkmode
# Task Scheduler C++ input list to vector, JS add queue
# Design Tweeter C++

"""
Preview:

{
    int: int
    chr: chr
    0 or "0"(water): "·"
    1 or "1"(land): "■"
    -1: "
}

┌───────────┐
│ ■ ■ · · · │
│ ■ ■ · · · │
│ · · ■ · · │
│ · · · ■ ■ │
└───────────┘

┌─────────────┐
│  1  3  5  7 │
│ 10 11 16 20 │
│ 23 30 34 60 │
└─────────────┘

┌─────────────┐
│ # # * . * . │
│ # # # * . . │
│ # # # . # . │
└─────────────┘



Test Cases:
[[[2, 7, 11, 15], 9], [0, 1]]
{"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}
{"data": [[[2, 7, 11, 15], 9], [0, 1]]}
{"data": {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}}
{"data": {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}, "is_hidden": false, "explanation": ""}

# operations, arguments, expected 
{"data": [["TimeMap", "set", "get", "get", "set", "get", "get"], [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]], [null, null, "bar", "bar", null, "bar2", "bar2"]], "is_hidden": false, "explanation": ""}





metadata
{"problem_type": "binary_tree", "method_name": "invertTree", "parameters": [{"name": "root", "type": "binary_tree"}], "return_type": "binary_tree", "comparison_type": "equal"}

{
  "problem_type": "binary_tree", 
  "method_name": "invertTree",
  "parameters": [
    {
      "name": "root",
      "type": "binary_tree"
    }
  ],
  "return_type": "binary_tree",
  "comparison_type": "binar_tree_equal"
}


{
  "problem_type": "function", 
  "method_name": "twoSum",
  "parameters": [
    {
      "name": "nums",
      "type": "list[int]"
    },
    {
      "name": "target",
      "type": "int"
    }
  ],
  "return_type": "list[int]",
  "comparison_type": "deep_equal",
  "constraints": {
    "nums.length": [2, 10000]
  }
}


{
  "problem_type": "class",
  "class_name": "TimeMap",

  "constructor": {
    "parameters": []
  },

  "methods": [
    {
      "name": "set",
      "parameters": [
        {"name": "key", "type": "string"},
        {"name": "value", "type": "string"},
        {"name": "timestamp", "type": "int"}
      ],
      "return_type": "void"
    },
    {
      "name": "get",
      "parameters": [
        {"name": "key", "type": "string"},
        {"name": "timestamp", "type": "int"}
      ],
      "return_type": "string"
    }
  ]
}

"""


