//$(window).on('load', function(){ getMostViewed(); getTopRated(); });

window.addEventListener('DOMContentLoaded', () => {
    getMostViewed();
    getTopRated();
});

async function getMostViewed(){
    let resp = await fetch('/v1/most_viewed');
    let data = await resp.json();
    let name = data.name.charAt(0).toUpperCase() + data.name.substring(1).toLowerCase();
    document.getElementById('most-viewed-name').innerHTML = name;
    document.getElementById('most-viewed-link').href = '/v1/drink/' + data.id;
    document.getElementById('most-viewed-img').src = data.image;
};

async function getTopRated(){
    let resp = await fetch('/v1/top_rated');
    let data = await resp.json();
    let name = data.name.charAt(0).toUpperCase() + data.name.substring(1).toLowerCase();
    document.getElementById('top-rated-name').innerHTML = name;
    document.getElementById('top-rated-link').href = '/v1/drink/' + data.id;
    document.getElementById('top-rated-img').src = data.image;
};
