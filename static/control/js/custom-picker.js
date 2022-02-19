$(document).ready(function () {
  $("#coupon-start").dateDropper({
    dropWidth: 200,
    dropPrimaryColor: "#1abc9c",
    dropBorder: "1px solid #1abc9c",
    dropBorderRadius: "5",
    format: 'Y-m-d'
  }),
    $("#coupon-end").dateDropper({
      dropWidth: 200,
      dropPrimaryColor: "#1abc9c",
      dropBorder: "1px solid #1abc9c",
      dropBorderRadius: "5",
      format: 'Y-m-d'
    });
});
