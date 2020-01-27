<template>
  <div style="color: white; margin: 10px; margin-left: 2%;">
    <h1 style="font-size: 40px;">Scoreboard</h1>
    <h1 style="font-size: 20px;">The winner is: <span style="font-weight: 600;">{{ game['winner'][0] }}</span>! You get a cookie!</h1>
    <div style="margin: 10px" v-for="(values, name) in game['scores']" v-bind:key="name">
      <p><span style="font-weight: 600;">{{ name }}:</span> {{ values }} points</p>
      <progress class="progress is-success" :value="values" max="10"></progress>
    </div>
    <router-link style="margin-top: 10px;" to="/" tag="button" class="button is-info">Return to homepage</router-link>
  </div>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'scoreboard',
  computed: {
    ...mapState(['game'])
  }
}
</script>
<style scoped>

</style>
