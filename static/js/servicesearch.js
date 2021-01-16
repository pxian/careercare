function chooseType() {
  var value = $("select option:selected").val();
  if (value == "Home") {
    $(".temp").prop("hidden", true);
    $(".subevents").prop("hidden", true);
    $(".suboffice").prop("hidden", true);
    $(".sublessons").prop("hidden", true);
    $(".subhealth").prop("hidden", true);
    $(".subhome").prop("disabled", false);
    $(".subhome").prop("hidden", false);
  } else if (value == "Events") {
    $(".temp").prop("hidden", true);
    $(".subhome").prop("hidden", true);
    $(".suboffice").prop("hidden", true);
    $(".sublessons").prop("hidden", true);
    $(".subhealth").prop("hidden", true);
    $(".subevents").prop("disabled", false);
    $(".subevents").prop("hidden", false);
  } else if (value == "Office") {
    $(".temp").prop("hidden", true);
    $(".subhome").prop("hidden", true);
    $(".subevents").prop("hidden", true);
    $(".sublessons").prop("hidden", true);
    $(".subhealth").prop("hidden", true);
    $(".suboffice").prop("disabled", false);
    $(".suboffice").prop("hidden", false);
  } else if (value == "Lessons") {
    $(".temp").prop("hidden", true);
    $(".subhome").prop("hidden", true);
    $(".subevents").prop("hidden", true);
    $(".suboffice").prop("hidden", true);
    $(".subhealth").prop("hidden", true);
    $(".sublessons").prop("disabled", false);
    $(".sublessons").prop("hidden", false);
  } else {
    $(".temp").prop("hidden", true);
    $(".subhome").prop("hidden", true);
    $(".subevents").prop("hidden", true);
    $(".suboffice").prop("hidden", true);
    $(".sublessons").prop("hidden", true);
    $(".subhealth").prop("disabled", false);
    $(".subhealth").prop("hidden", false);
  }
}
