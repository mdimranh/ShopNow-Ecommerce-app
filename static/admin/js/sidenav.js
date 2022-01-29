$("#menu-btn").on("click", function () {
  $("#sidenav").toggleClass("expand");
  $(".main").toggleClass("expand");
});

// var topnav = $("#topnav");
// $("#sidenav").css({ top: topnav.outerHeight() + "px" });

$(".sidenav .menu").on("click", function () {
  if ($(".sidenav").hasClass("expand") !== true) {
    if ($(this).hasClass("selected")) {
      $(this).removeClass("selected");
    } else {
      $(this).addClass("selected");
      $(".sidenav .menu.selected").not($(this)).removeClass("selected");
    }
  }
});

$(window).resize(function () {
  if ($(window).width() < 641) {
    if ($("#sidenav").hasClass("expand") === false) {
      $("#sidenav").addClass("expand");
      $(".main").addClass("expand");
    }
  }
});

var el = document.querySelectorAll(".submenu");
el.forEach((element) => {
  let height = element.scrollHeight;
  element.style.setProperty("--height", height + "px");
});
