$(".side-nav-toggle").click(function(){$("#side-nav").css("width", "100vw");$(this).addClass("nav-hidden");$(".nav-icon-close").removeClass("nav-hidden");});$(".side-nav-content").click(function(e){e.stopPropagation();});$("#side-nav").click(function(){$(this).css("width", "0vw");$(".nav-icon-close").addClass("nav-hidden");$(".nav-icon-menu").removeClass("nav-hidden");});$(document).ready(function () {$(window).scroll(function() {var winOffset = document.documentElement.scrollTop || document.body.scrollTop;if(winOffset > 50) {$('.uk-navbar-container').addClass("nav-bar");} else {$('.uk-navbar-container').removeClass("nav-bar");}});});$(document).ready(function () {var winOffset = document.documentElement.scrollTop || document.body.scrollTop;if(winOffset > 50) {$('.uk-navbar-container').addClass("nav-bar");} else {$('.uk-navbar-container').removeClass("nav-bar");}});
const config = {
    rootMargin: '0px 0px 50px 0px',
    threshold: 0
};
let observer = new intersectionObserver(function(entries, self) {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            preloadImage(entry.target);
            self.unobserve(entry.target);
        }
    });
}, config);
const imgs = document.querySelectorAll('[data-src]');
imgs.forEach(img => {
    observer.observe(img);
});