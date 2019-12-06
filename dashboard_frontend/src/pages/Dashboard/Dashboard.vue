<template>
  <div>
    <div class="md-layout">
      <div class="md-layout-item md-size-80 mx-auto">
        <md-card class="md-card-calendar">
          <md-card-content>
            <div id="fullCalendar"></div>
          </md-card-content>
        </md-card>
        </div>
    </div>
    <!-- Filtros -->
    <div class="md-layout">
      <div class="md-layout-item md-small-size-100">
        <md-card>
          <md-card-header class="md-card-header-icon md-card-header-green">
            <div class="card-icon">
              <md-icon>today</md-icon>
            </div>
            <h4 class="title">Fecha inicial</h4>
          </md-card-header>

          <md-card-content>
            <md-datepicker v-model="startDatetime">
              <label>Selecciona una fecha</label>
            </md-datepicker>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-small-size-100">
        <md-card>
          <md-card-header class="md-card-header-icon md-card-header-green">
            <div class="card-icon">
              <md-icon>today</md-icon>
            </div>
            <h4 class="title">Fecha final</h4>
          </md-card-header>

          <md-card-content>
            <md-datepicker v-model="finishDatetime">
              <label>Selecciona una fecha</label>
            </md-datepicker>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-small-size-100">
        <md-card>
          <md-card-header class="md-card-header-icon md-card-header-green">
            <div class="card-icon">
              <md-icon>person_pin_circle</md-icon>
            </div>
            <h4 class="title">Organizador</h4>
          </md-card-header>

          <md-card-content>
            <md-field>
                <label for="organizers">Organizador</label>
                    <md-select v-model="organizerName" name="organizers" id="organizers">
                        <md-option value="">Todos</md-option>
                        <md-option v-for="organizer in listOrganizers.edges" :key="organizer.id" :value="organizer.node.name">{{organizer.node.name}}</md-option>
                    </md-select>
            </md-field>
          </md-card-content>
        </md-card>
      </div>
    </div>
    <!-- ./ Filtros -->
    <div class="md-layout">
      <!-- Eventos -->
      <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-50" style="z-index:0;">
        <md-card class="md-card-stats">
          <md-card-header class="md-card-header-icon md-card-header-blue">
            <div class="card-icon">
              <md-icon>event</md-icon>
            </div>
            <p class="category">Eventos</p>
            <h3 class="title">
            <span v-show="this.$apollo.queries.allOrganizers.loading == false">{{totalEvents}}</span>
            <md-progress-spinner v-show="this.$apollo.queries.allOrganizers.loading == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
            </h3>
          </md-card-header>

          <md-card-actions md-alignment="left">
            <div class="stats">
              <md-icon>update</md-icon>
              Los datos no son en tiempo real
            </div>
          </md-card-actions>
        </md-card>
      </div>
      <!-- ./ Eventos -->
      <!-- Noticias -->
      <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-50" style="z-index:0;">
        <md-card class="md-card-stats">
          <md-card-header class="md-card-header-icon md-card-header-blue">
            <div class="card-icon">
              <md-icon>library_books</md-icon>
            </div>
            <p class="category">Noticias</p>
            <h3 class="title">
                <span v-show="this.$apollo.queries.allNews.loading == false">{{totalNews}}</span>
                <md-progress-spinner v-show="this.$apollo.queries.allNews.loading == true"  class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
            </h3>
          </md-card-header>

          <md-card-actions md-alignment="left">
            <div class="stats">
              <md-icon>update</md-icon>
              Los datos no son en tiempo real
            </div>
          </md-card-actions>
        </md-card>
      </div>
      <!-- ./Noticias -->
    </div>
    
    
  </div>
</template>
<script>
import { Datetime } from 'vue-datetime';
import swal from "sweetalert2";
import $ from "jquery";
import "fullcalendar";
import "fullcalendar/dist/locale/es";
import  gql  from 'graphql-tag';
import { ALL_EVENTS_DASHBOARD, ALL_ORGANIZERS_REPORTS, GET_ORGANIZER_REPORTS , ALL_NEWS_REPORTS} from '../../plugins/graphql';
import moment from 'moment';
import momentTz from 'moment-timezone';


