import DropDown from "./components/Dropdown.vue";
import Vue from 'vue'
import tinymce from 'vue-tinymce-editor'
/**
 * You can register global components here and use them as a plugin in your main Vue instance
 */

const GlobalComponents = {
  install(Vue) {
    Vue.component("drop-down", DropDown);
    Vue.component('tinymce', tinymce)
  }
};

export default GlobalComponents;
