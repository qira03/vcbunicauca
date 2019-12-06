import DashboardLayout from "@/pages/Dashboard/Layout/DashboardLayout.vue";
import AuthLayout from "@/pages/Dashboard/Pages/AuthLayout.vue";
import Login from "@/pages/Dashboard/Pages/Login.vue";
// Dashboard pages
import Dashboard from "@/pages/Dashboard/Dashboard.vue";

//Slider pages
import Slider from "@/pages/Dashboard/Slider.vue";

// User pages
import Users from "@/pages/Dashboard/Users/Users.vue";
import AddUsers from "@/pages/Dashboard/Users/Add.vue";
import EditUser from "@/pages/Dashboard/Users/Edit.vue";
import PasswordEdit from "@/pages/Dashboard/Users/PasswordEdit.vue";

//Event pages
import Events from "@/pages/Dashboard/Events/Events.vue";
import AddEvent from "@/pages/Dashboard/Events/AddEvent.vue";
import EditEvent from "@/pages/Dashboard/Events/EditEvent.vue";
  //Categories
  import Categories from "@/pages/Dashboard/Events/Categories/Categories.vue";
  import AddCategory from "@/pages/Dashboard/Events/Categories/AddCategory.vue";
  import ShowCategory from "@/pages/Dashboard/Events/Categories/ShowCategory.vue";
  import EditCategory from "@/pages/Dashboard/Events/Categories/EditCategory.vue";
  import RelatedLinks from "@/pages/Dashboard/Events/Categories/RelatedLinks.vue";
  //Organizers
  import Organizers from "@/pages/Dashboard/Events/Organizers/Organizers.vue";
  import AddOrganizer from "@/pages/Dashboard/Events/Organizers/AddOrganizer.vue";
  import EditOrganizer from "@/pages/Dashboard/Events/Organizers/EditOrganizer.vue";
  //Venues
  import Venues from "@/pages/Dashboard/Events/Venues/Venues.vue";
  import AddVenue from "@/pages/Dashboard/Events/Venues/AddVenue.vue";
  import ShowVenue from "@/pages/Dashboard/Events/Venues/ShowVenue.vue";
  import EditVenue from "@/pages/Dashboard/Events/Venues/EditVenue.vue";

// News Pages
import News from "@/pages/Dashboard/News/News.vue";
import AddNews from "@/pages/Dashboard/News/AddNews.vue";
import EditNews from "@/pages/Dashboard/News/EditNews.vue";

let authPages = {
  path: "/",
  component: AuthLayout,
  name: "Authentication",
  children: [
    {
      path: "/login",
      name: "Login",
      component: Login
    }
  ]
};

const routes = [
  {
    path: "/",
    redirect: "/login",
    name: "Login"
  },
  authPages,
  {
    path: "/",
    component: DashboardLayout,
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        components: { default: Dashboard }
      },
      {
        path: "slider",
        name: "Slider",
        components: { default: Slider }
      },
      {
        path: "users",
        name: "Usuarios",
        components: { default: Users }
      },
      {
        path: "users/add",
        name: "Agregar usuario",
        components: { default: AddUsers }
      },
      {
        path: "users/edit/:user_id",
        name: "Editar usuario",
        components: { default: EditUser }
      },
      {
        path: "users/password_edit/:user_id",
        name: "Editar contraseña de usuario",
        components: { default: PasswordEdit }
      },
      {
        path: "events/categories",
        name: "Categorías",
        components: { default: Categories }
      },
      {
        path: "events/categories/add",
        name: "Agregar categoría",
        components: { default: AddCategory }
      },
      {
        path: "events/categories/show/:category_id",
        name: "Visualizar categoría",
        components: { default: ShowCategory }
      },
      {
        path: "events/categories/edit/:category_id",
        name: "Editar categoría",
        components: { default: EditCategory }
      },
      {
        path: "events/categories/related_links/:category_id",
        name: "Enlaces relacionados",
        components: { default: RelatedLinks }
      },
      {
        path: "events/organizers",
        name: "Organizadores",
        components: { default: Organizers }
      },
      {
        path: "events/organizers/add",
        name: "Agregar organizador",
        components: { default: AddOrganizer }
      },
      {
        path: "events/organizers/edit/:organizer_id",
        name: "Editar organizador",
        components: { default: EditOrganizer }
      },
      {
        path: "events/venues",
        name: "Lugares",
        components: { default: Venues }
      },
      {
        path: "events/venues/add",
        name: "Agregar lugar",
        components: { default: AddVenue }
      },
      {
        path: "events/venues/show/:venue_id",
        name: "Visualizar lugar",
        components: { default: ShowVenue }
      },
      {
        path: "events/venues/edit/:venue_id",
        name: "Editar lugar",
        components: { default: EditVenue }
      },
      {
        path: "news",
        name: "Noticias",
        components: { default: News }
      },
      {
        path: "news/add",
        name: "Agregar noticia",
        components: { default: AddNews }
      },
      {
        path: "news/edit/:news_id",
        name: "Editar noticia",
        components: { default: EditNews }
      },
      {
        path: "events/events",
        name: "Eventos",
        components: { default: Events }
      },
      {
        path: "events/events/add",
        name: "Agregar eventos",
        components: { default: AddEvent }
      },
      {
        path: "events/events/edit/:event_id",
        name: "Editar eventos",
        components: { default: EditEvent }
      },
      {
        path: "*",
        name: "Dashboard",
        components: { default: Dashboard }
      }
    ]
  }
];

export default routes;
