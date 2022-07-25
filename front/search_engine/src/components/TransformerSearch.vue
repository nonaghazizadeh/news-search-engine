<template>
  <div class="row column header">
    <h1 class="cover-heading">{{headerTitle}}</h1>
    <div class="medium-6 medium-offset-3 ctrl">
      <div class="searchForm">
        <div style="float:right">
        <input class="input-container" 
        type="text" 
        v-model="searchQuery" 
        placeholder="متن جستجو خود را بنویسید..."
        >
        </div>
        <div style="float:right">
        <a class="raised-button ink" @click="search">
          <b-icon icon="search" aria-hidden="true"></b-icon>
        </a>
        </div>
      </div>
    </div>
          <div>
    <b-form-checkbox dir="rtl" v-model="checked" name="check-button" switch>
      گسترش کوئری
    </b-form-checkbox>
  </div>
      <div v-if="loading" class="d-flex justify-content-center mb-3">
    <b-spinner></b-spinner>
  </div>
    <ul class="data-results">
      <li :v-show="showResults" v-for="(value, key) in info" :key="key">
        <p :class="[Object.keys(info).length - 1 == key ? '' : 'outset']"> 
          <a class='title-results' :href="value.link" > {{value.title}}</a>
        </p>
      </li>
    </ul>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);

export default {
  name: 'TransformerSearch',
  data(){
    return{
      headerTitle: "Transformer Search",
      searchQuery: '',
      info: [],
      showResults: false,
      loading: false,
      checked: false

    }
  },
  methods: {
    search(){
    this.info = []
    this.loading = true;
    let api = "http://127.0.0.1:8000/search?model=transformer&query=" + this.searchQuery
                  + "&qe_en=" + this.checked
    Vue.axios.get(api)
      .then(response => {
        this.info = response.data;
        this.showResults = true;
        this.loading = false;
      })
    }
  }
}
</script>

<style>
.ctrl {
  margin-bottom: 1.6rem;  
}

.header {
  color: #201c34;
  height: 100%;
  text-align: center;
  padding-top: 5px;
  padding-left: 200px;
  padding-right: 100px;
}

.header .cover-heading {
  font-size: 40px;
  color: #201c34;
  margin-top: 1.6rem;
  margin-bottom: 1.6rem;
}

.searchForm {
  margin-bottom: 2.6rem;
  position: relative;  
}

.raised-button {
    display: inline-block;
    text-align: center;
    line-height: 1;
    cursor: pointer;
    -webkit-appearance: none;
    transition: all 0.25s ease-out;
    vertical-align: middle;
    border: 1px solid transparent;
    border-radius: 0.25rem;
    padding: 0.85em 1em;
    margin: 0 1rem 1rem 0;
    font-size: 0.9rem;
    background: #201c34;
    color: #FAFAFA;
    text-decoration: none;
}
.raised-button:hover, .raised-button:focus {
    background: #fff;
    color: #201c34;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.5), 0 1px 5px 0 rgba(0, 0, 0, 0.5);
}

input:focus { 
  outline:none; 
}

[type="text"] {
    display: block;
    box-sizing: border-box;
    width: 100%;
    height: 2.4375rem;
    padding: 0.5rem;
    border: 0;
    margin: 0 0 1rem;
    font-family: inherit;
    font-size: 1rem;
    color: #201c34;
    background-color: white;
    box-shadow: none;
    border-radius: 0;
    transition: box-shadow 0.5s, border-color 0.25s ease-in-out;
    -webkit-appearance: none;
    -moz-appearance: none;
}
input[type="text"]{
  padding: 1rem 0 0.5rem 0;
  margin: 1.75rem 0 0.5rem;
  border-bottom: 1px solid #e0e0e0;
  border-radius: 0;
  background: transparent;
}
</style>
