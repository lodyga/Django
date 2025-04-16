// import { Queue } from '@datastructures-js/queue';

/**
 * @file Utility functions for binary tree operations in JavaScript.
 * @module treeUtils
 * @description Provides a Queue class and tree utilities for level-order traversal.
 * @example
 * const queue = new Queue([1, 2]);
 * queue.enqueue(3);
 */

/**
 * Vanilla JS queue data structure.
 */
class Queue {
   constructor(items) {
      this.items = items || [];
   }
   enqueue(item) {
      this.items.push(item);
   }
   push(item) {
      this.enqueue(item);
   }
   dequeue() {
      return this.items.shift();
   }
   pop(item) {
      return this.dequeue(item);
   }
   isEmpty() {
      return this.items.length === 0;
   }
}


class TreeNode {
   constructor(val = null, left = null, right = null) {
      this.val = val
      this.left = left
      this.right = right
   }
}


/**
 * Build binary tree from level order traversal list.
 * @param {*} nodeList 
 * @returns 
 */
function buildTree(nodeList) {
   while (nodeList.length && !nodeList[nodeList.length - 1]) {
      nodeList.pop();
   }

   if (!nodeList.length) {
      return null
   }

   const root = new TreeNode(nodeList[0]);
   const queue = new Queue([root]);
   let index = 1;

   while (index < nodeList.length) {
      let node = queue.pop();

      // Assign the left child if available
      if (
         index < nodeList.length &&
         nodeList[index] != null
      ) {
         node.left = new TreeNode(nodeList[index]);
         queue.push(node.left)
      }
      index++;

      // Assign the right child if available
      if (
         index < nodeList.length &&
         nodeList[index] != null
      ) {
         node.right = new TreeNode(nodeList[index]);
         queue.push(node.right)
      }
      index++;
   }
   return root
};


/**
 * Return tree node values in level order traversal format.
 * @param {*} root 
 * @returns 
 */
function getTreeValues(root) {
   if (!root) {
      return []
   }

   const values = [];
   const queue = [];
   queue.push(root);

   while (queue.some(node => node)) {
      const queueForLevel = [];
      while (queue.length) {
         let node = queue.shift();
         values.push(node ? node.val : null);
         queueForLevel.push(node ? node.left : null);
         queueForLevel.push(node ? node.right : null);
      }
      queue.length = 0;
      queue.push(...queueForLevel);
   }

   while (!values[values.length - 1]) {
      values.pop();
   }
   return values
};