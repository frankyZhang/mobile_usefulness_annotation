/**
 * Created by luocheng on 14/12/2016.
 */
var page = require('webpage').create();

console.log('Loading a web page');
var args = require('system').args;
var page = require('webpage').create();
var url = args[1];
page.viewportSize = {
  width: 375
};


page.open(url, function(){
    console.log(page.evaluate(function(){
        return JSON.stringify({
            "document.body.scrollHeight": document.body.scrollHeight,
            "document.body.offsetHeight": document.body.offsetHeight,
            "document.documentElement.clientHeight": document.documentElement.clientHeight,
            "document.documentElement.scrollHeight": document.documentElement.scrollHeight
        }, undefined, 4);
    }));
    phantom.exit();
});