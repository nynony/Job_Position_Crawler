<template>
  <v-app>
    <v-main>
      <!-- 화면 상단바 메뉴   -->
      <div class="menu">
        <a v-for="(menu_name, i) in menus" :key="i">{{ menu_name }}</a>
      </div>
      <!-- 리스트 출력 -->
      <div v-for="(job_info, i) in job_group" :key="i">
        <!-- 회사명 출력 -->
        <h3 class="text-sm-left">{{job_info[0].company}}</h3>
        <!-- 채용공고 출력 -->
        <p class="job_str" align="left" v-for="(job, j) in job_info" :key="j"> {{job.title}}
        <v-btn color=white elevation="2" @click="fetchData(job_info[0].company, j)">Save</v-btn>
        <v-btn color=white elevation="2" @click="hold_func(job_info[0].company, j)">Hold</v-btn>
        <v-btn color=white elevation="2" @click="close_func(job_info[0].company, j)">Close</v-btn>
        </p>
      </div>
    </v-main>
  </v-app>
</template>


<script>

import jsonData from '../../config/job_group.json';
import axios from 'axios'




export default {
  name: 'App',
  data() {
    return {
      menus : ['All', 'Wait', 'Save', 'Hold', 'Close'],
      job_group : jsonData,
      modal_status : false,
      test_title : '',
    }
  },
  methods : {
    save_func(edit_company, edit_num) {
      this.edit_company = edit_company;
      this.edit_num = edit_num;
      console.log(this.edit_company);
      console.log(this.edit_num);
      console.log(this.job_group[this.edit_company][this.edit_num].title);
    },
    hold_func(edit_company, edit_num) {
      this.edit_company = edit_company;
      this.edit_num = edit_num;
      console.log(this.edit_company);
      console.log(this.edit_num);
    },
    close_func(edit_company, edit_num) {
      this.edit_company = edit_company;
      this.edit_num = edit_num;
      console.log(this.edit_company);
      console.log(this.edit_num);
      console.log(this.job_group[this.edit_company][this.edit_num].title);
      this.job_group[this.edit_company][this.edit_num].status = 'save';
      console.log(this.job_group[this.edit_company][this.edit_num].status)
    },
    fetchData: function() {
              axios.get("http://127.0.0.1:8000/return_info_len/")
                .then(function(response) {
                console.log(response);
                })
                .catch(function(error) {
                console.log(error);
                });
              
              // axios.get('http://127.0.0.1:8000/return_info_len/')
              // .then(function(response) {
              // console.log(response);
              // })
              // .catch(function(error) {
              // console.log(error);
              // });
            },
    },

  components: {

  }
}


</script>



<style>
body {
    margin: 0
}
div {
  box-sizing: border-box;
}
.black-bg {
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
  position: fixed; padding: 20px;
}
.white-bg {
  width: 100%; background: white;
  border-radius: 8px;
  padding: 20px;
}



#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

.menu {
  background: darkslateblue;
  padding: 15px;
  border-radius: 5px;
}

.menu a{
  color: white;
  padding: 20px;
}

.text-sm-left {
  margin-top: 30px;
  margin-left: 20px;
  padding: 10px;
  
}
.job_str {
  padding: 10px;
  margin-left: 50px;
}
</style>
