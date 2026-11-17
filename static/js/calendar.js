/* Keeps the "this month / next month" calendar links current in the
   visitor's browser, even if the site was last rebuilt in an earlier month. */
(function () {
  var data = document.getElementById("calendar-data");
  if (!data) return;
  var months;
  try { months = JSON.parse(data.textContent); } catch (e) { return; }
  var names = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
  var now = new Date();
  var slots = [];
  for (var i = 0; i < 2; i++) {
    var d = new Date(now.getFullYear(), now.getMonth() + i, 1);
    var key = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0");
    slots.push({ label: names[d.getMonth()] + " " + d.getFullYear(), url: months[key] || "" });
  }
  var icon = '<svg aria-hidden="true" viewBox="0 0 24 24" class="cal-icon"><path fill="currentColor" d="M7 2h2v2h6V2h2v2h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3zm12 8H5v9h14zM5 8h14V6H5z"/></svg>';
  document.querySelectorAll("[data-calendar]").forEach(function (list) {
    list.querySelectorAll("li").forEach(function (li, i) {
      var s = slots[i];
      if (!s) return;
      var label = '<span><span class="cal-month">' + s.label + '</span><span class="cal-sub">' +
        (s.url ? "Parish calendar (PDF)" : "Calendar coming soon") + "</span></span>";
      li.innerHTML = s.url
        ? '<a class="cal-link" href="' + s.url + '">' + icon + label + "</a>"
        : '<span class="cal-link is-missing">' + icon + label + "</span>";
    });
  });
})();
