// ==UserScript==
// @name         Preload dns for Google results
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Freddyzeng
// @include      ^http://www.google.*
// @include      ^https://www.google.*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    // Your code here...
    // var nodesSnapshot = document.evaluate('//a[contains(@rel, "noopener")]', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null );
    var nodesSnapshot = document.evaluate('//cite', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null );
    let siteSet = new Set();
    for ( var i=0 ; i < nodesSnapshot.snapshotLength; i++ )
    {
        var site_string = nodesSnapshot.snapshotItem(i).textContent
        // console.log(site_string)
        var site = site_string.split("›", 1)[0];
        // console.log(site)
        if(!site.startsWith('http')) {
            continue
        }
        site = site.split("//")[1];
        // console.log(site)
        site = site.replace(/\s/g, '');
        siteSet.add(site)
    }

    var requests=new Array(siteSet.size);
    for (let item of siteSet) {
        // console.log(item);
        const Http = new XMLHttpRequest();
        // const url = 'https://' + item + '/xxqueryxx';
        const url = 'https://192.168.50.2:53535?domain=' + item;
        // const url = item;
        // Http.open("GET", url);
        // Http.send();
        // Http.onload = function() {
        //     console.log('onload');
        // }
        // requests.push(Http)
        sendRequest(url)
    }

    function sendRequest(url) {
        var img = new Image();
        img.src = url;
        document.body.appendChild(img);
    }

    const url='https://www.google.com';
    sendRequest(url)
    // const Http_google = new XMLHttpRequest();
    // Http_google.open("GET", url);
    // Http_google.send();
    // Http_google.onload = function() {
    //     console.log('onload');
    // }
    // requests.push(Http_google)

    const url_hk='https://www.google.com.hk';
    sendRequest(url_hk)
    // const Http_google_hk = new XMLHttpRequest();
    // Http_google_hk.open("GET", url_hk);
    // Http_google_hk.send();
    // Http_google_hk.onload = function() {
    //     console.log('onload');
    // }
    // requests.push(Http_google_hk)

    const url_jp='https://www.google.co.jp';
    sendRequest(url_jp)
//     const Http_google_jp = new XMLHttpRequest();
//     Http_google_jp.open("GET", url_jp);
//     Http_google_jp.send();
//     Http_google_jp.onload = function() {
//         console.log('onload');
//     }
//     requests.push(Http_google_jp)

    const url_uk='https://www.google.co.uk';
    sendRequest(url_uk)
    // const Http_google_uk = new XMLHttpRequest();
    // Http_google_uk.open("GET", url_uk);
    // Http_google_uk.send();
    // Http_google_uk.onload = function() {
    //     console.log('onload');
    // }
    // requests.push(Http_google_uk)

})();
