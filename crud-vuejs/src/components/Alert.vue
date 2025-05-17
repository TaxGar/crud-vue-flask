<script>
export default {
  name: 'App',
  props: ['message'],
};
</script>

<template>

  <div class="">
    <div class="alert alert-success" role="alert">{{ message }}</div>
    <br />
  </div>

</template>
