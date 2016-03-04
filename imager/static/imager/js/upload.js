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
      success: onUploadFinished
	}).fail(function() {
      alert( "上传失败: 请联系管理员");
  	}); 
    return false;
  });
  var onUploadFinished = function(data){
  	if(data.result) {
	  alert(data.url);
  	}
  	else{
  		alert('上传失败: ' + data.message);
  	}
  }
});