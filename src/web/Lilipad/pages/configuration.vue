/* eslint-disable no-console */

<template>
  <v-app>
    <v-card>
      <v-card-title color="white">
        Zabbix
      </v-card-title>
      <v-card-actions>
        <v-card-text>
          <v-layout row>
            <v-flex xs4>
              <v-subheader>IP del servidor Zabbix</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field
                v-model="ip"
                label="Ip de la forma xxx.xxx.xxx.xxx"
              />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs4>
              <v-subheader>Ususario del Servidor Zabbix</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field v-model="usuario" label="Usuario" />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs4>
              <v-subheader>Password del Servidor Zabbix</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field
                v-model="password"
                :append-icon="mostrar ? 'visibility' : 'visibility_off'"
                :type="mostrar ? 'text' : 'password'"
                name="input-10-2"
                class="input-group--focused"
                label="Password"
                @click:append="mostrar = !mostrar"
              />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs4>
              <v-subheader>Usuarios Actuales</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field v-model="user_actual" label="Usuarios Actuales" />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs4>
              <v-subheader>Usuarios Futuros</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field v-model="user_new" label="Usuarios Futuros" />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex xs4>
              <v-subheader>Tiempo Inicio</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field
                v-model="start_time"
                label="De la forma DD/MM/YYYY"
              />
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs4>
              <v-subheader>Final</v-subheader>
            </v-flex>
            <v-flex xs8>
              <v-text-field v-model="end_time" label="De la forma DD/MM/YYYY" />
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-spacer />
            <v-btn color="blue darken-1" flat router to="actual" @click="save()">
              Save
            </v-btn>
          </v-layout>
        </v-card-text>
      </v-card-actions>
    </v-card>
  </v-app>
</template>
<script>
export default {
  // eslint-disable-next-line quotes
  layout: "general_layout",
  // eslint-disable-next-line space-before-function-paren
  data() {
    return {
      server_prox: {},
      // eslint-disable-next-line quotes
      init: "init",
      datos: {},
      mostrar: false,
      // eslint-disable-next-line quotes
      ip: "",
      // eslint-disable-next-line quotes
      usuario: "",
      // eslint-disable-next-line quotes
      user_new: "",
      // eslint-disable-next-line quotes
      user_actual: "",
      // eslint-disable-next-line quotes
      start_time: "",
      // eslint-disable-next-line quotes
      end_time: "",
      // eslint-disable-next-line quotes
      password: "",
      zabbix_server: [],
      dialog: false
      // eslint-disable-next-line semi
    };
  },
  methods: {
    // eslint-disable-next-line space-before-function-paren
    async save () {
      this.datos = {
        ip: this.ip,
        usuario: this.usuario,
        password: this.password,
        user_new: this.user_new,
        user_actual: this.user_actual,
        start_time: this.start_time,
        end_time: this.end_time
      }
      //   this.proxmox_server.push(this.datos)
      // eslint-disable-next-line no-unused-vars
      const data = await this.$axios.post(
        'http://10.8.1.231:8000/zabb_conf',
        this.datos
        // eslint-disable-next-line semi
      );
    }
    // async service () {
    //   this.datos = {
    //     ip: this.ip,
    //     usuario: this.usuario,
    //     password: this.password,
    //     user_new: this.user_new,
    //     user_actual: this.user_actual,
    //     start_time: this.start_time,
    //     end_time: this.end_time
    //   }
    //   //   this.proxmox_server.push(this.datos)
    //   // eslint-disable-next-line no-unused-vars
    //   const data = await this.$axios.post(
    //     // eslint-disable-next-line quotes
    //     "http://api-lilipad.cujae.edu.cu:8000/services",
    //     this.datos
    //     // eslint-disable-next-line semi
    //   );
    // }
  }
}

</script>
