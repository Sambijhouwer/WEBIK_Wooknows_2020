<template>
    <div>
        <div class="container is-fluid">
  <div class="tile is-ancestor">
    <div class="tile is-vertical is-3">

      <!-- Room information tile -->
      <div class="tile is-child box" id="room_info">
        <p class="title">{{ game.game_name }}</p>
        <p class="subtitle">current quizmaster: {{game.quizmaster}} </p>
      </div>

      <!-- Player scoreboard tile -->
      <div class="tile is-child box" id="room_board">
        <p class="title">Player list</p>
                <ul id="scoreboard">
              <li class="leftTitle"> Names </li> <li class="rightTitle"> Score</li>
          <li v-for="player in game.players" v-bind:key="player" class="roomplayers">
            <span v-if=  "game.ready[player] === true" class="ready">
            <span class="usernameInList"> {{ player }}</span> <span class="room_score" >{{ game.scores[player] }}</span></span>
            <span v-else class="unready">
            <span class="usernameInList"> {{ player }} </span> <span class="room_score">{{ game.scores[player] }}</span></span>
          </li>
        </ul>
      </div>

      <!-- Ready up tile -->
      <div class="tile is-child box" id="room_ready" v-if="game.players.length > 1">
          <div v-if="ready === false">
            <p class="subtitle">Are you ready?</p>
            <button class="button is-success is-large is-fullwidth" type="submit" v-on:click="ready_up">READY!</button>
          </div>
          <div v-else>
              <p class="subtitle">You're ready!</p>
          </div>
      </div>
      <div v-else>
        <p class='subtitle'>You need at least 2 players to start a game</p>
      </div>
    </div>

        <!-- Tile which holds Q&A -->
        <div class="tile" id="questionbox">

          <!-- If quizmaster has already selected a category: -->
          <article class="tile notification is-vertical" id="QnA_container">

            <div class="content" v-if="wrong === true">
              <p class="title" style="text-align: center;">Correct!</p>
            </div>
            <div class="content" v-if="wrong === false">
              <p class="title" style="text-align: center;">Wrong!</p>
            </div>

            <!-- Question -->
            <div class="content" v-if="currentquestions === ''">
              <p class="title">Waiting for new question....</p>
            </div>

            <div v-else>
              <div class="content">
                <p class="title" v-html="currentquestions"></p>
              </div>

              <!-- Answers -->
              <div class="tile">
                <div class="tile is-parent is-vertical" >

                  <!-- Option A -->
                  <div class="tile is-child is-info box" v-on:click="send_ans" :data-ans="answers[0]" v-html="answers[0]">
                    <!-- <p class="subtitle" v-on:click="send_ans" :data-ans="answers[0]" v-html="answers[0]"></p> -->
                  </div>

                  <!-- Option B -->
                  <div class="tile is-child is-primary box" v-on:click="send_ans" :data-ans="answers[1]" v-html="answers[1]">
                    <!-- <p class="subtitle" v-on:click="send_ans" :data-ans="answers[1]" v-html="answers[1]"></p> -->
                  </div>
                </div>
                <div class="tile is-parent is-vertical">

                  <!-- Option C -->
                  <div class="tile is-child is-danger box" v-on:click="send_ans" :data-ans="answers[2]" v-html="answers[2]">
                      <!-- <p class="subtitle" v-on:click="send_ans" :data-ans="answers[2]" v-html="answers[2]"></p> -->
                </div>

                  <!-- Option D -->
                  <div class="tile is-child is-warning box" v-on:click="send_ans" :data-ans="answers[3]" v-html="answers[3]">
                      <!-- <p class="subtitle" v-on:click="send_ans" :data-ans="answers[3]" v-html="answers[3]"></p> -->
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
              <h3 class="title">
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
      wrong: undefined
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
        this.wrong = undefined
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
      this.wrong = event.target.getAttribute('data-ans') === this.correct
      this.$socket.emit('answers', { 'ans': this.wrong, 'room_id': this.game['game_id'], 'user': this.username })
    }
  }
}

</script>
<style scoped>
.leftTitle{
  float:left;
}
.rightTitle{
  text-align:right;
  padding-right:17px;
}
.roomplayers{
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.ready{
  color: green;
}
.unready{
  color: #f25b35;
  width:20em;
}
.usernameInList{
  max-width:65%;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  text-align:left;
  padding-right:0;
  display:inline-block;
}
.room_score{
  color:white;
  float:right;
  padding-right:2em;
}
.title{
  text-align: center;
}
/* Four tiles answers; game lobby */
.tile.is-child.is-info.box {
  background-color: #1FB58F;
  color: white;
  padding-top: 5%;
  text-align: center;
  font-size: 25px;

  border-color: #168267;
  border-width: 4px;
  border-style: solid;
}

.tile.is-child.is-info.box:hover {
  filter: brightness(92%);
}

.tile.is-child.is-primary.box {
  background-color: #EAB126;
  color: white;
  padding-top: 5%;
  text-align: center;
  font-size: 25px;

  border-color: #c2921f;
  border-width: 4px;
  border-style: solid;
}

.tile.is-child.is-primary.box:hover {
  filter: brightness(92%);
}

.tile.is-child.is-danger.box {
  background-color: #F24C4E;
  color: white;
  padding-top: 5%;
  text-align: center;
  font-size: 25px;

  border-color: #d13f40;
  border-width: 4px;
  border-style: solid;
}

.tile.is-child.is-warning.box {
  background-color: #1B7B34;
  color: white;
  padding-top: 5%;
  text-align: center;
  font-size: 25px;

  border-color: #155e28;
  border-width: 4px;
  border-style: solid;

}

.tile.is-child.is-warning.box:hover {
  filter: brightness(92%);
}

/* Score board; game lobby */
#room_board {
  border-color: white;
  border-width: 2px;
  border-style: solid;
  background-color: #373995;
  color: white;
}

/* Ready up tile; game lobby */
#room_ready {
  border-color: white;
  border-width: 2px;
  border-style: solid;
  background-color: #373995;
}

/* Room information; game lobby */
#room_info {
  border-color: white;
  border-width: 2px;
  border-style: solid;
  background-color: #373995;
}

/* Fix room score; game lobby */
.room_score {
  padding-left: 0px;
}

/* The container for the questions; game lobby */
#questionbox {
  padding: .75rem;
}

#QnA_container {
  background-color: #373995;
  color: white;
  border-width: 2px;
  border-color: white;
  border-style: solid;
}

</style>
