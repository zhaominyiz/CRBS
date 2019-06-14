<template>
  <div id="app">
    <div class="layout" :class="{'layout-hide-text': spanLeft < 5}">
      <div class="layout-ceiling">
            <div class="layout-ceiling-main">
                <a href="#" v-if="usr!=null" @click="logout">退出</a>
                <a href="#" v-else @click="showSignup">注册</a> |
                <a href="#" v-if="usr!=null">{{ usr }}</a>
                <a href="#" v-else @click="showLogin">登录</a>
<!--                <a href="#" @click="showSignup">注册</a> |-->
<!--                <a href="#" @click="showLogin" >登录</a>-->
            </div>
        </div>
        <Row type="flex">
            <Col :span="spanLeft" class="layout-menu-left">
                <Menu :active-name="currentMenu" theme="dark" width="auto" @on-select="navigate">
                    <Menu-item name="newtask">
                        <Icon type="ios-navigate" :size="iconSize"></Icon>
                        <span class="layout-text">新建任务</span>
                    </Menu-item>
                    <Menu-item name="history">
                        <Icon type="ios-keypad" :size="iconSize"></Icon>
                        <span class="layout-text">重构记录</span>
                    </Menu-item>
                    <Menu-item name="userInfo">
                        <Icon type="ios-analytics" :size="iconSize"></Icon>
                        <span class="layout-text">用户信息</span>
                    </Menu-item>
                </Menu>
            </Col>
            <i-col :span="spanRight">
                <div class="layout-content">
                    <div class="layout-content-main">
                        <router-view></router-view>
                    </div>
                </div>
                <div class="layout-copy">
                    2018-2019 &copy; NJUST Fishteam
                </div>
            </i-col>
        </Row>
      </div>
      <Modal v-model="loginModal"
        title="用户登录"
        :width="400"
        ok-text="登录"
        @on-ok="login"
      >
      <Form :model="loginForm">
        <Form-item prop="user">
            <Input type="text" v-model="loginForm.user" placeholder="Username">
                <Icon type="ios-person-outline" size="22px" slot="prepend"></Icon>
            </Input>
        </Form-item>
        <Form-item prop="password">
            <Input type="password" v-model="loginForm.password" placeholder="Password">
                <Icon type="ios-locked-outline" slot="prepend"></Icon>
            </Input>
        </Form-item>
        <!--<Form-item>-->
            <!--<Button type="primary" @click="handleSubmit('formInline')">登录</Button>-->
        <!--</Form-item>-->
    </Form>
      </Modal>

    <Modal v-model="signupModal"
        title="用户注册"
        :width="400"
        ok-text="注册"
        @on-ok="signup"
      >
      <Form :model="signupForm">
        <Form-item prop="user">
            <Input type="text" v-model="signupForm.user" placeholder="Username">
                <Icon type="ios-person-outline" size="22px" slot="prepend"></Icon>
            </Input>
        </Form-item>
        <Form-item prop="password">
            <Input type="password" v-model="signupForm.password" placeholder="Password">
                <Icon type="ios-locked-outline" slot="prepend"></Icon>
            </Input>
        </Form-item>
        <!--<Form-item>-->
            <!--<Button type="primary" @click="handleSubmit('formInline')">登录</Button>-->
        <!--</Form-item>-->
    </Form>
      </Modal>

  </div>
</template>

<script>

export default {
  name: 'app',
  data () {
      return {
          spanLeft: 5,
          spanRight: 19,
          usr:sessionStorage.getItem('username'),
          loginModal: false,
          loginForm: {
              user: '',
              password: '',
          },
          signupModal: false,
          signupForm:{
              user: '',
              password: '',
          }
      }
  },
  computed: {
    iconSize () {
        return this.spanLeft === 5 ? 14 : 24;
    },
    currentMenu () {
        // '/history/detial' => history
        return this.$route.path.split('/')[1]
    }
  },
  methods: {
    showLogin () {
        this.loginModal = true
    },
    login () {
        this.$store.dispatch('login', {userName: this.loginForm.user,
             password: this.loginForm.password, vm: this})
    },
    logout () {
        sessionStorage.removeItem('username')
        this.$Message.success("您已登出")
        var t = setTimeout(function(){window.location.reload();},1000);
    },
    navigate (path) {
        this.$router.push('/' + path + '/')
    },
    showSignup(){
      this.signupModal = true
    },
    signup(){
      this.$store.dispatch('signup', {userName: this.signupForm.user,
             password: this.signupForm.password, vm: this})
    }

  },
}
</script>

<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: hidden;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 480px;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        padding: 10px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .layout-menu-left{
        background: #464c5b;
    }
    .layout-header{
        height: 60px;
        background: #fff;
        box-shadow: 0 1px 1px rgba(0,0,0,.1);
    }
    .layout-logo-left{
        width: 90%;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        margin: 15px auto;
    }
    .layout-ceiling-main a{
        color: #9ba7b5;
    }
    .layout-hide-text .layout-text{
        display: none;
    }
    .ivu-col{
        transition: width .2s ease-in-out;
    }
    .layout-ceiling{
        background: #464c5b;
        padding: 12px 0;
        overflow: hidden;
    }
    .layout-ceiling-main{
        float: right;
        margin-right: 18px;
    }
    .layout-ceiling-main a{
      font-size: 14px;
        color: #9ba7b5;
    }
</style>
