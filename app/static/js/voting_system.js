$(window).on('load', function(){ displayRate(); });

$(function() {
    $('.star').on('click', function(){ var starId = this.id;
                                       var drinkId = $('#drink_id').val();
                                       var userId = $('#user_id').val();
                                       sendVote(starId, userId, drinkId);
                                       });
    $('.star').mouseenter(function(){
        var starNumber = this.id.slice(-1);
        for (i=starNumber; i>=0; i--){
            $('#star'+i).addClass('star-mouseover');
        };
    });

    $('.star').mouseleave(function(){
        var starNumber = this.id.slice(-1);
        $('#star'+starNumber).removeClass('star-mouseover');
    });

    $('#stars').mouseleave(function(){
        displayRate();
        for (i=1; i < 6; i++){
            $('#star'+i).removeClass('star-mouseover');
        };
    });
});

function sendVote(starId, userId, drinkId){
    var value = starId.slice(-1);
    var voteData = {'drink_id': drinkId, 'user_id': userId, 'value': value};
    var data = JSON.stringify(voteData);
    $.ajax('/v1/add_vote', {
        type: 'POST',
        data: data,
        dataType: 'json',
        contentType: 'application/json',
        success: function(){ displayRate(); },
        error: function(){ alert('Only registered users can vote.'); }
    });
};

function displayRate(){
  drinkId = $('#drink_id').val();
  $.getJSON('/v1/display_rate/' + drinkId, function (data){
    displayStars(data.rate);
    if (data.amount == 1){
        $('#rate').html('Rate: ' + data.rate + ' (' + data.amount + ' vote)');
    }
    else {
        $('#rate').html('Rate: ' + data.rate + ' (' + data.amount + ' votes)');
    };
  });
};

function fillAllStar(starNumber){
    for (i=1; i < starNumber+1; i++){
            $('#star'+i).html('<i class="icon-star"></i>');
        };
};

function emptyAllStar(starNumber){
    for (i=5; i >= starNumber; i--){
        $('#star'+i).html('<i class="icon-star-empty"></i>');
    };
};

function displayStars(rate){
    if (0 < rate && rate < 0.25 ) {
        $('#star1').html('<i class="icon-star-half-alt"></i>');
        emptyAllStar(2);
    }
    else if (0.24 < rate && rate < 1.25 ) {
        fillAllStar(1);
        emptyAllStar(2);
    }
    else if (1.24 < rate && rate < 1.75) {
        fillAllStar(1);
        $('#star2').html('<i class="icon-star-half-alt"></i>');
        emptyAllStar(3);
    }
    else if (1.74 < rate && rate < 2.25 ){
        fillAllStar(2);
        emptyAllStar(3);
    }
    else if (2.24 < rate && rate < 2.75){
        fillAllStar(2);
        $('#star3').html('<i class="icon-star-half-alt"></i>');
        emptyAllStar(4);
    }
    else if (2.74 < rate && rate < 3.25){
        fillAllStar(3);
        emptyAllStar(4);
    }
    else if (3.24 < rate && rate < 3.75){
        fillAllStar(3);
        $('#star4').html('<i class="icon-star-half-alt"></i>');
        emptyAllStar(5);
    }
    else if (3.74 < rate && rate < 4.25){
        fillAllStar(4);
        emptyAllStar(5);
    }
    else if (4.24 < rate && rate < 4.75){
        fillAllStar(4);
        $('#star5').html('<i class="icon-star-half-alt"></i>');
    }
    else if (rate > 4.74) { fillAllStar(5); };
};
