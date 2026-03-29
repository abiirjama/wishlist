// Find all the delete buttons, add a click event listener to all buttons
// On click event, show a confirm dialog
// Browsers will handle these events before the click that submits the form
// to provide the opportunity to intercept the form submit with JavaScript.
// If the click event handler prevents the event propagating, the form submit
// never happens.  If the click event doesn't prevent the event propagating,
// the form will be submitted as usual.
var deleteButtons = document.querySelectorAll('.delete');

deleteButtons.forEach(function(button){

  //add click event listener
  button.addEventListener('click', function(ev){

    //show confirm dialog
    var okToDelete = confirm("Delete place - are you sure?");

    //if user presses no,prevent form submit
    if (!okToDelete) {
      ev.preventDefault();
    }

    //otherwise,form submits normally
  })
});