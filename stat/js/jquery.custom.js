jQuery(document).ready(function($) {

	$( '.ticket-attachment' ).hide();
	
	$( '.attach-file' ).click(function() {
		$( '.ticket-attachment' ).toggle();
		
		return false;
	});
	
	/** That's it... for now ;) */

}); 