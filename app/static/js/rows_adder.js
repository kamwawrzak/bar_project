
var i = 1;
function add(){
var add_ingredient = document.getElementById("add_ingredient");
var br = document.createElement("br");

var ingredient = document.createElement("input");
ingredient.setAttribute("type", "text");
ingredient.setAttribute("name", "ingredient"+i);

var amount = document.createElement("input");
amount.setAttribute("type", "number");
amount.setAttribute("name", "amount"+i);

add_ingredient.appendChild(ingredient);

add_ingredient.appendChild(amount);
add_ingredient.appendChild(br);
i++;
}
