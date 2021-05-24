function move() {
    var elem1 = document.getElementById("bar1");
    var elem2 = document.getElementById("bar2");
    var elem3 = document.getElementById("bar3");

    var width = 1;
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
}
