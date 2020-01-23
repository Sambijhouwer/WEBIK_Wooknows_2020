import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: '',
    game: {},
    categories: [],
    questions: [],
    correct: '',
    answers: []
  },
  getters: {
  },
  mutations: {
    set_username (state, name) {
      state.username = name
    },
    set_game (state, game) {
      state.game = game
    },
    ask_categorie (state, categorieen) {
      state.categories = categorieen
    },
    add_questions (state, question) {
      state.questions.push(question)
    },
    pop_question (state) {
      state.questions.pop()
    },
    set_correct (state, answer) {
      state.correct = answer
    },
    shuffle_answers (state, a) {
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]]
      }
      state.answers = a
    }

  },
  actions: {
  },
  modules: {
  }
})
