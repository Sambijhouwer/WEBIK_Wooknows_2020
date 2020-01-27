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
        <info></info>

      </div>
    </div>
  </div>
</template>

<script>
import username from '../components/username.vue'
import createroom from '../components/createroom.vue'
import joinroom from '../components/join_room.vue'
import info from '../components/info.vue'
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
    joinroom,
    info
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
