$(window).on('load', function(){ getMostViewed(); });

function getMostViewed(){
    $.getJSON('/v1/most_viewed', function (data){
    $('#most-viewed-name').html(data.name);
    $('a[href="/most-viewed-drink"]').each(function(){
        this.href = this.href.replace('/most-viewed-drink', '/v1/drink/' + data.id);})
    var path = '/static/images/drinks/' + data.image;
    $('#most-viewed-img').attr('src', path);
    });
};