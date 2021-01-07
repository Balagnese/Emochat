import Vue from 'vue'
import Router from 'vue-router'
import Registration from '@/components/Registration'
import SignIn from '@/components/SignIn'
import Chat from '@/components/Chat'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/registration',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/signin',
      name: 'SignIn',
      component: SignIn
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat
    }

  ]
})
