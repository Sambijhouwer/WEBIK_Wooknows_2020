<template>
  <div>
    <p v-if="errors.length">
      <ul>
        <li id="error_list" class="notification is-danger" v-for="error in errors" v-bind:key="error">
          <span class="icon has-text-warning">
          <i class="fas fa-exclamation-triangle"></i>
          </span>
          {{ error }}</li>
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
        <joinroom v-on:error="error_handler" v-on:no-error="reset_error"></joinroom>

        <!-- Green how to play section -->
        <div class="tile is-parent">
          <article class="tile is-child notification is-success">
            <div class="content">
              <p class="title">How to play</p>
              <p class="subtitle">1. Choose a unique username</p>
              <p class="subtitle">2. Join or create a quiz room.</p>
              <p class="subtitle">3. A quizmaster will be selected at random. The quizmaster gets to choose the category for the coming questions.</p>
              <p class="subtitle">4. You earn points by answering the questions correctly. The person with the most points wins!</p>
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
import joinroom from '../components/join_room.vue'
import { mapState } from 'vuex'
export default {
  name: 'home',
  data: function () {
    return {
      errors: []
    }
  },
  components: {
    username,
    createroom,
    joinroom
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
    }
  }
}
</script>
