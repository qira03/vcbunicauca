<template>
<div class="md-layout text-center">
    
    <div class="md-layout-item md-size-33 md-medium-size-50 md-small-size-70 md-xsmall-size-100">
      <offline @detected-condition="handleConnectivityChange">
        <!-- Only renders when the device is offline -->
        
      </offline>
      <div v-bind:style="{display: myDisplay}" class="alert alert-warning alert-with-icon" data-notify="container">
          <i data-notify="icon" class="material-icons">add_alert</i>
          <span data-notify="message">No hay conexión a internet en estos momentos, tan pronto haya conectividad este mensaje desaparecerá.</span>
      </div>
      <br><br>
      <login-card header-color="primary">
        <h4 slot="title" class="title">Iniciar sesión</h4>
        <p slot="description" class="description">Ingresa tus credenciales</p>
        <md-field class="md-form-group" slot="inputs">
          <md-icon>person</md-icon>
          <label>Nombre de usuario</label>
          <md-input v-model="username"></md-input>
        </md-field>
        <md-field class="md-form-group" slot="inputs">
          <md-icon>lock_outline</md-icon>
          <label>Contraseña</label>
          <md-input v-on:keyup.enter="Login" type="password" v-model="password"></md-input>
        </md-field>
        <md-button  @click="Login" slot="footer" class="md-success md-lg">
          Iniciar sesión
        </md-button>
      </login-card>
    </div>
  </div>
</template>
<script>
import Vue from 'vue';
import { LoginCard } from "@/components";
import  gql  from 'graphql-tag';
import { LOGIN, REFRESH_TOKEN, GET_USER_BY_USERNAME} from '../../../plugins/graphql';
import offline from 'v-offline';
Vue.use(offline);
export default {
  apollo:{
        allUsers: {
                    query: GET_USER_BY_USERNAME,
                    // Reactive variables
                    variables() {
                      return {
                        username: this.username_gql
                      }
                    },
                    // Disable the query
                    skip() {
                      return this.skipQuery
                    },
                      // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                    if(data.allUsers.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay usuarios');
                    }
                    else
                    {
                      this.setUserStore();
                    }
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Tus credenciales son incorrectas, revisa de nuevo');
                    },
                  },
      },
  components: {
    LoginCard,
    offline
  },
  data() {
    return {
      skipQuery: true,
      user:'',
      username_gql: '',
      username: null,
      password: null,
      myDisplay: 'none',
    };
  },
  methods:{
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
        // Función que muestra las notificaciones
        notifyVue: function(verticalAlign, horizontalAlign,type,message) {
          this.$notify({
            message:message,
            icon: "add_alert",
            horizontalAlign: horizontalAlign,
            verticalAlign: verticalAlign,
            type: type
          });
        },
        // Función que ejecuta la query de los usuarios
        triggerMyUser: function() {
          this.$apollo.queries.allUsers.skip = false
          this.$apollo.queries.allUsers.refetch()
        },
        // Función que setea en el store el usuario que se autenticó
        setUserStore: function(){
          this.$store.commit({
            type: 'updateUser', 
            message: this.allUsers.edges[0].node.username
          });
          this.$store.commit({
                  type: 'updateUserId', 
                  message: this.allUsers.edges[0].node.id
          });
          this.$store.commit({
                  type: 'updateName', 
                  message: this.allUsers.edges[0].node.firstName+' '+this.allUsers.edges[0].node.lastName
          });
          this.$router.push('/dashboard');
          
        },
        // Mutación que inicia sesión
        Login: function(){
          if(this.username == null || this.password == null)
          {
            this.notifyVue('top','right','info','Debes ingresar tus credenciales');
            return;
          }
          const username = this.username;
          const password = this.password;
          this.username = '';
          this.password = '';
          this.$apollo.mutate({
            mutation: LOGIN,
            variables:{
              username: username,
              password: password
            }
          }).then((data) => {
            // Mutación que refresca el token
            this.$apollo.mutate({
              mutation: REFRESH_TOKEN,
              variables:{
                token: data.data.tokenAuth.token
              }
            }).then((data) => {
              this.username_gql = data.data.refreshToken.payload.username;
              this.$store.commit({
                  type: 'updateToken', 
                  message: data.data.refreshToken.token
              });
              // Función que ejecuta la query de usuarios
              this.triggerMyUser();
            }).catch((error) => {
              // Error
              this.notifyVue('top','right','warning','Tus credenciales son incorrectas, revisa de nuevo');
            });
          }).catch((error) => {
            // Error
            this.notifyVue('top','right','warning','Tus credenciales son incorrectas, revisa de nuevo');
          });
        }
    },
};
</script>

<style>
</style>
