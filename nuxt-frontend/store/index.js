import { defineStore } from 'pinia'

// useStore could be anything like useUser, useCart
// the first argument is a unique id of the store across your application

const isPrime = (n) => {
  if (n < 2) return false;
  for (let i = 2; i < n/2+1; i++) {
    if (n % i === 0) return false;
  }
  return true;
}


export const useStore = defineStore('store', {
  // state

  state: () => {
    return {
      counter: 0,
    }
  },

  // actions
  actions: {
    increment() {
      this.counter++;
    },

    double() {
      this.counter *= 2;
    }
  },
  // getters
  getters: {
    doubleCounter() {
      return this.counter * 2
    },


    


    primeList() {
      

      const primeList = [];
      for (let i = 2; i < this.counter; i++) {
        if (isPrime(i)) {
          primeList.push(i);
        }
      }
      return primeList;
    }

  },
})
