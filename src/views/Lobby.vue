<template>
    <div>
        <div class="container is-fluid">
  <div class="tile is-ancestor">
    <div class="tile is-vertical is-3">

      <!-- Room information tile -->
      <div class="tile is-child box" id="room_info">
        <p class="title">{{ game.game_name }}</p>
        <p class="subtitle">information</p>
      </div>

      <!-- Player scoreboard tile -->
      <div class="tile is-child box" id="room_board">
        <p class="title">Player list</p>
        <p style="text-align: left;">Names Score</p>
        <ul id="scoreboard">
          <li v-for="player in game.players" v-bind:key="player" style="max-width:150px;"> <span v-if=  "game.ready[player] === true" style="color: green; max-width:10em; word-wrap:break-word;"><span>{{ player }} </span> <span class="room_score" style="color:white;">{{ game.scores[player] }}</span></span> <span v-else style="color: #f25b35;">{{ player }} <span class="room_score" style="color:white;">{{ game.scores[player] }}</span></span></li>
        </ul>
      </div>

      <!-- Ready Up tile -->
      <div class="tile is-child box" id="room_ready">
          <div v-if="ready === false">
            <p class="subtitle">Ready up for the game to start</p>
            <button class="button is-success is-large is-fullwidth" type="submit" v-on:click="ready_up">READY!</button>
          </div>
          <div v-else>
              <p class="subtitle">You're ready!</p>
          </div>

          <!-- Player scoreboard tile -->
          <div class="tile is-child box" id="room_board">
            <p class="title">Player list</p>
            <p style="text-align: left;">Names Score</p>
            <ul id="scoreboard">
              <li v-for="player in game.players" v-bind:key="player">{{ player }}<span class="room_score">{{ game.scores[player] }}... {{ game.ready[player] }}</span></li>
            </ul>
          </div>

          <!-- Ready Up tile -->
          <div class="tile is-child box" id="room_ready">
              <div v-if="ready === false">
                <p class="subtitle">Ready up for the game to start</p>
                <button class="button is-success is-large is-fullwidth" type="submit" v-on:click="ready_up">READY!</button>
              </div>
              <div v-else>
                  <p class="subtitle">You're ready!</p>
              </div>
          </div>
        
        </div>

        <!-- Tile which holds Q&A -->
        <div class="tile" id="questionbox">

          <!-- If quizmaster has already selected a category: -->
          <article class="tile notification is-vertical" id="QnA_container">

            <div class="content" v-if="gofo === true">
              <p class="title" style="text-align: center;">Correct!</p>
            </div>
            <div class="content" v-if="gofo === false">
              <p class="title" style="text-align: center;">Wrong!</p>
            </div>
            
            <!-- Question -->
            <div class="content" v-if="currentquestions === ''">
              <p class="title" style="text-align: center;">Waiting for new question....</p>
            </div>

            <div v-else>
              <div class="content">
                <p class="title" style="text-align: center;" v-html="currentquestions"></p>
              </div>

              <!-- Answers -->
              <div class="tile">
                <div class="tile is-parent is-vertical" >

                  <!-- Option A -->
                  <div class="tile is-child is-info box" >
                    <p class="subtitle" v-on:click="send_ans" :data-ans="answers[0]" v-html="answers[0]"></p>
                  </div>

                  <!-- Option C -->
                  <div class="tile is-child is-primary box">
                    <p class="subtitle" v-on:click="send_ans" :data-ans="answers[1]" v-html="answers[1]"></p>
                  </div>
                </div>
                <div class="tile is-parent is-vertical">

                  <!-- Option B -->
                  <div class="tile is-child is-danger box" >
                      <p class="subtitle" v-on:click="send_ans" :data-ans="answers[2]" v-html="answers[2]"></p>
                  </div>

                  <!-- Option D -->
                  <div class="tile is-child is-warning box">
                      <p class="subtitle" v-on:click="send_ans" :data-ans="answers[3]" v-html="answers[3]"></p>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- Modal which holds choosable categories -->
      <div class="modal" id="myModal" v-bind:class="{'is-active': modalActive === true}">
        <div class="modal-background"></div>
        <div class="modal-content">
          <div class="content">
            <div class="tile is-parent is-vertical is-info notification">
              <h3 style="color: white; text-align: center;">
                Congrats! You are the quizmaster. <br>
                Please pick one of the listed categories:
              </h3>

              <!-- Category options -->
              <div class="buttons has-addons is-centered is-large">
                <div class="tile is-parent is-vertical">

                  <!-- Category 1 -->
                  <div class="tile is-child">
                    <button class="button is-danger is-fullwidth" id="category" v-on:click="send_cat" :data-choice="categories[0]">{{ categories[0] }}</button>
                  </div>

                  <!-- Category 2 -->
                  <div class="tile is-child">
                    <button class="button is-link is-fullwidth" id="category" v-on:click="send_cat" :data-choice="categories[1]">{{ categories[1] }}</button>
                  </div>
                </div>
                <div class="tile is-parent is-vertical">

                  <!-- Category 3 -->
                  <div class="tile is-child">
                    <button class="button is-warning is-fullwidth" id="category"  v-on:click="send_cat" :data-choice="categories[2]">{{ categories[2] }}</button>
                  </div>

                  <!-- Category 4 -->
                  <div class="tile is-child">
                    <button class="button is-success is-fullwidth" id="category"  v-on:click="send_cat" :data-choice="categories[3]">{{ categories[3] }}</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState, mapMutations } from 'vuex'
export default {
  name: 'lobby',
  data: function () {
    return {
      ready: false,
      modalActive: false,
      currentquestions: '',
      gofo: undefined
    }
  },
  watch: {
    categories: function () {
      if (this.username === this.game.quizmaster) {
        this.modalActive = true
      }
    },
    questions: function () {
      if (this.questions.length !== 0) {
        this.gofo = undefined
        this.currentquestions = this.questions.pop()
        this.pop_question()
      }
    }
  },
  computed: {
    ...mapState(['game', 'username', 'categories', 'questions', 'answers', 'correct'])
  },
  methods: {
    ...mapMutations(['pop_question']),
    ready_up: function () {
      this.ready = true
      this.$socket.emit('ready', { 'user': this.username, 'room_id': this.game['game_id'] })
    },
    send_cat: function (event) {
      this.$socket.emit('categorie', { 'categorie': event.target.getAttribute('data-choice'), 'room_id': this.game['game_id'] })
      this.modalActive = false
    },
    send_ans: function (event) {
      this.currentquestions = ''
      this.gofo = event.target.getAttribute('data-ans') === this.correct
      this.$socket.emit('antwoorden', { 'antwoord': this.gofo, 'room_id': this.game['game_id'], 'user': this.username })
    }
  }
}
</script>
