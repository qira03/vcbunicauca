import 'es6-promise/auto';
import Vue from 'vue';
import Vuex, {Payload, Store} from 'vuex';
import VuexPersistence from 'vuex-persist';
import mutations from './mutations';

Vue.use(Vuex);

// ============Vuex Persistence object start===========
const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})
// ============Vuex Persistence object end===========

//=======vuex store start===========
const store = new Vuex.Store({
    state: {
        
        user: {
            id: "",
            name: "",
            username: '',
            picture: "",
            role: "",
            url:""
        },
        token:'',
        
    },
    mutations ,
    plugins: [vuexLocal.plugin],

    getters: {
        getUsername: state => {
            return state.user.username;
          },
        getUserPicture: state => {
            return state.user.picture;
          },
        getName: state => {
            return state.user.name;
          },
        getRole: state => {
            return state.user.role;
          },
        getUserUrl: state => {
            return state.user.url;
          },
        getUserId: state => {
            return state.user.id;
          },
        getToken: state => {
            return state.token;
        },
        isLoggedIn: state => {
            if(state.user.token == "")
            {
                return false
            }
            else
            {
                return true
            }
        },
    }
});
//=======vuex store end===========
export default store
