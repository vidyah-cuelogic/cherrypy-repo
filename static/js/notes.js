var notesServices = (function($) {

	var addNotes = function(){

		var postdata = {note: $("#note_content").text()} ;
        $.post('/submit', postdata, function(data) {
            // and set the title with the result
            console.log(data)
           });
        return false ;



	 //      var requestData = {
	 //        note: $("#note_content").text()
		//     };

		//     //the URL where we'll send the AJAX request
		//     var url = 'UsernameExists';

		//     //make the AJAX call over POST
		//     $.post({
		//         contentType: 'application/json',
		//         dataType: 'json',
		//         data: JSON.stringify(requestData),
		//         url: url,
		//         error:function () {
		//             alert('Sorry, an error occurred. Please try again later.');
		//         },
		//         success: function(response) {
		//             alert(response.exists); //this will alert "true" if the user exists
		//         }
		   
		// });
	}
	var service = {};
	service.addNotes = addNotes
	return service;
})(jQuery);
