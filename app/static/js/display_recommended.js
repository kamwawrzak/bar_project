window.addEventListener('DOMContentLoaded', () => {
    getRecommended();
});

async function getRecommended(){
    // Get data from the server
    let resp = await fetch('/v1/recommended');
    let data = await resp.json();
    // Render top rated drink
    topRatedDrink = data['top_rated'];
    document.getElementById('top-rated-name').innerHTML = capitalizeName(topRatedDrink.name);
    document.getElementById('top-rated-link').href = '/v1/drink/' + topRatedDrink.id;
    document.getElementById('top-rated-img').src = topRatedDrink.image;
    // Render most viewed drink
    mostViewedDrink = data['most_viewed'];
    document.getElementById('most-viewed-name').innerHTML = capitalizeName(mostViewedDrink.name);
    document.getElementById('most-viewed-link').href = '/v1/drink/' + mostViewedDrink.id;
    document.getElementById('most-viewed-img').src = mostViewedDrink.image;
};

function capitalizeName(drinkName){
    return drinkName.charAt(0).toUpperCase() + drinkName.substring(1).toLowerCase();
};
