<template>
  <v-app>
    <v-card>
      <v-text v-for="server in servers" :key="server">
        {{ server }}
      </v-text>
      <v-text>{{ total }}</v-text>
    </v-card>
    <v-btn router to="actual" @click="service()">
      Next
    </v-btn>
  </v-app>
</template>

<script>
export default {
  // eslint-disable-next-line quotes
  layout: "general_layout",
  data () {
    return {
      ok: {},
      servers: {},
      total: {}
    }
  },
  mounted () {
    setInterval(this.show, 3000)
  },
  methods: {
    async show () {
      this.servers = await this.$axios.$get('http://localhost:8000/server')
    },
    async service () {
      await this.$axios.$get('http://localhost:8000/services')
    }
  }
}
</script>
