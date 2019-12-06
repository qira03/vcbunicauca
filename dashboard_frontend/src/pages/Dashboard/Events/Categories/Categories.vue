<template>
  <div class="md-layout">
    <div class="md-layout-item">
         <router-link to="/events/categories/add">
            <md-button style="float: right;"
                class="md-button md-just-icon md-theme-default md-info mr-10">
                <md-tooltip  md-direction="left">Agregar categoría</md-tooltip>
                <md-icon>add</md-icon>
            </md-button>
         </router-link>
      <md-card>
        <md-card-header class="md-card-header-icon md-card-header-primary">
          <div class="card-icon">
            <md-icon>category</md-icon>
          </div>
          <h4 class="title">Lista de categorías</h4>
        </md-card-header>
        <md-card-content>
          <md-table :value="queriedData" :md-sort.sync="currentSort" :md-sort-order.sync="currentSortOrder" :md-sort-fn="customSort" class="paginated-table table-striped table-hover">
            <md-table-toolbar>
              <md-field>
                <label for="pages">Por página</label>
                <md-select v-model="pagination.perPage" name="pages">
                  <md-option
                    v-for="item in pagination.perPageOptions"
                    :key="item"
                    :label="item"
                    :value="item">
                    {{ item }}
                  </md-option>
                </md-select>
              </md-field>

              <md-field>
                <md-input
                  type="search"
                  class="mb-3"
                  clearable
                  style="width: 200px"
                  placeholder="Buscar..."
                  v-model="searchQuery">
                </md-input>
              </md-field>
            </md-table-toolbar>

            <md-table-row slot="md-table-row" slot-scope="{ item }">
              <md-table-cell md-label="Nombre" md-sort-by="name">{{ item.name }}</md-table-cell>
              <md-table-cell md-label="Descripción" md-sort-by="description">{{ item.description }}</md-table-cell>
              <md-table-cell md-label="Acciones">
                <router-link :to="'/events/categories/show/'+item.id">
                    <md-button class="md-just-icon md-info">
                        <md-tooltip  md-direction="top">Ver</md-tooltip>
                        <md-icon>remove_red_eye</md-icon>
                    </md-button>
                </router-link>
                <router-link :to="'/events/categories/edit/'+item.id">
                    <md-button class="md-just-icon md-warning">
                        <md-tooltip  md-direction="top">Editar</md-tooltip>
                        <md-icon>create</md-icon>
                    </md-button>
                </router-link>
                <router-link :to="'/events/categories/related_links/'+item.id">
                    <md-button class="md-just-icon md-default">
                        <md-tooltip  md-direction="left">Enlaces relacionados</md-tooltip>
                        <md-icon>link</md-icon>
                    </md-button>
                </router-link>
                <!-- <md-button
                  class="md-just-icon md-danger"
                  @click.native="handleDelete(item)">
                  <md-tooltip  md-direction="top">Desactivar</md-tooltip>
                  <md-icon>pause</md-icon>
                </md-button> -->
              </md-table-cell>
            </md-table-row>
          </md-table>
          <div class="footer-table md-table">
            <table>
              <tfoot>
                <tr>
                  <th v-for="item in footerTable" :key="item.name" class="md-table-head">
                    <div class="md-table-head-container md-ripple md-disabled">
                      <div class="md-table-head-label">
                        {{item}}
                      </div>
                    </div>
                  </th>
                </tr>
              </tfoot>
            </table>
          </div>
        </md-card-content>
        <md-card-actions md-alignment="space-between">
          <div class="">
            <p class="card-category">Mostrando {{from + 1}} a {{to}} de {{total}} registros</p>
          </div>
          <pagination class="pagination-no-border pagination-primary"
                        v-model="pagination.currentPage"
                        :per-page="pagination.perPage"
                        :total="total">
          </pagination>
        </md-card-actions>
      </md-card>
    </div>
  </div>

</template>

<script>
import { Pagination } from "@/components";
import Fuse from "fuse.js";
import swal from "sweetalert2";
import  gql  from 'graphql-tag';
import { ALL_USERS, ALL_CATEGORIES} from '../../../../plugins/graphql';


export default {
    apollo:{
      allCategories: {
                query: ALL_CATEGORIES,
                fetchPolicy: 'network-only',
                // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {
                    
                    if(data.allCategories.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay categorías');
                    }
                    else
                    {
                        this.setCategories(data.allCategories);
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
    /***
     * Returns a page from the searched data or the whole data. Search is performed in the watch section below
     */
    queriedData() {
      let result = this.tableData;
      if (this.searchedData.length > 0) {
        result = this.searchedData;
      }
      return result.slice(this.from, this.to);
    },
    to() {
      let highBound = this.from + this.pagination.perPage;
      if (this.total < highBound) {
        highBound = this.total;
      }
      return highBound;
    },
    from() {
      return this.pagination.perPage * (this.pagination.currentPage - 1);
    },
    total() {
      return this.searchedData.length > 0
        ? this.searchedData.length
        : this.tableData.length;
    }
  },
  data() {
    return {
      skipQuery: true,
      allUsers:'',
      allCategories:'',
      currentSort: "name",
      currentSortOrder: "asc",
      pagination: {
        perPage: 5,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50],
        total: 0
      },
      footerTable: ["Nombre", "Descripción", "Acciones"],
      searchQuery: "",
      propsToSearch: ["name", "description"],
      tableData: [],
      searchedData: [],
      fuseSearch: null
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
    // Función que setea las categorías para ser visualizados en la tabla
    setCategories: function(allCategories){
        for(var i=0;i<allCategories.edges.length;i++)
        {
            this.tableData.push({
                id: allCategories.edges[i].node.id,
                name: allCategories.edges[i].node.name,
                description: allCategories.edges[i].node.description,
            })
        }
    },
    customSort(value) {
      return value.sort((a, b) => {
        const sortBy = this.currentSort;
        if (this.currentSortOrder === "desc") {
          return a[sortBy].localeCompare(b[sortBy]);
        }
        return b[sortBy].localeCompare(a[sortBy]);
      });
    },
    
  },
  mounted() {
    // Fuse search initialization.
    this.fuseSearch = new Fuse(this.tableData, {
      keys: ["name", "description"],
      threshold: 0.3
    });
  },
  destroyed(){
      
  },
  watch: {
    /**
     * Searches through the table data by a given query.
     * NOTE: If you have a lot of data, it's recommended to do the search on the Server Side and only display the results here.
     * @param value of the query
     */
    searchQuery(value) {
      let result = this.tableData;
      if (value !== "") {
        result = this.fuseSearch.search(this.searchQuery);
      }
      this.searchedData = result;
    }
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
