<<<<<<< HEAD
importScripts("/static/precache-manifest.9d1736ff4a8dcc08100d8feb89586762.js", "https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");
=======
<<<<<<<< HEAD:backend/drinkif/static/registerServiceWorker.js
importScripts("/static/precache-manifest.544088cdf8cc41b45c5904f65737f48c.js", "https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");
>>>>>>> origin/master

/* eslint-disable no-console */

import { register } from 'register-service-worker'

if (process.env.NODE_ENV === 'production') {
  register(`${process.env.BASE_URL}service-worker.js`, {
    ready () {
      console.log(
        'App is being served from cache by a service worker.\n' +
        'For more details, visit https://goo.gl/AFskqB'
      )
    },
    registered () {
      console.log('Service worker has been registered.')
    },
    cached () {
      console.log('Content has been cached for offline use.')
    },
    updatefound () {
      console.log('New content is downloading.')
    },
    updated () {
      console.log('New content is available; please refresh.')
    },
    offline () {
      console.log('No internet connection found. App is running in offline mode.')
    },
    error (error) {
      console.error('Error during service worker registration:', error)
    }
  })
}

<<<<<<< HEAD
=======
========
>>>>>>>> origin/master:backend/drinkif/static/src/vue/dist/registerServiceWorker.js
>>>>>>> origin/master
