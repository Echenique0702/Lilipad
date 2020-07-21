<template>
  <v-card>
    <v-card-title>
      Tabla Futura
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
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
        { text: 'RAM_avg(kb)', value: 'ram_avg' },
        { text: 'RAM_95p(kb)', value: 'ram_95p' },
        { text: 'RAM_max(kb)', value: 'ram_max' },
        { text: 'Disco_avg(kB)', value: 'disk_avg' },
        { text: 'Disco_95p(kB)', value: 'disk_95p' },
        { text: 'Disco_max(kB)', value: 'disk_max' },
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
        { text: 'Read_95p(kB/s)', value: 'read_95p' },
        { text: 'Write_avg(kB/s)', value: 'write_avg' },
        { text: 'Write_95p(kB/s)', value: 'write_avg' },
        { text: 'Write_95p(kB/s)', value: 'write_95p' }

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
      this.items = await this.$axios.$get('http://10.8.1.231:8000/futura')
    }
  }
}
</script>
