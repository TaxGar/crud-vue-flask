<script>
import axios from "axios";
export default {
  name: 'App',
  data() {
    return {
      mensaje: 'Nuevo mensaje desde Vue Js'
    }
  },
  methods: {
    getMensaje () {
      const path = 'http://localhost:5000/mensaje'
      axios.get(path).then((respuesta)=>{
        this.mensaje = respuesta.data
      })
      .catch((error)=>{
        console.error(error);
      })
    }
  },
  created (){
    this.getMensaje()
  },
}
</script>

<template>

  <div class="container">
    <button type="button" class="btn btn-primary">{{ mensaje }}</button>
  </div>

</template>

<style scoped>

</style>
