<template>
    <div class="md-layout">
        <div class="md-layout-item md-small-size-100">
            <form>
                <md-card>
                <md-card-header class="md-card-header-icon md-card-header-primary">
                    <div class="card-icon">
                    <md-icon>link</md-icon>
                    </div>
                    <h4 class="title">Enlaces relacionados</h4>
                </md-card-header>

                <md-card-content>
                    <md-button  @click.native="removeLink" style="float: right;"
                        class="md-button md-just-icon md-theme-default md-danger mr-10">
                        <md-tooltip  md-direction="top">Quitar enlace</md-tooltip>
                        <md-icon>remove</md-icon>
                    </md-button>
                    <md-button v-show="input_count < 10" @click.native="addLink" style="float: right;"
                        class="md-button md-just-icon md-theme-default md-info mr-10">
                        <md-tooltip  md-direction="top">Agregar enlace</md-tooltip>
                        <md-icon>add</md-icon>
                    </md-button>
                    <!-- Nombre de enlace -->
                     <div v-for="(row,index) in input_count" :key="index" class="md-layout">
                        <div class="md-layout-item md-size-5 md-small-size-100">
                            <md-checkbox v-model="relatedLinks[index].checked" ></md-checkbox>
                        </div>
                        <div class="md-layout-item md-size-30 md-small-size-100">
                             <!-- Nombre -->
                            <md-field :class="[
                            {'md-valid': !errors.has('relatedLinkName') && touched.relatedLinkName},
                            {'md-error': errors.has('relatedLinkName')}]">
                            <label>Nombre de enlace</label>
                            <md-input
                                v-model="relatedLinks[index].name"
                                data-vv-name="relatedLinkName"
                                type="text"
                                required
                                v-validate="modelValidations.relatedLinkName">
                            </md-input>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('relatedLinkName') && touched.relatedLinkName">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('relatedLinkName') && touched.relatedLinkName">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ Nombre -->
                        </div>
                        <div class="md-layout-item md-size-65 md-small-size-100">
                             <!-- URL -->
                            <md-field :class="[
                            {'md-valid': !errors.has('relatedLinkUrl') && touched.relatedLinkUrl},
                            {'md-error': errors.has('relatedLinkUrl')}]">
                            <label>URL</label>
                            <md-input 
                                v-model="relatedLinks[index].link"
                                data-vv-name="relatedLinkUrl"
                                type="text"
                                required
                                v-validate="modelValidations.relatedLinkUrl">
                            </md-input>
                            <span class="md-helper-text">Incluya la etiqueta http:// o htps:// según corresponda</span>
                            <slide-y-down-transition>
                                <md-icon class="error" v-show="errors.has('relatedLinkUrl') && touched.relatedLinkUrl">close</md-icon>
                            </slide-y-down-transition>
                            <slide-y-down-transition>
                                <md-icon class="success" v-show="!errors.has('relatedLinkUrl') && touched.relatedLinkUrl">done</md-icon>
                            </slide-y-down-transition>
                            </md-field>
                            <!-- ./ URL -->
                        </div>
                     </div>   
                     <!-- ./ Nombre de enlace -->
                   <div class="form-category">* Campos obligatorios</div>
                </md-card-content>

                <md-card-actions md-alignment="space-between">
                    <router-link to="/events/categories"><md-button class="md-default">Cancelar</md-button></router-link>
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
import { CREATE_CATEGORY,GET_CATEGORY_BY_ID, CREATE_RELATED_LINKS, DELETE_RELATED_LINK } from '../../../../plugins/graphql';
import { myUrl } from '../../../../plugins/params';
import { uploadFilesToGraphQLXr } from '../../../../plugins/uploadFilesToGraphQLXr';
export default {
    apollo:{
        category: {
                    query: GET_CATEGORY_BY_ID,
                    // Reactive variables
                    fetchPolicy: 'network-only',
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
                      this.category_id= data.category.id;
                      if(data.category.relatedLinks.edges.length == 0)
                      {
                          
                      }
                      else
                      {
                          this.setRelatedLinks();
                      }
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
    SlideYDownTransition
  },
  data() {
    return {
      category:'',
      category_id:'',
      sending: false,
      formData:"",
      input_count:1,
      boolean: null,
      relatedLinkName: "",
      relatedLinkUrl: "",
      relatedLinks:[
          {
              id:'',
              name:'',
              link:'',
              checked: false
          }
      ],
      mutationLinks:[],
      touched: {
        relatedLinkName: false,
        relatedLinkUrl: false,
      },
      modelValidations: {
        relatedLinkName:{
            required: true,
            min: 1,
            max: 32
        },
        relatedLinkUrl:{
            required: true,
            min: 5,
            max: 128,
            url:true
        },
      }
    };
  },
  methods: {
    // Función que setea los links desde la consulta de graphql
    setRelatedLinks: function(){
        this.relatedLinks = [];
        this.input_count = this.category.relatedLinks.edges.length;
        for(var i=0;i<this.category.relatedLinks.edges.length;i++)
        {
            this.relatedLinks.push({
                id: this.category.relatedLinks.edges[i].node.id,
                name: this.category.relatedLinks.edges[i].node.name,
                link: this.category.relatedLinks.edges[i].node.link,
                checked: false
            })
        }
        this.input_count = this.category.relatedLinks.edges.length;
    },
    // Función para agregar un link
    addLink: function(){
        this.input_count++;
        this.relatedLinks.push({
            id:'',
            name:'',
            link:'',
            checked: false
        })
    },
    // Función para quitar un link
    removeLink: function(){
        // this.relatedLinks.splice(this.input_count-1)
        // this.input_count--;
        var count = 0;
        for(var i=0;i<this.relatedLinks.length;i++)
        {
            if(this.relatedLinks[i].checked == true)
            {
                count++;
            }
        }
        if(count == 0)
        {
            this.notifyVue('top','right','warning','No ha seleccionado ningún enlace para eliminar');
        }
        else
        {
            this.deleteMutation();
        }

    },
    // Función para eliminar un enlace directamente al servidor
    deleteMutation: function(){
        var i=this.relatedLinks.length-1;
        while(i >= 0){
            if(this.relatedLinks[i].checked == true)
            {
                if(this.relatedLinks[i].id != '')
                {
                    this.$apollo.mutate({
                        mutation: DELETE_RELATED_LINK,
                        variables:{
                            input:{
                                id: this.relatedLinks[i].id,
                            }
                        }
                    }).then((data) => {
                        this.notifyVue('top','right','success','Enlaces editados correctamente');
                        this.relatedLinks.splice(i);
                        this.input_count = this.input_count - 1;
                        if(this.input_count == 0)
                        {
                            this.addLink();
                        }
                        
                    }).catch((error) => {
                        // Error
                        this.sending = false;
                        this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
                    });
                }
                else{
                    this.relatedLinks.splice(i);
                    this.input_count = this.input_count - 1;
                    if(this.input_count == 0)
                    {
                        this.addLink();
                    }
                }
            }
            i = i-1;
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
            for(var i=0;i<this.relatedLinks.length;i++)
            {
                if(this.relatedLinks[i].id == '')
                {
                    this.mutationLinks.push({
                        name: this.relatedLinks[i].name,
                        link: this.relatedLinks[i].link
                    });
                }
                
            }
            this.sending = true;
            // Iniciamos el envío de la mutación
            this.$apollo.mutate({
            mutation: CREATE_RELATED_LINKS,
            variables:{
              input:{
                  id: this.category_id,
                  relatedLinks: this.mutationLinks
              }
            }
          }).then((data) => {
            this.notifyVue('top','right','success','Enlaces editados correctamente');
            this.$router.push('/events/categories');
            
          }).catch((error) => {
            // Error
            this.sending = false;
            this.notifyVue('top','right','warning','Ha ocurrido un error, inténtalo de nuevo');
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
    
  },
  watch: {
    relatedLinkName() {
      this.touched.relatedLinkName = true;
    },
    relatedLinkUrl() {
      this.touched.relatedLinkUrl = true;
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
