$(".side-nav-toggle").click(function(){$("#side-nav").css("width", "100vw");$(this).addClass("nav-hidden");$(".nav-icon-close").removeClass("nav-hidden");});$(".side-nav-content").click(function(e){e.stopPropagation();});$("#side-nav").click(function(){$(this).css("width", "0vw");$(".nav-icon-close").addClass("nav-hidden");$(".nav-icon-menu").removeClass("nav-hidden");});$(document).ready(function () {$(window).scroll(function() {var winOffset = document.documentElement.scrollTop || document.body.scrollTop;if(winOffset > 50) {$('.uk-navbar-container').addClass("nav-bar");} else {$('.uk-navbar-container').removeClass("nav-bar");}});});$(document).ready(function () {var winOffset = document.documentElement.scrollTop || document.body.scrollTop;if(winOffset > 50) {$('.uk-navbar-container').addClass("nav-bar");} else {$('.uk-navbar-container').removeClass("nav-bar");}});
document.addEventListener("DOMContentLoaded", function() {
    var lazyloadImages = document.querySelectorAll("img[data-src]");    
    var lazyloadThrottleTimeout;
    
    function lazyload () {
      if(lazyloadThrottleTimeout) {
        clearTimeout(lazyloadThrottleTimeout);
      }    
      
      lazyloadThrottleTimeout = setTimeout(function() {
          var scrollTop = window.pageYOffset;
          lazyloadImages.forEach(function(img) {
              if(img.offsetTop < (window.innerHeight + scrollTop)) {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
              }
          });
          if(lazyloadImages.length == 0) { 
            document.removeEventListener("scroll", lazyload);
            window.removeEventListener("resize", lazyload);
            window.removeEventListener("orientationChange", lazyload);
          }
      }, 0);
    }
    
    document.addEventListener("scroll", lazyload);
    window.addEventListener("resize", lazyload);
    window.addEventListener("orientationChange", lazyload);
  });