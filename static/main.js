
const numInputs = document.querySelectorAll('input[type=number]')

numInputs.forEach(function(input) {
  input.addEventListener('change', function(e) {
    if (e.target.value == '') {
      e.target.value = 0
    }
  })
})

$(document).ready(function(){
  $('input[name="starter_tool_1"]').change(function() {
  $("#myForm").validate();
    if ($('#starter_tool_1_1').is(':checked') || $('#starter_tool_1_2').is(':checked')) {
      $("#extra_tool_1").show();
      $('input[name="starter_tool_1"]').rules('add', {required: true});
        }
    else{
      $("#extra_tool_1").hide();
      $('input[name="starter_tool_1"]').rules('remove', 'required');
    }
  });
})
$(document).ready(function(){
  $('input[name="starter_tool_2"]').change(function() {
  $("#myForm").validate();
    if ($('#starter_tool_2_1').is(':checked') || $('#starter_tool_2_2').is(':checked')) {
      $("#extra_tool_2").show();
      $('input[name="starter_tool_2"]').rules('add', {required: true});
    }
    else{
      $("#extra_tool_2").hide();
      $('input[name="starter_tool_2"]').rules('remove', 'required');
    }
  });
})
$(document).ready(function(){
  $('input[name="starter_tool_3"]').change(function() {
  $("#myForm").validate();
    if ($('#starter_tool_3_1').is(':checked') || $('#starter_tool_3_2').is(':checked')) {
      $("#extra_tool_3").show();
      $('input[name="starter_tool_3"]').rules('add', {required: true});
        }
    else{
      $("#extra_tool_3").hide();
      $('input[name="starter_tool_3"]').rules('remove', 'required');
    }
  });
})


$(document).ready(function() {
     $("#myForm").validate({
          rules: {
      on_field: "required",
      scouter_name: "required",
      game_num: "required",
      team_num: "required",
      starter_location: "required",
      starter_tool_1: "required",
      auto_seesaw: "required",
      mobility: "required",
      grid_co_h: "required",
      grid_co_m: "required",
      grid_co_l: "required",
      grid_cu_h: "required",
      grid_cu_m: "required",
      grid_cu_l: "required",
      cone_shoot: "required",
      cube_shoot: "required",
      defence_execute: "required",
      defence_receive: "required",
      dysfunction: "required",
      flip: "required"
     },
     submitHandler: function(form) {
        $("#submit-btn").attr("disabled", true);
        $("#submit-btn").val("Sending, please wait...");
        form.submit();
     },
     errorPlacement: function(error, element) {
        error.appendTo('#errorContainer');
     }
   });
});
