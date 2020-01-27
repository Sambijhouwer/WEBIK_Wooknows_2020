<template>
  <div>
    <header class="header" id="headerStyle">
      <div class="container is-fluid">
        <div class="level-left">
          <router-link to="/">
            <img src="https://i.ibb.co/Y34k3hV/logo-no.png" width="80" height="89" alt="logo">
          </router-link>
          <h1 id="logo1">Hoo&nbsp;</h1>
          <h2 id="logo2">Knows</h2>
        </div>
      </div>
    </header>
    <router-view>
    </router-view>
  </div>
</template>
<script>
import { mapMutations } from 'vuex'
export default {
  data () {
    return {
    }
  },
  sockets: {
    lobby: function (data) {
      this.set_game(data['game'])
      this.$router.push('game')
    },
    spel: function (data) {
      console.log('Categorieeen')
      this.ask_categorie(data['categorie'])
      this.set_game(data['game'])
    },
    questions: function (data) {
      this.set_correct(data['answers'][0])
      this.add_questions(data['question'])
      this.shuffle_answers(data['answers'])
    },
    scoreboard: function (data) {
      this.set_game(data['game'])
      this.$router.push('scoreboard')
    }
  },
  methods: {
    ...mapMutations(['set_game', 'ask_categorie', 'add_questions', 'set_correct', 'shuffle_answers'])
  }
}
</script>

<style>
html, body{
  background-color:#292861;
  position: absolute;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Global classes */
a.no_style {
  text-decoration-line: none;
}

.title {
  color: white;
}

.subtitle {
  color: white;
  font-size: x-large;
}

.tile.is-vertical>.tile.is-child:not(:last-child) {
  margin-bottom: 0.7rem!important;
}

.tile.is-parent.flonk {
  padding: .75rem;
  padding-left: 0.5rem;
}

.tile.is-vertical.is-3 {
  padding: .75rem;
}

.content.is-child {
  text-align: center;
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

/* Four tiles answers; game lobby */
.tile.is-child.is-info.box {
  background-color: #1FB58F;
  color: white;
  padding-top: 10%;
  text-align: center;

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
  padding-top: 10%;
  text-align: center;

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
  padding-top: 10%;
  text-align: center;

  border-color: #d13f40;
  border-width: 4px;
  border-style: solid;
}

.tile.is-child.is-danger.box:hover {
  filter: brightness(92%);
}

.tile.is-child.is-warning.box {
  background-color: #1B7B34;
  color: white;
  padding-top: 10%;
  text-align: center;

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

/* Style for the room list; home page */

#room_list{
  border-radius: 10px;
  max-height: 300px;
  width: 100%;
  overflow: auto;
  text-decoration: none;
  display: block;
  overflow-y: scroll;
  color: white;
  font-size: larger;
}

#room_list::-webkit-scrollbar {
  display: none !important;
}

#room_buttons {
  background-color: rgb(36, 142, 213);
  text-decoration: none !important;
  color: white;
  border-bottom: none;
}

#room_buttons:hover{
  background-color: rgb(35, 137, 205);
  text-decoration: none !important;
  border-bottom: none;
}

#room_buttons.is-active{
  background-color:rgb(34, 95, 206);
  text-decoration: none !important;
  display: block;
  border-bottom: none;
}

#joinGame {
  margin-top: 15px;
}

/* Zet de score in de room netjes */
.room_score {
  padding-left: 0px;
}

 /* Style for the logo */
#logo1{
  font-size: 4vw;
  color: rgb(109, 110, 113)
}
#logo2{
  font-size: 4vw;
  color: rgb(242, 175, 88);
}
#headerStyle{
  padding-top: 10px;
  padding-bottom: 10px;
}

</style>
