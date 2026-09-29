(function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.addEventListener("click", function (e) {
    var node = e.target;
    if (!node) return;
    if (node.nodeType !== 1) node = node.parentElement;
    if (!node || !node.closest) return;
    var el = node.closest("[data-track]");
    if (!el) return;
    track(el.getAttribute("data-track"), {
      label: el.getAttribute("data-track-label") || "",
      href: el.getAttribute("href") || "",
    });
  });

  var params = new URLSearchParams(window.location.search);
  var interest = params.get("interest") || "";
  if (
    interest === "virtual-bookkeeping" ||
    interest === "bookkeeping" ||
    interest === "catch-up-bookkeeping"
  ) {
    var dest = sitePrefix() + "virtual-bookkeeping/fit-check/";
    if (interest === "catch-up-bookkeeping") dest += "?intent=catch-up";
    window.location.replace(dest);
    return;
  }

  initRequestForm(interest);
  initBookkeepingForm(params);

  function sitePrefix() {
    var parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.length && parts[parts.length - 1].indexOf(".") !== -1) parts.pop();
    var prefix = "";
    for (var i = 0; i < parts.length; i++) prefix += "../";
    return prefix || "./";
  }

  function track(eventName, payload) {
    if (!eventName) return;
    var paramsObj = payload || {};
    try {
      if (window.dataLayer && typeof window.dataLayer.push === "function") {
        var entry = { event: eventName };
        Object.keys(paramsObj).forEach(function (key) {
          entry[key] = paramsObj[key];
        });
        window.dataLayer.push(entry);
      }
      if (typeof window.gtag === "function") window.gtag("event", eventName, paramsObj);
      if (typeof window.plausible === "function") {
        window.plausible(eventName, { props: paramsObj });
      }
    } catch (err) {
      /* Analytics is optional. A missing or broken provider must not block the form. */
    }
  }

  var FORM_ENDPOINT = "https://zw6ddzuiurwjyywaeedub55xne0kfovs.lambda-url.us-west-2.on.aws/";

  function formEndpoint(form) {
    return (form && form.getAttribute("data-endpoint")) || FORM_ENDPOINT;
  }

  function formToObject(form) {
    var data = new FormData(form);
    var obj = {};
    data.forEach(function (value, key) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        if (!Array.isArray(obj[key])) obj[key] = [obj[key]];
        obj[key].push(value);
      } else {
        obj[key] = value;
      }
    });
    Object.keys(obj).forEach(function (key) {
      if (Array.isArray(obj[key])) obj[key] = obj[key].join(", ");
    });
    return obj;
  }

  function postIntake(endpoint, payload) {
    return fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    }).then(function (res) {
      return res.text().then(function (text) {
        var body = {};
        if (text) {
          try {
            body = JSON.parse(text);
          } catch (err) {
            body = {};
          }
        }
        if (!res.ok || body.ok === false) {
          var error = new Error((body && body.error) || "The form could not be sent.");
          error.status = res.status || 0;
          throw error;
        }
        return body;
      });
    });
  }

  function initRequestForm(interestValue) {
    var form = document.getElementById("request-form");
    if (!form) return;

    var interestInput = document.getElementById("interest");
    if (interestInput && interestValue) interestInput.value = interestValue;
    if (interestValue) {
      var tools = document.getElementById("tools");
      if (tools) tools.required = false;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var success = document.getElementById("form-success");
      var delivery = document.getElementById("request-form-delivery");
      var errorBox = document.getElementById("request-form-errors");
      var submitBtn = form.querySelector('[type="submit"]');
      var warning = form.parentElement ? form.parentElement.querySelector(".form-warning") : null;

      var ack = form.querySelector("#secrets-ack");
      if (ack && !ack.checked) {
        alert("Please confirm you have not pasted secrets, API keys, or credentials.");
        return;
      }

      var problem = (form.querySelector("#problem") || {}).value || "";
      var interest = (form.querySelector("#interest") || {}).value || "";
      var messageInput = document.getElementById("request-message");
      var notesInput = document.getElementById("request-notes");
      var planInput = document.getElementById("request-plan");
      var planInterest = document.getElementById("request-plan-interest");
      if (messageInput) messageInput.value = problem.trim();
      if (notesInput) notesInput.value = problem.trim();
      if (planInput) planInput.value = interest;
      if (planInterest) planInterest.value = interest;

      var payload = formToObject(form);
      payload.form = "diagnostic";
      payload.message = problem.trim();
      payload.notes = problem.trim();
      payload.plan = interest;
      payload.plan_interest = interest;
      if (!payload.company_website) payload.company_website = "";

      function showSuccess(viaMailto) {
        if (delivery) {
          if (viaMailto) {
            delivery.hidden = false;
            delivery.textContent =
              "The form could not connect. Your email app should open a draft to hello@meridian.dev. Send that draft to complete the request.";
          } else {
            delivery.hidden = true;
            delivery.textContent = "";
          }
        }
        if (errorBox) {
          errorBox.textContent = "";
          errorBox.classList.remove("show");
        }
        if (success) {
          success.classList.add("show");
          success.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
        form.hidden = true;
        if (warning) warning.hidden = true;
        if (submitBtn) submitBtn.disabled = false;
      }

      function showError(message) {
        if (submitBtn) submitBtn.disabled = false;
        if (!errorBox) return;
        errorBox.textContent = message;
        errorBox.classList.add("show");
        errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }

      if (submitBtn) submitBtn.disabled = true;
      postIntake(formEndpoint(form), payload)
        .then(function () {
          showSuccess(false);
        })
        .catch(function (err) {
          if (err && err.status) {
            showError(err.message || "The form could not be sent. Email hello@meridian.dev instead.");
            return;
          }
          mailtoFallback(payload);
          showSuccess(true);
        });
    });

    function mailtoFallback(data) {
      var name = data.name || "";
      var email = data.email || "";
      var company = data.company || "";
      var tools = data.tools || "";
      var problem = data.problem || data.message || "";
      var repo = data.repo || "";
      var interestField = data.interest || "";
      var body =
        "Name: " +
        name +
        "\nEmail: " +
        email +
        "\nCompany: " +
        company +
        "\nInterest: " +
        interestField +
        "\nTools: " +
        tools +
        "\nRepo (optional): " +
        repo +
        "\n\nProblem:\n" +
        problem;
      var subject = interestField
        ? "Meridian inquiry: " + interestField
        : "Vibe Code Rescue diagnostic request";
      window.location.href =
        "mailto:hello@meridian.dev?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);
    }
  }

  function initBookkeepingForm(query) {
    var form = document.getElementById("bookkeeping-fit-form");
    if (!form) return;

    var packageMap = {
      starter: "Starter",
      standard: "Standard",
      "catch-up": "Catch-up",
      "not-sure": "Not sure",
    };
    var softwareMap = {
      qbo: "QuickBooks Online",
      xero: "Xero",
      wave: "Wave",
      spreadsheets: "Spreadsheet / none",
      other: "Other",
    };

    var inquiry = document.getElementById("bk-inquiry");
    var source = document.getElementById("bk-source");
    var software = document.getElementById("bk-software");
    var softwareOtherWrap = document.getElementById("bk-software-other-wrap");
    var softwareOther = document.getElementById("bk-software-other");
    var packageSelect = document.getElementById("bk-package");
    var elseBox = document.getElementById("bk-need-else");
    var elseWrap = document.getElementById("bk-else-wrap");
    var elseInput = document.getElementById("bk-else");
    var catchupNote = document.getElementById("catchup-note");
    var catchupNeed = form.querySelector('input[name="needs"][value="Catch-up / backlog"]');

    ["source", "medium", "campaign", "content"].forEach(function (key) {
      var input = document.getElementById("bk-utm-" + key);
      var value = query.get("utm_" + key) || "";
      if (input && value.length <= 120) input.value = value;
    });
    var landing = document.getElementById("bk-landing");
    if (landing) landing.value = window.location.pathname + window.location.search;

    var sourceParam = query.get("source") || "";
    if (source && /^[a-z0-9-]{1,40}$/i.test(sourceParam)) source.value = sourceParam;
    if (software && softwareMap[query.get("software")]) software.value = softwareMap[query.get("software")];
    if (packageSelect && packageMap[query.get("package")]) {
      packageSelect.value = packageMap[query.get("package")];
    }

    if (query.get("intent") === "catch-up") {
      if (inquiry) inquiry.value = "Catch-up quote";
      if (source && !query.get("source")) source.value = "catch-up";
      if (packageSelect) packageSelect.value = "Catch-up";
      if (catchupNeed) catchupNeed.checked = true;
      if (catchupNote) catchupNote.hidden = false;
    }

    function syncSoftwareOther() {
      var isOther = software && software.value === "Other";
      if (softwareOtherWrap) softwareOtherWrap.hidden = !isOther;
      if (!isOther && softwareOther) softwareOther.value = "";
    }
    function syncElse() {
      var on = elseBox && elseBox.checked;
      if (elseWrap) elseWrap.hidden = !on;
      if (!on && elseInput) {
        elseInput.value = "";
        clearField(elseInput);
      }
    }
    if (software) software.addEventListener("change", syncSoftwareOther);
    if (elseBox) elseBox.addEventListener("change", syncElse);
    syncSoftwareOther();
    syncElse();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var errors = validateBookkeepingForm(form);
      var errorBox = document.getElementById("books-form-errors");
      if (errors.length) {
        if (errorBox) {
          errorBox.textContent = "";
          var list = document.createElement("ul");
          errors.forEach(function (message) {
            var item = document.createElement("li");
            item.textContent = message;
            list.appendChild(item);
          });
          errorBox.appendChild(list);
          errorBox.classList.add("show");
          errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
        return;
      }
      if (errorBox) {
        errorBox.textContent = "";
        errorBox.classList.remove("show");
      }

      var submitted = document.getElementById("bk-submitted");
      if (submitted) submitted.value = new Date().toISOString();
      var packageValue = valueOf(form, "bk-package");
      var done = valueOf(form, "bk-done");
      var notes = valueOf(form, "bk-notes");
      var planInput = document.getElementById("bk-plan");
      var planInterest = document.getElementById("bk-plan-interest");
      var messageInput = document.getElementById("bk-message");
      var message = [done, notes].filter(function (part) { return part; }).join("\n\n");
      if (planInput) planInput.value = packageValue;
      if (planInterest) planInterest.value = packageValue;
      if (messageInput) messageInput.value = message;

      var data = formToObject(form);
      data.form = "fit-check";
      data.plan = packageValue;
      data.plan_interest = packageValue;
      data.message = message;
      if (!data.company_website) data.company_website = "";

      var submitBtn = form.querySelector('[type="submit"]');
      var eventPayload = {
        inquiry: data.inquiry || "",
        source: data.source || "",
        package: data.package || "",
        software: data.software || "",
        behind: data.behind || "",
        needs: data.needs || "",
        budget: data.budget || "",
        timing: data.timing || "",
        delivery: "lambda",
      };

      function showSuccess(viaMailto) {
        var success = document.getElementById("books-form-success");
        var delivery = document.getElementById("books-form-delivery");
        var card = document.getElementById("books-form-card");
        if (delivery) {
          if (viaMailto) {
            delivery.hidden = false;
            delivery.textContent =
              "The form could not connect. Your email app should open a draft to hello@meridian.dev. Send that draft to complete the request.";
          } else {
            delivery.hidden = true;
            delivery.textContent = "";
          }
        }
        if (card) card.hidden = true;
        if (success) {
          success.classList.add("show");
          success.focus();
          success.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
        if (submitBtn) submitBtn.disabled = false;
      }

      function showError(message) {
        if (submitBtn) submitBtn.disabled = false;
        if (!errorBox) return;
        errorBox.textContent = message;
        errorBox.classList.add("show");
        errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }

      if (submitBtn) submitBtn.disabled = true;
      postIntake(formEndpoint(form), data)
        .then(function () {
          track("bookkeeping_fit_check_submit", eventPayload);
          showSuccess(false);
        })
        .catch(function (err) {
          if (err && err.status) {
            showError(err.message || "The form could not be sent. Email hello@meridian.dev instead.");
            return;
          }
          eventPayload.delivery = "mailto_fallback";
          track("bookkeeping_fit_check_submit", eventPayload);
          booksMailto(data);
          showSuccess(true);
        });
    });

    function booksMailto(data) {
      var lines = [
        ["Name", "name"],
        ["Email", "email"],
        ["Company", "company"],
        ["Role", "role"],
        ["Stage", "stage"],
        ["Team size", "team_size"],
        ["Software", "software"],
        ["Other software", "software_other"],
        ["How far behind", "behind"],
        ["Needs", "needs"],
        ["Needs other", "needs_other"],
        ["CPA", "cpa"],
        ["Plan", "plan"],
        ["Package", "package"],
        ["Done in 90 days", "done_90"],
        ["Timing", "timing"],
        ["Budget", "budget"],
        ["Heard about", "hear_about"],
        ["Inquiry", "inquiry"],
        ["Source", "source"],
        ["Anything else", "notes"],
      ].map(function (pair) {
        return pair[0] + ": " + (data[pair[1]] || "");
      });
      window.location.href =
        "mailto:hello@meridian.dev?subject=" +
        encodeURIComponent("Meridian bookkeeping fit check") +
        "&body=" +
        encodeURIComponent(lines.join("\n"));
    }
  }

  function clearField(input) {
    if (!input) return;
    input.classList.remove("invalid");
    input.removeAttribute("aria-invalid");
    var slot = document.getElementById(input.id + "-error");
    if (slot) slot.textContent = "";
  }

  function setFieldError(input, message) {
    if (!input) return message;
    input.classList.add("invalid");
    input.setAttribute("aria-invalid", "true");
    var slot = document.getElementById(input.id + "-error");
    if (slot) slot.textContent = message;
    return message;
  }

  function validateBookkeepingForm(form) {
    var messages = [];
    var firstInvalid = null;

    function check(id, message, ok) {
      var input = form.querySelector("#" + id);
      if (!input) return;
      if (ok) {
        clearField(input);
        return;
      }
      setFieldError(input, message);
      messages.push(message);
      if (!firstInvalid) firstInvalid = input;
    }

    check("bk-name", "Enter your name (at least 2 characters).", valueOf(form, "bk-name").length >= 2);
    check("bk-email", "Enter a valid work email.", /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valueOf(form, "bk-email")));
    check("bk-company", "Enter the company name.", valueOf(form, "bk-company").length >= 2);
    check("bk-role", "Choose your role.", valueOf(form, "bk-role").length > 0);
    check("bk-stage", "Choose the company stage.", valueOf(form, "bk-stage").length > 0);
    check("bk-team", "Choose the team size.", valueOf(form, "bk-team").length > 0);
    check("bk-software", "Choose the accounting software.", valueOf(form, "bk-software").length > 0);
    check("bk-behind", "Say how far behind the books are.", valueOf(form, "bk-behind").length > 0);
    check("bk-cpa", "Say whether you have a CPA.", valueOf(form, "bk-cpa").length > 0);
    check("bk-package", "Choose a package, or Not sure.", valueOf(form, "bk-package").length > 0);
    check("bk-done", "Describe what done looks like in at least 20 characters.", valueOf(form, "bk-done").length >= 20);
    check("bk-timing", "Choose when you want to start.", valueOf(form, "bk-timing").length > 0);
    check("bk-budget", "Choose a budget band, or Not sure yet.", valueOf(form, "bk-budget").length > 0);

    var needs = form.querySelectorAll('input[name="needs"]:checked');
    var needsError = document.getElementById("bk-needs-error");
    var needsGroup = document.getElementById("bk-needs-group");
    if (needs.length) {
      if (needsError) needsError.textContent = "";
      if (needsGroup) needsGroup.classList.remove("invalid");
    } else {
      if (needsError) needsError.textContent = "Choose at least one need.";
      if (needsGroup) needsGroup.classList.add("invalid");
      messages.push("Choose at least one need.");
      if (!firstInvalid) firstInvalid = form.querySelector('input[name="needs"]');
    }

    var elseOn = document.getElementById("bk-need-else") && document.getElementById("bk-need-else").checked;
    if (elseOn) {
      check("bk-else", "Tell us briefly what the something else is.", valueOf(form, "bk-else").length >= 8);
    } else {
      clearField(form.querySelector("#bk-else"));
    }

    if (firstInvalid && typeof firstInvalid.focus === "function") firstInvalid.focus();
    return messages;
  }

  function valueOf(form, id) {
    var input = form.querySelector("#" + id);
    return input ? String(input.value || "").trim() : "";
  }
})();
