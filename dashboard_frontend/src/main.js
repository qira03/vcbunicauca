import Vue from "vue";
import VueRouter from "vue-router";
import store from './store/store'
import DashboardPlugin from "./material-dashboard";
import VueApollo from 'vue-apollo';
import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { ApolloLink, concat, split } from 'apollo-link';
import { L } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';

import VueLazyLoad from 'vue-lazyload';

import VueResource from 'vue-resource';
Vue.use(VueResource);

Vue.use(VueLazyLoad);


// Plugins
import App from "./App.vue";
import Chartist from "chartist";
import { myUrl } from './plugins/params';

// router setup
import routes from "./routes/routes";

// plugin setup
Vue.use(VueRouter);
Vue.use(DashboardPlugin);
Vue.use(VueApollo);



// Leaflet
// this part resolve an issue where the markers would not appear
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

//httplink
const httpLink = new HttpLink({
  uri: myUrl,
})

const authMiddleware = new ApolloLink((operation, forward) => {
  // add the authorization to the headers
  operation.setContext({
    headers: {
      authorization: 'jwt '+store.getters.getToken || null,
    }
  });
  return forward(operation);
})
// Cache implementation
const cache = new InMemoryCache()

// Create the apollo client
const apolloClient = new ApolloClient({
  link: concat(authMiddleware, httpLink),
  cache,
  connectToDevTools: true
})

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
});

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkExactActiveClass: "nav-item active"
});

// global library setup
Object.defineProperty(Vue.prototype, "$Chartist", {
  get() {
    return this.$root.Chartist;
  }
});

/* eslint-disable no-new */
new Vue({
  el: "#app",
  render: h => h(App),
  router,
  store,
  apolloProvider,
  data: {
    Chartist: Chartist
  }
});
