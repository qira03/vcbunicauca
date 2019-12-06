import { myUrl } from './params';
import store from '../store/store';

export function uploadFilesToGraphQLXr(formData){
    const promise = new Promise(function (resolve, reject){
        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            var myObject ={};
            myObject = JSON.parse(this.responseText);
            if(myObject.data != null)
            {
                resolve(myObject);
            }
            else if(myObject.errors != null)
            {
                reject(myObject);
            }
        }
        });
        xhr.open("POST", myUrl);
        xhr.setRequestHeader("Authorization", "JWT "+store.getters.getToken);
        xhr.send(formData);
    });
    return promise
}