<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>create</md-icon>
                    </div>
                    <h4 class="title">Editar contraseña de usuario</h4>
                </md-card-header>

                <md-card-content>
                    <!-- Contraseña y confirmación -->
                     <div class="md-layout">
                         <!-- Contraseña -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('password') && touched.password},
                                {'md-error': errors.has('password')}]">
                                <label>Contraseña</label>
                                <md-input
                                    v-model="password"
                                    data-vv-name="password"
                                    type="password"
                                    ref="password"
                                    required
                                    v-validate="modelValidations.password">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('password') && touched.password">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('password') && touched.password">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Contraseña -->
                        <!-- Confirmar contraseña -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('confirmPassword') && touched.confirmPass},
                                {'md-error': errors.has('confirmPassword')}]">
                                <label>Confirmar contraseña</label>
                                <md-input
                                    v-model="confirmPassword"
                                    data-vv-name="confirmPassword"
                                    data-vv-as="password"
                                    type="password"
                                    required
                                    v-validate="modelValidations.confirmPassword">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('confirmPassword') && touched.confirmPassword">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('confirmPassword') && touched.confirmPassword">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Confirmar contraseña -->
                     </div>   
                     <!-- ./ Contraseña y confirmación     -->
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
import { UPDATE_USER_PASSWORD, GET_USER_BY_ID } from '../../../plugins/graphql';
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
      password: "",
      confirmPassword: "",
      touched: {
        password: false,
        confirmPass: false
      },
      modelValidations: {
        password: {
          required: true,
          min: 5,
          max:15
        },
        confirmPassword: {
          required: true,
          confirmed: "password"
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
            mutation: UPDATE_USER_PASSWORD,
            variables:{
              input:{
                  id: this.user_id,
                  password: this.password
              }
            }
          }).then((data) => {
            this.notifyVue('top','right','success','Usuario editado correctamente');
            if(this.$store.getters.getUserId == this.user_id)
            {
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
            else
            {
                this.$router.push('/users');
            }
            
            
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
    password() {
      this.touched.password = true;
    },
    confirmPassword() {
      this.touched.confirmPass = true;
    }
  }
};
</script>
<style lang="scss" scoped>
.md-card .md-card-actions {
  border: none;
}
</style>
