window.addEventListener('load', () => { displayRate();

    const allStars = document.getElementsByClassName('star');
    Array.from(allStars).forEach( (star) => {
        star.addEventListener('click', () => {
            let starId = star.id;
            let drinkId = document.getElementById('drink_id').value;
            let userId = document.getElementById('user_id').value;
            sendVote(starId, userId, drinkId);
        });

        star.addEventListener('mouseover', () => {
            let starNumber = star.id.slice(-1);
            for (i=starNumber; i>0; i--){
                let s = document.getElementById('star'+i);
                s.classList.add('star-mouseover');
            };
        });

        star.addEventListener('mouseleave', () => {
            let starNumber = star.id.slice(-1);
            for (i=1; i < 6; i++){
                let s = document.getElementById('star'+i);
                s.classList.remove('star-mouseover');
            };
        });
    });

    function sendVote(starId, userId, drinkId){
        let value = starId.slice(-1);
        let voteData = {'drink_id': drinkId, 'user_id': userId, 'value': value};
        let data = JSON.stringify(voteData);
        let url = '/v1/add_vote';
        let xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function(){
            if (this.readyState === XMLHttpRequest.DONE){
                if (this.status === 200) {
                    displayRate();
                } else if (this.status === 401){
                    alert('Only registered users can vote.');
                };
            };
        };
        xmlhttp.open('POST', url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(data);
    };

    async function displayRate(){
      let drinkId = document.getElementById('drink_id').value;
      let resp = await fetch('/v1/display_rate/' + drinkId);
      let data = await resp.json();
      displayStars(data.rate);
      if (data.amount == 1){
        document.getElementById('rate').innerHTML = ('Rate: ' + data.rate + ' (' + data.amount + ' vote)');
      } else {
        document.getElementById('rate').innerHTML = ('Rate: ' + data.rate + ' (' + data.amount + ' votes)');
      };
    };

    function fillAllStar(starNumber){
        for (i=1; i < starNumber+1; i++){
            document.getElementById('star'+i).innerHTML = '<i class="icon-star"></i>';
        };
    };

    function emptyAllStar(starNumber){
        for (i=5; i >= starNumber; i--){
            document.getElementById('star'+i).innerHTML = '<i class="icon-star-empty"></i>';
        };
    };

    function displayStars(rate){
        if (0 < rate && rate < 0.25 ) {
            document.getElementById('star1').innerHTML = '<i class="icon-star-half-alt"></i>';
            emptyAllStar(2);
        }
        else if (0.24 < rate && rate < 1.25 ) {
            fillAllStar(1);
            emptyAllStar(2);
        }
        else if (1.24 < rate && rate < 1.75) {
            fillAllStar(1);
            document.getElementById('star2').innerHTML = '<i class="icon-star-half-alt"></i>';
            emptyAllStar(3);
        }
        else if (1.74 < rate && rate < 2.25 ){
            fillAllStar(2);
            emptyAllStar(3);
        }
        else if (2.24 < rate && rate < 2.75){
            fillAllStar(2);
            document.getElementById('star3').innerHTML = '<i class="icon-star-half-alt"></i>';
            emptyAllStar(4);
        }
        else if (2.74 < rate && rate < 3.25){
            fillAllStar(3);
            emptyAllStar(4);
        }
        else if (3.24 < rate && rate < 3.75){
            fillAllStar(3);
            document.getElementById('star4').innerHTML = '<i class="icon-star-half-alt"></i>';
            emptyAllStar(5);
        }
        else if (3.74 < rate && rate < 4.25){
            fillAllStar(4);
            emptyAllStar(5);
        }
        else if (4.24 < rate && rate < 4.75){
            fillAllStar(4);
            document.getElementById('star5').innerHTML = '<i class="icon-star-half-alt"></i>';
        }
        else if (rate > 4.74) { fillAllStar(5); };
    };
});