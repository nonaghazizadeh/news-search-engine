<template>
<div>
  <div class="row column header">
    <h1 class="cover-heading">{{headerTitle}}</h1>
    <div class="medium-6 medium-offset-3 ctrl">
      <div class="searchForm">
        <input type="text" v-model="searchQuery" placeholder="Enter your title to find its category">
      </div>
      <a class="raised-button ink" @click="submitSearch">Search</a>
    </div>
  </div>
    <div>
    <b-button class="modal-button" v-b-modal.eval-modal>Evaluation Criteria</b-button>
    <b-modal id="eval-modal" hide-footer>
        <p class="mb-4 ml-4">accuracy score: {{accuracyScore}}</p>
        <p class="mt-4 ml-4">f1 macro: {{f1Macro}}</p>
    </b-modal>
  </div>
</div>
</template>

<script>
export default {
  name: 'ClassificationTransformers',
  data(){
    return{
      headerTitle: "Classification based on transformers",
      searchQuery: '',
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

input[type="text"]:focus {
  border: none;
  border-bottom: 2px solid #201c34;
  box-shadow: none;
  position: relative;
  top: 1px;
  background: transparent;
}
.modal-button {
    position: absolute;
    right: 0;
    bottom: 0;
    margin-bottom: 5px;
    margin-right: 5px;
    color: #fff !important;
    background-color: #201c34 !important;
    border-color: transparent;
    outline: none;
    box-shadow: none;
}

.modal-button:hover, .modal-button:focus, .modal-button:active{
    border-color: transparent;
    outline: none;
    box-shadow: none;
}

.close {
    background-color: #fff;
    border: none;
    color: #201c34;
}
</style>
