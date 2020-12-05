$(document).ready(function(){
    var navPosition = $('#topnav').offset().top;

    var stickyNavbar = function(){
        var windowScroll = $(window).scrollTop();

        if (windowScroll > navPosition){ $('#topnav').addClass('sticky-topnav') }
        else { $('#topnav').removeClass('sticky-topnav') };
    }

    stickyNavbar();
    $(window).scroll(function(){ stickyNavbar(); });
})
