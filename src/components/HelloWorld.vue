<template>
  <div class="hello">
    <form id="uploadForm" name="uploadForm" enctype="multipart/form-data">

      <input type="file" id="file" name="file" multiple><br>

      <input type=button value=Upload @click="this.uploadFiles">

    </form>
    <div v-if="loading">Загрузка</div>
    <video v-if="urlFunky && !loading && !editing" id="videoFunky" controls>
      <source :src="urlFunky" type="video/mp4"></source>
    </video>
    <div>
      <button v-if="urlBase" @click="modify">МОДИФАНУТЬ</button>
      <button v-if="urlBase" @click="addAction('reverse')">Ревёрс</button>
      <button v-if="urlBase" @click="addAction('loop')">Луп</button>
      <button v-if="urlBase" @click="addAction('reflect'  )">Рефлект</button>
      <button v-if="urlBase" @click="addAction('random')">Случайный</button>
      <social-sharing v-if="urlFunky" url="vk.com/id0"
                      title="блин блинский до новoго года 5 минут"
                      description="Если вы читаете это, то вы 10 лет лежите в коме, пожалуйста, просыпайтесь, родные вас ждут"
                      quote="Как говорил джейсон стэтэм: 'Мой отец твой дед, здравствуй сын!'"
                      hashtags="мойсыночек"
                      inline-template>
        <div>
          <network network="facebook">
            <i class="fa fa-facebook"></i> <b>ПОСТАНУТЬ В ФЭЙСБУЧКУ</b>
          </network>
        </div>
      </social-sharing>
    </div>
    <div v-if="urlBase">
      <div v-for="(action, idx) in actions">
        {{action.random ? 'Рандом: ' : action.type + ': '}}  Начало {{action.start}} {{action.random ? '' : 'Конец ' + action.end + ': '}} {{!action.random && action.type === 'loop' ? 'Повторов ' + action.count : ''}}
        <div @click="removeAction(idx)">X</div>
      </div>
    </div>
    <div v-if="editing">Обрабатывается</div>
    <video v-if="urlBase && !loading" id="video" controls>
      <source :src="urlBase" type="video/mp4"></source>
    </video>
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
          urlBase: '',
          urlFunky: '',
          loading: false,
          editing: false,
          actions: [
            ]
          }
    },
    methods: {
      addAction(inType) {
          const time = document.getElementById("video").currentTime;
          const data = {
              start: time,
              end: time + 0.20,
              count: 4,
              type: inType
          };
          if (inType === 'reflect')
              data.end += 0.30
          if (inType === 'random') {
              data.random = true
              const rand = Math.random();
              if (rand < 0.3) data.type = 'reflect'
              else if (rand < 0.65) data.type = 'loop'
              else data.type = 'reverse'
          }
          this.actions.push(data);
      },
      removeAction(index) {
          this.$delete(this.actions, index)
      },
        uploadFiles () {
            var s = this
            const data = new FormData();
            var imagefile = document.querySelector('#file');
            data.append('file', imagefile.files[0]);
            this.loading = true;
            this.actions = [];
            axios.post('http://localhost:8000/api/video', data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(function(response) {
                this.urlFunky = '';
                this.loading = false;
                this.urlBase = response.data.url.substring(40)
            }.bind(this))
            .catch(error => {
                    console.log(error.response)
            })
        },
        modify(isRandom) {
          const data = {
              url: this.urlBase,
              actions: this.actions
          };
          this.editing = true
            this.urlFunky = '';

            axios.post('http://localhost:8000/api/apply', data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(function(response) {
                    this.urlFunky = response.data.url.substring(40)
                    this.editing = false;
                }.bind(this))
                .catch(error => {
                console.log(error.response)
        })
        }
    }
}
</script>

