#include <vector>
using namespace std;


struct ListNode {
   int val;
   ListNode* next;
   ListNode() : val(-1), next(nullptr) {}
   ListNode(int val) : val(val), next(nullptr) {}
   ListNode(int val, ListNode* next) : val(val), next(next) {}
};


struct LinkedList {
   ListNode* buildLinkedList(const vector<int> nums, int cyclePosition = -1) {
      ListNode* node = new ListNode();
      ListNode* anchor = node;
      ListNode* cycleNode = nullptr;

      for (int position = 0; position < nums.size(); ++position) {
         int num = nums[position];
         node->next = new ListNode(num);
         node = node->next;

         if (position == cyclePosition) {
            ListNode* cycleNode = node;
         }
      }

      if (cycleNode) {
         node->next = cycleNode;
      }

      return anchor->next;
   }

   vector<int> serializeLinkedList(ListNode* node) {
      vector<int> values;

      while (node) {
         values.push_back(node->val);
         node = node->next;
      }

      return values;
   }

   bool areLinkedListsEqueal(ListNode* root1, ListNode* root2) {
      ListNode* node1 = root1;
      ListNode* node2 = root2;

      while (node1 || node2) {
         if (node1 == nullptr && node2 == nullptr) {
            return true;
         }
         else if (
            (node1 == nullptr || node2 == nullptr)
            || node1->val != node2->val
            ) {
            return false;
         }

         node1 = node1->next;
         node2 = node2->next;
      }

      return true;
   }
};

