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
    let lazyImages = [].slice.call(document.querySelectorAll("img[data-src]"));
    let active = false;
    const lazyLoad = function() {
      if (active === false) {
        active = true;
        setTimeout(function() {
          lazyImages.forEach(function(lazyImage) {
            if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== "none") {
              lazyImage.src = lazyImage.dataset.src;
              lazyImages = lazyImages.filter(function(image) {
                return image !== lazyImage;
              });
              if (lazyImages.length === 0) {
                document.removeEventListener("scroll", lazyLoad);
                window.removeEventListener("resize", lazyLoad);
                window.removeEventListener("orientationchange", lazyLoad);
              }
            }
          });
          active = false;
        }, 200);
      }
    };
    document.addEventListener("scroll", lazyLoad);
    window.addEventListener("resize", lazyLoad);
    window.addEventListener("orientationchange", lazyLoad);
});