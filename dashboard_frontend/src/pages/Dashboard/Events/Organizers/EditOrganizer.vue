<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>person_pin_circle</md-icon>
                    </div>
                    <h4 class="title">Editar organizador</h4>
                </md-card-header>

                <md-card-content>
                     <!-- Nombre y teléfono -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Nombre -->
                            <md-field :class="[
                            {'md-valid': !errors.has('name') && touched.name},
                            {'md-error': errors.has('name')}]">
                            <label>Nombre</label>
                            <md-input
                                v-model="name"
                                data-vv-name="name"
                                type="text"
                                required
                                v-validate="modelValidations.name">
                            </md-input>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('name') && touched.name">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('name') && touched.name">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Nombre -->
                        </div>
                        <div class="md-layout-item md-size-50 md-small-size-100">
                        <!-- Teléfono -->
                        <md-field :class="[
                        {'md-valid': !errors.has('phone') && touched.phone},
                        {'md-error': errors.has('phone')}]">
                        <label>Teléfono</label>
                        <md-input
                            v-model="phone"
                            data-vv-name="phone"
                            required
                            v-validate="modelValidations.phone">
                        </md-input>
                        <slide-y-down-transition>
                            <md-icon class="error" v-show="errors.has('phone') && touched.phone">close</md-icon>
                        </slide-y-down-transition>
                        <slide-y-down-transition>
                            <md-icon class="success" v-show="!errors.has('phone') && touched.phone">done</md-icon>
                        </slide-y-down-transition>
                        </md-field>
                        <!-- ./ Teléfono -->
                        </div>
                     </div>   
                     <!-- ./ Nombres y teléfono -->
                     <!-- Correo electrónico y sitio web -->
                     <div class="md-layout">
                         <!-- Sitio web -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('website') && touched.website},
                                {'md-error': errors.has('website')}]">
                                <label>Sitio web</label>
                                <md-input
                                    v-model="website"
                                    data-vv-name="website"
                                    type="text"
                                    v-validate="modelValidations.website">
                                </md-input>
                                <span class="md-helper-text">Incluya la etiqueta http:// o htps:// según corresponda</span>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('website') && touched.website">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('website') && touched.website">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Sitio web -->
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
                    <!-- ./ Correo electrónico y sitio web-->
                   <div class="form-category">* Campos obligatorios</div>
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/events/organizers"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-progress-spinner v-show="sending == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Editar</md-button>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import { SlideYDownTransition } from "vue2-transitions";
import { UPDATE_ORGANIZER, GET_ORGANIZER_BY_ID } from '../../../../plugins/graphql';
export default {
    apollo:{
        organizer: {
                    query: GET_ORGANIZER_BY_ID,
                    // Reactive variables
                    variables() {
                      return {
                        id: this.$route.params.organizer_id
                      }
                    },
                    // Disable the query
                    // skip() {
                    //   return this.skipQuery
                    // },
                      // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                    if(data.organizer == null)
                    {
                        this.notifyVue('top','right','info','No existe el organizador');
                        this.$router.push('/events/organizers');
                    }
                    else
                    {
                      this.setOrganizer(data.organizer);
                    }
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Algo ha pasado, inténtalo de nuevo');
                    },
                  },
      },
  components: {
    SlideYDownTransition
  },
  data() {
    return {
      sending:false,
      boolean: null,
      id: "",
      name: "",
      phone: "",
      website: "",
      email: "",
      touched: {
        name: false,
        phone: false,
        website: false,
        email: false
      },
      modelValidations: {
        name:{
            required: true,
            min: 1,
            max: 32
        },
        phone:{
            required: true,
            min: 3,
            max: 18
        },
        website:{
            min:1,
            max: 256,
            url:true
        },
        email: {
          email: true,
          min: 1,
          max: 64
        }
      }
    };
  },
  methods: {
    // Función que setea la categoría
    setOrganizer: function(organizer){
        this.id = organizer.id;
        this.name = organizer.name;
        this.phone = organizer.phone;
        this.website = organizer.website;
        this.email = organizer.email;
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
    // Función que valida que todo el formulario esté correcto
    validate() {
      this.$validator.validateAll().then(isValid => {
        if(isValid)
        {
            this.sending = true;
            // Iniciamos el envío de la mutación
            this.$apollo.mutate({
            mutation: UPDATE_ORGANIZER,
            variables:{
              input:{
                  id: this.id,
                  organizer:{
                      name: this.name,
                      phone: this.phone,
                      email: this.email,
                      website: this.website
                  }
              }
            }
          }).then((data) => {
            this.notifyVue('top','right','success','Organizador editado correctamente');
            this.$router.push('/events/organizers');
            
          }).catch((error) => {
            // Error
            this.sending = false;
            this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
          });
        }
        else
        {
            this.sending = false;
            this.notifyVue('top','right','warning','Los campos no están correctamente diligenciados');
        }
        // this.$emit("on-submit", this.registerForm, isValid);
      });
    }
  },
  watch: {
    name() {
      this.touched.name = true;
    },
    phone() {
      this.touched.phone = true;
    },
    website(){
      this.touched.website = true;
    },
    email() {
      this.touched.email = true;
    }
  }
};
</script>
<style lang="scss" scoped>
.md-card .md-card-actions {
  border: none;
}
.md-progress-spinner {
    margin: 24px;
  }
</style>
