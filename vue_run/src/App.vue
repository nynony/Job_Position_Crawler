<template>
  
  <div class="black-bg" v-if="modal_status == true">
    <div class="white-bg">
      <h4>상세페이지</h4>
      <p>상세페이지 내용</p>
      <button @click="modal_status=false">닫기</button>
    </div>
  </div>

  <!-- 화면 상단바 메뉴   -->
  <div class="menu">
    <a v-for="(menu_name, i) in menus" :key="i">{{ menu_name }}</a>
  </div>


<!-- 리스트 출력 -->
  <div v-for="(job_info, i) in job_group" :key="i">
    <!-- 회사명 출력 -->
    <h4>{{job_info[0].company}}</h4>
    <!-- 채용공고 출력 -->
    <p v-for="(job, j) in job_info" :key="j"> {{job.title}}
    <button type="button" @click="save_func(job_info[0].company, j)">Save</button>
    <button type="button" @click="hold_func(job_info[0].company, j)">Hold</button>
    <button type="button" @click="close_func(job_info[0].company, j)">Close</button>
    </p>
    
  </div>

</template>

<script>

import jsonData from '../../config/job_group.json';


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
      console.log(this.job_group[this.edit_company][this.edit_num].title);
    },
    close_func(edit_company, edit_num) {
      this.edit_company = edit_company;
      this.edit_num = edit_num;
      console.log(this.edit_company);
      console.log(this.edit_num);
      console.log(this.job_group[this.edit_company][this.edit_num].title);
    }
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
  padding: 10px;
}
</style>
