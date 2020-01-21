/*//材料名の表示
let strFoods = '';
let foods = ['バナナ', 'リンゴ', 'メロン', 'ブドウ'];
for(let food of foods){
  strFoods += '<li class="list-group-item text-center">'+food+'</li>';
  console.log(strFoods);
}
//document.getElementById('foodstaffs').innerHTML = strFoods;
*/
/*
//個数の表示
let strFoodsNum = '';
let foodsNum = ['1本', '3個', '2個', '5個'];
for(let foodNum of foodsNum){
  strFoodsNum += '<li class="list-group-item text-center">'+foodNum+'</li>';
  console.log(strFoodsNum);
}
document.getElementById('foodstaffsnum').innerHTML = strFoodsNum;
*/
//作り方の表示
// let strRecipe = "";
// let recipeNum = 5;
// let recipeArray = ["手順1", "手順2", "手順3", "手順4", "手順5"];
// for (i = 0; i < recipeNum; i++) {
//   strRecipe += '<li class="list-group-item">' + recipeArray[i] + "</li>";
//   console.log(strRecipe);
// }
// document.getElementById("recipes").innerHTML = strRecipe;

//お気入りのアイコン切り替え
function switchingFavorite() {
  let favo = document.getElementById("favorite");
  // classにfasがあるか判定
  let result = favo.classList.contains("fas");
  console.log(result);
  if (result) {
    favo.classList.remove("fas");
    favo.classList.add("far");
  } else {
    favo.classList.remove("far");
    favo.classList.add("fas");
  }
}
