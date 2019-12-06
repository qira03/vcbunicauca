import  gql  from 'graphql-tag';

export const ALL_NEWS =  gql`query News($after: String, $first: Int!,$slug: String){
    allNews(active:true,first:$first, after:$after, slug: $slug){
    edges{
    node{
            id,
            name,
            abstract,
            slug,
            createdAt,
            post{
                images(principal:true){
                edges{
                    node{
                        imageFile,
                        principal
                        }
                    }
                }
                }

            }
    }
    pageInfo{
        endCursor,
        hasNextPage
    }
    }
    }`;
export const ALL_NEWS_SLUG =  gql`query News($after: String, $first: Int!,$slug: String){
    allNews(active:true,first:$first, after:$after, slug: $slug){
    edges{
    node{
            id,
            name,
            abstract,
            slug,
            createdAt,
            description,
            post{
                images{
                edges{
                    node{
                        imageFile,
                        principal
                        }
                    }
                }
                }

            }
    }
    pageInfo{
        endCursor,
        hasNextPage
    }
    }
}`;
export const ALL_EVENTS = gql`query Events($after: String, $first: Int!,$slug:String){
    allEvents(active:true,first:$first, after:$after, slug: $slug){
    edges{
    node{
        id,
        name,
        slug,
        abstract,
        startDatetime,
        categories(first:1){
            edges{
                node{
                    name
                }
            }
        },
        post{
            images(principal:true){
                edges{
                    node{
                        imageFile
                    }
                }
            }
        }
    }
    }
    pageInfo{
        endCursor,
        hasNextPage
    }
    }
}`;
export const ALL_EVENTS_DASHBOARD = gql`query Events($finishDatetime_Gt: DateTime!){
    allEvents(finishDatetime_Gt:$finishDatetime_Gt){
        edges{
            node{
                id,
                name,
                slug,
                startDatetime,
                finishDatetime
                }
            }
            }
    }`;
export const ALL_EVENTS_SLUG = gql`query Events($after: String, $first: Int!,$slug:String){
    allEvents(active:true,first:$first, after:$after, slug: $slug){
        edges{
            node{
                id,
                name,
                slug,
                abstract,
                description,
                startDatetime,
                finishDatetime,
                website,
                price,
                limited,
                venue{
                    id,
                    name,
                    latitude,
                    longitude,
                    address,
                    city
                },
                organizers{
                    edges{
                        node{
                            id,
                            name
                        }
                    }
                }
                categories(first:1){
                                    edges{
                                        node{
                                            name
                                            }
                                        }
                                    },
                post{
                    images{
                        edges{
                            node{
                                imageFile,
                                principal
                                }
                            }
                          }
                    }
                }
            }

        }
}`;

export const LOGIN = gql`mutation Login($username: String!, $password: String!){
    tokenAuth(username: $username, password: $password){
        token
    }
}`;
export const REFRESH_TOKEN = gql`mutation RefreshToken($token: String!){
    refreshToken(token: $token){
        token
        payload
    }
}`;

export const GET_USER_BY_USERNAME = gql`query GetAllUsers($username: String!){
    allUsers(username: $username){
        edges{
            node{
                id
                username
                email
                firstName
                lastName
                isSuperuser
                isActive
            }
        }
    }
}`;

export const ALL_USERS = gql`query {allUsers{
    edges{
        node{
            id
            username
            email
            firstName
            lastName
            isSuperuser
            isActive
        }
    }
}
}`;

export const CREATE_USER = gql`mutation CreateUser($input: CreateUserInput!){
    createUser(input: $input){
        newUser{
            id
            username
            email
            firstName
            lastName
            isSuperuser
            isActive
        }
    }
}`;

export const GET_USER_BY_ID = gql`query GetUserById($id: ID!){
    user(id: $id){
        id
        username
        email
        firstName
        lastName
    }
}`;

export const UPDATE_USER = gql`mutation UpdateUser($input: UpdateUserInput!){
    updateUser(input: $input){
        updatedUser{
            id
            username
            firstName
            lastName
        }
    }
}`;

export const UPDATE_USER_PASSWORD = gql`mutation UpdateUserPassword($input: UpdateUserPasswordInput!){
    updateUserPassword(input: $input){
        updatedUser{
            id
            username
            firstName
        }
    }
}`;

