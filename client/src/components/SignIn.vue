<template>
  <div class="container">

    <div class="topnav">
      <a v-on:click="navButtonClick">{{buttonText}}</a>
    </div>
    <br><br><br><br><br><br>
    <div class="row">
      <div class="col">
        <h1>Вход</h1>
        <hr><br><br>
        <p>{{ msg }}</p>
        <div>
          <input v-model="email" type="email" name="email" placeholder="Email" autofocus="">
        </div>
        <br>
        <div>
          <input v-model="password" type="password" name="password" placeholder="Пароль">
        </div>
        <br>
        <div>
          <input v-model="checked" type="checkbox" id="checkbox"> Запомнить меня
        </div>
        <br>
        <button v-on:click="signIn" type="button" class="btn btn-primary btn-lg">Войти</button>
        <br><br>

        <div>
          Нет аккаунта?
          <button v-on:click="getRegistrationComponent" type="button" class="btn btn-link">Зарегистрироваться</button>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
    export default {
      name: "SignIn",
      sockets: {
        connect: function () {
          console.log('socket connected')
        }
      },
      data() {
        return {
          checked: true,
          email: "",
          password: "",
          buttonText: 'Войти',
          msg: ''
        };
      },
      methods: {
        getRegistrationComponent() {
          this.$router.push('/registration');
        },
        signIn() {
          if (this.email == "") {
            this.msg = "Введите email";
            return
          }
          if (this.password == "") {
            this.msg = "Введите пароль";
            return
          }

          this.$socket.emit('login', {
            "email": this.email,
            "password": this.password,
            "remember": this.checked
          });
        },
        navButtonClick(){

        }
      },
      mounted() {

        this.sockets.subscribe('login_response', (data) => {
          //console.log(data)
          if (data.code == 200) {
            console.log(data);
            localStorage.setItem('userId', data.user.id);
            localStorage.setItem('name', data.user.name);
            localStorage.setItem('email', data.user.email);
            this.$router.push('/chat')
          }
          else {
            this.msg = "Не удалось войти";
          }
        });
      },


    }
</script>

<style scoped>
  /* Add a black background color to the top navigation */
.topnav {
  background-color: #0056b3;
  overflow: hidden;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}

/* Style the links inside the navigation bar */
.topnav a {
  float: right;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
  cursor: pointer;
}

/* Change the color of links on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
  background-color: #4CAF50;
  color: white;
}
</style>
