/**
 * Represents a node in a singly-linked list.
 * @class
 * @param {number} [val=0] - The value stored in the node
 * @param {ListNode|null} [next=null] - Reference to the next node in the list
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
function buildLinkedList(numbers, { cyclePosition = null }) {
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
function getLinkedListValues(node) {
   const values = [];
   while (node) {
      values.push(node.val);
      node = node.next;
   }
   return values
}