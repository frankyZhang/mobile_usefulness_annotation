/**
 * Created by luocheng on 14/12/2016.
 */

console.log('Loading a web page');
var args = require('system').args;
var page = require('webpage').create();
var url = args[1];
var filename = args[2];
page.viewportSize = {
  width: 375,
  height: 2000
};

page.open(url, function (status) {
  //Page is loaded!
  page.render(filename);
  phantom.exit();
});

