<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>library_books</md-icon>
                    </div>
                    <h4 class="title">Registrar noticia</h4>
                </md-card-header>

                <md-card-content>
                     <!-- Nombre de noticia -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Nombre -->
                            <md-field :class="[
                            {'md-valid': !errors.has('newsName') && touched.newsName},
                            {'md-error': errors.has('newsName')}]">
                            <label>Nombre de noticia</label>
                            <md-input
                                v-model="newsName"
                                data-vv-name="newsName"
                                type="text"
                                required
                                v-validate="modelValidations.newsName">
                            </md-input>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('newsName') && touched.newsName">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('newsName') && touched.newsName">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Nombre -->
                        </div>
                     </div>   
                     <!-- ./ Nombre de noticia -->
                      <!-- Resumen de noticia -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Resumen -->
                            <md-field :class="[
                            {'md-valid': !errors.has('newsAbstract') && touched.newsAbstract},
                            {'md-error': errors.has('newsAbstract')}]">
                            <label>Resumen de noticia</label>
                            <md-textarea md-autogrow
                                v-model="newsAbstract"
                                data-vv-name="newsAbstract"
                                type="text"
                                required
                                v-validate="modelValidations.newsAbstract">
                            </md-textarea>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('newsAbstract') && touched.newsAbstract">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('newsAbstract') && touched.newsAbstract">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Resumen -->
                        </div>
                     </div>   
                     <!-- ./ Resumen de noticia -->
                     <!-- Imagen de noticia existente -->
                     <div v-show="principalImage.id != ''" class="md-layout md-alignment-top-center" >
                        <div class="md-layout-item md-size-30 md-xsmall-size-100 " >
                            <h4 class="card-title">Imagen principal de noticia*</h4>
                            <product-card
                                header-animation="false">
                                <img class="img" slot="imageHeader" :src="principalImage.imageFile">
                                <div slot="footer" class="button-container md-layout text-center">
                                    <md-button v-show="sendingPrincipalImage == false" @click.native="deletePrincipalImage(principalImage.id)" class="md-danger">Eliminar</md-button>
                                    <md-progress-spinner v-show="sendingPrincipalImage == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                                </div>
                                 
                                 
                            </product-card>
                        </div>
                    </div>
                     <!-- ./ Imagen de noticia existente -->
                     <!-- Imagen principal de noticia -->
                     <div v-show="principalImage.id == ''" class="md-layout md-alignment-top-center" >
                        <div class="md-layout-item md-size-30 md-xsmall-size-100 " >
                            <h4 class="card-title">Imagen principal de noticia*</h4>
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
                                <!-- <md-button class="md-danger md-round" @click="removeImage" v-if="imageRegular"><i class="fa fa-times"></i>Eliminar</md-button> -->
                                <md-button class="md-success  md-fileinput">
                                    <template v-if="!imageRegular">Seleccione imagen</template>
                                    <template v-else>Cambiar</template>
                                    <input required type="file" @change="onFileChange">
                                </md-button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <br>
                     <!-- ./ Imagen principal de noticia -->
                     <!-- Descripción de noticia -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                          <h4 class="card-title">Descripción completa de la noticia*</h4>
                             <md-button @click.native="showPreview" style="float: right;" class="md-simple md-default md-just-icon">
                                <i class="fa fa-eye"></i>
                                <md-tooltip  md-direction="right">Vista previa</md-tooltip>
                             </md-button>
                             <!-- Descripción -->
                            <vue-editor v-model="newsDescription" :editorToolbar="customToolbar"></vue-editor>
                             <!-- ./ Descripción -->
                        </div>
                        <div v-show="preview == true" class="md-layout-item md-size-100 md-small-size-100">
                          <h4 class="card-title">Vista previa de la noticia</h4>
                             <!-- Preview de descripción -->
                            <div class='browser-window'>
                                <div class='top-bar'>
                                  <div class='circles'>
                                    <div class="circle circle-red"></div>
                                    <div class="circle circle-yellow"></div>
                                    <div class="circle circle-green"></div>
                                  </div>
                                </div>
                                <div style="word-wrap:break-word;" v-html="newsDescription" class='content'>
                                  
                                </div>
                              </div>
                              <!-- ./ preview de descripción -->
                        </div>
                     </div> 
                     <!-- ./ Descripción de noticia -->
                     <!-- Galería de noticia -->
                     <!-- Imagen de noticia existente -->
                     <div style="margin-top:20px;" v-show="newsImages != []" class="md-layout " >
                        <div v-for="image in newsImages" :key="image.id" class="md-layout-item md-size-30 md-xsmall-size-100 " >
                            <product-card
                                header-animation="false">
                                <img class="img" slot="imageHeader" :src="image.imageFile">
                                <div slot="footer" class="button-container md-layout text-center">
                                    <md-button v-show="sendigImage == false" @click.native="deleteImage(image.id)" class="md-danger">Eliminar</md-button>
                                    <md-progress-spinner v-show="sendigImage == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                                </div>
                                 
                                 
                            </product-card>
                        </div>
                    </div>
                     <!-- ./ Imagen de noticia existente -->
                     <div style="margin-top:50px;" class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                            <h4 class="card-title">Galería de imágenes</h4>
                             <!-- Galería -->
                            <vue-upload-multiple-image class="image-change"
                                :dragText="dragText"
                                :browseText="browseText"
                                :dropText="dropText"
                                :primaryText="primaryText"
                                :markIsPrimaryText="markIsPrimarytext"
                                :popupText="popupText"
                                @upload-success="uploadImageSuccess"
                                @before-remove="beforeRemove"
                                @edit-image="editImage"
                                @data-change="dataChange"
                                :data-images="images"
                                ></vue-upload-multiple-image>
                            <!-- ./ Galería -->
                        </div>
                     </div>   
                     <!-- ./ Galería de noticia -->
                   <div class="form-category">* Campos obligatorios</div>
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/news"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Actualizar</md-button>
                    <md-progress-spinner v-show="sending == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import swal from "sweetalert2";
