<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>event</md-icon>
                    </div>
                    <h4 class="title">Registrar evento</h4>
                </md-card-header>

                <md-card-content>
                     <!-- Nombre de evento -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Nombre -->
                            <md-field :class="[
                            {'md-valid': !errors.has('eventName') && touched.eventName},
                            {'md-error': errors.has('eventName')}]">
                            <label>Nombre del evento</label>
                            <md-input
                                v-model="eventName"
                                data-vv-name="eventName"
                                type="text"
                                required
                                v-validate="modelValidations.eventName">
                            </md-input>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('eventName') && touched.eventName">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('eventName') && touched.eventName">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Nombre -->
                        </div>
                     </div>
                     <!-- ./ Nombre de evento -->
                    <!-- Resumen de evento -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                             <!-- Resumen -->
                            <md-field :class="[
                            {'md-valid': !errors.has('eventAbstract') && touched.eventAbstract},
                            {'md-error': errors.has('eventAbstract')}]">
                            <label>Resumen del evento</label>
                            <md-textarea md-autogrow
                                v-model="eventAbstract"
                                data-vv-name="eventAbstract"
                                type="text"
                                required
                                v-validate="modelValidations.eventAbstract">
                            </md-textarea>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('eventAbstract') && touched.eventAbstract">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('eventAbstract') && touched.eventAbstract">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Resumen -->
                        </div>
                     </div>
                     <!-- ./ Resumen de evento -->
                     <!-- Categoría y organizadores -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Categoría -->
                            <md-field  v-show="$apollo.queries.allCategories.loading != true">
                                <label for="categories">Categorías</label>
                                    <md-select required v-model="selectedCategories" name="categories" id="categories" multiple>
                                        <md-option v-for="category in allCategories.edges" :key="category.id" :value="category.node.id">{{category.node.name}}</md-option>
                                    </md-select>
                            </md-field>
                            <md-field v-show="$apollo.queries.allCategories.loading == true">
                                <label >Cargando categorías...</label>
                            </md-field>
                            <!-- {{selectedCategories}} -->
                            <!-- ./ Categoría -->
                        </div>
                         <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Organizadores -->
                             <md-field  v-show="$apollo.queries.allOrganizers.loading != true">
                                <label for="organizers">Organizadores</label>
                                    <md-select required v-model="selectedOrganizers" name="organizers" id="organizers" multiple>
                                        <md-option v-for="organizer in allOrganizers.edges" :key="organizer.id" :value="organizer.node.id" >{{organizer.node.name}}</md-option>
                                    </md-select>
                            </md-field>
                             <md-field  v-show="$apollo.queries.allOrganizers.loading == true">
                                <label >Cargando organizadores</label>
                            </md-field>
                            <!-- {{selectedOrganizers}} -->
                            <!-- ./ Organizadores -->
                        </div>
                     </div>
                     <!-- ./ Categoría y organizadores -->
                     <!--Lugar y sitio web del evento -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Lugar del evento -->
                            <md-field  v-show="$apollo.queries.allVenues.loading != true">
                                <label for="venues">Lugar del evento</label>
                                    <md-select required v-model="selectedVenue" name="venues" id="venues">
                                        <md-option v-for="venue in allVenues.edges" :key="venue.id" :value="venue.node.id">{{venue.node.name}}</md-option>
                                    </md-select>
                            </md-field>
                            <md-field v-show="$apollo.queries.allCategories.loading == true">
                                <label >Cargando lugar del evento...</label>
                            </md-field>
                            <!-- ./ Lugar del evento -->
                        </div>
                         <!-- Sitio web -->
                          <div class="md-layout-item md-size-50 md-small-size-100">
                              <md-field :class="[
                                  {'md-valid': !errors.has('eventWebsite') && touched.eventWebsite},
                                  {'md-error': errors.has('eventWebsite')}]">
                                  <label>Sitio web</label>
                                  <md-input
                                      v-model="eventWebsite"
                                      data-vv-name="eventWebsite"
                                      type="text"
                                      v-validate="modelValidations.eventWebsite">
                                  </md-input>
                                  <span class="md-helper-text">Incluya la etiqueta http:// o htps:// según corresponda</span>
                                  <slide-y-down-transition>
                                      <md-icon class="error" v-show="errors.has('eventWebsite') && touched.eventWebsite">close</md-icon>
                                  </slide-y-down-transition>
                                  <slide-y-down-transition>
                                      <md-icon class="success" v-show="!errors.has('eventWebsite') && touched.eventWebsite">done</md-icon>
                                  </slide-y-down-transition>
                              </md-field>
                          </div>
                          <!-- ./ Sitio web -->

                     </div>
                     <!-- ./Lugar y sitio web del evento -->
                     <!-- Fecha de inicio y fecha de finalización -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Fecha de inicio -->
                            <md-field class="md-field md-theme-default">
                                <datetime required style="min-width:100%" value-zone="UTC-5"  :type="'datetime'" :use12-hour='true' :phrases="{ok: 'Ok', cancel: 'Cancelar'}" input-class="md-input" zone="UTC-5" placeholder="Fecha y hora de inicio*"  v-model="startDatetime"></datetime>
                            </md-field>
                            <!-- ./ Fecha de inicio -->
                        </div>
                         <div class="md-layout-item md-size-50 md-small-size-100">
                             <!-- Fecha de finalización -->
                            <md-field class="md-field md-theme-default">
                                <datetime required value-zone="UTC-5"  type="datetime" :use12-hour='true' input-class="md-input" :phrases="{ok: 'Ok', cancel: 'Cancelar'}" zone="UTC-5"  placeholder="Fecha y hora de finalización*" v-model="finishDatetime"></datetime>
                            </md-field>
                            <!-- ./ Fecha de finalización -->
                        </div>
                     </div>
                     <!-- ./ Fecha de inicio y fecha de finalización -->
                     <!-- Precio y sitio web -->
                     <div class="md-layout">
                        <!-- Precio -->
                        <div class="md-layout-item md-size-50 md-small-size-100">
                             <md-field :class="[
                                {'md-valid': !errors.has('eventPrice') && touched.eventPrice},
                                {'md-error': errors.has('eventPrice')}]">
                                <label>Precio</label>
                                <md-input
                                    v-model="eventPrice"
                                    data-vv-name="eventPrice"
                                    type="number"
                                    v-validate="modelValidations.eventPrice">
                                </md-input>
                                <slide-y-down-transition>
                                    <md-icon class="error" v-show="errors.has('eventPrice') && touched.eventPrice">close</md-icon>
                                </slide-y-down-transition>
                                <slide-y-down-transition>
                                    <md-icon class="success" v-show="!errors.has('eventPrice') && touched.eventPrice">done</md-icon>
                                </slide-y-down-transition>
                            </md-field>
                        </div>
                        <!-- ./ Precio -->
                       <!-- Cupo limitado -->
                       <div class="md-layout-item md-size-50 md-small-size-100">
                          <md-checkbox v-model="eventLimited">Cupo limitado</md-checkbox>
                       </div>
                       <!-- ./ Cupo limitado -->
                     </div>
                    <!-- ./ Precio y sitio web-->

                     <!-- Imagen principal de evento -->
                     <div class="md-layout md-alignment-top-center" >
                        <div class="md-layout-item md-size-30 md-xsmall-size-100 " >
                            <h4 class="card-title">Imagen principal del evento</h4>
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
                                    <input type="file" @change="onFileChange">
                                </md-button>
                                </div>

                                <div role="form">
                                        <form>
                                            <div class="form-group">
                                                <label class="btn btn-primary">
                                                    <i class="fa fa-folder-open-o" aria-hidden="true"></i>&nbsp;Seleccionar un archivo
                                                    <input type="file" accept=".pdf" @change="onFileSelected" name="myfile">
                                                </label>
                                            </div>
                                        </form>
                                    </div>


                            </div>
                        </div>
                    </div>
                    <br>
                    <br>
                     <!-- ./ Imagen principal de evento -->
                     <!-- Descripción de evento -->
                     <div class="md-layout">
                        <div class="md-layout-item md-size-100 md-small-size-100">
                            <h4 class="card-title">Descripción completa del evento*</h4>
                             <md-button @click.native="showPreview" style="float: right;" class="md-simple md-default md-just-icon">
                                <i class="fa fa-eye"></i>
                                <md-tooltip  md-direction="right">Vista previa</md-tooltip>
                             </md-button>
                             <!-- Descripción -->
                            <tinymce id="d1" v-model="eventDescription" ></tinymce>
                             <!-- ./ Descripción -->
                             <md-button @click.native="showPreview" style="float: right;" class="md-simple md-default md-just-icon">
                                <i class="fa fa-eye"></i>
                                <md-tooltip  md-direction="right">Vista previa</md-tooltip>
                             </md-button>
                        </div>
                        <!-- ./ preview de descripción -->
                        <div v-show="preview == true" class="md-layout-item md-size-100 md-small-size-100">
                          <h4 class="card-title">Vista previa del evento</h4>
                            <div class='browser-window'>
                                <div class='top-bar'>
                                  <div class='circles'>
                                    <div class="circle circle-red"></div>
                                    <div class="circle circle-yellow"></div>
                                    <div class="circle circle-green"></div>
                                  </div>
                                </div>
                                <div style="word-wrap:break-word;" v-html="eventDescription" class='content'>
                                </div>
                              </div>
                        </div>
                         <!-- ./ preview de descripción -->
                     </div>
                     <!-- ./ Descripción de evento -->
                     <!-- Galería de evento -->
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
                     <!-- ./ Galería de evento -->
                   <div class="form-category">* Campos obligatorios</div>
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/events/events"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Registrar</md-button>
                    <md-progress-spinner v-show="sending == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                </md-card-actions>
                </md-card>
            </form>
        </div>
    </div>
