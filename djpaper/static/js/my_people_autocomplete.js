$(document).ready(function(){
	$("#id_p_name").autocomplete('/ajax/people/autocomplete/',{multiple:true,multipleSeparator:' '});
});


