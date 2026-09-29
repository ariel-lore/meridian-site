(function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Client-side lead form: Formspree-ready or mailto fallback + local success
  var form = document.getElementById("request-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var success = document.getElementById("form-success");
    var submitBtn = form.querySelector('[type="submit"]');
    var data = new FormData(form);
    var endpoint = form.getAttribute("data-formspree") || "";

    // Never allow secret-looking fields to be silently sent without the warning ack
    var ack = form.querySelector("#secrets-ack");
    if (ack && !ack.checked) {
      alert("Please confirm you have not pasted secrets, API keys, or credentials.");
      return;
    }

    function showSuccess() {
      if (success) {
        success.classList.add("show");
        success.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      form.reset();
      if (submitBtn) submitBtn.disabled = false;
    }

    if (endpoint && endpoint.indexOf("YOUR_FORM_ID") === -1) {
      if (submitBtn) submitBtn.disabled = true;
      fetch(endpoint, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
      })
        .then(function (res) {
          if (res.ok) showSuccess();
          else throw new Error("Form error");
        })
        .catch(function () {
          mailtoFallback(data);
          showSuccess();
        });
    } else {
      mailtoFallback(data);
      showSuccess();
    }
  });

  function mailtoFallback(data) {
    var name = data.get("name") || "";
    var email = data.get("email") || "";
    var company = data.get("company") || "";
    var tools = data.get("tools") || "";
    var problem = data.get("problem") || "";
    var repo = data.get("repo") || "";
    var body =
      "Name: " + name +
      "\nEmail: " + email +
      "\nCompany: " + company +
      "\nTools: " + tools +
      "\nRepo (optional): " + repo +
      "\n\nProblem:\n" + problem;
    var mailto =
      "mailto:hello@meridian.dev?subject=" +
      encodeURIComponent("Vibe Code Rescue diagnostic request") +
      "&body=" +
      encodeURIComponent(body);
    window.location.href = mailto;
  }
})();
