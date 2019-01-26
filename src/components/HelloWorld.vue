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
    <social-sharing url="vk.com/id0"
                    title="Найдём эту мразь"
                    description="блин блинский до новго года 5 минут"
                    quote="Как говорил джейсон стэтэм: 'Мой отец твой дед, здравствуй сын!'"
                    hashtags="тугосеря, пропукиваться"
                    @open="onOpen"
                    inline-template>
      <div>
        <network network="facebook">
          <i class="fa fa-facebook"></i> Facebook
        </network>
      </div>
    </social-sharing>
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
          url: '',
          actions: [
            {start: 4.5, end: 5.7, type: 'refraction'},
            {start: 6.5, end: 6.7, iters: 4, type: 'loop'},
            {start: 7, end: 7.15, type: 'reverse'},
            {start: 11.40, end: 11.80, type: 'reverse'},
            {start: 11.59, end: 11.80, type: 'reverse'},
            {start: 11.70, end: 11.90, type: 'reverse'}
            ]
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
            const data = new FormData();
            var imagefile = document.querySelector('#file');
            data.append('file', imagefile.files[0]);
            data.append('actions', this.actions);
            axios.post('http://test1488.us-east-2.elasticbeanstalk.com/api/video', data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                    console.log(error.response)
            })
        },
        onOpen(nw, url) {
          console.log(nw)
          console.log(url)
        }
    }
}
</script>

