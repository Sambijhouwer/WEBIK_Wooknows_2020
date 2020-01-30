<template>
    <div class="tile">
        <div class="tile is-parent is-vertical">
            <article class="tile is-child notification is-warning" id="centered">
                <div v-if='username === ""'>
                    <p class="title">Join</p>
                    <p class="subtitle">Choose your username</p>
                    <img src="https://i.ibb.co/Y34k3hV/logo-no.png" class="level" id="owl_homepage" width="81" alt="logo">
                    <div class="container is-fluid">
                        <div class="container is-fluid">
                            <div class="field">
                                <div class="input-is-hovered">
                                    <input class="input" type="text" placeholder="Username" v-model="user">
                                </div>
                            </div>
                            <button class="button is-success is-medium" v-on:click="get_user">Go!</button>
                        </div>
                    </div>
                </div>
            <!-- Greet user -->
                <div v-else>
                    <p class="title">Welcome {{ username }}</p>
                    <img src="https://i.ibb.co/Y34k3hV/logo-no.png" class="level" id="owl_homepage" width="81" alt="logo">
                </div>
            </article>
        </div>
    </div>
</template>
<script>
import { mapState, mapMutations } from 'vuex'
export default {
  name: 'Username',
  data: function () {
    return {
      user: ''
    }
  },
  computed: {
    ...mapState(['username'])
  },
  methods: {
    ...mapMutations(['set_username']),
    get_user: function () {
      if (this.user !== '') {
        this.$emit('no-error')
        this.$socket.emit('check_name', { 'name': this.user })
      } else {
        this.$emit('error', 'Fill in a valid name')
      }
    }
  },
  sockets: {
    username: function (data) {
      if (data['available']) {
        this.$emit('no-error')
        this.set_username(data['username'])
      } else {
        this.$emit('error', 'Name is already taken')
      }
    }
  }
}
</script>
<style scoped>
#owl_homepage {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
#centered{
  text-align:center;
}
</style>
