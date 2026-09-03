#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
#include <optional>
#include <limits.h>
using namespace std;


// Definition for a binary tree node.
struct TreeNode {
   int val;
   TreeNode* left;
   TreeNode* right;
   TreeNode() : val(0), left(nullptr), right(nullptr) {}
   TreeNode(int val) : val(val), left(nullptr), right(nullptr) {}
   TreeNode(int val, TreeNode* left, TreeNode* right) : val(val), left(left), right(right) {}
};


TreeNode* buildBinaryTree(const vector<optional<int>>& orgValues) {
   // TreeNode* buildBinaryTree(const vector<int>& orgValues) {
   vector<optional<int>> values(orgValues);
   // vector<int> values(orgValues);

   while (!values.empty() && !values.back()) {
      values.pop_back();
   }

   if (values.empty() || !values[0]) {
      return nullptr;
   }

   TreeNode* root = new TreeNode(values[0].value());
   // TreeNode* root = new TreeNode(values[0]);
   queue<TreeNode*> q({ root });
   size_t idx = 1;

   while (idx < values.size()) {
      TreeNode* node = q.front();
      q.pop();

      // Assign the left child if available
      if (idx < values.size() && values[idx]) {
         node->left = new TreeNode(values[idx].value());
         // node->left = new TreeNode(values[idx]);
         q.push(node->left);
      }
      ++idx;

      // Assign the right child if available
      if (idx < values.size() && values[idx]) {
         node->right = new TreeNode(*values[idx]);
         // node->right = new TreeNode(values[idx]);
         q.push(node->right);
      }
      ++idx;
   }

   return root;
};


// vector<optional<int>> serializeBinaryTree(TreeNode* root) {
vector<int> serializeBinaryTree(TreeNode* root) {
   if (root == nullptr) {
      return {};
   }

   // vector<optional<int>> values;
   vector<int> values;
   queue<TreeNode*> q;
   q.push(root);

   while (!q.empty()) {
      TreeNode* node = q.front();
      q.pop();

      if (node) {
         values.push_back(node->val);
         q.push(node->left);
         q.push(node->right);
      }
      else {
         // values.push_back(nullopt);
         values.push_back(INT_MAX);
      }
   }

   // while (!values.empty() && !values.back()) {
   while (!values.empty() && values.back() == INT_MAX) {
      values.pop_back();
   }

   return values;
};


bool isSameTree(TreeNode* root1, TreeNode* root2) {
   auto dfs = [](auto&& self, TreeNode* node1, TreeNode* node2) -> bool {
      if (!node1 && !node2) {
         return true;
      }

      if (!node1 || !node2) {
         return false;
      }

      if (node1->val != node2->val) {
         return false;
      }

      return (
         self(self, node1->left, node2->left)
         && self(self, node1->right, node2->right)
         );
      };

   return dfs(dfs, root1, root2);
};
