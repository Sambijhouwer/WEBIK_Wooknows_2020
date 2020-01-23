<template>
    <div>
        <h1>{{ game['winner'] }}</h1>
        <div v-for="(values, name) in game['scores']" v-bind:key="name">
            <p>{{ name }}</p>
            <progress class="progress is-primary" :value="values" max="10"></progress>
        </div>
        <router-link to="/" tag="button" class="button is-info is-rounded">return to homepage</router-link>
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
