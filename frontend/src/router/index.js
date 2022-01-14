import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Phrases from '../views/Phrases.vue'
import Share from '../views/Share.vue'
import Friends from '../views/Friends.vue'
import Profile from '../views/Profile.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/phrases',
    name: 'Phrases',
    component: Phrases
  },
  {
    path: '/share/:id',
    name: 'Share',
    component: Share
  },
  {
    path: '/friends',
    name: 'friends',
    component: Friends
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
