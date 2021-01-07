<template>
  <div class="container">
    <div class="topnav">
      <a v-on:click="navButtonClick" >{{buttonText}}</a>
    </div>


    <table width="100%" cellpadding="5">
      <tr>
        <td style='background:#F0F8FF;' valign="top" width="20%" height="800px">

          <h1>Беседы</h1>
          <hr>
          <div class="row">
            <div class="col">
              <div class="roomButton" v-on:click="showCreatingRoomComponent"> Создать </div>
              <!--<button class="btn btn-primary btn-lg" v-on:click="showCreatingRoomComponent">Создать</button>-->
            </div>
            <div class="col">
              <div class="roomButton" v-on:click="showSearchingRoomComponent"> Искать </div>
               <!--<button class="btn btn-primary btn-lg" v-on:click="showSearchingRoomComponent">Искать</button>-->
            </div>
          </div>

          <div v-show="isCreatingRoomComponentVisible">
            <br>
            <input v-model="creatingRoomName" name="roomName" placeholder="Название беседы">
            <button v-on:click="createRoom"> Создать</button>
          </div>
          <div v-show="isSearchingRoomComponentVisible">
            <br>
            <input v-model="searchingRoomName" name="roomName" placeholder="Название беседы">
            <button v-on:click="getRoomsByName"> Искать</button>
          </div>

          <br v-show="isSearchedRoomsComponentVisible">
          <h4 v-show="isSearchedRoomsComponentVisible">Результаты поиска:</h4>
          <div class="roomTable" v-show="isSearchedRoomsComponentVisible">
            <table v-for="(room, id) in searchedRooms" v-bind:key="id"   >
              <tr align="center" >
                <!--<th valign="top" width="25%"></th>-->
                <th class="roomTableElement" valign="top" width="95%"><h5>Беседа: "{{room.name}}"</h5></th>
                <th valign="top"><button v-on:click="addRoom(room.id)"> + </button></th>
              </tr>
            </table>
          </div>
          <br v-show="isSearchedRoomsComponentVisible">
          <button  v-show="isSearchedRoomsComponentVisible" v-on:click="showUserRoomsComponentVisible">Скрыть</button>

        <br><br>

        <div class="roomTable" v-show="isShowUserRoomsComponentVisible">
          <table v-on:click="selectRoom(room.id)" v-for="(room, id) in userRooms" v-bind:key="id"   >
              <tr align="center" >
                <!--<th valign="top" width="25%"></th>-->
                <th class="roomTableElement" valign="top" width="95%"><h5>Беседа: "{{room.name}}"</h5></th>
                <th valign="top"><button v-on:click="leaveRoom(room.id)"> - </button></th>
              </tr>
          </table>
        </div>





        <td valign="top" width="80%">
        <h1>Мессенджер</h1>

        <hr>
        <h3>Беседа: "<b>{{roomName}}</b>"</h3>
        <br>
        <div class="messageDiv" id="messageDivId" ref="messageDivRef">
          <div>
            <div v-for="(message, id) in messages" v-bind:key="id">
              <div class="messageElement">
                <div v-if="userId != message.user_id">
                  <div align="left"> <h5>{{message.user_name}}</h5></div>
                  <div :style="getColor(message.color)" align="left"> <h4>{{message.content}}</h4> </div>
                  <div align="left">{{message.time}}</div>
                </div>
                <div v-if="userId == message.user_id">
                  <div align="right"> <h5>{{message.user_name}}</h5></div>
                  <div :style="getColor(message.color)" align="right"> <h4>{{message.content}}</h4> </div>
                  <div align="right">{{message.time}}</div>
                </div>
              </div>

            </div>
          </div>
        </div>



        <br>
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Сообщение" aria-label="Recipient's username" aria-describedby="basic-addon2"
          v-model="messageContent">
          <div class="input-group-append">
            <button @click="sendMessage" class="btn btn-outline-secondary" type="button">Отправить</button>
          </div>
        </div>



          <div class="row">
            <div class="col" v-for="(col, id) in colors" v-bind:key="id">
                <div v-on:click="selectColor(col)" :style="getBackgroundColor(col)">
                  {{col.text}}
                </div>
            </div>
          </div>

        <br>
        <div align="left" >
          Выбранный цвет: <span :style="getColor(selectedColor.color)">{{selectedColor.text}}</span>
        </div>


        </td>


      </tr>
    </table>
  </div>

