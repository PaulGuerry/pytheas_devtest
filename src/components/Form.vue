<script>
let id = 0

export default {
  name: 'TodoForm',
  data() {
    return {
      newTodo: '',
      hideCompleted: false,
      todoL: [
        { id: id++, text: 'Learn HTML' , done: true},
        { id: id++, text: 'Learn JavaScript', done: false },
        { id: id++, text: 'Learn Vue', done: true }
      ]
    }
  },
  methods: {
    addTodo() {
      this.todoL.push({id: id++, text: this.newTodo}),
      this.newTodo = ''
    },
    removeTodo(todo) {
      this.todoL = this.todoL.filter((t) => t != todo)
    }
  },
  computed: { 
    hideList () {
      return (this.hideCompleted ? this.todoL.filter((t) => !t.done) : this.todoL)
    }
  } 
}
</script>

<template>
    <h3>Todo List</h3>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo" >
    <button class="button">Add Todo</button>    
  </form>
  <ul>
    <li v-for="todo in hideList" :key="todo.id">
      <input type="checkbox" v-model="todo.done">
       <span :class="{ done: todo.done }">{{ todo.text }}</span>
      <button @click="removeTodo(todo)" class="letter_button">X</button>
    </li>
  </ul>
  <button @click="hideCompleted = !hideCompleted">
    {{ hideCompleted ? 'Show all' : 'Hide completed' }}
  </button>
</template>


<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
input {
  width: 25%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border: none;
  border-bottom: 2px solid #42b893;
  font-size: 12px;
  border-radius: 4px;
}
.button {
  background-color: none;
  border: 2x #42b893;
  color: black;
  padding: 12px 24px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 12 px;
  margin: 4px 2px;
  cursor: pointer;
}
.letter_button {
  background-color: none;
  border: 2px #42b893;
  color: black;
  padding: 2px 4px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 10 px;
  margin: 4px 2px;
  cursor: pointer;
}
.done {
  text-decoration: line-through;
}
</style>
