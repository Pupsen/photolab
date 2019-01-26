<template>
  <div class="hello">
    <button v-if="false" @click="getTime()">GETTIME</button>
    <video v-if="url" id="video" height="768" width="1280" controls>
      <source :src="url" type="video/mp4"></source>
    </video>
    <form id="uploadForm" name="uploadForm" enctype="multipart/form-data">

      <input type="file" id="file" name="file" multiple><br>

      <input type=button value=Upload @click="this.uploadFiles">

    </form>
  </div>
</template>

<script>
  import axios from 'axios'

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
    data() {
      return {
          input: '',
          url: ''
      }
    },
    methods: {
      getTime() {
          var vid = document.getElementById("video");
          console.log(vid.currentTime)
      },
      getURL() {
          this.url = this.input;
      },
      uploadFiles () {
          var s = this
          const data = new FormData(document.getElementById('uploadForm'))
          var imagefile = document.querySelector('#file')
          this.url = imagefile.files[0]
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
