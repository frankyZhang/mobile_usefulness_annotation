
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



var filename = "./happy.txt";
fout = new ActiveXObject("Scripting.FileSystemObject");
tf = fout.CreateTextFile(filename)
tf.writeln("123");
tf.close()



var visible_elements = [];

    $(':visible').each(
        function (idx, e) {
            var rect = e.getBoundingClientRect();
            if (e.innerText != "" || e.innerText =="") {
                var box = {
                    left: rect.left,
                    top: rect.top,
                    right: rect.right,
                    bottom: rect.bottom,
                    text: e.innerText,
                };
                visible_elements.push(box);
            }
        }
    );