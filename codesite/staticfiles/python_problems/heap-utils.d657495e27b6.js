// import { MinPriorityQueue } from '@datastructures-js/priority-queue';

class PriorityQueue {
   constructor() {
      this.elements = [];
   };

   size() {
      return this.elements.length
   };

   isEmpty() {
      return this.elements.length === 0;
   };

   dequeue() {
      return this.elements.shift();
   };

   front() {
      return this.elements[0];
   }
}


class MinPriorityQueue extends PriorityQueue {
   enqueue(element) {
      this.elements.push(element);
      this.elements.sort((a, b) => a - b);
   };

}


class MaxPriorityQueue extends PriorityQueue {
   enqueue(element) {
      this.elements.push(element);
      this.elements.sort((a, b) => b - a);
   };

}


// import { MinHeap } from '@datastructures-js/heap';

class Heap {
   constructor() {
      this.elements = [];
   };

   size() {
      return this.elements.length
   };

   isEmpty() {
      return this.elements.length === 0;
   };

   pop() {
      return this.elements.shift();
   };

   top() {
      return this.elements[0];
   }
}

class MinHeap extends Heap {
   static heapify(elements) {
      const heap = new MinHeap();
      heap.elements = elements.slice().sort((a, b) => a - b);
      return heap;
   }

   push(element) {
      this.elements.push(element);
      this.elements.sort((a, b) => a - b);
   };

}

class MaxHeap extends Heap {
   static heapify(elements) {
      const heap = new MaxHeap();
      heap.elements = elements.slice().sort((a, b) => b - a);
      return heap;
   }

   push(element) {
      this.elements.push(element);
      this.elements.sort((a, b) => b - a);
   };
}