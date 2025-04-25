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
 * @param {Array<number>} values - Array of values to convert
 * @returns {ListNode} Head node of the constructed linked list
 */
function buildLinkedList(values) {
   let node = new ListNode();
   const anchor = node;
   for (const value of values) {
      node.next = new ListNode(value);
      node = node.next;
   }
   return anchor.next
}


/**
 * Converts a linked list back to an array
 * @param {ListNode} node - Head node of the linked list
 * @returns {Array<number>} Array containing the list values
 */
function getLinkedListValues(node) {
   const values = [];
   while (node) {
      values.push(node.val);
      node = node.next;
   }
   return values
}