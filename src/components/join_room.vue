<template>
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
                            v-bind:key="room.game_id">
                            {{ room.game_name }}
                            </a>
                        </div>
                    </div>
                <button class="button is-warning is-medium" id="joinGame" v-on:click="join_room">Join</button>
            </div>
            <div v-else>
                <p class="title">Hello! Welcome to our trivia game.</p>
                <img src="https://i.ibb.co/j5TdskZ/wijzendeuil.png" width="200" height="209" alt="logo">
                <p class="title">Please select a username before starting</p>
            </div>
        </article>
    </div>
</template>
<script>
import { mapState, mapMutations } from 'vuex'
export default {
  name: 'joinroom',
  data: function () {
    return {
      Active_Room: undefined
    }
  },
  computed: {
    ...mapState(['username', 'rooms'])
  },
  methods: {
    ...mapMutations(['set_rooms', 'add_room']),
    // Join selected room
    join_room: function () {
      if (this.Active_Room !== undefined) {
        this.$emit('no-error')
        this.$socket.emit('joinGame', { 'name': this.username, 'room_id': this.Active_Room })
      } else {
        this.$emit('error', 'Please pick a room')
      }
    }
  },
  sockets: {
    // Fetch available rooms on connect
    connect: function () {
      this.$socket.emit('get_rooms')
    },
    // Add fetched rooms
    all_rooms: function (data) {
      this.set_rooms(data)
    },
    // Add new room to array
    new_room: function (data) {
      this.add_room(data['room'])
    }
  }
}
</script>
<style scoped>
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

</style>
