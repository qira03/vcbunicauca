<template>
  <div class="md-layout">
    <div class="md-layout-item">
         <router-link to="/events/venues/add">
            <md-button style="float: right;"
                class="md-button md-just-icon md-theme-default md-info mr-10">
                <md-tooltip  md-direction="left">Agregar lugar de evento</md-tooltip>
                <md-icon>add</md-icon>
            </md-button>
         </router-link>
      <md-card>
        <md-card-header class="md-card-header-icon md-card-header-primary">
          <div class="card-icon">
            <md-icon>pin_drop</md-icon>
          </div>
          <h4 class="title">Lista de lugares</h4>
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
              <md-table-cell md-label="Dirección" md-sort-by="phone">{{ item.address }}</md-table-cell>
              <md-table-cell md-label="Ciudad" md-sort-by="website">{{ item.city }}</md-table-cell>
              <md-table-cell md-label="Teléfono" md-sort-by="email">{{ item.phone }}</md-table-cell>
              <md-table-cell md-label="Acciones">
              <router-link :to="'/events/venues/show/'+item.id">
                <md-button class="md-just-icon md-info">
                    <md-tooltip  md-direction="top">Ver</md-tooltip>
                    <md-icon>remove_red_eye</md-icon>
                </md-button>
              </router-link>
              <router-link :to="'/events/venues/edit/'+item.id">
                <md-button class="md-just-icon md-warning">
                    <md-tooltip  md-direction="top">Editar</md-tooltip>
                    <md-icon>create</md-icon>
                </md-button>
              </router-link>
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
import { ALL_VENUES} from '../../../../plugins/graphql';


export default {
    apollo:{
      allVenues: {
                query: ALL_VENUES,
                // Additional options here
                fetchPolicy: 'network-only',
                // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {
                    
                    if(data.allVenues.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay lugares de eventos');
                    }
                    else
                    {
                        this.setVenues(data.allVenues);
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
      allOrganizers:'',
      currentSort: "name",
      currentSortOrder: "asc",
      pagination: {
        perPage: 5,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50],
        total: 0
      },
      footerTable: ["Nombre", "Dirección","Ciudad","Teléfono", "Acciones"],
      searchQuery: "",
      propsToSearch: ["name", "address", "city", "phone"],
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
    // Función que setea los organizadores para ser visualizados en la tabla
    setVenues: function(allVenues){
        for(var i=0;i<allVenues.edges.length;i++)
        {
            this.tableData.push({
                id: allVenues.edges[i].node.id,
                name: allVenues.edges[i].node.name,
                address: allVenues.edges[i].node.address,
                city: allVenues.edges[i].node.city,
                phone: allVenues.edges[i].node.phone
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
    handleLike(item) {
      swal({
        title: `You liked ${item.name}`,
        buttonsStyling: false,
        type: "success",
        confirmButtonClass: "md-button md-success"
      });
    },
    handleEdit(item) {
      swal({
        title: `You want to edit ${item.name}`,
        buttonsStyling: false,
        confirmButtonClass: "md-button md-info"
      });
    },
    handleDelete(item) {
      swal({
        title: "Are you sure?",
        text: `You won't be able to revert this!`,
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: "md-button md-success btn-fill",
        cancelButtonClass: "md-button md-danger btn-fill",
        confirmButtonText: "Yes, delete it!",
        buttonsStyling: false
      }).then(result => {
        if (result.value) {
          this.deleteRow(item);
          swal({
            title: "Deleted!",
            text: `You deleted ${item.name}`,
            type: "success",
            confirmButtonClass: "md-button md-success btn-fill",
            buttonsStyling: false
          });
        }
      });
    },
    deleteRow(item) {
      let indexToDelete = this.tableData.findIndex(
        tableRow => tableRow.id === item.id
      );
      if (indexToDelete >= 0) {
        this.tableData.splice(indexToDelete, 1);
      }
    }
  },
  mounted() {
    // Fuse search initialization.
    this.fuseSearch = new Fuse(this.tableData, {
      keys: ["name", "address", "city", "phone"],
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
