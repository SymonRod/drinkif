import { createRouter, createWebHashHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AboutPage from '../views/AboutPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import PhrasesPage from '../views/PhrasesPage.vue'
import SharePage from '../views/SharePage.vue'
import FriendsPage from '../views/FriendsPage.vue'
import ProfilePage from '../views/ProfilePage.vue'


const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/about',
    name: 'AboutPage',
    component: AboutPage
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/phrases',
    name: 'PhrasesPage',
    component: PhrasesPage
  },
  {
    path: '/share/:id',
    name: 'SharePage',
    component: SharePage
  },
  {
    path: '/friends',
    name: 'friendsPage',
    component: FriendsPage
  },
  {
    path: '/profile',
    name: 'profilePage',
    component: ProfilePage
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
