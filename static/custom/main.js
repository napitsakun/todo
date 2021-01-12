$('.btn.btn-primary.reset').click(function() {
	$('.form-register').trigger('reset');
});

$('.delete-task').click(function(){
	var item_id = $(this).attr('item-id');
	// console.log(item_id)

	$.ajax({
		type: 'GET',
		url: 'delete/' + item_id,
		success: function(response)  {
			if (response.success == true) {
				alert('Deleted');
				window.location = '/todo/'
			}
			else {
				alert('Not deleted');
			}
		}
	})
})

$('.completed-task').click(function(){
	var item_id = $(this).attr('item-id');
	// console.log(item_id)

	$.ajax({
		type: 'GET',
		url: 'delete/' + item_id,
		success: function(response)  {
			if (response.success == true) {
				alert('Removed');
				window.location = '/todo/'
			}
			else {
				alert('Not removed');
			}
		}
	})
})


// $('.deactivate-profile').click(function(){
// 	status = confirm('Sure?')
// 	var item_id = $(this).attr('data-id')
// 	var deactivate_url = $(this).attr('url')
// 	console.log(status)

// 	if (status) {
// 		// console.log('if')
// 		$.ajax({
// 			type: 'POST',
// 			url: deactivate_url,
// 			success: function(response){
// 				if (response.success == true) {
// 					window.location = '/'
// 				}
// 			}
// 		});
// 	}
// 	else {
// 		window.location = '/profile/' + item_id
// 		// console.log('else')
// 	}
// })
