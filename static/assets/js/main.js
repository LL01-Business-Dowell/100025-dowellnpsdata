(function ($) {
  "use strict";

  // Events
  $(".dropdown-container")
    .on("click", ".dropdown-button", function () {
      $(this).siblings(".dropdown-list").toggle();
    })
    .on("input", ".dropdown-search", function () {
      var target = $(this);
      var dropdownList = target.closest(".dropdown-list");
      var search = target.val().toLowerCase();

      if (!search) {
        dropdownList.find("li").show();
        return false;
      }

      dropdownList.find("li").each(function () {
        var text = $(this).text().toLowerCase();
        var match = text.indexOf(search) > -1;
        $(this).toggle(match);
      });
    })
    .on("change", '[type="checkbox"]', function () {
      var container = $(this).closest(".dropdown-container");
      var numChecked = container.find('[type="checkbox"]:checked').length;
      container.find(".quantity").text(numChecked || "Any");
      // console.log(container.find('[type="checkbox"]:checked')[0].name);
    });

  // <li> template
  var stateTemplate = _.template(
    "<li>" +
      '<label class="checkbox-wrap"><input name="<%= name %>" type="checkbox"> <span for="<%= name %>"><%= name %></span> <span class="checkmark"></span></label>' +
      // '<label for="<%= abbreviation %>"><%= capName %></label>' +
      "</li>"
  );

  const endPoint =
    "https://100074.pythonanywhere.com/countries/johnDoe123/haikalsb1234/100074/";
  fetch(endPoint, {
    method: "GET",
  })
    .then((response) => {
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        throw new TypeError("Oops, we haven't got JSON!");
      }
      return response.json();
    })
    .then((data) => {
      /* process your data further */
      _.each(data, function (s) {
        data.name = _.startCase(s.name.toLowerCase());
        $("ul").append(stateTemplate(s));
      });
    })
    .catch((error) => console.error(error));
})(jQuery);
