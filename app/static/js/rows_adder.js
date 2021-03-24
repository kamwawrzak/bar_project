window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('add-ingredient').addEventListener("click", addIngredient, false);
});


function addIngredient() {
  let i = document.getElementById('ingredient-iterator').value * 1;
  if (i < 6) {
      var table = document.getElementById('ingredients-tab'),
          row = table.insertRow(-1),
          cell1 = row.insertCell(0),
          cell2 = row.insertCell(1),
          cell3 = row.insertCell(2);

      row.setAttribute("class", "ingredient-row");

      var ingredient = document.createElement("input");
      ingredient.setAttribute("type", "text");
      ingredient.setAttribute("name", "ingredient"+i);
      ingredient.setAttribute("class", "ingredient-input");
      ingredient.setAttribute("placeholder", "Ingredient Name");
      ingredient.setAttribute("minlength", "3");
      ingredient.setAttribute("maxlength", "30");

      var amount = document.createElement("input");
      amount.setAttribute("type", "number");
      amount.setAttribute("name", "amount"+i);
      amount.setAttribute("class", "ingredient-input");
      amount.setAttribute("placeholder", "Amount");
      amount.setAttribute("maxlength", "1000");
      amount.setAttribute("step", "0.1");


      var unit = document.createElement("select");
      unit.setAttribute("name", "unit"+i);
      unit.setAttribute("class", "dropdownlist");
      unit.id = "unit";

      var option1 = document.createElement("option");
      option1.text = "Unit";
      option1.value = " ";
      option1.selected = true;
      option1.hidden = true;
      unit.appendChild(option1);

      var option2 = document.createElement("option");
      option2.text = "ml";
      option2.value = "ml";
      unit.appendChild(option2);

      var option3 = document.createElement("option");
      option3.text = "piece(s)";
      option3.value = "piece(s)";
      unit.appendChild(option3);

      var option4 = document.createElement("option");
      option4.text = "drop(s)";
      option4.value = "drop(s)";
      unit.appendChild(option4);

      cell1.appendChild(ingredient);
      cell2.appendChild(amount);
      cell3.appendChild(unit);

      row.appendChild(cell1);
      row.appendChild(cell2);
      row.appendChild(cell3);

      table.appendChild(row);

      document.getElementById('ingredient-iterator').setAttribute('value', i+1);
  } else {
    alert('You can add maximum 6 ingredients.');
  };
};
