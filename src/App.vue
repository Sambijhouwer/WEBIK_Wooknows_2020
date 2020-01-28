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
    game: function (data) {
      this.ask_categorie(data['categories'])
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

/* Style for error list */
#error_list{
  color: white;
  margin-left: 2%;
  margin-right: 2%;
  margin-bottom: 1%;
  text-align: center;
  padding: 5px 5px;
}

 /* Style for the logo; top bar */
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
