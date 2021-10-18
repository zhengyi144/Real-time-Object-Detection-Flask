// Functions to deal with button events
$(function () {
  // Preview switch
  $("a#cam-preview").bind("click", function () {
    $.getJSON("/request_preview_switch", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // Flip horizontal switch
  $("a#flip-horizontal").bind("click", function () {
    $.getJSON("/request_flipH_switch", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // Model switch
  $("a#use-model").bind("click", function () {
    $.getJSON("/request_model_switch", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // exposure down
  $("a#exposure-down").bind("click", function () {
    $.getJSON("/request_exposure_down", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // exposure up
  $("a#exposure-up").bind("click", function () {
    $.getJSON("/request_exposure_up", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // contrast down
  $("a#contrast-down").bind("click", function () {
    $.getJSON("/request_contrast_down", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // contrast up
  $("a#contrast-up").bind("click", function () {
    $.getJSON("/request_contrast_up", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function () {
  // reset camera
  $("a#reset-cam").bind("click", function () {
    $.getJSON("/reset_camera", function (data) {
      // do nothing
    });
    return false;
  });
});

$(function(){
   //reset frame info
   $("a#reset-frame").bind("click",function(){
    var width=$("#width").val();
    var height=$("#height").val();
    var fps=$("#fps").val();
    $.ajax({
        type:'POST',
        url: '/reset-frame', 
        data: {"width":width ,"height":height,"fps":fps},
        async: false,
        dataType: 'json',
        success: function(data){
           //do nothing
        }
    });
   });
});
