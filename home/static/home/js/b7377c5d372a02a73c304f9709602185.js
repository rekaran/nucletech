// var projectKey = {};
// var context = {};
// const projectkey = "U2FsdGVkX19MPl9PptQJfToPOsrAu8kGoKYbx9tPRXRA4dth4BONBSEXtSzExZfcYyTiUbSiKQgpP0Gh/Xa3z0bSOuHogI+ItTXLQn0kw03IXf7WDNGMZt6ADNBDds4zlrigBcrLbPueIBwSN95r7kLALLqlYvqq+N/VwCUI1xMBJBOhOcQP99ViunpxsKj0";
const url = "https://www.nuclechat.com/key/"+window.location.hostname;
const Http = new XMLHttpRequest();

let resourceNegotiator = (url, sync, res) => {
    let filetype = url.split(".")[url.split(".").length-1];
    let filename = url.split("/")[url.split("/").length-1];
    let s;
    if(res.indexOf(filename)===-1){
        if(filetype=="js"){
            s = document.createElement('script');
            s.type = 'text/javascript';
            s.async = sync;
            s.src = url;
        }else if(filetype=="css"){
            s = document.createElement('link');
            s.rel = "stylesheet";
            s.as = "style";
            s.type = 'text/css';
            s.href = url;
        }
        let x = document.getElementsByTagName('head')[0];
        x.appendChild(s);
    }
};
let getResourceList = res => {
    if(Object.keys(projectKey).length!==0){
        let url = "https://www.nuclechat.com/resources/"+projectKey.domain;//+window.location.hostname;
        let Http = new XMLHttpRequest();
        Http.open("POST", url, true);
        Http.setRequestHeader("Content-Type", "application/json");
        Http.setRequestHeader("Authorization", projectkey);
        Http.send(JSON.stringify({key: projectKey.hash, timestamp: projectKey.timestamp, keys: projectKey.key}));
        Http.onload = () =>{
            if (Http.status == 200) {
                let decData = CryptoJS.RabbitLegacy.decrypt(Http.responseText, projectkey);
                let response = JSON.parse(decData.toString(CryptoJS.enc.Utf8));
                response.async.forEach(data=>{
                    resourceNegotiator(data, true, res);
                });
                response.sync.forEach(data=>{
                    resourceNegotiator(data, false, res);
                });
            }else{
                console.warn("You are not authorised to use the bot.");
            }
        };
    }else{
        console.warn("You are not authorised to use the bot.");
    }
};
let startScript = () =>{
    let primaryAnchor = document.getElementsByClassName("nt-primary-link");
    if(Object.keys(primaryAnchor).length>0){
        if(primaryAnchor[0].getAttribute("rel")=='follow'){
            if(primaryAnchor[0].getAttribute("href")=="https://www.nucletech.com"){
                Http.open("POST", url, true);
                Http.setRequestHeader("Content-Type", "application/json");
                Http.setRequestHeader("Authorization", projectkey);
                Http.send(JSON.stringify({key: projectkey}));
                Http.onload = () =>{
                    if (Http.status == 200) {
                        let decData = CryptoJS.RabbitLegacy.decrypt(Http.responseText, projectkey);
                        projectKey = JSON.parse(decData.toString(CryptoJS.enc.Utf8));
                        context = projectKey.context;
                        delete projectKey.context;
                        if(Object.keys(projectKey).length!==0){
                            let res = [];
                            Object.values(document.getElementsByTagName("script")).forEach(script=>{
                                if(script.src){
                                    let name = script.src.split("/");
                                    name = name[name.length -1];
                                    if(name.indexOf(".")!==-1)
                                    res.push(name);
                                }
                            });
                            Object.values(document.getElementsByTagName("link")).forEach(style=>{
                                if(style.href){
                                    let name = style.href.split("/");
                                    name = name[name.length -1];
                                    if(name.indexOf(".")!==-1)
                                    res.push(name);
                                }
                            });
                            getResourceList(res);
                        }else{
                            console.warn("You are not authorised to use the bot.");
                        }
                    }else{
                        console.warn("You are not authorised to use the bot.");
                    }
                };
            }else{
                console.error("Change in the code was detected, copy paste the code from the nucletech pltform");
            }
        }else{
            console.error("Change in the code was detected, copy paste the code from the nucletech pltform");
        }
    }else{
        console.error("Change in the code was detected, copy paste the code from the nucletech pltform");
    }
};
// if(navigator.onLine){
//     startScript();
// }
startScript();
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('https://www.nuclechat.com/static/js/sw.js')
    .then(registration => {
        // Registration was successful
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
      }, err => {
        // registration failed :(
        console.log('ServiceWorker registration failed: ', err);
      });
}