import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
//import { createGtag } from "vue-gtag"
import './style.css'

// import rubik font using fontsource
import "@fontsource/rubik/300.css"
import "@fontsource/rubik/400.css"
import "@fontsource/rubik/500.css"
import "@fontsource/rubik/600.css"
import "@fontsource/rubik/700.css"

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { faUser } from '@fortawesome/free-solid-svg-icons'
import { faCartShopping } from '@fortawesome/free-solid-svg-icons'
import { faSearch } from '@fortawesome/free-solid-svg-icons'


// gtag
//const gtag = createGtag({
//  tagId: "G-Z1TQ8HNHV1"
//})

/* add icons to the library */
library.add(faUserSecret, faUser, faCartShopping, faSearch)

//createApp(App).use(store).use(router).use(gtag).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
createApp(App).use(store).use(router).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