var today = new Date();
var y = today.getFullYear();
var m = today.getMonth();
var d = today.getDate();
export default {
  apollo:{
        allEvents: {
                    query: ALL_EVENTS_DASHBOARD,
                    // Reactive variables
                    variables() {
                      return {
                        finishDatetime_Gt: this.startMonth
                      }
                    },
                    fetchPolicy: 'network-only',
                    // skip() {
                    //   return true
                    // },
                    // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                    if(data.allEvents.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay eventos para mostrar');
                    }
                    else
                    {
                      this.setEvents(data.allEvents);
                    }
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                    },
                  },
        allOrganizers: {
                    query: ALL_ORGANIZERS_REPORTS,
                    // Reactive variables
                    variables() {
                      return {
                        startDatetime_Gt: this.startDatetime,
                        startDatetime_Lt: this.finishDatetime,
                        organizerName: this.organizerName
                      }
                    },
                    fetchPolicy: 'network-only',
                    // skip() {
                    //   return true
                    // },
                    // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                    if(data.allOrganizers.edges.length == 0)
                    {
                        // this.notifyVue('top','right','info','No hay eventos para mostrar');
                        this.totalNews = 0;
                    }
                    else
                    {
                      this.totalSetOrganizers();
                    }
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                    },
                  },
          organizer: {
                    query: GET_ORGANIZER_REPORTS,
                    // Reactive variables
                    variables() {
                      return {
                        id: this.organizer_id,
                        startDatetime_Gt: this.startDatetime_Gt,
                        startDatetime_Lt: null.startDatetime_Lt,
                      }
                    },
                    // Disable the query
                    skip() {
                      return this.skipQuery
                    },
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
        allNews: {
                    query: ALL_NEWS_REPORTS,
                    // Reactive variables
                    variables() {
                      return {
                        createdAt_Gt: this.startDatetime,
                        createdAt_Lt: this.finishDatetime,
                      }
                    },
                    fetchPolicy: 'network-only',
                    // skip() {
                    //   return true
                    // },
                    // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                    if(data.allNews.edges.length == 0)
                    {
                        // this.notifyVue('top','right','info','No hay noticias para mostrar');
                        this.totalNews = 0;
                    }
                    else
                    {
                      this.totalNews = data.allNews.edges.length;
                    }
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                    },
                  },
      },
  components: {
    Datetime
  },
  data() {
    return {
      // Borrar
      startDatetime: new Date("2018/01/01"),
      finishDatetime: new Date("2019/12/31"),
      organizerName: '',
      selectedClose: null,
      // Borrar
      
      totalEvents: 0,
      totalNews: 0,
      organizer_id: null,
      startDatetime_Gt: null,
      startDatetime_Lt: null,
      allEvents:'',
      allOrganizers:'',
      listOrganizers:[],
      allnews:'',
      startMonth: new Date(),
      events: []
    };
  },
  // Filtros para la fecha y hora
    filters: {
      momentUtc: function (date) {
          
      },
      momentWithHour: function (date) {
          moment.locale('es');
          return moment(date).format('LL');
      }

    },
  watch: {
    startDatetime() {
      this.$apollo.queries.allOrganizers.refetch();
      this.$apollo.queries.allNews.refetch();
    },
    finishDatetime() {
      this.$apollo.queries.allOrganizers.refetch();
      this.$apollo.queries.allNews.refetch();
    },
    organizerName(){
      this.$apollo.queries.allOrganizers.refetch();
    }
  },
  methods: {
    // Función para mostrar la información básica del evento
    showSwal: function(eventName,eventStart,eventFinish){
      moment.locale('es');
       var str='<b>Fecha de inicio: </b> '+ moment(eventStart).format("LL, h:mm a") + '<br><b>Fecha de finalización:</b>'+ moment(eventFinish).format("LL, h:mm a")
       swal({
          title: eventName,
          buttonsStyling: false,
          confirmButtonClass: "md-button md-success",
          html: str
        });
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
    // Función que setea los eventos recibidos desde el servidor
    totalSetOrganizers: function(){
      
        if(this.organizerName == '')
        {
          this.listOrganizers = this.allOrganizers;
        }
        var count=0;
        for(var i=0;i<this.allOrganizers.edges.length;i++)
        {
          count = count + this.allOrganizers.edges[i].node.events.edges.length;
        }
        this.totalEvents = count;
      
    },
    // Función que setea los eventos recibidos desde el servidor
    setEvents: function(allEvents){
      for(var i=0;i<this.allEvents.edges.length;i++)
      {
        var start_date = new Date();
        start_date = momentTz.tz(allEvents.edges[i].node.startDatetime,"America/New_York");
        var finish_date = new Date();
        finish_date = momentTz.tz(allEvents.edges[i].node.finishDatetime,"America/New_York");
        this.events.push({
          title: allEvents.edges[i].node.name,
          start: start_date,
          end: finish_date,
          className: "event-red"
        })
      }
      window.$ = window.jQuery = $;
      this.initCalendar($);
    },
    // Función que inicia el calendario
    initCalendar($) {
      var self = this;
      var $calendar = $("#fullCalendar");
      $calendar.fullCalendar({
      eventClick: function(calEvent, jsEvent, view) {
          self.showSwal(calEvent.title,calEvent.start,calEvent.end);
      },
      locale: 'es',
      timeZone: 'UTC-5',
      timeFormat: 'h(:mm)a',
      header: {
        left: "title",
        center: "month,agendaWeek,agendaDay",
        right: "prev,next,today"
      },
      defaultDate: today,
      selectable: false,
      selectHelper: true,
      views: {
        month: {
          // name of view
          titleFormat: "MMMM YYYY"
          // other view-specific options here
        },
        week: {
          titleFormat: " D MMMM YYYY"
        },
        day: {
          titleFormat: "D MMM, YYYY"
        }
      },
      editable: false,
      eventLimit: true, // allow "more" link when too many events
      // color classes: [ event-blue | event-azure | event-green | event-orange | event-red ]
      events: self.events
      });
    }
  },
  beforeCreate(){
    moment.locale('es');
    var stringDate = moment().startOf('month').format("YYYY-MM-DD");
    this.startMonth = moment.utc(stringDate).toISOString();
  },
  mounted() {
    this.$material.locale.days= ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    this.$material.locale.shortDays= ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'];
    this.$material.locale.shorterDays= ['D', 'L', 'M', 'M', 'J', 'V', 'S'];
    this.$material.locale.months= ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    this.$material.locale.shortMonths= ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sept', 'Oct', 'Nov', 'Dic'];
    this.$material.locale.shorterMonths= ['E', 'F', 'M', 'A', 'M', 'Jn', 'Jl', 'A', 'S', 'O', 'N', 'D']
  }
};
</script>
<style lang="scss" scoped>
#fullCalendar {
  min-height: 300px;
}

.md-card-calendar {
  .md-card-content {
    padding: 0 !important;
  }
}

.text-center {
  text-align: center;
}
.md-progress-spinner {
    // margin: 24px;
  }
</style>
