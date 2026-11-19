/* The homepage story from parish life shows for a few weeks after the event.
   Once that time is over, this swaps back to the usual photos, even if the
   site has not been rebuilt. */
(function () {
  var feature = document.querySelector("[data-feature-until]");
  var fallback = document.querySelector("[data-feature-fallback]");
  if (!feature || !fallback) return;
  var d = new Date();
  var today = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  if (feature.getAttribute("data-feature-until") < today) {
    feature.hidden = true;
    fallback.hidden = false;
  }
})();
