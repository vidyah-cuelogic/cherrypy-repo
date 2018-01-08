var notesServices = (function($) {

	var addNotes = function(){

		if (!$("#note_title").text() && !$("#note_content").text())
		{
			$("#edit").hide();
            $("#editable").show();
			return
		}
		var postdata = {
			title: $("#note_title").text() ,
			note: $("#note_content").text()
		};
        $.post('/submit', postdata, function(data) {
            // and set the title with the result
            $("#edit").hide();
            $("#editable").show();
            location.reload();
           });
        return false;
	}

	var showModal = function(index){
		var id = $("#note_id_"+index).val(),
			title = $("#title_"+index).html(),
			body = $("#body_"+index).html(); 
		$("#modal_note_id").val(id);
		$("#modal_title").val(title);
		$("#modal_body").val(body);
		$("#myModal").modal()
	}
	

	var updateNotes = function(){

		$("#modal_title").removeClass('error');
		$("#modal_body").removeClass('error');

		if(!$('#modal_title')[0].checkValidity() ){
			$("#modal_title").addClass('error');
			return;
		}
		if(!$('#modal_body')[0].checkValidity() ){ 
			$("#modal_body").addClass('error');
			return;
		} 

		var postdata = {
			note_id: $("#modal_note_id").val() ,
			title: $("#modal_title").val() ,
			note: $("#modal_body").val()
		} ;

        $.post('/update_data', postdata, function(data) {
            // and set the title with the result
            location.reload();
           });
        return false;
	}

	var deleteNotes = function(index){
		var postdata = {
			note_id: $("#note_id_"+index).val() 
		} ;
        $.post('/delete_data', postdata, function(data) {
            // and set the title with the result
            location.reload();
           });
        return false;
	}

	// var fetchAll_notes = function(){

	// 	var postdata = {
	// 	}
 //        $.post('/all_notes', postdata, function(data) {
 //            // and set the title with the result
 //            console.log(data.data)
 //            // all_notes
	// 						// <div class="panel panel-default section">
	// 						// 	<div class="edit_note"><a href="#" data-toggle="modal" data-target="#myModal"><i class="fa fa-pencil fa-lg"></i></a></div>
	// 						//     <div class="panel-heading">{{ note.title }}</div>
	// 						//     <div class="panel-body">{{ note.note }}</div>
	// 				  //   	</div>
						
 //           });
 //        return false;
	// }



	var service = {};
	service.addNotes = addNotes;
	service.showModal = showModal;
	service.updateNotes = updateNotes;
	service.deleteNotes = deleteNotes;
	return service;
})(jQuery);



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