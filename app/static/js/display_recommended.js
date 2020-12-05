$(window).on('load', function(){ getRecommended(); });

function getRecommended(){
    $.getJSON('/v1/most_viewed', function (data){
        $('#most-viewed-name').html(data.name);
        $('a[href="/most-viewed-drink"]').each(function(){
            this.href = this.href.replace('/most-viewed-drink', '/v1/drink/' + data.id);})
        var path = '/static/images/drinks/' + data.image;
        $('#most-viewed-img').attr('src', path);
    });

    $.getJSON('/v1/top_rated', function (data){
        $('#top-rated-name').html(data.name);
        $('a[href="/top-rated-drink"]').each(function(){
            this.href = this.href.replace('/top-rated-drink', '/v1/drink/' + data.id);})
        var path = '/static/images/drinks/' + data.image;
        $('#top-rated-img').attr('src', path);
    });
};