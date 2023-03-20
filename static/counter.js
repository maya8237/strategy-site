document.querySelectorAll('.add').forEach(function(item) {
  item.addEventListener('click', function() {
    var input = this.nextElementSibling;
    input.value = +input.value + 1;
  });
});

document.querySelectorAll('.sub').forEach(function(item) {
  item.addEventListener('click', function() {
    var input = this.previousElementSibling;
    if (input.value > 0) {
      input.value = +input.value - 1;
    }
  });
});

