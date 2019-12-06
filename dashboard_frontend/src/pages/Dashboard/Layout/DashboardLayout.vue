<template>
  <div class="wrapper" :class="[{'nav-open': $sidebar.showSidebar}, {'rtl': $route.meta.rtlActive}]">
    <notifications></notifications>
     <side-bar>
      <user-menu></user-menu>
      <!-- <mobile-menu></mobile-menu> -->
      <template slot="links">
        <sidebar-item :link="{name: 'Dashboard', icon: 'dashboard', path: '/dashboard'}">
        </sidebar-item>
        <sidebar-item :link="{name: 'Slider', icon: 'insert_photo', path: '/slider'}"></sidebar-item>
        <sidebar-item :link="{name: 'Usuarios', icon: 'people', path: '/users'}">
        </sidebar-item>
        <sidebar-item :link="{name: 'Eventos', icon: 'event'}">
          <sidebar-item :link="{name: 'Categorías', path: '/events/categories'}"></sidebar-item>
          <sidebar-item :link="{name: 'Organizadores', path: '/events/organizers'}"></sidebar-item>
          <sidebar-item :link="{name: 'Lugares', path: '/events/venues'}"></sidebar-item>
          <sidebar-item :link="{name: 'Eventos', path: '/events/events'}"></sidebar-item>
        </sidebar-item>
        <sidebar-item :link="{name: 'Noticias', icon: 'library_books', path: '/news'}">
        </sidebar-item>
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>
      <!-- Offline detection -->
      <offline @detected-condition="handleConnectivityChange"></offline>
      <div v-bind:style="{display: myDisplay}" class="alert alert-warning alert-with-icon" data-notify="container">
          <i data-notify="icon" class="material-icons">add_alert</i>
          <span data-notify="message">No hay conexión a internet en estos momentos, tan pronto haya conectividad este mensaje desaparecerá.</span>
      </div>
      <!-- ./ Offline detection -->
      <div :class="{content: !$route.meta.hideContent}" @click="toggleSidebar">
        <zoom-center-transition :duration="200" mode="out-in">
          <!-- your content here -->
          <router-view></router-view>
        </zoom-center-transition>
      </div>
      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
    </div>
  </div>
</template>
<script>
/* eslint-disable no-new */
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";

function hasElement(className) {
  return document.getElementsByClassName(className).length > 0;
}

function initScrollbar(className) {
  if (hasElement(className)) {
    new PerfectScrollbar(`.${className}`);
  } else {
    // try to init it later in case this component is loaded async
    setTimeout(() => {
      initScrollbar(className);
    }, 100);
  }
}
import Vue from 'vue';
import IdleVue from 'idle-vue';
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import MobileMenu from "./Extra/MobileMenu.vue";
import UserMenu from "./Extra/UserMenu.vue";
import { ZoomCenterTransition } from "vue2-transitions";
import offline from 'v-offline';
const eventsHub = new Vue();
Vue.use(offline);
Vue.use(IdleVue, {
  eventEmitter: eventsHub,
  idleTime: 3600000
});
export default {
  components: {
    TopNavbar,
    ContentFooter,
    MobileMenu,
    UserMenu,
    ZoomCenterTransition,
    offline
  },
  data() {
    return {
      myDisplay: 'none',
      state: null,
    };
  },
  onIdle() {
    this.$store.commit({
                  type: 'resetToken', 
                  message: ''
    });
    this.$store.commit({
              type: 'resetUser', 
              message: ''
    });
    this.$router.push('/login');
    alert('El tiempo de sesión caducó, inicia de nuevo');
  },
  // onActive() {
  //   alert('hola de nuevo');
  // },
  methods: {
    // Función que verifica si hay internet y muestra el mensaje permanente
    handleConnectivityChange(status) {
      if(status == false)
      {
        this.myDisplay = 'block';
      }
      else
      {
        this.myDisplay = 'none';
      }
    },
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    }
  },
  mounted() {
    let docClasses = document.body.classList;
    let isWindows = navigator.platform.startsWith("Win");
    if (isWindows) {
      // if we are on windows OS we activate the perfectScrollbar function
      initScrollbar("sidebar");
      initScrollbar("sidebar-wrapper");
      initScrollbar("main-panel");

      docClasses.add("perfect-scrollbar-on");
    } else {
      docClasses.add("perfect-scrollbar-off");
    }
  }
};
</script>
<style lang="scss">
$scaleSize: 0.95;
@keyframes zoomIn95 {
  from {
    opacity: 0;
    transform: scale3d($scaleSize, $scaleSize, $scaleSize);
  }
  to {
    opacity: 1;
  }
}
.main-panel .zoomIn {
  animation-name: zoomIn95;
}
@keyframes zoomOut95 {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
    transform: scale3d($scaleSize, $scaleSize, $scaleSize);
  }
}
.main-panel .zoomOut {
  animation-name: zoomOut95;
}
</style>
