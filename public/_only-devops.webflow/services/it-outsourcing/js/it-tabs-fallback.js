/* Fallback for Webflow Tabs on IT page body (main webflow.js has no IT export bindings). */
(function ($) {
  if (!$) return;

  function activateTab($tabs, tabName) {
    $tabs.find(".w-tab-link").removeClass("w--current");
    $tabs.find('.w-tab-link[data-w-tab="' + tabName + '"]').addClass("w--current");
    $tabs.find(".w-tab-pane").removeClass("w--tab-active");
    $tabs.find('.w-tab-pane[data-w-tab="' + tabName + '"]').addClass("w--tab-active");
  }

  function bindTabs($tabs) {
    $tabs.find(".w-tab-link").on("click", function (e) {
      var $link = $(this);
      if ($link.hasClass("w--current")) return;
      e.preventDefault();
      activateTab($tabs, $link.attr("data-w-tab"));
    });
  }

  $(function () {
    $(".main-wrapper .w-tabs").each(function () {
      bindTabs($(this));
    });
  });
})(window.jQuery);
