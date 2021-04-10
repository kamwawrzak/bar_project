window.addEventListener('DOMContentLoaded', () => {
    let navPosition = document.getElementById('topnav').offsetTop;
    let stickyNavbar = () => {
        let windowScroll = window.scrollY;

        if (windowScroll > navPosition){
            document.getElementById('topnav').classList.add('sticky-topnav');
        } else {
            document.getElementById('topnav').classList.remove('sticky-topnav');
        };
    };
    let pageHeight = document.body.scrollHeight;
    if(pageHeight > 800){
        stickyNavbar();
        window.addEventListener('scroll', stickyNavbar);
    };
});
