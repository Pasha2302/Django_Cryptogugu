"use strict";
import {
  setEventTrendingCoins,
  setOpenAndCloseFilters,
  setShowRowsNumber,
  setNextBackPages,
  setObserverTrendingCoins,

  setShowMore,
  setEventTrendingCoinsFilterItem,
  setEventTrendingCoinsFilterItemSublist,
  setEventResetFilters,

} from "./moduls/modul_index.js";
import getDropdownManager from "./moduls/dropdown.js";


window.addEventListener('load', () => {
  console.log("\nindex_control.")
  var dropdownManager = getDropdownManager();
  
  setObserverTrendingCoins();
  setShowRowsNumber();
  setNextBackPages();
  setOpenAndCloseFilters();

  setShowMore();

  setEventTrendingCoins(
    [
      {
        triggerSelector: ".trending-coins__filter-item_sub",
        targetSelector: ".trending-coins__filter-item-sub",
        className: "open",
      },

      {
        triggerSelector: ".show-rows-filter.show-rows-filter1",
        targetSelector: ".show-rows-filter.show-rows-filter1",
        className: "open",
      },

      {
        triggerSelector: ".show-rows-filter.show-rows-filter2",
        targetSelector: ".show-rows-filter.show-rows-filter2",
        className: "open",
      },

    ],
    dropdownManager
  );

  setEventTrendingCoinsFilterItem();
  setEventTrendingCoinsFilterItemSublist();
  setEventResetFilters();


  const buttons = document.querySelectorAll(".coin-table thead button");

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      // Переключение стрелки
      const svg = this.querySelector("svg use");
      const currentHref = svg.getAttribute("xlink:href");

      if (currentHref === "#icon-arrow-bott") {
        svg.setAttribute("xlink:href", "#icon-arrow-up");
      } else {
        svg.setAttribute("xlink:href", "#icon-arrow-bott");
      }

      // Удаление класса 'active' у всех кнопок
      buttons.forEach((btn) => btn.classList.remove("active"));

      // Добавление класса 'active' к текущей кнопке
      this.classList.add("active");
    });
  });

});
