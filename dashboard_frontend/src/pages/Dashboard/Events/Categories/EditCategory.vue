<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>category</md-icon>
                    </div>
                    <h4 class="title">Editar categoría</h4>
                </md-card-header>

                <md-card-content>
                     <!-- Nombre de categoría -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Nombre -->
                            <md-field :class="[
                            {'md-valid': !errors.has('categoryName') && touched.categoryName},
                            {'md-error': errors.has('categoryName')}]">
                            <label>Nombre de categoría</label>
                            <md-input
                                v-model="categoryName"
                                data-vv-name="categoryName"
                                type="text"
                                required
                                v-validate="modelValidations.categoryName">
                            </md-input>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('categoryName') && touched.categoryName">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('categoryName') && touched.categoryName">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Nombre -->
                        </div>
                     </div>   
                     <!-- ./ Nombre de categoría -->
                      <!-- Descripción de categoría -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Descripción -->
                            <md-field :class="[
                            {'md-valid': !errors.has('categoryDescription') && touched.categoryDescription},
                            {'md-error': errors.has('categoryDescription')}]">
                            <label>Descripción de categoría</label>
                            <md-textarea md-autogrow
                                v-model="categoryDescription"
                                data-vv-name="categoryDescription"
                                type="text"
                                required
                                v-validate="modelValidations.categoryDescription">
                            </md-textarea>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('categoryDescription') && touched.categoryDescription">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('categoryDescription') && touched.categoryDescription">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Descripción -->
                        </div>
                     </div>   
                     <!-- ./ Descripción de categoría -->
                     <!-- Subir imagen de categoría -->
                     <div class="md-layout md-alignment-top-center" >
                        <div class="md-layout-item md-size-30 md-xsmall-size-100 " >
                            <h4 class="card-title">Imagen de categoría</h4>
                            <div class="file-input">
                                <div v-if="!imageRegular">
                                <div class="image-container">
                                    <img :src="regularImg" title="">
                                </div>
                                </div>
                                <div class="image-container" v-else>
                                <img :src="imageRegular" />
                                </div>
                                <div class="button-container">
                                <md-button class="md-success  md-fileinput">
                                    <template v-if="!imageRegular">Seleccione imagen</template>
                                    <template v-else>Cambiar</template>
                                    <input required type="file" @change="onFileChange">
                                </md-button>
                                </div>
                            </div>
                        </div>
                    </div>
                     <!-- ./ Subir imagen de categoría -->
                   <div class="form-category">* Campos obligatorios (Imagen opcional)</div>
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/events/categories"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Actualizar</md-button>
                    <md-progress-spinner v-show="sending == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import { SlideYDownTransition } from "vue2-transitions";
import { GET_CATEGORY_BY_ID, UPDATE_CATEGORY } from '../../../../plugins/graphql';
import { mediaUrl, myUrl } from '../../../../plugins/params';
import { uploadFilesToGraphQLXr } from '../../../../plugins/uploadFilesToGraphQLXr';
import { ProductCard } from "@/components";
export default {
    apollo:{
        category: {
                    query: GET_CATEGORY_BY_ID,
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
 props: {
    regularImg: {
      type: String,
      default: "./img/image_placeholder.jpg"
    }
  },
  components: {
    SlideYDownTransition,
    ProductCard
  },
  data() {
    return {
      sending: false,
      formData:"",
      imageRegular: "",
      boolean: null,
      categoryId:"",
      categoryName: "",
      categoryDescription: "",
      categoryImage:"",
      imageName: "",
      touched: {
        categoryName: false,
        categoryDescription: false,
      },
      variables:{
        input:{
          id:'',  
          category:{
            name:'',
            description:'',
            image:''
          }
        }
      },
      modelValidations: {
        categoryName:{
            required: true,
            min: 1,
            max: 32
        },
        categoryDescription:{
            required: true,
            min: 5,
            max: 128
        },
      }
    };
  },
  methods: {
      // Función que setea la categoría
      setCategory: function(category){
        this.categoryName = category.name;
        this.categoryDescription = category.description;
        this.categoryId = category.id;
        this.categoryImage = mediaUrl+category.image;
      },
      // Función para inicializar el formData
      initializeFormData: function(){
        this.formData = new FormData();
        this.formData.append("query",UPDATE_CATEGORY);
      },
      // función para setear el formData
      removeImg: function(){

      },
      onFileChange(e) {
      if(this.imageName != '')
      {
        this.formData.delete(this.imageName);
      }
      let files = e.target.files || e.dataTransfer.files;
      this.formData.append(files[0].name,files[0]);
      this.imageName = files[0].name; 
      if (!files.length) return;
      if (e.target.name) {
        this.createImage(files[0], "circle");
      } else {
        this.createImage(files[0]);
      }
    },
    createImage(file, type) {
      let reader = new FileReader();
      let vm = this;

      reader.onload = e => {
        if (type === "circle") {
          vm.imageCircle = e.target.result;
        } else {
          vm.imageRegular = e.target.result;
        }
      };
      reader.readAsDataURL(file);
    },
    removeImage: function(type) {
      if (type === "circle") {
        this.imageCircle = "";
      } else {
        this.imageRegular = "";
        this.formData.delete(this.imageName);
        this.imageName = '';
      }
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
            this.variables.input.id = this.categoryId;
            this.variables.input.category.name = this.categoryName;
            this.variables.input.category.description = this.categoryDescription;
            this.variables.input.category.image = this.imageName;
            this.formData.append("variables",JSON.stringify(this.variables));
            uploadFilesToGraphQLXr(this.formData).then(() => {
              this.notifyVue('top','right','success','Categoría editada correctamente');
              this.$router.push('/events/categories');
            }).catch(() => {
              this.sending = false;
              this.notifyVue('top','right','danger','Algo ha salido mal, inténtalo de nuevo');
            })

        }
        else
        {
            this.notifyVue('top','right','warning','Los campos no están correctamente diligenciados');
        }
        
      });
    }
  },
  mounted(){
    this.initializeFormData();
  },
  watch: {
    categoryName() {
      this.touched.categoryName = true;
    },
    categoryDescription() {
      this.touched.categoryDescription = true;
    },
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
