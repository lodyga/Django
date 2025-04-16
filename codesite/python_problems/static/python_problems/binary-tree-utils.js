// import { Queue } from '@datastructures-js/queue';

class TreeNode {
   constructor(val = null, left = null, right = null) {
      this.val = val
      this.left = left
      this.right = right
   }
};

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
   // const queue = new Queue([root]);
   const queue = [root];
   let index = 1;

   while (index < nodeList.length) {
      // let node = queue.pop();
      let node = queue.shift();

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