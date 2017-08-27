// Handlers used in section-hover change-color effect
function handlerIn(){
 $(this).css("background-color","red");
}
function handlerOut(){
 $(this).css("background-color","blue");
}

// Handlers used for transforming lyric elements into clickable button elements
function handleInputLeft(){
  console.log("Left side was clicked")
}
function handleInputRight(){
  console.log("Right side was clicked")
}


function setupHandlers(){
  $('.section').hover(handlerIn,handlerOut);
  $('#section-left').click(handleInputLeft)
  $('#section-right').click(handleInputRight)
}



$(document).ready(setupHandlers);
