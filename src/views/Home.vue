<template>
  <div class="home">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue'
import axios from 'axios'

export default {
  name: 'home',
  components: {
    HelloWorld
  },
    mounted() {
      axios.get('http://test1488.us-east-2.elasticbeanstalk.com/api/video')
    }

}
</script>
