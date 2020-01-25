<template>
  <div>
    <p v-if="errors.length">
      <ul>
        <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
      </ul>
    </p>
    <div class="container is-fluid">
      <div class="tile is-ancestor">

        <!-- Left pair of yellow and red tiles -->
        <div class="tile is-vertical is-4">

          <!-- Yellow username tile -->
          <username v-on:error="error_handler" v-on:no-error="reset_error"></username>

          <!-- Red create room tile -->
          <createroom v-on:error="error_handler" v-on:no-error="reset_error"></createroom>
        </div>

        <!-- Blue join room list tile -->
        <div class="tile is-parent">
          <article class="tile is-child notification is-info" style="text-align: center;">
            <div v-if="username !== ''">
              <p class="title">Available quiz rooms</p>
              <div class="container is-fluid">
                <div class="list is-hoverable" id="room_list">
                  <!-- Room list is inserted here -->
                  <a
                  class="list-item"
                  id="room_buttons"
                  v-for="room in rooms"
                  v-bind:class="{'is-active': room.game_id === Active_Room}"
                  v-on:click="Active_Room = room.game_id"
                  v-bind:key="room"
                  >{{ room.game_name }}</a>
                </div>
              </div>
              <button class="button is-warning is-medium" id="joinGame" v-on:click="join_room">Join</button>
            </div>
            <div v-else>
              <p class="title">Pick a name to join quiz rooms</p>
            </div>
          </article>
        </div>

        <!-- Green how to play section -->
        <div class="tile is-parent">
          <article class="tile is-child notification is-success">
            <div class="content">
              <p class="title">How to play</p>
              <p class="subtitle">1. Choose a unique username</p>
              <p class="subtitle">2. Join or create a quiz room.</p>
              <p class="subtitle">3. A quizmaster will be selected at random. The quizmaster gets to choose the category for the coming questions.
                The amount of questions in this category are also random. </p>
              <p class="subtitle">4.You earn points by answering the questions correctly. The person with the most points wins!</p>
            </div>
          </article>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import username from '../components/username.vue'
import createroom from '../components/createroom.vue'
import { mapState } from 'vuex'
export default {
  name: 'home',
  data: function () {
    return {
      Active_Room: undefined,
      errors: [],
      rooms: []
    }
  },
  components: {
    username,
    createroom
  },
  sockets: {
    connect: function () {
      this.$socket.emit('get_rooms')
    },
    all_rooms: function (data) {
      this.rooms = data
    },
    new_room: function (data) {
      this.rooms.push(data['room'])
    },
    join_room: function (data) {
      let roomId = data.room['game_id']
      this.$socket.emit('joinGame', { 'room_id': roomId, 'name': this.username })
    }
  },
  computed: {
    ...mapState(['username'])
  },
  methods: {
    error_handler: function (error) {
      this.errors.pop()
      this.errors.push(error)
    },
    reset_error: function () {
      this.errors = []
    },
    join_room: function () {
      if (this.Active_Room !== undefined) {
        this.$socket.emit('joinGame', { 'name': this.username, 'room_id': this.Active_Room })
      } else {
        this.errors.push('Please pick a room')
      }
    }
  }
}
</script>
