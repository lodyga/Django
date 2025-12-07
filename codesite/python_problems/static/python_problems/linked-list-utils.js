// export { ListNode, buildLinkedList, getLinkedListValues, areLinkedListsEqueal }


/**
 * Represents a node in a singly-linked list.
 * @class
 * @param {number|null} [val=null]
 * @param {ListNode|null} [next=null]
 */
class ListNode {
   constructor(val = null, next = null) {
      this.val = val;
      this.next = next;
   }
}


/**
 * Converts an array of values into a linked list
 * @param {number[]} numbers
 * @returns {ListNode}
 */
const buildLinkedList = (numbers, { cyclePosition = null } = {}) => {
   let node = new ListNode();
   const anchor = node;
   let hasCycle = false;
   let cycleNode;

   for (let position = 0; position < numbers.length; position++) {
      const number = numbers[position];
      node.next = new ListNode(number);
      node = node.next;

      if (position === cyclePosition) {
         cycleNode = node;
         hasCycle = true;
      }
   }
   if (hasCycle) {
      node.next = cycleNode;
   }
   return anchor.next
}


/**
 * Converts a linked list back to an array
 * @param {ListNode} node
 * @returns {Array<number>}
 */
const getLinkedListValues = (node) => {
   const values = [];
   while (node) {
      values.push(node.val);
      node = node.next;
   }
   return values
}


/**
 * Compare two linked lists value by value.
 * @param {ListNode} root1 
 * @param {ListNode} root2 
 * @returns {boolean}
 */
const areLinkedListsEqueal = (root1, root2) => {
   let node1 = root1;
   let node2 = root2;

   while (node1 || node2) {
      if (node1 === null && node2 === null) {
         return true
      } else if (
         (node1 === null || node2 === null) ||
         node1.val !== node2.val
      ) {
         return false
      }
      node1 = node1.next;
      node2 = node2.next;
   }
   return true
}
