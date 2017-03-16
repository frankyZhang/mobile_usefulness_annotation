// <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>

<script type="text/javascript">
    var visible_elements = [];
    $(':visible').each(
        function (idx, e) {
            var rect = e.getBoundingClientRect();
            if (true) {
                var box = {
                    left: rect.left,
                    top: rect.top,
                    right: rect.right,
                    bottom: rect.bottom,
                    text: e.innerText,
                };
                console.log("<position>\n");
                console.log(box.left+" "+ box.right+" "+box.top+" "+box.bottom+"\n");
                console.log("</position>\n");
                console.log("<nodecontent>\n");
                console.log(e.outerHTML);
                console.log("</nodecontent>\n");
                visible_elements.push(box);
            }
        }
    );
</script>