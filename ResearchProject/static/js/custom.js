$(document).ready(function() {
    $('.add-to-cart').on('click', function(e) {
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            food_id: food_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
            }
        })

    });
});
$(function(){
  $('#mainNavbar').on('click', function(e){
    e.stopPropagation();
  });
  $(document).on('click', '.navbar-collapse.show .nav-link', function(){
    $('.navbar-collapse').collapse('hide');
  });
});