</template>

<script>
    export default {
      name: "Chat",
      sockets: {
        connect: function () {
          console.log('socket connected')
        }
      },
      mounted(){
        this.sockets.subscribe('create_room_response', (data) => {
          if (data.code == 200) {
            this.roomsmsg = data.message;
            this.isCreatingRoomComponentVisible = false;
          }
          else {
            this.roomsmsg = "Не удалось создать беседу";
          }
        });
        this.sockets.subscribe('get_rooms_response', (data) => {
          if (data.code == 200) {
            console.log(data);
            this.userRooms = data.rooms;
          }
          else {
            this.roomsmsg = "Не удалось получить беседы";
          }
        });
        this.sockets.subscribe('get_rooms_by_name_response', (data) => {
          if (data.code == 200) {
            console.log(data);
            this.searchedRooms = data.rooms;
            this.isSearchingRoomComponentVisible = false;
            this.isSearchedRoomsComponentVisible = true;
          }
          else {
            this.roomsmsg = "Не удалось найти беседы";
          }
        });
        this.sockets.subscribe('add_room_response', (data) => {
          if (data.code == 200) {
            this.isSearchingRoomComponentVisible = false;
            this.isSearchedRoomsComponentVisible = false;
            this.isShowUserRoomsComponentVisible = true;
          }
          else {
            this.roomsmsg = "Не удалось добавить беседу";
          }
        });
        this.sockets.subscribe('get_messages_response', (data) => {
          if (data.code == 200) {
            this.messages = data.messages;
            this.scrollMessageDiv();
          }
          else {
            this.messagemsg = "Не удалось получить сообщения";
          }
        });
        this.sockets.subscribe('send_message_response', (data) => {
          if (data.code == 200) {
            this.messagemsg = data.message;
            this.messageContent = '';

          }
          else {
            this.messagemsg = "Не удалось отправить сообщение";
          }
        });
        this.sockets.subscribe('new_message_broadcast', (data) => {
          if (data.code == 200) {
            //this.messages.push(data.message);
            this.getMessages();
          }
          else {
            this.messagemsg = "Не удалось получить сообщение";
          }
        });
        this.sockets.subscribe('get_room_info_response', (data) => {
          if (data.code == 200) {
            this.roomName = data.room.name;
          }
          else {
            this.messagemsg = "Не удалось получить информацию о беседе";
          }
        });
      },
      created() {
        this.userId = localStorage.getItem('userId');
        this.userName = localStorage.getItem('name');
        this.email = localStorage.getItem('email');
        if (this.userId == null){
          this.$router.push('signin')
        }
        this.getUserRooms();
      },
      data() {
        return {
          userName: '',
          isCreatingRoomComponentVisible: true,
          creatingRoomName: '',
          isSearchingRoomComponentVisible: false,
          isSearchedRoomsComponentVisible: false,
          isShowUserRoomsComponentVisible: true,
          searchingRoomName: '',
          searchedRooms: [],
          userRooms: [],
          userId: Number,
          email: '',
          roomsmsg: '',
          messagemsg: '',
          messageContent: '',
          selectedColor: {"color": "#FF8C00", "text": "IndianRed"},
          messages: [],
          roomId: Number,
          roomName: '',
          buttonText: "Выйти",
          colors: [{"color": "#FF8C00", "text": "IndianRed"},
            {"color": "#FF00FF", "text": "Magenta"},
            {"color": "#1E90FF", "text": "DodgerBlue"},
            {"color": "#3CB371", "text": "MediumSeaGreen"},
            {"color": "#BC8F8F", "text": "RosyBrown"},
            {"color": "#FF0000", "text": "Red"},
          ],
        }
      },
      methods: {
        scrollMessageDiv(){
          try{
            var obj = this.$refs['messageDivRef'];
            obj.scrollTop = obj.scrollHeight;
          }
          catch(e){
            console.log(e)
          }
        },
        createRoom() {
          if (this.creatingRoomName == "") {
            this.roomsmsg = "Введите название беседы";
          }
          else {
            this.$socket.emit('create_room', {
              "room_name": this.creatingRoomName,
              "id": this.userId
            });
          }
        },
        showCreatingRoomComponent() {
          this.isCreatingRoomComponentVisible = true;
          this.isSearchingRoomComponentVisible = false;
          this.isShowUserRoomsComponentVisible = true;
          this.hideSearchedRoomsComponent();
        },
        showSearchingRoomComponent() {
          this.isShowUserRoomsComponentVisible = false;
          this.isSearchingRoomComponentVisible = true;
          this.isCreatingRoomComponentVisible = false;

          this.hideSearchedRoomsComponent();

        },
        showUserRoomsComponentVisible(){
          this.isShowUserRoomsComponentVisible = true;
          this.hideSearchedRoomsComponent();
        },
        hideSearchedRoomsComponent() {
          this.isSearchedRoomsComponentVisible = false;
          this.searchedRooms = [];
          this.searchingRoomName = "";
        },
        getUserRooms() {
          this.$socket.emit('get_rooms', {
            "id": this.userId
          });
        },
        getRoomsByName() {
          this.$socket.emit('get_rooms_by_name', {
            "room_name": this.searchingRoomName
          });
        },
        addRoom(id) {

          this.$socket.emit('add_room', {
            "room_id": id,
            "user_id": this.userId
          });

        },
        leaveRoom(id){
          this.$socket.emit('leave_room', {
            "room_id": id,
            "user_id": this.userId
          });
        },
        selectRoom(id) {
          this.roomId = id;
          this.getMessages();
          this.getRoomInfo();
        },
        getRoomInfo(){
          this.$socket.emit('get_room_info', {
            "room_id": this.roomId,
            "user_id": this.userId
          });
        },
        getMessages(){
          this.$socket.emit('get_messages', {
            "room_id": this.roomId,
            "user_id": this.userId
          });
        },
        sendMessage() {
          if (this.userId == null){
            return
          }
          if (this.roomId == null){
            return
          }
          this.$socket.emit('send_message', {
            "room_id": this.roomId,
            "user_id": this.userId,
            "content": this.messageContent,
            "color": this.selectedColor.color
          });
        },
        getColor(color){
          return {"color": color}
        },
        getBackgroundColor(col){
          // if (this.color == col)
          // //return {"background-color": color, "border": "black 2px solid"};
          //   return {"background-color": col, "order-color": "#9ecaed", "box-shadow": "0 0 20px "+col };
          // else
            return {"background-color": col.color, "cursor": "pointer"};
        },
        navButtonClick(){
          localStorage.clear();
          this.$router.push('/signin')
        },
        selectColor(col){
          this.selectedColor = col;
        }
      }
    }

</script>

<style scoped>
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
.roomButton {
  background: #ccc;
  padding: 5px;
  /*float: left;*/
  float: bottom;
  width: 100%;
  cursor: pointer;
}
.roomTable{
  overflow:scroll;
  height:70%;
  float: bottom;
}
  .roomTableElement{
    cursor: pointer;
  }
  .messageDiv{
    overflow:scroll;
    height:550px;

  }
  .messageElement{
    padding: 15px;
    /*float: left;*/
    float: bottom;
    width: 100%;
  }
</style>
