<template>
  <v-app>
    <v-main>
      <!-- 화면 상단바 메뉴   -->
      <div class="menu">
        <!-- <a v-for="(menu_name, i) in menus" :key="i">{{ menu_name }}</a> -->
        <v-btn v-for="(menu_name, i) in menus" :key="i" class="btn_st" color="white--text" rounded elevation="2" @click="fetchData()">{{ menu_name }}</v-btn>
      </div>
      <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData()">LOAD</v-btn>
      <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData_wait()">WAIT</v-btn>
      <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData()">SAVE</v-btn>
      <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData()">HOLD</v-btn>
      <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData()">CLOSE</v-btn>
      
      <!-- 리스트 출력 -->
      <div v-for="(job_info, i) in job_group" :key="i">
        <!-- 회사명 출력 -->
        <h3 class="text-sm-left">{{job_info[0].company}}</h3>
        <!-- 채용공고 출력 -->
        <p class="job_str" align="left" v-for="(job, j) in job_info" :key="j"> {{job.title}}
        <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="update_func(job_info[0].company, j, 1)">Save</v-btn>
        <v-btn color=white rounded elevation="2" @click="update_func(job_info[0].company, j, 2)">Hold</v-btn>
        <v-btn color=white rounded elevation="2" @click="update_func(job_info[0].company, j, 3)">Close</v-btn>
        </p>
      </div>
    </v-main>
  </v-app>
</template>


<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      menus : ['All', 'Wait', 'Save', 'Hold', 'Close'],
      job_group : 0,
      modal_status : false,
      test_title : '',

    }
  },
  methods : {
    update_func(edit_company, edit_num, status_num) {
      this.edit_company = edit_company;
      this.edit_num = edit_num;
      this.edit_status = status_num;
      
      axios.get("http://127.0.0.1:8000/update_item/", {
        params: {
          str_company: String(this.edit_company),
          job_list: Number(this.edit_num),
          status: Number(this.edit_status),
        }
      })
      .then(function (response) {
        console.log(response)
        }).catch(function (error) {
          console.log(error)
          }).then(function() {
            // 항상 실행
            });
    },
    fetchData: function() {
              axios.get('http://127.0.0.1:8000/return_info/').then((response) => {
                console.log(response.data);
                this.job_group = Object(response.data);
              })
              .catch(function(error) {
                console.log(error);
              });
    },
    fetchData_wait: function() {
              axios.get('http://127.0.0.1:8000/return_info/', {
                params: {
                  status: Number(4)
                }
              }).then((response) => {
                console.log(response.data);
                this.job_group = Object(response.data);
              })
              .catch(function(error) {
                console.log(error);
              });
    },
    sendData: function() {
      axios.get("http://127.0.0.1:8000/update_item/?str_company='삼성전자'&job_list=0&status=1")
                
              .then(function (response) {
                  console.log(response)
              }).catch(function (error) {
                  console.log(error)
              }).then(function() {
                  // 항상 실행
              });
              
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
  margin-left: 80px;
}

.btn_st {
  margin-left: 20px;
}
</style>
