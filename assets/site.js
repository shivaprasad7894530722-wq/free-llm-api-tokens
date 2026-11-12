(function () {
  try {
    var t = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", t);
  } catch (e) {
    document.documentElement.setAttribute("data-theme", "dark");
  }
})();

function setThemeColor(theme) {
  var meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", theme === "light" ? "#f3f5fb" : "#070910");
}

document.addEventListener("DOMContentLoaded", function () {
  try {
    setThemeColor(document.documentElement.getAttribute("data-theme") || "dark");
  } catch (e) {}

  var btn = document.getElementById("themeBtn");
  if (btn) {
    btn.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
      setThemeColor(next);
    });
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest(".copy");
    if (b) copyText(b);
  });
});

function copyText(btn) {
  var text = btn.getAttribute("data-c") || "";
  var done = function () {
    var old = btn.textContent;
    btn.textContent = "Copied";
    btn.classList.add("done");
    setTimeout(function () {
      btn.textContent = old;
      btn.classList.remove("done");
    }, 1200);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(function () { fallbackCopy(text, done); });
  } else fallbackCopy(text, done);
}

function fallbackCopy(text, done) {
  var ta = document.createElement("textarea");
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand("copy"); done(); } catch (e) {}
  ta.remove();
}