export const ALL_CATEGORIES = gql`query {allCategories{
        edges{
            node{
                id
                name
                slug
                description
            }
        }
    }
}`;

export const CREATE_CATEGORY = gql`mutation CreateCategory($input: CreateCategoryInput!){
    createCategory(input: $input){
        newCategory{
            id
            name
            slug
            description
            image
            createdAt
            updatedAt
        }
    }
}`;

export const GET_CATEGORY_BY_ID = gql`query GetCategoryById($id: ID!){
    category(id: $id){
        id
        name
        description
        image
        relatedLinks{
            edges{
                node{
                    id
                    name
                    link
                }
            }
        }
    }
}`;

export const UPDATE_CATEGORY = `mutation UpdateCategory($input: UpdateCategoryInput!){
    updateCategory(input: $input){
        updatedCategory{
            id
            name
            slug
            description
            image
            createdAt
            updatedAt
        }
    }
}`;

export const ALL_ORGANIZERS = gql`query {
    allOrganizers{
        edges{
            node{
                id
                name
                phone
                website
                email
            }
        }
    }
}`;

export const CREATE_ORGANIZER = gql`mutation CreateOrganizer($input: CreateOrganizerInput!){
    createOrganizer(input: $input){
        newOrganizer{
            id
            name
        }
    }
}`;

export const GET_ORGANIZER_BY_ID = gql`query GetOrganizerById($id: ID!){
    organizer(id: $id){
        id
        name
        phone
        website
        email
    }
}`;

export const UPDATE_ORGANIZER = gql`mutation UpdateOrganizer($input: UpdateOrganizerInput!){
    updateOrganizer(input: $input){
        updatedOrganizer{
            id
        }
    }
}`;

export const ALL_VENUES = gql`query {
    allVenues{
        edges{
            node{
                id
                name
                address
                city
                phone
            }
        }
    }
}`;

export const CREATE_VENUE = gql`mutation CreateVenue($input: CreateVenueInput!){
    createVenue(input: $input){
        newVenue{
            id,
            latitude,
            longitude
        }
    }
}`;

export const GET_VENUE_BY_ID = gql`query GetVenueById($id: ID!){
    venue(id: $id){
        id
        name
        address
        city
        state
        phone
        website
        latitude
        longitude
    }
}`;

export const UPDATE_VENUE = gql`mutation UpdateVenue($input: UpdateVenueInput!){
    updateVenue(input: $input){
        updatedVenue{
            id
        }
    }
}`;

export const LAST_NEWS =  gql`query News($after: String, $first: Int!,$slug: String){
    lastNews(active:true,first:$first, after:$after, slug: $slug){
        edges{
        node{
                id,
                name,
                abstract,
                slug,
                createdAt,
                post{
                    images(principal:true){
                    edges{
                        node{
                            imageFile,
                            principal
                            }
                        }
                    }
                    }

                }
        }
        pageInfo{
            endCursor,
            hasNextPage
        }
        }
}`;

export const CREATE_NEWS = gql`mutation CreateNews($input: CreateNewsInput!){
    createNews(input: $input){
        newNews{
            id
        }
    }
}`;

export const UPDATE_NEWS = gql`mutation UpdateNewsById($input: UpdateNewsInput!) {
    updateNews(input: $input) {
        updatedNews {
            id
        }
    }
}`;

export const DELETE_NEWS = gql`mutation DeleteNews($input: DeleteNewsInput!){
    deleteNews(input: $input){
        success
    }
}`;

export const ADD_IMAGES_TO_POST = `mutation AddImagesToPost($input: AddImagesToPostInput!){
	addImagesToPost(input: $input){
    post{
      images{
        edges{
          node{
            id
            imageFile
          }
        }
      }
    }
  }
}`;

export const GET_NEWS_BY_ID = gql`query GetNewsById($id: ID!){
    news(id: $id){
        id
        name
        slug
        abstract
        description
        active
        createdAt
        updatedAt
        post{
            images{
                edges{
                    node{
                        id
                        imageFile
                        principal
                    }
                }
            }
        }
    }
}`;

export const DELETE_IMAGE_BY_ID = gql`mutation DeleteImageById($input: DeleteImageInput!) {
    deleteImage(input: $input){
        success
    }
}`;

