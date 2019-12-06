<template>
  <div class="md-layout">
    <div class="md-layout-item md-size-100">
      <router-link to="/news/add">
        <md-button style="float: right;"
            class="md-button md-just-icon md-theme-default md-info mr-10">
            <md-tooltip  md-direction="left">Agregar noticia</md-tooltip>
            <md-icon>add</md-icon>
        </md-button>
      </router-link>
      <md-card>
        <md-card-header class="md-card-header-icon md-card-header-primary">
          <div class="card-icon">
            <md-icon>library_books</md-icon>
          </div>
          <h4 class="title">Lista de noticias</h4>
        </md-card-header>
        <md-card-content>
            <md-table v-model="lastNews.edges" class="paginated-table table-striped table-hover">
            <md-table-row slot="md-table-row" slot-scope="{ item }">
              <md-table-cell md-label="Nombre">{{ item.node.name }}</md-table-cell>
              <md-table-cell md-label="Resumen">{{ item.node.abstract }}</md-table-cell>
              <md-table-cell md-label="Fecha de publicación">{{ item.node.createdAt | moment }}</md-table-cell>
              <md-table-cell md-label="Acciones" >
                 <a :href="website+'noticias/'+item.node.slug" target="_blank">
                    <md-button class="md-just-icon md-info">
                        <md-tooltip  md-direction="top">Ver</md-tooltip>
                        <md-icon>remove_red_eye</md-icon>
                    </md-button>
                </a>
                    <md-button class="md-just-icon md-danger" @click.native="deleteNews(item.node.id)">
                        <md-tooltip  md-direction="top">Eliminar</md-tooltip>
                        <md-icon>delete</md-icon>
                    </md-button> 
                <router-link :to="'/news/edit/'+item.node.id">
                    <md-button class="md-just-icon md-warning">
                        <md-tooltip  md-direction="top">Editar</md-tooltip>
                        <md-icon>create</md-icon>
                    </md-button>
                </router-link>
              </md-table-cell>
            </md-table-row>
          </md-table>
        </md-card-content>
      </md-card>
      <md-button v-show="lastNews.pageInfo && lastNews.pageInfo.hasNextPage == true" @click.native="loadMore" style="float: right;"
            class="md-info  md-info mr-10">Ver más
        </md-button>
    </div>
  </div>

</template>

<script>
import { Pagination } from "@/components";
import Fuse from "fuse.js";
import swal from "sweetalert2";
import  gql  from 'graphql-tag';
import { LAST_NEWS, DELETE_NEWS} from '../../../plugins/graphql';
import { website } from '../../../plugins/params';
import moment from 'moment';

export default {
    apollo:{
      lastNews: {
                query: LAST_NEWS,
                // Additional options here
                // Reactive variables
                variables() {
                    return {
                    first: 10,
                    after: null
                    }
                },
                fetchPolicy: 'network-only',
                // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {

                    if(data.lastNews.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay noticias');
                    }
                    else
                    {
                        this.setNews(data.lastNews);
                    }

                },
                // Si encontró algún error.
                error(error) {
                    this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                },
              },
      },
  components: {
    Pagination
  },
  computed: {

  },
  data() {
    return {
      website:'',
      skipQuery: true,
      lastNews:'',
      tableData: [],
    };
  },
  // Filtros para la fecha y hora
    filters: {
      moment: function (date) {
          moment.locale('es');
          return moment(date).format('LL, h:mm a');
          // return moment(date).format('LLLL a')
      },
      momentWithHour: function (date) {
          moment.locale('es');
          return moment(date).format('LL');
      }

    },
  methods: {
    // Función para cargas más noticias
      loadMore: function(){
          this.$apollo.queries.lastNews.fetchMore({

              variables:{
                  first:10,
                  after: this.lastNews.pageInfo.endCursor
              },
              updateQuery: (previousResult, { fetchMoreResult }) => {
              const newEdges = fetchMoreResult.lastNews.edges;
              const pageInfo = fetchMoreResult.lastNews.pageInfo;

              return newEdges.length
                  ? {
                      // Put the new news at the end of the list and update `pageInfo`
                      // so we have the new `endCursor` and `hasNextPage` values
                      lastNews: {
                      __typename: previousResult.lastNews.__typename,
                      edges: [...previousResult.lastNews.edges, ...newEdges],
                      pageInfo
                      }
                  }
                  : previousResult;
              }
          })
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
//   Función que elimina una noticia
      deleteNews: function(newId){
          swal({
          title: "¿Está seguro?",
          text: `La noticia será eliminada del almacenamiento`,
          type: "warning",
          showCancelButton: true,
          confirmButtonClass: "md-button md-success",
          cancelButtonClass: "md-button md-danger",
          cancelButtonText: "Cancelar",
          confirmButtonText: "Si, borrar",
          buttonsStyling: false
        }).then(result => {
          if (result.value) {
                this.sendingNews = true;
                // Iniciamos el envío de la mutación
                this.$apollo.mutate({
                    mutation: DELETE_NEWS,
                    variables:{
                    input:{
                        id: newId,
                    }
                    }
                }).then((data) => {
                    if(data.data.deleteNews.success == true)
                    {
                        this.notifyVue('top','right','success','Noticia eliminada correctamente');
                        this.sendingNews = false;

                
                    }
                    else
                    {
                        this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
                        this.sendingNews = false;
                    }


                }).catch((error) => {
                    // Error
                    this.sendingNews = false;
                    this.notifyVue('top','right','warning','Ha ocurrido un errorsito, inténtalo de nuevo');
                });
          }
        });

      },
    // Función que setea las categorías para ser visualizados en la tabla
    setNews: function(allnews){
        moment.locale('es');
        for(var i=0;i<allnews.edges.length;i++)
        {
            this.tableData.push({
                id: allnews.edges[i].node.id,
                slug: allnews.edges[i].node.slug,
                name: allnews.edges[i].node.name,
                abstract: allnews.edges[i].node.abstract,
                createdAt: moment(allnews.edges[i].node.createdAt).format("LL, h:mm a"),
            })
        }
    },
  },
  mounted() {
    this.website = website;
  },
  destroyed(){

  },
  watch: {

  }
};
</script>

<style lang="css" scoped>
.md-card .md-card-actions{
  border: 0;
  margin-left: 20px;
  margin-right: 20px;
}
.custom-tooltip {
  background-color: black !important;
  color: white !important;

}
</style>