import { ProductCard } from "@/components";
import { SlideYDownTransition } from "vue2-transitions";
import { UPDATE_NEWS, GET_NEWS_BY_ID, ADD_IMAGES_TO_POST, DELETE_IMAGE_BY_ID } from '../../../plugins/graphql';
import { mediaUrl,myUrl } from '../../../plugins/params';
import { uploadFilesToGraphQLXr } from '../../../plugins/uploadFilesToGraphQLXr';
// Editors
import {VueEditor} from 'vue2-editor';

import VueUploadMultipleImage from 'vue-upload-multiple-image';
export default {
apollo:{
    news: {
                query: GET_NEWS_BY_ID,
                // Reactive variables
                variables() {
                    return {
                    id: this.$route.params.news_id
                    }
                },
                fetchPolicy: 'network-only',
                // Disable the query
                // skip() {
                //   return this.skipQuery
                // },
                    // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {
                if(data.news == null)
                {
                    this.notifyVue('top','right','info','No existe la noticia');
                    this.$router.push('/news');
                }
                else
                {
                    this.setNews(data.news);
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
    VueEditor,
    VueUploadMultipleImage,
    ProductCard
  },
  data() {
    return {
      editor:null,
      // Propiedades para el editor de texto -> Vue-editor
      customToolbar: [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'script': 'sub' }, { 'script': 'super' }],      // superscript/subscript
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'color': [] }, { 'background': [] }], 
        ['link'],         // dropdown with defaults from theme
        ['clean']
      ],
      news:'',
      dragText:"Arrastre los archivos aquí",
      browseText:"Buscar archivos...",
      dropText:"Suelte los archivos aquí...",
      markIsPrimarytext:"Galería de imágenes",
      popupText:"Estas imágenes serán visualizadas en la galería de la noticia",
      primaryText:"Galería de imagenes",
      // Propiedad para saber si el formulario se está enviando y ocultar el botón de registrar
      sendingPrincipalImage: false,
      sendigImage:false,
      sending: false,
      preview: false,
      formData:"",
      imageRegular: "",
      boolean: null,
      principalImage:{
          imageFile:'',
          id:''
      },
      newsImages:[],
      newsId:"",
      newsName: "",
      newsAbstract: "",
      newsDescription: "<h1>Escriba aquí el contenido de la noticia...</h1>",
      imageName: "",
      images: [],
      touched: {
        newsName: false,
        newsAbstract: false,
      },
      variables:{
        input:{
          id:'',
          images: [],
        }
      },
      modelValidations: {
        newsName:{
            required: true,
            min: 1,
            max: 64
        },
        newsAbstract:{
            required: true,
            min: 5,
            max: 140
        },
      }
    };
  },
  methods: {
      // Función para mostrar la vista previa
      showPreview: function(){
        this.preview = !(this.preview);
      },
      //   Función que elimina cualquier imagen
      deleteImage: function(imageId){
          swal({
          title: "¿Está seguro?",
          text: `La imagen será eliminada del almacenamiento`,
          type: "warning",
          showCancelButton: true,
          confirmButtonClass: "md-button md-success",
          cancelButtonClass: "md-button md-danger",
          cancelButtonText: "Cancelar",
          confirmButtonText: "Si, borrar",
          buttonsStyling: false
        }).then(result => {
          if (result.value) {
            this.sendingImage = true;
            // Iniciamos el envío de la mutación
            this.$apollo.mutate({
            mutation: DELETE_IMAGE_BY_ID,
            variables:{
              input:{
                  id: imageId,
              }
            }
            }).then((data) => {
            if(data.data.deleteImage.success == true)
            {
                this.notifyVue('top','right','success','Imagen  eliminada correctamente');
                this.sendingImage = false;
                for(var i=0;i<this.newsImages.length;i++)
                {
                    if(this.newsImages[i].id == imageId)
                    {
                        this.newsImages.splice(i,1);
                    }
                }
            }
            else
            {
                this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
                this.sendingImage = false;
            }
          }).catch((error) => {
            // Error
            this.sendingImage = false;
            this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
          });
          }
        });
        
      },
    //   Función que elimina la imagen principal
      deletePrincipalImage: function(imageId){
          swal({
          title: "¿Está seguro?",
          text: `La imagen será eliminada del almacenamiento`,
          type: "warning",
          showCancelButton: true,
          confirmButtonClass: "md-button md-success",
          cancelButtonClass: "md-button md-danger",
          cancelButtonText: "Cancelar",
          confirmButtonText: "Si, borrar",
          buttonsStyling: false
        }).then(result => {
          if (result.value) {
                this.sendingPrincipalImage = true;
                // Iniciamos el envío de la mutación
                this.$apollo.mutate({
                    mutation: DELETE_IMAGE_BY_ID,
                    variables:{
                    input:{
                        id: imageId,
                    }
                    }
                }).then((data) => {
                    if(data.data.deleteImage.success == true)
                    {
                        this.notifyVue('top','right','success','Imagen principal eliminada correctamente');
                        this.sendingPrincipalImage = false;
                        this.principalImage.imageFile = "";
                        this.principalImage.id = "";
                    }
                    else
                    {
                        this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
                        this.sendingPrincipalImage = false;
                    }
                    
                    
                }).catch((error) => {
                    // Error
                    this.sendingPrincipalImage = false;
                    this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
                });
          }
        });
        
      },
    // Función que setea la noticia
    setNews: function(news){
        this.newsId = news.id;
        this.newsName = news.name;
        this.newsAbstract = news.abstract;
        this.newsDescription = news.description;
        for(var i = 0;i<news.post.images.edges.length;i++)
        {
            if(news.post.images.edges[i].node.principal == true)
            {
                this.principalImage.id = news.post.images.edges[i].node.id;
                this.principalImage.imageFile = mediaUrl+news.post.images.edges[i].node.imageFile;
            }
            else
            {
                this.newsImages.push({
                    id: news.post.images.edges[i].node.id,
                    imageFile: mediaUrl+news.post.images.edges[i].node.imageFile
                })
            }
        }
      },
       uploadImageSuccess(formData, index, fileList) {
        this.formData.append(formData.get("file").name,formData.get("file"));
        this.variables.input.images.push({
          principal: false,
          imageFile: formData.get("file").name
        })
    },
    beforeRemove (index, done, fileList) {
      this.formData.delete(fileList[index].name);
      for(var i=0;i<this.variables.input.images.length;i++)
      {
        if(this.variables.input.images[i].imageFile == fileList[index].name)
        {
          this.variables.input.images.splice(i,1);
          done()
          return
        }
      }
      
      
    },
    editImage (formData, index, fileList) {
      this.formData.delete(fileList[index].name);
      for(var i=0;i<this.variables.input.images.length;i++)
      {
        if(this.variables.input.images[i].imageFile == fileList[index].name)
        {
          this.variables.input.images.splice(i,1);
          this.formData.append(formData.get("file").name,formData.get("file"));
          this.variables.input.images.push({
              principal: false,
              imageFile: formData.get("file").name
            })
          return
        }
      }
      
      
    },
    dataChange (data) {
    },
    
    // Función para inicializar el formData
    initializeFormData: function(){
      this.formData = new FormData();
      this.formData.append("query",ADD_IMAGES_TO_POST);
    },
    // función para setear el formData
    removeImg: function(){

    },
    onFileChange(e) {
    if(this.imageName != '')
    {
      this.formData.delete(this.imageName);
      for(var i=0;i<this.variables.input.images.length;i++)
      {
        if(this.variables.input.images[i].imageFile == this.imageName)
        {
          console.log('se está eliminando la imagen: '+this.variables.input.images[i].imageFile);
          this.variables.input.images.splice(i,1);
          console.log('nuevo arreglo de imágenes: '+JSON.stringify(this.variables)) ;
        }
      }
    }
    let files = e.target.files || e.dataTransfer.files;
    this.formData.append(files[0].name,files[0]);
    this.imageName = files[0].name; 
    this.variables.input.images.push({
      principal: true,
      imageFile: files[0].name
    })
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
            if(this.formData.get(this.imageName) == null && this.principalImage.id == '')
            {
              this.notifyVue('top','right','warning','No hay una imagen principal seleccionada');
              return
            }
            if(this.newsDescription == null)
            {
              this.notifyVue('top','right','warning','No hay una descripción de la noticia');
              return
            }
            this.$apollo.mutate({
              mutation: UPDATE_NEWS,
              variables:{
                input:{
                  id: this.newsId,
                  news:{
                    name: this.newsName,
                    abstract: this.newsAbstract,
                    description: this.newsDescription
                  }
                }
              }
            }).then((data) => {
              // Mutación que refresca el token
              var news_id = data.data.updateNews.updatedNews.id;
              this.variables.input.id = news_id;
              // Finaliza las mutaciones
              this.sending = true;
              this.formData.append("variables",JSON.stringify(this.variables));
              uploadFilesToGraphQLXr(this.formData).then(() => {
                this.notifyVue('top','right','success','Noticia editada correctamente');
                this.$router.push('/news');
              }).catch(() => {
                this.sending = false;
                this.notifyVue('top','right','danger','Algo ha salido mal, inténtalo de nuevo');
              })
              
            }).catch((error) => {
              // Error
              this.notifyVue('top','right','warning','Algo ha pasado y la noticia no ha sido guardada, inténtalo de nuevo');
            });
            

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
    newsName() {
      this.touched.newsName = true;
    },
    newsAbstract() {
      this.touched.newsAbstract = true;
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
.image-change{
  /deep/ .image-container{
    width: 100%;
    max-width: 100%;
    background-color: rgb(231, 231, 231);
  }
   /deep/  .image-icon-drag{
   fill: gray;
  }
}


// browser window css
$bottomColor: #E2E2E1;
$topColor: lighten($bottomColor, 2%);

$border: $bottomColor;

$width: 800px;
$height: 500px;

.browser-window {
  text-align: left;
  // margin: 20px;
  width: 100%;
  height: $height;
  display: inline-block;
  border-radius: 5px;
  background-color: #fff;
}
.browser-window .top-bar {
  height: 30px;
  border-radius: 5px 5px 0 0;
  border-top: thin solid lighten($topColor, 1%);
  border-bottom: thin solid darken($bottomColor, 1%);
  background: linear-gradient($topColor, $bottomColor);
}
.browser-window .circle {
  height: 8px;
  width: 8px;
  display: inline-block;
  border-radius: 50%;
  background-color: lighten($topColor, 10%);
}
.browser-window .circles { margin: 5px 11px; }
.browser-window .content {
  margin: 0;
  width: 100%;
  min-height: 50%;
  display: inline-block;
  border-radius: 0 0 5px 5px;
  background-color: #fafafa;
}

.browser-window .dev-tools {
  width: 100%;
  min-height: 50%;
  margin: 0;
  padding: 0;
}

.browser-window .dev-tools .bar {
  margin-top: -4px;
  border-top: thin solid $topColor;
  border-bottom: thin solid $topColor;
  color: $topColor;
  .dev-bar-content {
    padding: 10px;
    float: left;
  }
  .close { 
    float: right;
    border-left: thin solid $topColor;
    padding: 10px;
  }
}

.browser-window .dev-tools .content {
  .html {
    height: 100%;
    width: 69%;
    border-right: thin solid $topColor;
  }
  .css { 
    float: right;
    height: 100%;
    width: 30%;
  }
}

.clear { clear: both; }
</style>
