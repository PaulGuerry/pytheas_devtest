// 240829: https://vueform.com/docs/handling-form-data

import { defineStore } from 'pinia'

export const useFormsStore = defineStore('forms', {
  state: () => {
    return {
      registration: {}
    }
  },
})