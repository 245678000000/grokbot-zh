(function () {
  try {
    var saved = localStorage.getItem("gb-theme");
    var theme = saved || "light";
    document.documentElement.setAttribute("data-theme", theme);
  } catch (e) {
    document.documentElement.setAttribute("data-theme", "light");
  }
})();
