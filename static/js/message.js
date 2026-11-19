// Contact page message form.
// With a Web3Forms access key (content/site.json "contact_form_key") the
// message is sent straight to the parish email. Without a key, or if sending
// fails, it opens the visitor's own email app with the message filled in.
(function () {
  var form = document.getElementById("message-form");
  if (!form) return;
  var error = document.getElementById("msg-error");
  var status = document.getElementById("msg-status");
  var button = form.querySelector('button[type="submit"]');
  var key = form.getAttribute("data-key");
  var to = form.getAttribute("data-email");

  function mailto(name, email, phone, message) {
    var body = message + "\n\n" + name + "\n" + email + (phone ? "\n" + phone : "");
    window.location.href = "mailto:" + to +
      "?subject=" + encodeURIComponent("Message from " + name) +
      "&body=" + encodeURIComponent(body);
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var f = form.elements;
    var name = f.name.value.trim();
    var email = f.email.value.trim();
    var phone = f.phone.value.trim();
    var message = f.message.value.trim();
    var problems = [];
    if (!name) problems.push(["name", "Please enter your name."]);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) problems.push(["email", "Please enter your email address so we can reply."]);
    if (!message) problems.push(["message", "Please write your message."]);
    ["name", "email", "message"].forEach(function (k) { f[k].removeAttribute("aria-invalid"); });
    status.textContent = "";
    if (problems.length) {
      error.textContent = problems.map(function (p) { return p[1]; }).join(" ");
      problems.forEach(function (p) { f[p[0]].setAttribute("aria-invalid", "true"); });
      f[problems[0][0]].focus();
      return;
    }
    error.textContent = "";
    if (f.botcheck.value) return; // a robot filled the hidden field

    if (!key) { mailto(name, email, phone, message); return; }

    button.disabled = true;
    status.textContent = "Sending…";
    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        access_key: key,
        subject: "Website message from " + name,
        from_name: "St. Elizabeth website",
        name: name, email: email, phone: phone || "-", message: message,
        botcheck: ""
      })
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (!res.success) throw new Error(res.message || "failed");
      form.reset();
      status.textContent = "Thank you, " + name + ". Your message was sent. We'll reply to " + email + " soon.";
      button.disabled = false;
    }).catch(function () {
      button.disabled = false;
      status.textContent = "";
      error.textContent = "Sorry, the message could not be sent. Your email app will open so you can send it from there, or call " + "(419) 662-3922.";
      mailto(name, email, phone, message);
    });
  });
})();
