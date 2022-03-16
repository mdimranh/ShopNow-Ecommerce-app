
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


$("#order-status").change(function () {
  document.getElementById("overlay").style.display = "block";
  var id = $(".id").text()
  $.ajax({
    type: "POST",
    url: "/control/order/" + id,
    data: {
      "status": $(this).val()
    },
    success: function (res) {
      document.getElementById("overlay").style.display = "none";
      new PNotify({
        title: 'Successfully Updated',
        type: 'success',
        text: `Order status updated successfully`,
        addclass: 'stack-bottom-right',
        icon: true,
        delay: 2500
      });
    },
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
  })
})