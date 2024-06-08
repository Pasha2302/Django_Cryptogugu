

window.addEventListener("load", () => {
  if ($(window).width() < 767) {
    $(".trending-coins__filters-items").hide();
  }
  localStorage.setItem("tf", $(".trending-coins__filters-items").is(":visible"));

  $("body").on("click", ".open-filters", function () {
    localStorage.setItem("tf", !$(".trending-coins__filters-items").is(":visible"));
    $(".trending-coins__filters-items").slideToggle();
  });
});
