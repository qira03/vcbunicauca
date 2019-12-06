<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>insert_photo</md-icon>
                    </div>
                    <h4 class="title">Editar slider</h4>
                </md-card-header>

                <md-card-content>
                <!-- Imagen de noticia existente -->
                <div style="margin-top:20px;" v-show="sliderImages != []" class="md-layout " >
                <div v-for="image in sliderImages" :key="image.id" class="md-layout-item md-size-30 md-xsmall-size-100 " >
                    <product-card
                        header-animation="false">
                        <img class="img" slot="imageHeader" :src="image.imageFile">
                        <div slot="footer" class="button-container md-layout text-center">
                            <md-button v-show="sendingImage == false" @click.native="deleteImage(image.id)" class="md-danger">Eliminar</md-button>
                            <md-progress-spinner v-show="sendingImage == true" class="md-accent" :md-diameter="30" md-mode="indeterminate"></md-progress-spinner>
                        </div>
                            
                            
                    </product-card>
                </div>
                </div>
                <!-- ./ Imagen de noticia existente -->
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
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/dashboard"><md-button class="md-default">Cancelar</md-button></router-link>
                    <md-button v-show="sending == false" native-type="submit" @click.native.prevent="validate" class="md-success">Registrar</md-button>
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
import { ALL_SLIDERS ,ADD_IMAGES_TO_POST, DELETE_IMAGE_BY_ID } from '../../plugins/graphql';
import { mediaUrl,myUrl } from '../../plugins/params';
import { uploadFilesToGraphQLXr } from '../../plugins/uploadFilesToGraphQLXr';
// Editor
import VueUploadMultipleImage from 'vue-upload-multiple-image';
import { all } from 'async';

export default {
 apollo:{
     allSliders: {
                query: ALL_SLIDERS,
                // Reactive variables
                variables() {
                    return {
                    position: "HOME"
                    }
                },
                fetchPolicy: 'network-only',
                // Disable the query
                // skip() {
                //   return true
                // },
                    // Si tenemos un resultado, pero no encontró el slug.
                result({ data, loading, networkStatus }) {
                    this.setSliderImages(data.allSliders);
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
    VueUploadMultipleImage,
    ProductCard
  },
  data() {
    return {
      allSliders:'',
      dragText:"Arrastre los archivos aquí",
      browseText:"Buscar archivos...",
      dropText:"Suelte los archivos aquí...",
      markIsPrimarytext:"Galería de imágenes",
      popupText:"Estas imágenes serán visualizadas en la galería del evento",
      primaryText:"Galería de imagenes",
      // Propiedad para saber si el formulario se está enviando y ocultar el botón de registrar
      sendingImage:false,
      sending: false,
      preview:false,
      formData:"",
      imageRegular: "",
      boolean: null,
      images: [],
      sliderImages:[],
      sliderId:'',
      variables:{
        input:{
          id:'',
          images: [],
        }
      },
      
    };
  },
  methods: {
      setSliderImages: function(allSliders){
          this.sliderId = allSliders.edges[0].node.id;
          for(var i=0;i<allSliders.edges[0].node.post.images.edges.length;i++)
          {
              this.sliderImages.push({
                  id: allSliders.edges[0].node.post.images.edges[i].node.id,
                  imageFile: mediaUrl+allSliders.edges[0].node.post.images.edges[i].node.imageFile,
              })
          }
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
                for(var i=0;i<this.sliderImages.length;i++)
                {
                    if(this.sliderImages[i].id == imageId)
                    {
                        this.sliderImages.splice(i,1);
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
           // Mutación que refresca el token
              var slider_id = this.sliderId;
              this.variables.input.id = slider_id;
              // Finaliza las mutaciones
              this.sending = true;
              this.formData.append("variables",JSON.stringify(this.variables));
              uploadFilesToGraphQLXr(this.formData).then(() => {
                this.notifyVue('top','right','success','Slider editado correctamente');
                this.$router.push('/dashboard');
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

</style>
