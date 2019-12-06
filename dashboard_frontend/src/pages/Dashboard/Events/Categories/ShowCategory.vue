<template>
  <div class="md-layout">
    <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-33">
      <product-card v-bind:url="'/events/categories/edit/'+categoryId"
        header-animation="true">
        <img class="img" slot="imageHeader" :src="categoryImage">
        <md-icon slot="fixed-button">build</md-icon>
        <template slot="first-button">
            <md-icon >edit</md-icon>
            <md-tooltip md-direction="bottom">Editar</md-tooltip>
        </template>
        <h4 slot="title" class="title">
          {{categoryName}}
        </h4>
        <div slot="description" class="card-description">
         {{categoryDescription}}
        </div>
        <template slot="footer">
          <router-link to="/events/categories"><md-button class="md-default">Volver</md-button></router-link>
        </template>
      </product-card>
    </div>
  </div>
</template>

<script>
import { GET_CATEGORY_BY_ID } from '../../../../plugins/graphql';
import { mediaUrl } from '../../../../plugins/params';
import {
  ProductCard,
  AnimatedNumber,
} from "@/components";

export default {
  apollo:{
        category: {
                    query: GET_CATEGORY_BY_ID,
                    fetchPolicy: 'network-only',
                    // Reactive variables
                    variables() {
                      return {
                        id: this.$route.params.category_id
                      }
                    },
                    // Disable the query
                    // skip() {
                    //   return this.skipQuery
                    // },
                      // Si tenemos un resultado, pero no encontró el slug.
                    result({ data, loading, networkStatus }) {
                    if(data.category == null)
                    {
                        this.notifyVue('top','right','info','No existe la categoría');
                        this.$router.push('/events/categories');
                    }
                    else
                    {
                      this.setCategory(data.category);
                    }
                    },
                    // Si encontró algún error.
                    error(error) {
                        this.notifyVue('top','right','warning','Algo ha pasado, inténtalo de nuevo');
                    },
                  },
      },
  components: {
    AnimatedNumber,
    ProductCard
  },
  data() {
    return {
      categoryName:'',
      categoryDescription:'',
      categoryId:'',
      categoryImage:'',
      product1: "./img/card-2.jpg",
      product2: "./img/card-3.jpg",
      product3: "./img/card-1.jpg",
      seq2: 0,
     
      
    };
  },
  methods:{
      // Función que setea la categoría
      setCategory: function(category){
        this.categoryName = category.name;
        this.categoryDescription = category.description;
        this.categoryId = category.id;
        this.categoryImage = mediaUrl+category.image
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
  mounted(){
  }
};
</script>
