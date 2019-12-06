<template>
  <div class="user">
    <div class="photo">
      <img :src="avatar" alt="avatar"/>
    </div>
    <div class="user-info">
      <a data-toggle="collapse" :aria-expanded="!isClosed" @click.stop="toggleMenu" @click.capture="clicked">
      <!-- <a data-toggle="collapse"> -->
          <span>
             {{this.$store.getters.getUsername}}
             <b class="caret"></b>
          </span>
      </a>

        <collapse-transition>
            <div v-show="!isClosed">
              <ul class="nav" >
                <slot>
                  <!-- <li>
                    <a href="#vue">
                      <span class="sidebar-mini">MP</span>
                      <span class="sidebar-normal">Mi Perfil</span>
                    </a>
                  </li> -->
                  <li>
                    <a>
                      <span class="sidebar-mini">CS</span>
                      <span @click="logout" class="sidebar-normal">Cerrar sesión</span>
                    </a>
                  </li>
                  <!-- <li>
                    <a v-if="$route.meta.rtlActive" href="#vue">
                      <span class="sidebar-mini">و</span>
                      <span class="sidebar-normal">إعدادات</span>
                    </a>
                    <a v-else href="#vue">
                      <span class="sidebar-mini">S</span>
                      <span class="sidebar-normal">Settings</span>
                    </a>
                  </li> -->
                </slot>
              </ul>
          </div>
        </collapse-transition>
    </div>
  </div>
</template>
<script>
import { CollapseTransition } from "vue2-transitions";

export default {
  components: {
    CollapseTransition
  },
  props: {
    title: {
      type: String,
      default: "Tania Andrew"
    },
    rtlTitle: {
      type: String,
      default: "تانيا أندرو"
    },
    avatar: {
      type: String,
      default: "./img/faces/avatar.jpg"
    }
  },
  data() {
    return {
      isClosed: true
    };
  },
  methods: {
    clicked: function(e) {
      e.preventDefault();
    },
    toggleMenu: function() {
      this.isClosed = !this.isClosed;
    },
    logout: function(){
        this.$store.commit({
                  type: 'resetToken', 
                  message: ''
        });
        this.$store.commit({
                  type: 'resetUser', 
                  message: ''
        });
        this.$router.push('/login');
    }
  }
};
</script>
<style>
.collapsed {
  transition: opacity 1s;
}
</style>
