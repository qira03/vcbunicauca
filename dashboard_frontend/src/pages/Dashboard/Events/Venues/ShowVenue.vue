<template>
  <div>
    <div class="md-layout">
      <div class="md-layout-item">
        <md-card>
          <md-card-content>
            <div id="typography">
               <div class="title">
                   <h2>{{name}}</h2>
               </div>
               <br>
               <div class="row">
                   
                   <div class="tim-typo">
                       <span class="tim-note">Dirección</span>
                       <p class="text-muted">
                           {{address}}
                       </p>
                   </div>
                   <div class="tim-typo">
                       <span class="tim-note">Ciudad</span>
                       <p class="text-muted">
                           {{city}}
                       </p>
                   </div>
                   <div class="tim-typo">
                       <span class="tim-note">Departamento</span>
                       <p class="text-muted">
                           {{state}}
                       </p>
                   </div>
                   <div v-show="phone != ''" class="tim-typo">
                       <span class="tim-note">Teléfono</span>
                       <p class="text-muted">
                           {{phone}}
                       </p>
                   </div>
                   <div v-show="website != ''" class="tim-typo">
                       <span class="tim-note">Sitio web</span>
                       <p class="text-muted">
                           <a :href="website" target="_blank">{{website}}</a>
                       </p>
                   </div>
               </div>
           </div>
           <br>
           <div class="md-layout">
                <div class="md-layout-item md-size-100 md-small-size-100">
                        <!-- Mapa -->
                    <h3 class="title">Ubicación del lugar</h3>
                        <l-map :zoom="zoom" :center="center" style="height: 500px; width: 100%">
                        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                        <l-marker  :lat-lng="marker.position">
                            <l-popup :options="{ autoClose: true, closeOnClick: false }">Popup</l-popup>
                        </l-marker>      
                    </l-map>
                    <!-- ./ Mapa -->
                </div>
            </div>
            <br>
            <md-card-actions md-alignment="space-between">
                <router-link to="/events/venues"><md-button class="md-default">Volver</md-button></router-link>
                <router-link :to="'/events/venues/edit/'+id"><md-button class="md-warning">Editar</md-button></router-link>
            </md-card-actions>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>
<script>
import { GET_VENUE_BY_ID } from '../../../../plugins/graphql';
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
      name: "",
      address: "",
      city: "",
      state: "",
      phone: "",
      website: "",
    };
  },
  methods:{
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
  },
};
</script>
<style>
@import "~leaflet/dist/leaflet.css";
</style>
