$(".side-nav-toggle").click(function(){$("#side-nav").css("width", "100vw");$(this).addClass("nav-hidden");$(".nav-icon-close").removeClass("nav-hidden");});$(".side-nav-content").click(function(e){e.stopPropagation();});$("#side-nav").click(function(){$(this).css("width", "0vw");$(".nav-icon-close").addClass("nav-hidden");$(".nav-icon-menu").removeClass("nav-hidden");});$(document).ready(function () {$(window).scroll(function() {var winOffset = document.documentElement.scrollTop || document.body.scrollTop;if(winOffset > 50) {$('.uk-navbar-container').addClass("nav-bar");} else {$('.uk-navbar-container').removeClass("nav-bar");}});});$(document).ready(function () {var winOffset = document.documentElement.scrollTop || document.body.scrollTop;if(winOffset > 50) {$('.uk-navbar-container').addClass("nav-bar");} else {$('.uk-navbar-container').removeClass("nav-bar");}});
!function(window){
    var $q = function(q, res){
          if (document.querySelectorAll) {
            res = document.querySelectorAll(q);
          } else {
            var d=document
              , a=d.styleSheets[0] || d.createStyleSheet();
            a.addRule(q,'f:b');
            for(var l=d.all,b=0,c=[],f=l.length;b<f;b++)
              l[b].currentStyle.f && c.push(l[b]);
  
            a.removeRule(0);
            res = c;
          }
          return res;
        }
      , addEventListener = function(evt, fn){
          window.addEventListener
            ? this.addEventListener(evt, fn, false)
            : (window.attachEvent)
              ? this.attachEvent('on' + evt, fn)
              : this['on' + evt] = fn;
        }
      , _has = function(obj, key) {
          return Object.prototype.hasOwnProperty.call(obj, key);
        }
      ;
  
    function loadImage (el, fn) {
      var img = new Image()
        , src = el.getAttribute('data-src');
      img.onload = function() {
        if (!! el.parent)
          el.parent.replaceChild(img, el)
        else
          el.src = src;
  
        fn? fn() : null;
      }
      img.src = src;
    }
  
    function elementInViewport(el) {
      var rect = el.getBoundingClientRect()
  
      return (
         rect.top    >= 0
      && rect.left   >= 0
      && rect.top <= (window.innerHeight || document.documentElement.clientHeight)
      )
    }
  
      var images = new Array()
        , query = $q('img.lazy')
        , processScroll = function(){
            for (var i = 0; i < images.length; i++) {
              if (elementInViewport(images[i])) {
                loadImage(images[i], function () {
                  images.splice(i, i);
                });
              }
            };
          }
        ;
      // Array.prototype.slice.call is not callable under our lovely IE8 
      for (var i = 0; i < query.length; i++) {
        images.push(query[i]);
      };
  
      processScroll();
      addEventListener('scroll',processScroll);
  
}(this);​