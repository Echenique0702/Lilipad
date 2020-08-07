<template>
  <v-app>
  <v-card>
    <v-card-title>
      Tabla Actual
      <v-spacer />
      <v-text-field
        v-model="search"
        label="Filtrar"
        single-line
        hide-details
      />
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="items"
      :search="search"
    />
  </v-card>
  </v-app>

</template>

<script>
export default {
  layout: 'general_layout',
  data () {
    return {
      search: '',
      headers: [
        {
          text: 'Nombre',
          align: 'left',
          sortable: false,
          value: 'name'
        },
        { text: 'Hipervisor', value: 'hipervisor' },
        { text: 'Service', value: 'service' },
        { text: 'Server', value: 'server' },
        { text: 'CPU_avg(%)', value: 'cpu_avg' },
        { text: 'CPU_95p(%)', value: 'cpu_95p' },
        { text: 'CPU_max(%)', value: 'cpu_max' },
        { text: 'RAM_avg(GB)', value: 'ram_avg' },
        { text: 'RAM_95p(GB)', value: 'ram_95p' },
        { text: 'RAM_max(GB)', value: 'ram_max' },
        { text: 'Disco_avg(GB)', value: 'disk_avg' },
        { text: 'Disco_95p(GB)', value: 'disk_95p' },
        { text: 'Disco_max(GB)', value: 'disk_max' },
        { text: 'Incoming_avg(Mbps)', value: 'inco_avg' },
        { text: 'Incoming_95p(Mbps)', value: 'inco_95p' },
        { text: 'Incoming_max(Mbps)', value: 'inco_max' },
        { text: 'Outcoming_avg(Mbps)', value: 'outc_avg' },
        { text: 'Outcoming_95p(Mbps)', value: 'outc_95p' },
        { text: 'Outcoming_max(Mbps)', value: 'outc_max' },
        { text: 'Iostat_avg(tps)', value: 'iost_avg' },
        { text: 'Iostat_95p(tps)', value: 'iost_95p' },
        { text: 'Iostat_max(tps)', value: 'iost_max' },
        { text: 'Read_avg(kB/s)', value: 'read_avg' },
        { text: 'Read_95p(kB/s)', value: 'read_95p' },
        { text: 'Read_max(kB/s)', value: 'read_max' },
        { text: 'Write_avg(kB/s)', value: 'write_avg' },
        { text: 'Write_95p(kB/s)', value: 'write_95p' },
        { text: 'Write_max(kB/s)', value: 'write_max' }
      ],
      items: []
    }
  },
  mounted () {
    setInterval(this.actual, 5000)
  },
  methods: {
    // async proxys () {
    //   const data = await this.$axios.$post('http://api-lilipad.cujae.edu.cu:8000/services', this.Proxys)
    //   console.log(data)
    // },
    async actual () {
      this.items = await this.$axios.$get('http://10.8.1.231:8000/actual')
    }
  }
}
</script>
