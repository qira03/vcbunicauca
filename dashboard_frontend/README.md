# Vicerrectoría de Cultura y Bienestar de la Universidad del Cauca - Frontend - Sistema Administrativo

Esta aplicación ha sido desarrollada haciendo uso de la plantilla [Vue Material Dashboard PRO](https://www.creative-tim.com/product/vue-material-dashboard-pro) la cual ha sido construida con  [Vue Material](https://vuematerial.io/) y [Vuejs](https://vuejs.org/v2/guide/). Para conocer, desarrollar y mantener esta aplicación es necesario tener conocimientos básicos de Javascript, [Vuejs](https://vuejs.org/v2/guide/),[Vue Router](https://router.vuejs.org/en/),[Vuex](https://vuex.vuejs.org) y [Vue apollo](https://vue-apollo.netlify.com).


## Tabla de contenido
- [Vicerrectoría de Cultura y Bienestar de la Universidad del Cauca - Frontend - Sistema Administrativo](#vicerrector%C3%ADa-de-cultura-y-bienestar-de-la-universidad-del-cauca---frontend---sistema-administrativo)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Documentación](#documentaci%C3%B3n)
  - [Estructura de archivos](#estructura-de-archivos)
  - [Navegadores soportados](#navegadores-soportados)
  - [Prerrequisitos](#prerrequisitos)
  - [Variables del sistema](#variables-del-sistema)
  - [Instalación rápida](#instalaci%C3%B3n-r%C3%A1pida)
  - [Soporte técnico](#soporte-t%C3%A9cnico)
  


## Documentación
La documentación oficial de la plantilla la puede encontrar en su [sitio web](https://demos.creative-tim.com/vue-material-dashboard-pro/documentation).


## Estructura de archivos

Una vez descargue el repositorio encontrará los siguientes directorios y archivos

```
Dashboard_backend/
├── CHANGELOG.md
├── README.md
├── babel.config.js
├── package.json
├── postcss.config.js
├── public
│   ├── img
│   └── index.html
├── src
│   ├── App.vue
│   ├── assets
│   │   ├── css
│   │   └── scss
│   │       ├── material-dashboard.scss
│   │       └── md
│   ├── components
│   │   ├── AnimatedNumber.vue
│   │   ├── Badge.vue
│   │   ├── Cards
│   │   │   ├── ChartCard.vue
│   │   │   ├── GlobalSalesCard.vue
│   │   │   ├── LockCard.vue
│   │   │   ├── LoginCard.vue
│   │   │   ├── NavTabsCard.vue
│   │   │   ├── PricingCard.vue
│   │   │   ├── ProductCard.vue
│   │   │   ├── SignupCard.vue
│   │   │   ├── StatsCard.vue
│   │   │   └── TestimonialCard.vue
│   │   ├── Collapse.vue
│   │   ├── Dropdown.vue
│   │   ├── Inputs
│   │   │   └── IconCheckbox.vue
│   │   ├── Modal.vue
│   │   ├── NotificationPlugin
│   │   │   ├── Notification.vue
│   │   │   ├── Notifications.vue
│   │   │   └── index.js
│   │   ├── Pagination.vue
│   │   ├── SidebarPlugin
│   │   │   ├── SideBar.vue
│   │   │   ├── SidebarItem.vue
│   │   │   └── index.js
│   │   ├── Slider.vue
│   │   ├── Tables
│   │   │   └── GlobalSalesTable.vue
│   │   ├── Tabs.vue
│   │   ├── Timeline
│   │   │   ├── TimeLine.vue
│   │   │   └── TimeLineItem.vue
│   │   ├── Wizard
│   │   │   ├── Wizard.vue
│   │   │   ├── WizardTab.vue
│   │   │   └── throttle.js
│   │   ├── WorldMap
│   │   │   ├── AsyncWorldMap.vue
│   │   │   ├── WorldMap.vue
│   │   │   └── world_map.js
│   │   └── index.js
│   ├── globalComponents.js
│   ├── globalDirectives.js
│   ├── main.js
│   ├── material-dashboard.js
│   ├── pages
│   │   ├── Dashboard
│   │   │   ├── Components
│   │   │   │   ├── Buttons.vue
│   │   │   │   ├── GridSystem.vue
│   │   │   │   ├── Icons.vue
│   │   │   │   ├── Notifications.vue
│   │   │   │   ├── Panels.vue
│   │   │   │   ├── SweetAlert.vue
│   │   │   │   └── Typography.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── Slider.vue
│   │   │   ├── Layout
│   │   │   │   ├── Content.vue
│   │   │   │   ├── ContentFooter.vue
│   │   │   │   ├── DashboardLayout.vue
│   │   │   │   ├── Extra
│   │   │   │   │   ├── MobileMenu.vue
│   │   │   │   │   └── UserMenu.vue
│   │   │   │   └── TopNavbar.vue
│   │   │   │
│   │   │   ├── Pages
│   │   │   │   ├── AuthLayout.vue
│   │   │   │   └── Login.vue
│   │   │   ├── Users   
│   │   │   │   ├── Add.vue
│   │   │   │   ├── Edit.vue
│   │   │   │   ├── PasswordEdit.vue
│   │   │   │   └── Users.vue
│   │   │   ├── News 
│   │   │   │   ├── AddNews.vue
│   │   │   │   ├── EditNews.vue
│   │   │   │   └── News.vue    
│   │   │   └── Events
│   │   │       ├── AddEvent.vue
│   │   │       ├── EditEvent.vue
│   │   │       ├── Events.vue
│   │   │       ├── Categories
│   │   │       │   ├── AddCategory.vue
│   │   │       │   ├── EditCategory.vue
│   │   │       │   ├── ShowCategory.vue
│   │   │       │   ├── RelatedLinks.vue
│   │   │       │   └── Categories.vue
│   │   │       ├── Organizers
│   │   │       │   ├── AddOrganizer.vue
│   │   │       │   ├── EditOrganizer.vue
│   │   │       │   ├── ShowOrganizer.vue
│   │   │       │   └── Organizers.vue
│   │   │       └── Venues
│   │   │           ├── AddVenue.vue
│   │   │           ├── EditVenue.vue
│   │   │           ├── ShowVenue.vue
│   │   │           └── Venues.vue            
│   │   │       
│   │   │       
│   │   │       
│   │   │       
│   │   │   
│   │   └── index.js
│   ├── plugins
│   │   ├── uploadFilesToGraphQLXr.js
│   │   ├── graphql.js
│   │   └── params.js
│   ├── routes
│   │   └── routes.js
│   └── store
│       ├── store.js
│       └── mutations.js
├── vue.config.js

```

## Navegadores soportados

La solución es compatible con las últimas dos versiones de los siguientes navegadores:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/opera.png" width="64" height="64">

## Prerrequisitos
Se debe tener desplegado el backend del sistema para poder incluir las variables del sistema en el archivo params.js

## Variables del sistema
El sistema hace uso de un archivo params.js ubicado en la carpeta Plugins. En este archivo deben configurarse las variables de 
- Url del servidor
- Url de los archivos media
- Url del sitio web de la vicerrectoría

## Instalación rápida
- Como prerrequisito es necesario tener instalado [Node js](https://nodejs.org/en/), y [npm](https://www.npmjs.com) o [yarn](https://yarnpkg.com/es-ES/) 
- Descargue el repositorio, inicie la consola y ubíquese en la raíz del proyecto
- El comando ```npm install``` o ```yarn install``` instalará todas las dependencias
- El comando ```npm run dev``` o ```yarn serve``` creará un servidor local para desarrollo
- El comando ```npm run build``` o ```yarn build``` construirá la aplicación para desplegar en producción


## Soporte técnico

Si tiene alguna pregunta [contáctenos](mailto:desarrollo@namtrikdev.co)


