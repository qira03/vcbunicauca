
let mutations = {
    
    
    updateUser(state,payload) {
        state.user.username = payload.message;
    },
    updateUserId(state,payload) {
        state.user.id = payload.message;
    },
    updateName(state,payload) {
        state.user.name = payload.message;
    },
    updateUserRole(state,payload) {
        state.user.role = payload.message;
    },
    updateUserUrl(state,payload) {
        state.user.url = payload.message;
    },
    updateUserPicture(state,payload) {
        state.user.picture = payload.message;
    },
    updateToken(state,payload){
        state.token = payload.message;
    },
    resetUser(state,payload) {
       
        state.user.id= '',
        state.user.name= '',
        state.user.username= ''
        
    },
    resetToken(state,payload){
        state.token = ''
    }

    
}
export default mutations
