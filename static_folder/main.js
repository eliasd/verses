// Handlers used in section-hover change-color effect
function handlerIn(){
 $(this).css("background-color","red");
}
function handlerOut(){
 $(this).css("background-color","blue");
}


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
}



$(document).ready(setupHandlers);
