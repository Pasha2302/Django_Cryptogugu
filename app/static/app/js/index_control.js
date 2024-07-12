"use strict";
import {
  setEventTrendingCoins,
  setOpenAndCloseFilters,
  setShowRowsNumber,
  setNextBackPages,

  // setObserverTrendingCoins,

  setShowMore,
  setEventTrendingCoinsFilterItem,
  setEventTrendingCoinsFilterItemSublist,
  setEventResetFilters,

  setEventTrendingCoinsFilterTableHead,
  getDataPromotedCoinsTable,

} from "./moduls/modul_index.js";
import getDropdownManager from "./moduls/dropdown.js";


window.addEventListener('load', () => {
  console.log("\nindex_control.")
  var dropdownManager = getDropdownManager();
  
  // setObserverTrendingCoins();
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

  setEventTrendingCoinsFilterTableHead();
  getDataPromotedCoinsTable();

});
