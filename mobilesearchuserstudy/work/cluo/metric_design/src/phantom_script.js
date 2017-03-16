
console.log('Loading a web page');
var page = require('webpage').create();
var url = 'http://www.sina.com.cn/';
page.viewportSize = {
  width: 1351,
  height: 1500
};
page.open(url, function (status) {
  //Page is loaded!
  console.log(status);
  var links = page.evaluate(function() {
	return $('a').map(function (i,  e) {return e.href;});
	});	
  
  for (var i = 0; i < links.length; i++) {
	console.log(links[i]);
	}
  phantom.exit();
});