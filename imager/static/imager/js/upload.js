$(function(){
  $imagesUploadBtn = $('.images-upload-btn');
  $imagesUploadForm = $('.images-upload-form');
  $imagesUploadBtn.on('click', function(){
  	var data = new FormData($imagesUploadForm.get(0));
  	$.ajax({
	  url: $imagesUploadForm.attr('action'),
  	  type: 'POST',
	  data:data,
	  contentType:false,
	  processData:false,
      success: function(data) {
  		console.log(data);
      }
	}).fail(function() {
      alert( "上传失败");
  	}); 
    return false;
  });
});