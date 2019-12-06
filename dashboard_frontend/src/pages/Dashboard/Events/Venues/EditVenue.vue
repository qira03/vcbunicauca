<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>pin_drop</md-icon>
                    </div>
                    <h4 class="title">Editar lugar</h4>
                </md-card-header>

                <md-card-content>
                     <!-- Nombre y dirección -->
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
                        <!-- Dirección -->
                        <md-field :class="[
                        {'md-valid': !errors.has('address') && touched.address},
                        {'md-error': errors.has('address')}]">
                        <label>Dirección</label>
                        <md-input
                            v-model="address"
                            data-vv-name="address"
                            required
                            v-validate="modelValidations.address">
                        </md-input>
                        <slide-y-down-transition>
                            <md-icon class="error" v-show="errors.has('address') && touched.address">close</md-icon>
                        </slide-y-down-transition>
                        <slide-y-down-transition>
                            <md-icon class="success" v-show="!errors.has('address') && touched.address">done</md-icon>
                        </slide-y-down-transition>
                        </md-field>
                        <!-- ./ Dirección -->
                        </div>
                     </div>   
                     <!-- ./ Nombres y dirección -->
                     <!-- Ciudad y Departament -->
                     <div class="md-layout">
                         <!-- Ciudad -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('city') && touched.city},
                                {'md-error': errors.has('city')}]">
                                <label>Ciudad</label>
                                <md-input
                                    v-model="city"
                                    data-vv-name="city"
                                    type="text"
                                    required
                                    v-validate="modelValidations.city">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('city') && touched.city">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('city') && touched.city">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Ciudad -->
                        <!-- Departamento -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('state') && touched.state},
                                {'md-error': errors.has('state')}]">
                                <label>Departamento</label>
                                <md-input
                                    v-model="state"
                                    data-vv-name="state"
                                    required
                                    v-validate="modelValidations.state">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('state') && touched.state">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('state') && touched.state">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Departamento -->
                     </div>    
                    <!-- ./ Ciudad y Departament-->
                    <!-- Teléfono y sitio web -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Teléfono -->
                            <md-field :class="[
                            {'md-valid': !errors.has('phone') && touched.phone},
                            {'md-error': errors.has('phone')}]">
                            <label>Teléfono</label>
                            <md-input
                                v-model="phone"
                                data-vv-name="phone"
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
                        <div class="md-layout-item md-size-50 md-small-size-100">
                            <!-- Sitio web -->
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
                            <!-- ./ Sitio web -->
                        </div>
                     </div>   
                     <!-- ./ Teléfono y sitio web -->
                     <!-- Mapa del evento -->
                     <br>
                     <br>
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Mapa -->
                            <h3 class="title">Ubicación del lugar</h3>
                             <l-map :zoom="zoom" :center="center" style="height: 500px; width: 100%">
                                <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                                <l-marker :draggable="true"  @update:latLng="updateMarker" :lat-lng="marker.position">
                                    <l-popup :options="{ autoClose: true, closeOnClick: false }">Popup</l-popup>
                                </l-marker>      
                            </l-map>
                            <!-- ./ Mapa -->
                        </div>
                     </div>   
                     <!-- ./ Mapa del evento -->
                   <div class="form-category">* Campos obligatorios</div>
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/events/venues"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-progress-spinner v-show="sending == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Registrar</md-button>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import { SlideYDownTransition } from "vue2-transitions";
import { UPDATE_VENUE, GET_VENUE_BY_ID } from '../../../../plugins/graphql';
import {LMap, LTileLayer, LMarker, LPopup, LTooltip , L } from 'vue2-leaflet';
export default {
    apollo:{
        venue: {
                query: GET_VENUE_BY_ID,
                // Reactive variables
                variables() {
                    return {
                    id: this.$route.params.venue_id
                    }
                },
                // Additional options here
                fetchPolicy: 'network-only',
                // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {
                    
                    if(data.venue == null)
                    {
                        this.notifyVue('top','right','info','El lugar no existe');
                    }
                    else
                    {
                        this.setVenue(data.venue);
                    }
                    
                },
                // Si encontró algún error.
                error(error) {
                    this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                },
                },
        },
  components: {
    SlideYDownTransition,
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LTooltip
  },
  data() {
    return {
      venue:'',
      zoom: 16,
      center: [2.442863855916537, -76.60455873934553],
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors |Implementado por Namtrik Development',
      marker:{
          position:{
              lat:2.442863855916537,
              lng:-76.60455873934553
          }
      },
      sending:false,
      boolean: null,
      id:"",
      name: "",
      address: "",
      city: "",
      state: "",
      phone: "",
      website: "",
      touched: {
        name: false,
        address: false,
        city: false,
        state: false,
        phone: false,
        website: false,
        
      },
      modelValidations: {
        name:{
            required: true,
            min: 1,
            max: 32
        },
        address:{
            required: true,
            min: 1,
            max: 32
        },
        city:{
            required: true,
            min: 1,
            max: 32
        },
        state:{
            required: true,
            min: 1,
            max: 32
        },
        phone:{
            min: 3,
            max: 18
        },
        website:{
            min:1,
            max: 256,
            url: true
        }
      }
    };
  },
  methods: {
    // Función que actualiza las coordenadas en caso de que sean editadas
      updateMarker: function(val){
        this.marker.position.lat = val.lat;
        this.marker.position.lng = val.lng;
      },
    // Función que setea el lugar
    setVenue: function(venue){
    this.id = venue.id;
    this.name = venue.name;
    this.address = venue.address;
    this.city = venue.city;
    this.state = venue.state;
    this.phone = venue.phone;
    this.website = venue.website;
    this.marker.position.lat = venue.latitude;
    this.marker.position.lng = venue.longitude;
    this.center = [venue.latitude,venue.longitude]
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
            mutation: UPDATE_VENUE,
            variables:{
              input:{
                  id: this.id,
                  venue:{
                      name: this.name,
                      address: this.address,
                      city: this.city,
                      state: this.state,
                      phone: this.phone,
                      website: this.website,
                      latitude: this.marker.position.lat,
                      longitude: this.marker.position.lng
                  }
              }
            }
          }).then((data) => {
            this.notifyVue('top','right','success','Lugar editado correctamente');
            this.$router.push('/events/venues');
            
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
    address() {
      this.touched.address = true;
    },
    city() {
      this.touched.city = true;
    },
    state() {
      this.touched.state = true;
    },
    phone() {
      this.touched.phone = true;
    },
    website(){
      this.touched.website = true;
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
@import "~leaflet/dist/leaflet.css";
</style>
