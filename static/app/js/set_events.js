"use strict";
import getDropdownManager from "./moduls/dropdown.js";

var setThemeEvent = () => {
  var theme = document.querySelector("body");
  var currentTheme = localStorage.getItem("theme");

  var setTheme = (name) => {
    theme.setAttribute("data-theme", name);
    localStorage.setItem("theme", name);
  };

  var toggleTheme = () => {
    if (theme.getAttribute("data-theme") === "light") {
      setTheme("dark");
    } else {
      setTheme("light");
    }
  };

  if (currentTheme) {
    theme.setAttribute("data-theme", currentTheme);
  } else {
    setTheme("light");
  }

  var themeButtons = [
    document.querySelector(".header__theme"),
    document.querySelector(".footer__theme"),
    document.querySelector(".header__theme-mob"),
  ];

  themeButtons.forEach((button) => {
    if (button) {
      button.addEventListener("click", toggleTheme);
    }
  });
};

var setMobileMenu = () => {
  document.querySelectorAll(".mobile-menu__link-sub").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      link.parentElement.classList.toggle("active");
    });
  });

  document.querySelector(".header__burger").addEventListener("click", (e) => {
    e.target.classList.toggle("active");
    document.querySelector(".mobile-menu").classList.toggle("open");
    document.querySelector("body").classList.toggle("body_hidden");
  });
};

var setSearchInput = (dropdownManager) => {
  var searchInput = document.querySelector("#header-search-input");
  var headerSearch = document.querySelector(".header__search");

  searchInput.addEventListener("input", (_) => {
    if (searchInput.value.length > 0) {
      headerSearch.classList.add("open");
    } else {
      headerSearch.classList.remove("open");
    }
  });

  dropdownManager.closeOnClickOutside(".header__search", "open");
};

var setCoinTableScroll = () => {
  document.querySelectorAll(".coin-table").forEach((item) => {
    // console.log(item.getElementsByTagName('table')[0].offsetWidth);
    // console.log(item.offsetWidth);
    if (
      item.getElementsByTagName("table")[0].offsetWidth - 10 >=
      item.offsetWidth
    ) {
      item.classList.add("coin-table_scroll");
      // console.log(1);
    } else {
      item.classList.remove("coin-table_scroll");
      // console.log(2);
    }
  });
};

var setEventLanguage = (dropdownManager) => {
  var dropdownConfigs = [
    {
      triggerSelector: ".header__lang-current",
      targetSelector: ".header__lang",
      className: "open",
    },
    {
      triggerSelector: ".header__lang-current-mob",
      targetSelector: ".header__lang-mob",
      className: "open",
    },
    {
      triggerSelector: ".footer__lang-current",
      targetSelector: ".footer__lang",
      className: "open",
    },
  ];

  dropdownConfigs.forEach(({ triggerSelector, targetSelector, className }) => {
    dropdownManager.toggleClassOnClick(
      triggerSelector,
      targetSelector,
      className
    );
    dropdownManager.closeOnClickOutside(targetSelector, className);
  });
};

var setBannerBlockRecapcha = () => {
  document.querySelectorAll(".banner-block__item-close").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.target.closest(".banner-block").classList.remove("open");
    });
  });

  document.querySelectorAll(".banner-block__overlay").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.target.closest(".banner-block").classList.remove("open");
    });
  });
};

var getUserId = () => {
  fetch("get-user-id/")
    .then((response) => response.json())
    .then((data) => {
      document.cookie = `userId=${data.user_id}; path=/`;
    })
    .catch((error) => console.error("Error fetching unique ID:", error));
};

var setLanguage = () => {
  var elemsLang = document.querySelectorAll('[class$="__lang-list-item"]');

  elemsLang.forEach(function (item) {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      var langCode = item.getAttribute("data-lang-code");
      var currentPath = window.location.pathname;
      var pathParts = currentPath.split("/").filter(function (part) {
        return part !== "";
      });

      // Проверяем, является ли первый элемент языковым кодом
      if (
        pathParts.length > 0 &&
        pathParts[0] in { en: "", ru: "", es: "", pt: "", "zh-hans": "" }
      ) {
        pathParts.shift();
      }

      // Формируем новый путь
      var newPath =
        "/" + (langCode === "en" ? "" : langCode + "/") + pathParts.join("/");
      window.location.href = newPath;
    });
  });
};


window.addEventListener("load", () => {
  var dropdownManager = getDropdownManager();

  setEventLanguage(dropdownManager);
  setLanguage()
  setThemeEvent();
  setMobileMenu();
  setSearchInput(dropdownManager);
  setBannerBlockRecapcha();

  getUserId();
  
});


window.addEventListener("resize", () => {
  // We execute the same script as before

  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty("--vh", `${vh}px`);
  setCoinTableScroll();
});
