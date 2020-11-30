$(window).on('load', function(){ popUp(); });

function popUp(){
    nick = $('#current-user-nick').val();
    if (nick == 'None'){
        $('#background-content').addClass('disable-background');
        $('body').css('overflow', 'hidden');
        $('#set-nick-window').removeClass('disable-background');}
    else { $('#background-content').removeClass('disable-background');
           $('body').css('overflow', 'auto');}

}