</template>
<script>
import { Datetime } from 'vue-datetime';
import { Settings } from 'luxon'
import 'vue-datetime/dist/vue-datetime.css';
import { SlideYDownTransition } from "vue2-transitions";
import { CREATE_EVENT, ADD_IMAGES_TO_POST, ALL_CATEGORIES, ALL_ORGANIZERS, ALL_VENUES } from '../../../plugins/graphql';
import { myUrl, mediaUrl } from '../../../plugins/params';
import { uploadFilesToGraphQLXr } from '../../../plugins/uploadFilesToGraphQLXr';
// Editor
import {VueEditor} from 'vue2-editor';
import {VueResource} from 'vue-resource';

import VueUploadMultipleImage from 'vue-upload-multiple-image';
Settings.defaultLocale = 'es'
export default {
 apollo:{
      allCategories: {
                query: ALL_CATEGORIES,
                // Additional options here
                fetchPolicy: 'network-only',
                // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {

                    if(data.allCategories.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay categorías');
                    }

                },
                // Si encontró algún error.
                error(error) {
                    this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                },
              },
      allOrganizers: {
                query: ALL_ORGANIZERS,
                // Additional options here
                fetchPolicy: 'network-only',
                // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {

                    if(data.allOrganizers.edges.length == 0)
                    {
                        this.notifyVue('top','right','info','No hay organizadores');
                    }
                },
                // Si encontró algún error.
                error(error) {
                    this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
                },
              },
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

                },
                // Si encontró algún error.
                error(error) {
                    this.notifyVue('top','right','warning','Algo ha pasado, recarga la página');
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
    Datetime
  },
  data() {
    return {
      allCategories:'',
      allOrganizers:'',
      allVenues:'',
      editor:null,
      // Propiedades para el editor de texto -> Vue-editor
      customToolbar: [
        ['bold', 'italic', 'underline', 'strike', 'tables'],        // toggled buttons
        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'script': 'sub' }, { 'script': 'super' }],      // superscript/subscript
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [{ 'color': [] }, { 'background': [] }],
        ['link'],         // dropdown with defaults from theme
        ['clean']
      ],

      toolbar: [
    'removeFormat', 'undo', '|', 'elements', 'fontName', 'fontSize', 'foreColor', 'backColor', 'divider',
    'bold', 'italic', 'underline', 'strikeThrough', 'links', 'divider', 'subscript', 'superscript',
    'divider', 'justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull', '|', 'indent', 'outdent',
    'insertOrderedList', 'insertUnorderedList', '|', 'picture', 'tables', '|', 'switchView'
  ],


      dragText:"Arrastre los archivos aquí",
      browseText:"Buscar archivos...",
      dropText:"Suelte los archivos aquí...",
      markIsPrimarytext:"Galería de imágenes",
      popupText:"Estas imágenes serán visualizadas en la galería del evento",
      primaryText:"Galería de imagenes",
      // Propiedad para saber si el formulario se está enviando y ocultar el botón de registrar
      sending: false,
      preview:false,
      startDatetime: null,
      finishDatetime: null,
      formData:"",
      imageRegular: "",
      boolean: null,
      eventName: "",
      eventAbstract: "",
      eventDescription: "<h1>Escriba aquí la descripción del evento.</h1>",
      eventPrice: 0,
      eventWebsite:"",
      eventLimited: false,
      imageName: "",
      images: [],
      selectedCategories:[],
      selectedOrganizers:[],
      selectedVenue:'',
      touched: {
        eventName: false,
        eventAbstract: false,
        eventDescription: false,
        eventPrice: false,
        eventWebsite: false,
      },
      variables:{
        input:{
          id:'',
          images: [],
        }
      },
      modelValidations: {
        eventName:{
            required: true,
            min: 1
        },
        eventAbstract:{
            required: true,
            min: 5
        },
        eventPrice:{
            numeric: true,
            max: 10
        },
        eventWebsite:{
            min:1,
            max: 256,
            url:true
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
    // Función para eliminar una imagen
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
    // Función para editar una imagen
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
    onFileSelected (e) {
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
            if(this.eventDescription == null)
            {
              this.notifyVue('top','right','warning','No hay una descripción de la noticia');
              return
            }
            if(this.selectedCategories == [])
            {
              this.notifyVue('top','right','warning','No hay categorías seleccionadas');
              return
            }
            if(this.selectedOrganizers == [])
            {
              this.notifyVue('top','right','warning','No hay organizadores seleccionados');
              return
            }
            if(this.selectedVenue == '')
            {
              this.notifyVue('top','right','warning','No hay un lugar seleccionado');
              return
            }
            this.$apollo.mutate({
              mutation: CREATE_EVENT,
              variables:{
                input:{
                  event:{
                    name: this.eventName,
                    abstract: this.eventAbstract,
                    description: this.eventDescription,
                    startDatetime: this.startDatetime,
                    finishDatetime: this.finishDatetime,
                    price: this.eventPrice,
                    website: this.eventWebsite,
                    limited: this.eventLimited,
                    categories: this.selectedCategories,
                    organizers: this.selectedOrganizers,
                    venue: this.selectedVenue
                  }
                }
              }
            }).then((data) => {
              // Mutación que refresca el token
              var event_id = data.data.createEvent.newEvent.id;
              this.variables.input.id = event_id;
              // Finaliza las mutaciones
              this.sending = true;
              this.formData.append("variables",JSON.stringify(this.variables));
              uploadFilesToGraphQLXr(this.formData).then(() => {
                this.notifyVue('top','right','success','Evento creado correctamente');
                this.$router.push('/events/events');
              }).catch(() => {
                this.sending = false;
                this.notifyVue('top','right','danger','Algo ha salido mal, inténtalo de nuevo');
              })

            }).catch((error) => {
              // Error
              this.notifyVue('top','right','warning','Algo ha pasado y la evento no ha sido guardada, inténtalo de nuevo');
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
    eventName() {
      this.touched.eventName = true;
    },
    eventAbstract() {
      this.touched.eventAbstract = true;
    },
    eventPrice() {
      this.touched.eventPrice = true;
    },
    eventWebsite() {
      this.touched.eventWebsite = true;
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

.full-date{
  min-width: 100% !important;
}
.clear { clear: both; }
@import '~vue-datetime/dist/vue-datetime.css';
</style>
