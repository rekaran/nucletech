// var projectKey = {};
// var context = {};
// const projectkey = "NDIyZDllNDZlOTRiYTFmOWNkZWEzNjZhYzNjNDczMzc5YjY0ZDQ0YzBiZDA5MWFkMTBiM2IxM2NlYTM3OTAzNGFhNWY1MzVkNTJlOGNlODdmMWI3ZWE0ZTY1ZDJjNWZjZWNkNjFkMzgzZjgwYTVjZjhkN2I5ZmEyNmYwNzZjYzc=";
// const projectHash = "U2FsdGVkX1+tETMxYy+6K69yNiYCtrFQi+1zuMlAXDzmej4Uilv3P/UIC/hy7hj+RGxqLCgkcX/zVoOuRPgnL2P+JUwWKL6wxVbqTtTlIAk7y7BvKZn9r4zD3iA23pNPOcPRol1mrlaLNrny0XIAX7aoETo7pv3LMx573fZiGgPO5QV23i1CbPz7nmZ4Sxdo"
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
        Http.setRequestHeader("Authorization", projectHash);
        Http.send(JSON.stringify({key: projectHash, timestamp: projectKey.timestamp}));
        Http.onload = () =>{
            if (Http.status == 200) {
                let response = JSON.parse(Http.responseText);
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
                Http.setRequestHeader("Authorization", projectHash);
                Http.send(JSON.stringify({key: projectHash}));
                Http.onload = () =>{
                    if (Http.status == 200) {
                        projectKey = JSON.parse(Http.responseText);
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