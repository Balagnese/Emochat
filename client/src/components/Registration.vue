<template>
<div class="container">
  <div>
    <div class="topnav">
      <a v-on:click="navButtonClick" >{{buttonText}}</a>
    </div>
  <br><br><br><br><br><br>
    <div class="row">
      <div class="col">

        <h1>Регистрация</h1>
        <hr><br><br>
        <p>{{ msg }}</p>
        <div>
          <input v-model="email" type="email" name="email" placeholder="Email" autofocus="">
        </div>
        <br>
        <div>
          <input v-model="name" type="email" name="email" placeholder="Имя" autofocus="">
        </div>
        <br>
        <div>
          <input v-model="password" type="password" name="password" placeholder="Пароль">
        </div>
        <br>
        <div>
          <input v-model="repeatedPassword" type="password" name="password" placeholder="Повторите пароль">
        </div>
        <br>
        <!--<button @click="ping" type="button" class="btn btn-primary btn-lg">Зарегистрироваться</button>-->
        <button @click="signup" type="button" class="btn btn-primary btn-lg">Зарегистрироваться</button>
        <br><br>

      </div>
    </div>
  </div>
    </div>
</template>

<script>
    export default {
      name: "Registration",
      data() {
        return {
          msg: '',
          email: '',
          name: '',
          password: '',
          repeatedPassword: '',
          buttonText: 'Войти'
        };
      },
      sockets: {
        connect: function () {
          console.log('socket connected')
        },
        // customEmit: function (data) {
        //   console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
        // }
      },
      mounted() {
        this.sockets.subscribe('message', (data) => {
          console.log(data.message);
          this.messages = data;
        });
        this.sockets.subscribe('registration_response', (data) => {
          if (data.code == 200){
            this.$router.push('/signin');
          }
          else{
            this.msg=data.message;
          }
        });
      },
      methods: {
        getColor(col) {
          return {color: col}
        },
        signup() {
          if (this.email == ""){
            this.msg = "Введите email";
            return
          }
          if (this.name == ""){
            this.msg = "Введите имя";
            return
          }
          if (this.password == ""){
            this.msg = "Введите пароль";
            return
          }
          if (this.repeatedPassword == ""){
            this.msg = "Повторите пароль";
            return
          }
          if (this.password.localeCompare(this.repeatedPassword) != 0){
            this.msg = "Пароли не совпадают";
            return
          }

          this.$socket.emit('registration', {
            "email": this.email,
            "name": this.name,
            "password": this.password
          });
        },
        navButtonClick(){
          this.$router.push('/signin')
        }
      }
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
