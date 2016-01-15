$(function(){
  $imageAddBtn = $('.images-add-btn');
  $imageAddBtn.on('click', function(){
    $imageAddBtn.before("<div><input name='docfile' type='file'></div>");
  });
});