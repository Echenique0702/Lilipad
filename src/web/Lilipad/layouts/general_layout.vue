<template>
  <v-app>
    <v-toolbar color="teal darken-1">
      <v-toolbar-title>Lilipad</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-btn text router to="configuration">Configuración</v-btn>
        <v-btn text router to="actual">Actual</v-btn>
        <v-btn text router to="futura">Futura</v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content color="withe">
      <nuxt />
    </v-content>
  </v-app>
</template>