export const LAST_EVENTS = gql`query Events($after: String, $first: Int!,$slug:String){
    lastEvents(active:true,first:$first, after:$after, slug: $slug){
    edges{
    node{
        id,
        name,
        slug,
        abstract,
        startDatetime,
        finishDatetime,
        createdAt
    }
    }
    pageInfo{
        endCursor,
        hasNextPage
    }
    }
}`;

export const CREATE_EVENT = gql`mutation CreateEvent($input: CreateEventInput!){
    createEvent(input: $input){
        newEvent{
            id
        }
    }
}`;

export const GET_EVENT_BY_ID = gql`query GetEventById($id: ID!){
    event(id: $id){
        id
        name
        slug
        startDatetime
        finishDatetime
        abstract
        description
        price
        website
        limited
        active
        createdAt
        updatedAt
        categories{
            edges{
                node{
                    id
                    name
                }
            }
        }
        organizers{
            edges{
                node{
                    id
                    name
                }
            }
        }
        venue{
            id
            name
        }
        post{
            images{
                edges{
                    node{
                        id
                        imageFile
                        principal
                    }
                }
            }
        }
    }
}`;

export const UPDATE_EVENT = gql`mutation UpdateEvent($input: UpdateEventInput!){
    updateEvent(input: $input){
        updatedEvent{
            id
        }
    }
}`;

export const DELETE_EVENT = gql`mutation DeleteEvent($input: DeleteEventInput!){
    deleteEvent(input: $input){
        success
    }
}`;

export const ALL_SLIDERS = gql`query AllSliders($position: String!){
    allSliders(position:$position){
        edges{
          node{
            id,
            name,
            position
            post{
              images{
                edges{
                  node{
                    id
                    imageFile
                  }
                }
              }
            }
          }
        }
    }
}`;

export const RECENT_EVENTS = gql`query Events($after: String, $first: Int!,$slug:String,$finishDatetime_Gt: DateTime!){
    recentEvents(active:true,first:$first, after:$after, slug: $slug, finishDatetime_Gt:$finishDatetime_Gt){
    edges{
    node{
        id,
        name,
        slug,
        abstract,
        startDatetime,
        finishDatetime,
        createdAt
    }
    }
    pageInfo{
        endCursor,
        hasNextPage
    }
    }
}`;

export const ALL_ORGANIZERS_REPORTS = gql`query AllOrganizersReports($startDatetime_Gt: DateTime, $startDatetime_Lt: DateTime, $organizerName: String){
    allOrganizers(name: $organizerName){
      edges{
        node{
          id
          name
          events(startDatetime_Gt: $startDatetime_Gt, startDatetime_Lt: $startDatetime_Lt){
            edges{
              node{
                id
                name
                startDatetime
                finishDatetime
              }
            }
          }
        }
      }
    }
  }`;

  export const GET_ORGANIZER_REPORTS = gql`query GetOrganizerReports($id: ID!,$startDatetime_Gt: DateTime, $startDatetime_Lt: DateTime){
    GetOrganizerById(id: $id){
      edges{
        node{
          id
          name
          events(startDatetime_Gt: $startDatetime_Gt, startDatetime_Lt: $startDatetime_Lt){
            edges{
              node{
                id
                name
                startDatetime
                finishDatetime
              }
            }
          }
        }
      }
    }
  }`;

export const ALL_NEWS_REPORTS = gql`query AllNewsReports($createdAt_Gt: DateTime, $createdAt_Lt: DateTime){
    allNews(createdAt_Gt: $createdAt_Gt, createdAt_Lt: $createdAt_Lt){
      edges{
        node{
          id
          name
        }
      }
    }
  }`;

export const CREATE_RELATED_LINKS = gql`mutation AddRelatedLinksToCategory($input: AddRelatedLinksToCategoryInput!){
    addRelatedLinksToCategory(input: $input){
        category{
            id
            name
            relatedLinks{
                edges{
                    node{
                        id
                        name
                        link
                    }
                }
            }
        }
    }
}`;

export const DELETE_RELATED_LINK = gql`mutation DeleteRelatedLink($input: DeleteRelatedLinkInput!){
    deleteRelatedLink(input: $input){
        success
    }
}`;
