const numInputs = document.querySelectorAll('input[type=number]')

numInputs.forEach(function(input) {
  input.addEventListener('change', function(e) {
    if (e.target.value == '') {
      e.target.value = 0
    }
  })
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
            form.submit();
            $("#submit-btn").attr("disabled", true);
            $("#submit-btn").val("Sending, please wait...");
        },
         errorPlacement: function(error, element) {
      error.appendTo('#errorContainer');}
   });
});

