// Pledge card: builds an email to the parish office from the form.
// Nothing is sent to or stored by the website.
(function () {
  var form = document.getElementById("pledge-form");
  if (!form) return;
  var error = document.getElementById("pledge-error");

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var f = form.elements;
    var amount = f.amount.value.replace(/[$,\s]/g, "");
    var name = f.name.value.trim();
    var email = f.email.value.trim();
    var problems = [];
    if (!/^\d+(\.\d{1,2})?$/.test(amount) || Number(amount) <= 0) problems.push(["amount", "Please enter the amount in dollars, for example 25."]);
    if (!name) problems.push(["name", "Please enter your name."]);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) problems.push(["email", "Please enter your email address."]);

    ["amount", "name", "email"].forEach(function (k) { f[k].removeAttribute("aria-invalid"); });
    if (problems.length) {
      error.textContent = problems.map(function (p) { return p[1]; }).join(" ");
      problems.forEach(function (p) { f[p[0]].setAttribute("aria-invalid", "true"); });
      f[problems[0][0]].focus();
      return;
    }
    error.textContent = "";

    var period = form.querySelector('input[name="period"]:checked').value;
    var lines = [
      "Pledge card",
      "",
      "Having prayerfully considered the need for support of St. Elizabeth New Martyr Mission, as a matter of faith, my financial commitment will be:",
      "",
      "$" + Number(amount).toFixed(2) + " " + period,
      "",
      "Name: " + name,
      "Email: " + email,
      "Phone: " + (f.phone.value.trim() || "-"),
      "Address: " + (f.address.value.trim() || "-"),
      "I need a stewardship envelope: " + (f.envelope.checked ? "Yes" : "No")
    ];
    var href = "mailto:" + form.getAttribute("data-email") +
      "?subject=" + encodeURIComponent("Pledge card from " + name) +
      "&body=" + encodeURIComponent(lines.join("\n"));
    var fallback = document.getElementById("pledge-fallback");
    fallback.querySelector("a").setAttribute("href", href);
    document.getElementById("pledge-text").value = "To: " + form.getAttribute("data-email") + "\nSubject: Pledge card from " + name + "\n\n" + lines.join("\n");
    document.getElementById("pledge-copied").textContent = "";
    fallback.hidden = false;
    window.location.href = href;
  });

  var copy = document.getElementById("pledge-copy");
  copy.addEventListener("click", function () {
    var box = document.getElementById("pledge-text");
    var done = function () { document.getElementById("pledge-copied").textContent = "Copied. Now paste it into an email."; };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(box.value).then(done, function () { box.select(); document.execCommand("copy"); done(); });
    } else { box.select(); document.execCommand("copy"); done(); }
  });
})();
