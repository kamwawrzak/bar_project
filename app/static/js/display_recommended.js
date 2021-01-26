$(window).on('load', function(){ getMostViewed(); getTopRated(); });

function getMostViewed(){
    $.getJSON('/v1/most_viewed', function (data){
        var drinkName = data.name;
        drinkName = drinkName.charAt(0).toUpperCase() + drinkName.substring(1).toLowerCase();
        $('#most-viewed-name').html(drinkName);
        $('a[href="/most-viewed-drink"]').each(function(){
            this.href = this.href.replace('/most-viewed-drink', '/v1/drink/' + data.id);})
        $('#most-viewed-img').attr('src', data.image);
    });
};

function getTopRated(){
    $.getJSON('/v1/top_rated', function (data){
        var drinkName = data.name;
        drinkName = drinkName.charAt(0).toUpperCase() + drinkName.substring(1).toLowerCase();
        $('#top-rated-name').html(drinkName);
        $('a[href="/top-rated-drink"]').each(function(){
            this.href = this.href.replace('/top-rated-drink', '/v1/drink/' + data.id);})
        $('#top-rated-img').attr('src', data.image);
    });
};