<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>create</md-icon>
                    </div>
                    <h4 class="title">Editar usuario</h4>
                </md-card-header>

                <md-card-content>
                     <!-- Nombres y apellidos -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Nombres -->
                            <md-field :class="[
                            {'md-valid': !errors.has('firstName') && touched.firstName},
                            {'md-error': errors.has('firstName')}]">
                            <label>Nombres</label>
                            <md-input
                                v-model="firstName"
                                data-vv-name="firstName"
                                type="text"
                                required
                                v-validate="modelValidations.firstName">
                            </md-input>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('firstName') && touched.firstName">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('firstName') && touched.firstName">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Nombres -->
                        </div>
                        <div class="md-layout-item md-size-50 md-small-size-100">
                        <!-- Apellidos -->
                        <md-field :class="[
                        {'md-valid': !errors.has('lastName') && touched.lastName},
                        {'md-error': errors.has('lastName')}]">
                        <label>Apellidos</label>
                        <md-input
                            v-model="lastName"
                            data-vv-name="lastName"
                            type="text"
                            required
                            v-validate="modelValidations.lastName">
                        </md-input>
                        <slide-y-down-transition>
                            <md-icon class="error" v-show="errors.has('lastName') && touched.lastName">close</md-icon>
                        </slide-y-down-transition>
                        <slide-y-down-transition>
                            <md-icon class="success" v-show="!errors.has('lastName') && touched.lastName">done</md-icon>
                        </slide-y-down-transition>
                        </md-field>
                        <!-- ./ Apellidos -->
                        </div>
                     </div>   
                     <!-- ./ Nombres y apellidos -->
                     <!-- Correo electrónico y nombre de usuario -->
                     <div class="md-layout">
                         <!-- Nombre de usuario -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('username') && touched.username},
                                {'md-error': errors.has('username')}]">
                                <label>Nombre de usuario</label>
                                <md-input
                                    v-model="username"
                                    data-vv-name="username"
                                    type="text"
                                    disabled
                                    required
                                    v-validate="modelValidations.username">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('username') && touched.username">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('username') && touched.username">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Nombre de usuario -->
                        <!-- Correo electrónico -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('email') && touched.email},
                                {'md-error': errors.has('email')}]">
                                <label>Correo electrónico</label>
                                <md-input
                                    v-model="email"
                                    data-vv-name="email"
                                    type="email"
                                    required
                                    v-validate="modelValidations.email">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('email') && touched.email">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('email') && touched.email">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Correo electrónico -->
                     </div>    
                    <!-- ./ Correo electrónico y nombre de usuario-->
                   <div class="form-category">* Campos obligatorios</div>
                </md-card-content>
                <md-card-actions md-alignment="space-between">
                    <router-link to="/users"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-button native-type="submit" @click.native.prevent="validate" class="md-success">Actualizar</md-button>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import { SlideYDownTransition } from "vue2-transitions";
import { UPDATE_USER, GET_USER_BY_ID } from '../../../plugins/graphql';
export default {
    apollo:{
        user: {
                    query: GET_USER_BY_ID,
                    // Reactive variables
                    variables() {
                      return {
                        id: this.$route.params.user_id
                      }
                    },
                    
                    // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                        this.user_id = data.user.id;
                        this.firstName = data.user.firstName;
                        this.lastName = data.user.lastName;
                        this.username = data.user.username;
                        this.email = data.user.email;
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Algo ha pasado, intenta de nuevo');
                    },
                  },
      },
  components: {
    SlideYDownTransition
  },
  data() {
    return {
      user:'',
      boolean: null,
      user_id: "",
      firstName: "",
      lastName: "",
      username: "",
      email: "",
      touched: {
        firstName: false,
        lastName: false,
        username: false,
        email: false
      },
      modelValidations: {
        firstName:{
            required: true,
            min: 3,
            max: 20
        },
        lastName:{
            required: true,
            min: 3,
            max: 20
        },
        username:{
            required: true,
            min: 3,
            max: 16,
            alpha_num: true
        },
        email: {
          required: true,
          email: true,
          min: 10,
          max: 30
        }
      }
    };
  },
  methods: {
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
    // Función que valida que todo el formulario esté correcto
    validate() {
      this.$validator.validateAll().then(isValid => {
        if(isValid)
        {
            // Iniciamos el envío de la mutación
            this.$apollo.mutate({
            mutation: UPDATE_USER,
            variables:{
              input:{
                  id: this.user_id,
                  user:{
                      email: this.email,
                      firstName: this.firstName,
                      lastName: this.lastName
                  }
              }
            }
          }).then((data) => {
            this.notifyVue('top','right','success','Usuario editado correctamente');
            this.$router.push('/users');
            
          }).catch((error) => {
            // Error
            this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
          });
        }
        else
        {
            this.notifyVue('top','right','warning','Los campos no están correctamente diligenciados');
        }
        // this.$emit("on-submit", this.registerForm, isValid);
      });
    }
  },
  watch: {
    firstName() {
      this.touched.firstName = true;
    },
    lastName() {
      this.touched.lastName = true;
    },
    username(){
      this.touched.username = true;
    },
    email() {
      this.touched.email = true;
    },

  }
};
</script>
<style lang="scss" scoped>
.md-card .md-card-actions {
  border: none;
}
</style>
