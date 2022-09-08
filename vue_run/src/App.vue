<template>
  <v-app>
    <v-main>
      <!-- 화면 상단바 메뉴   -->
      <div class="menu">
        <!-- <a v-for="(menu_name, i) in menus" :key="i">{{ menu_name }}</a> -->
        <!-- <v-btn v-for="(menu_name, i) in menus" :key="i" class="btn_st" color="white--text" rounded elevation="2" @click="fetchData(i+1)">{{ menu_name }}</v-btn> -->
        <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData(1)">ALL</v-btn>
        <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData(2)">WAIT</v-btn>
        <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData(3)">SAVE</v-btn>
        <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData(4)">HOLD</v-btn>
        <v-btn class="btn_st" color="white--text" rounded elevation="2" @click="fetchData(5)">CLOSE</v-btn>
        <p></p>
        <v-p class="num_status">{{num_status_all}}</v-p>
        <v-p class="num_status">{{num_status_wait}}</v-p>
        <v-p class="num_status">{{num_status_save}}</v-p>
        <v-p class="num_status">{{num_status_hold}}</v-p>
        <v-p class="num_status">{{num_status_close}}</v-p>
      </div>
           
      <!-- 리스트 출력 -->
      <div v-for="(job_info, i) in job_group" :key="i">


        <!-- 회사명 출력 -->
        <p class="company_str" align="left">
          <a v-bind:href=job_info[0].company_link target="_blank" style="text-decoration:none;color:black;">
            <h2 class="text-sm-left">{{job_info[0].company}}</h2>
          </a>
            <!-- <v-btn class="btn_st_title" rounded elevation="2" @click="update_all_func(job_info[0].company, 5)">All Close</v-btn> -->
            <v-btn
              depressed 
              tile
              color="primary"
              class="btn_st_company_title"
              rounded elevation="2"
              @click="update_all_func(job_info[0].company, 5)">
              All Close
            </v-btn>
        </p>
       
        <!-- 채용공고 출력 -->
        <p class="job_str" align="left" v-for="(job, j) in job_info" :key="j">
          <a v-bind:href=job_info[j].title_link target="_blank" class="job_str2" style="text-decoration:none;color:black;">
             {{job.title}}
          </a>

        <!-- 리스트 내 버튼 클릭 -->
        <v-btn class="btn_st_title" rounded elevation="2" @click="update_func(job_info[j].company, job_info[j].title_idx, 3)">Save</v-btn>
        <v-btn class="btn_st_title" rounded elevation="2" @click="update_func(job_info[j].company, job_info[j].title_idx, 4)">Hold</v-btn>
        <v-btn class="btn_st_title" rounded elevation="2" @click="update_func(job_info[j].company, job_info[j].title_idx, 5)">Close</v-btn>
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
      num_status_all : 0,
      num_status_wait : 0,
      num_status_save : 0,
      num_status_hold : 0,
      num_status_close : 0,
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
    update_all_func(edit_company) {
      this.edit_company = edit_company;
      
      axios.get("http://127.0.0.1:8000/update_all_item/", {
        params: {
          str_company: String(this.edit_company),
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
    fetchData: function(status_num) {
              axios.get('http://127.0.0.1:8000/return_info/', {
                params: {
                  status: Number(status_num)
                }
              }).then((response) => {
                console.log(response.data);
                this.job_group = Object(response.data);
              })
              .catch(function(error) {
                console.log(error);
              });

              axios.get('http://127.0.0.1:8000/return_info_num/', {
                params: {
                
                }
              }).then((response) => {
                console.log(response.data);
                this.num_status_all = response.data.all
                this.num_status_wait = response.data.wait
                this.num_status_save = response.data.save
                this.num_status_hold = response.data.hold
                this.num_status_close = response.data.close
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
.company_str {
  padding: 10px;
  margin-left: 40px;
}
.btn_st {
  margin: 10px;
  width: 100px;
}
.btn_st_company_title {
  margin: 5px;
  margin-left: 10px;
}
.btn_st_title {
  margin: 5px;
}
.num_status {
  margin-top: 10px;
  color: white;
  margin: 55px;
}
.job_str2 {
  margin-right: 20px;
}
</style>
