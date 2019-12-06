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
                     <!-- Imagen principal de noticia -->
                     <div class="md-layout md-alignment-top-center" >
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
                                    <template v-else>Cambiar Imagen</template>
                                    <input required type="file" @change="onFileChange">
                                </md-button>
                                </div>
                                <div class="button-container">
                                <md-button class="md-success  md-fileinput" @click.native="deletePrincipalImage(principalImage.id)">
                                    <input type="file" id="file" ref="myFiles" class="custom-file-input" @change="previewFiles">Insertar Documento</input>
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
                            <tinymce id="addNewTiny" v-model="newsDescription" :editorToolbar="customToolbar"></tinymce>
                             <!-- ./ Descripción -->
                        </div>
                        <!-- ./ preview de descripción -->
                        <div v-show="preview == true" class="md-layout-item md-size-100 md-small-size-100">
                          <h4 class="card-title">Vista previa de la noticia</h4>
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
                        </div>
                         <!-- ./ preview de descripción -->
                     </div>
                     <!-- ./ Descripción de noticia -->
                     <!-- Galería de noticia -->
                     <div style="margin-top:20px;" class="md-layout">
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
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Registrar</md-button>
                    <md-progress-spinner v-show="sending == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import { SlideYDownTransition } from "vue2-transitions";
import { CREATE_NEWS, ADD_IMAGES_TO_POST } from '../../../plugins/graphql';
import { myUrl } from '../../../plugins/params';
import { uploadFilesToGraphQLXr } from '../../../plugins/uploadFilesToGraphQLXr';
// Editors
import {VueEditor} from 'vue2-editor';

import VueUploadMultipleImage from 'vue-upload-multiple-image';
export default {
 props: {
    regularImg: {
      type: String,
      default: "./img/image_placeholder.jpg"
    }
  },
  components: {
    SlideYDownTransition,
    VueEditor,
    VueUploadMultipleImage
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
      dragText:"Arrastre los archivos aquí",
      browseText:"Buscar archivos...",
      dropText:"Suelte los archivos aquí...",
      markIsPrimarytext:"Galería de imágenes",
      popupText:"Estas imágenes serán visualizadas en la galería de la noticia",
      primaryText:"Galería de imagenes",
      // Propiedad para saber si el formulario se está enviando y ocultar el botón de registrar
      sending: false,
      preview:false,
      formData:"",
      imageRegular: "",
      boolean: null,
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
            min: 1
        },
        newsAbstract:{
            required: true,
            min: 5
        },
      }
    };
  },
  methods: {
      // Función para mostrar la vista previa
      showPreview: function(){
        this.preview = !(this.preview);
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
          this.variables.input.images.splice(i,1);
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
    previewFiles() {
    this.files = this.$refs.myFiles.files
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
            if(this.formData.get(this.imageName) == null)
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
              mutation: CREATE_NEWS,
              variables:{
                input:{
                  news:{
                    name: this.newsName,
                    abstract: this.newsAbstract,
                    description: this.newsDescription
                  }
                }
              }
            }).then((data) => {
              // Mutación que refresca el token
              var news_id = data.data.createNews.newNews.id;
              this.variables.input.id = news_id;
              // Finaliza las mutaciones
              this.sending = true;
              this.formData.append("variables",JSON.stringify(this.variables));
              uploadFilesToGraphQLXr(this.formData).then(() => {
                this.notifyVue('top','right','success','Noticia creada correctamente');
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
