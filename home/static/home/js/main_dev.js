$(".side-nav-toggle").click(function() {
    $("#side-nav").css("width", "100vw");
    $(this).addClass("nav-hidden");
    $(".nav-icon-close").removeClass("nav-hidden");
});
$(".side-nav-content").click(function(e) {
    e.stopPropagation();
});
$("#side-nav").click(function() {
    $(this).css("width", "0vw");
    $(".nav-icon-close").addClass("nav-hidden");
    $(".nav-icon-menu").removeClass("nav-hidden");
});
$(document).ready(function() {
    $(window).scroll(function() {
        var winOffset = document.documentElement.scrollTop || document.body.scrollTop;
        if (winOffset > 50) {
            $('.uk-navbar-container').addClass("nav-bar");
        } else {
            $('.uk-navbar-container').removeClass("nav-bar");
        }
    });
});
$(document).ready(function() {
    var winOffset = document.documentElement.scrollTop || document.body.scrollTop;
    if (winOffset > 50) {
        $('.uk-navbar-container').addClass("nav-bar");
    } else {
        $('.uk-navbar-container').removeClass("nav-bar");
    }
});
document.addEventListener("DOMContentLoaded", function() {
    var e, t = document.querySelectorAll("img[data-src]");

    function o() {
        e && clearTimeout(e), e = setTimeout(function() {
            var n = window.pageYOffset;
            t.forEach(function(e) {
                e.offsetTop < window.innerHeight + n + 100 && (e.src = e.dataset.src)
            }), (document.removeEventListener("scroll", o), window.removeEventListener("resize", o), window.removeEventListener("orientationChange", o))
        }, 0);
    }
    document.addEventListener("scroll", o), window.addEventListener("resize", o), window.addEventListener("orientationChange", o)
    let fi = document.querySelectorAll("img[data-src]")[0];
    if (fi) fi.src = fi.dataset.src;
});