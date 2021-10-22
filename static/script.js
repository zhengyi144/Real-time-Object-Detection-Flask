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

$("#reset-frame").click(function(){
  var width=parseInt($("#width").val());
  var height=parseInt($("#height").val());
  var fps=parseInt($("#fps").val());
  $.ajax({
      type:'POST',
      url: '/reset_frame_info', 
      data: JSON.stringify({"width":width ,"height":height,"fps":fps}),
      //contentType: 'application/json; charset=UTF-8',
      dataType: 'json',
      success: function(data){
         //do nothing
      }
  });
});


$(function(){
  //reset camera url
  $("a#reset-url").bind("click",function(){
   var input_url=parseInt($("#input_url").val());
  
   $.ajax({
       type:'POST',
       url: '/reset_camera_url', 
       data: JSON.stringify({"input_url":input_url}),
       //contentType: 'application/json; charset=UTF-8',
       dataType: 'json',
       success: function(data){
          //do nothing
       }
   });
  });
});
