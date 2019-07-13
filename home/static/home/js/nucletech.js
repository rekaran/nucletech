const url = "https://www.nuclechat.com/key/"+"nucletech.com";//+window.location.hostname;
const Http = new XMLHttpRequest();

let resourceNegotiator = (url, sync) => {
    let filetype = url.split(".")[url.split(".").length-1];
    let s;
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
};
let getResourceList = () => {
    if(Object.keys(projectKey).length!==0){
        let url = "https://www.nuclechat.com/resources/"+projectKey.domain;//+window.location.hostname;
        let Http = new XMLHttpRequest();
        Http.open("POST", url, true);
        Http.setRequestHeader("Content-Type", "application/json");
        Http.setRequestHeader("Authorization", projectkey);
        Http.send(JSON.stringify({key: projectKey.hash, timestamp: projectKey.timestamp, keys: projectKey.key}));
        Http.onload = () =>{
            if (Http.status == 200) {
                let response = JSON.parse(Http.responseText);
                response.sync.forEach(data=>{
                    resourceNegotiator(data, false);
                });
                response.async.forEach(data=>{
                    resourceNegotiator(data, true);
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
                        projectKey = JSON.parse(Http.responseText);
                        if(Object.keys(projectKey).length!==0){
                            getResourceList();
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
if(navigator.onLine){
    startScript();
}

// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('http://127.0.0.1:4000/js/sw.js');
// }