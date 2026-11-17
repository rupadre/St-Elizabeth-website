/* Moves events whose date has passed out of "Coming up", so the lists stay
   right in the visitor's browser between site rebuilds. */
(function () {
  var d = new Date();
  var today = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  var upcoming = document.querySelector('[data-events="upcoming"]');
  var past = document.querySelector('[data-events="past"]');
  if (!upcoming) return;
  var moved = Array.prototype.filter.call(upcoming.children, function (li) {
    return li.getAttribute("data-event-end") < today;
  });
  moved.forEach(function (li) {
    if (past) past.insertBefore(li, past.firstChild); else li.remove();
  });
  if (!upcoming.children.length) {
    var empty = document.querySelector("[data-events-empty]");
    if (empty) empty.hidden = false;
    var section = upcoming.closest("[data-events-section]");
    if (section) section.hidden = true;
  }
})();
