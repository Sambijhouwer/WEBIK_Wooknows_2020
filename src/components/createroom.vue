<template>
    <div class="tile is-parent">
        <article class="tile is-child notification is-danger">
            <div v-if="username !== ''">
                <p id="create_your_room" class="title">Create your own room!</p>
                <div class="content">
                    <div class="field is-grouped">
                        <p class= "control is-expanded">
                            <input class="input" type="text" placeholder="Create your own room" v-model.trim="game_name">
                        </p>
                        <p class="control">
                            <a class="button is-info" v-on:click="make_room">Create</a>
                        </p>
                    </div>
                </div>
            </div>
            <div v-else>
                <p id="create_your_room" class="title">Pick a name to create a room</p>
            </div>
        </article>
    </div>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'Create_room',
  data: function () {
    return {
      game_name: ''
    }
  },
  computed: {
    ...mapState(['username'])
  },
  methods: {
    make_room: function () {
      if (this.game_name !== '') {
        this.$emit('no-error')
        this.$socket.emit('createGame', { 'name': this.game_name })
      } else {
        this.$emit('error', 'Fill in a valid name')
      }
    }
  },
  sockets: {
    // Join created room
    join_room: function (data) {
      let roomId = data.room['game_id']
      this.$socket.emit('joinGame', { 'room_id': roomId, 'name': this.username })
    }
  }

}
</script>
<style scoped>
#create_your_room{
  margin-bottom: 1%;
}
</style>
