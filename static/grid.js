document.querySelectorAll('.add').forEach(function(item) {
  item.addEventListener('click', function() {
    var input = this.previousElementSibling;
    input.value = +input.value + 1;
  });
});

document.querySelectorAll('.sub').forEach(function(item) {
  item.addEventListener('click', function() {
    var input = this.nextElementSibling;
    if (input.value > 0) {
      input.value = +input.value - 1;
    }
  });
});