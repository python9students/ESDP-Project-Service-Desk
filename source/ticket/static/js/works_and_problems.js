var tabs = $('#nav a');
tabs.click(function(e){
    e.preventDefault();
    tabs.not(this).siblings('ul').slideUp();
    $(this).siblings('ul').slideToggle();
});