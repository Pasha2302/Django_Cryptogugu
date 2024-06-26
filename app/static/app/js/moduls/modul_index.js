"use strict";


var setObserverTrendingCoins = () => {
  // Целевой элемент для наблюдения
  const targetNode = document.querySelector('.trending-coins');
  // Конфигурация наблюдателя: следить за изменениями в дочерних элементах
  const config = { childList: true, subtree: true };

  // Функция обратного вызова при изменениях
  const callback = function(mutationsList, observer) {
      for(let mutation of mutationsList) {
          if (mutation.type === 'childList') {
              // console.log('\nИзменение в дочерних элементах:');
              // console.log('mutation:', mutation);
              // console.log('observer:', observer);
              // setShowRowsNumber();
              // setNextBackPages();
              document.querySelector('.open-filters').scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
      }
  };

  // Создать экземпляр наблюдателя с указанной функцией обратного вызова
  const observer = new MutationObserver(callback);

  // Начать наблюдение за целевым элементом с указанной конфигурацией
  observer.observe(targetNode, config);
}


var setEventTrendingCoins = (listSearchElements, dropdownManager) => {
  if (!listSearchElements) return 0
  var targetBlock = document.querySelector('.trending-coins');

  if (targetBlock) {
    targetBlock.addEventListener('click', (_event) => {
      var composedPath = _event.composedPath();

      for (var searchObj of listSearchElements) {
        var trigger = document.querySelector(searchObj.triggerSelector);
        if ( composedPath.includes(trigger) ) {
          // console.log("\nElement Event Trending Coins: ", _event.target);
          // console.log("\nComposed Path: ", composedPath);
          document.querySelector(searchObj.targetSelector).classList.toggle(searchObj.className);
          dropdownManager.closeOnClickOutside(searchObj.targetSelector, searchObj.className);
        }
      }
      
    });
  }
}


// Функция для получения CSRF-токена из cookie
var getCookie = (name) => {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Проверяем, совпадает ли cookie
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};


var requestServer = (_url, _method, query_data = null) => {
  // Получаем CSRF-токен
  // var csrftoken = getCookie("csrftoken");

  var requestOptions = {
    method: _method,
    headers: {
      "Content-Type": "application/json",
      // "X-CSRFToken": csrftoken,
      "X-CSRFToken": csrf_token,
    },
  };

  if (_method === "POST" || _method === "PUT") {
    var dataToSave = { data: query_data };
    requestOptions.body = JSON.stringify(dataToSave);
  }

  return new Promise((resolve, reject) => {
    fetch(_url, requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        // console.log("\ncontent-type", response.headers.get("content-type"));
        return response.json();
      })
      .then((data) => {
        resolve(data);
      })
      .catch((error) => {
        console.error(
          "!!! There was a problem saving/retrieving the data:",
          error
        );
        reject(error);
      });
  });
};


var setOpenAndCloseFilters = () => {
  if ($(window).width() < 767) {
    $(".trending-coins__filters-items").hide();
  }
  localStorage.setItem(
    "tf",
    $(".trending-coins__filters-items").is(":visible")
  );

  $("body").on("click", ".open-filters", function () {
    localStorage.setItem(
      "tf",
      !$(".trending-coins__filters-items").is(":visible")
    );
    $(".trending-coins__filters-items").slideToggle();
  });
};


var loadCoins = (data) => {
  var urlParams = new URLSearchParams(window.location.search);  // Получаем текущий номер страницы из URL
  var currentPage = parseInt(urlParams.get('page')) || 1;
  data['currentPage'] = currentPage;
  data['per_page'] = document.querySelector('.show-rows-filter__current span').textContent;

  requestServer(
    "set-settings-user/",
    "POST",
    data
  ).then((data) => {
      // var targetBlock = document.querySelector('.trending-coins');
      // console.log('\n[setShowRowsNumber] data ', data)
      var targetBlock = document.querySelector('.trending-coins .coin-table tbody');
      var targetBlockPagination = document.querySelector('.coin-table__nav-pagination');
      targetBlock.innerHTML = data.html;
      targetBlockPagination.innerHTML = data.pagination;
      setNextBackPages();
    });
}


function setShowRowsNumber() {
  var showRowsBlocks = document.querySelectorAll('.show-rows-filter__current');

  for (var elm of showRowsBlocks) {
    var parentBlock = elm.parentNode;
    // console.log('\nParent Block:', parentBlock)

    parentBlock.querySelectorAll('.trending-coins__filter-sublist-item').forEach(function(item) {
      item.addEventListener('click', function() {
          // Удаляем класс 'active' со всех элементов
          document.querySelectorAll('.trending-coins__filter-sublist-item').forEach(function(el) {
              el.classList.remove('active');
          });
          // Добавляем класс 'active' к текущему выбранному элементу
          this.classList.add('active');
          // console.log('\nThis:', this);
          // Обновляем текст основной кнопки с текущим выбранным значением
          var rowsNumber = this.textContent.trim();
          // Если первый дочерний узел текстовый, изменяем его значение
          document.querySelectorAll('.show-rows-filter__current span').forEach( (elm) => {
            if (elm.firstChild.nodeType === Node.TEXT_NODE) {
              elm.firstChild.nodeValue = `${rowsNumber} `;
            }
          })
          
          // Закрываем выпадающее меню (если это требуется)
          this.closest('.show-rows-filter').classList.remove('open');
          loadCoins( {} );

      });

    });
  }
  
}


function setNextBackPages() {
  // var urlParams = new URLSearchParams(window.location.search);  // Получаем текущий номер страницы из URL
  // var currentPage = parseInt(urlParams.get('page')) || 1;
  var navPaginationList = document.querySelector('.coin-table__nav-pagination-list');
  var currentPage = parseInt(navPaginationList.querySelector('li.active a').textContent)
  var pageNumbers = navPaginationList.querySelectorAll('a');
  var endPageNumber = Number(pageNumbers[pageNumbers.length - 1].textContent);

  var buttons = document.querySelectorAll('.coin-table__nav-pagination-button');

  buttons[0].addEventListener('click', function() {
    if (currentPage > 1) {
        var prevPage = currentPage - 1;
        window.location.search = `?page=${prevPage}`;
    }
  });

  buttons[1].addEventListener('click', function() {
    if (currentPage < endPageNumber) {
      var nextPage = currentPage + 1;
      window.location.search = `?page=${nextPage}`;
    }
  });

}


function setShowMore() {
  var showMoreButton = document.querySelector('.coin-table__nav-more');
  var clickCounter = 1;

  showMoreButton.addEventListener('click', function(_event) {
    var navPaginationList = document.querySelector('.coin-table__nav-pagination-list');
    var pageNumbers = navPaginationList.querySelectorAll('a');
    var endPageNumber = Number(pageNumbers[pageNumbers.length - 1].textContent);
    var morePage = parseInt(navPaginationList.querySelector('li.active a').textContent) + clickCounter;
    // console.log('\nShow More Button Event:', _event);
    
    console.log(`\nMore Page: ${morePage} // End Page: ${endPageNumber}`);
    if (morePage <= endPageNumber) {
      var per_page = document.querySelector('.show-rows-filter__current span').textContent;
      requestServer(
        "show-more/",
        "POST",
        { morePage, per_page }
      ).then((data) => {
          // console.log('\nShow More Button Data:', data);
          var targetBlock = document.querySelector('.trending-coins .coin-table tbody');
          targetBlock.innerHTML += data.coins_html;
          clickCounter += 1;
        });
    }

  })

}


var setEventResetFilters = () => {
  var resetFiltersButton = document.querySelector('button.trending-coins__filter-item-reset');
  var buttonsElms = document.querySelectorAll('button.trending-coins__filter-item');
  var filteredButtons = Array.from(buttonsElms).filter(button => !button.classList.contains('trending-coins__filter-item_sub'));
  
  var sublist = document.querySelector('.trending-coins__filter-item-sub');
  var buttonChain = sublist.querySelector('.trending-coins__filter-item.trending-coins__filter-item_sub');
  var subItemsButton = sublist.querySelectorAll('button.trending-coins__filter-sublist-item');

  resetFiltersButton.addEventListener('click', (_event) => {
    buttonChain.firstChild.nodeValue = ' Chain ';

    var filter_item = [];
    filteredButtons.forEach( (elm) => {
      elm.classList.remove('active');
      if (elm.dataset.info === 'all_time_best') elm.classList.add('active');
      
      filter_item.push( {data_info: elm.dataset.info, active: elm.classList.contains('active')} )
    });

    subItemsButton.forEach( (elm) => {
      elm.classList.remove('active');
    });

    filter_item.push( {data_info: 'item_sub_symbol', active: 'None'} )
    loadCoins( {filter_item} );

  });
}


var setEventTrendingCoinsFilterItemSublist = () => {
  var sublist = document.querySelector('.trending-coins__filter-item-sub');
  var buttonChain = sublist.querySelector('.trending-coins__filter-item.trending-coins__filter-item_sub');

  var subItemsButton = sublist.querySelectorAll('button.trending-coins__filter-sublist-item');

  for (var button of subItemsButton) {
    button.addEventListener('click', (_event) => {
      var elmEvent = _event.target;
      var info = elmEvent.dataset.info;
      buttonChain.firstChild.nodeValue = `Chain: ${elmEvent.textContent}`;

      subItemsButton.forEach( (elm) => elm.classList.remove('active'));
      elmEvent.classList.add('active');

      loadCoins( {filter_item: [ {data_info: 'item_sub_symbol', active: info} ]} );
    })
  }
}



var setEventTrendingCoinsFilterItem = () => {
  var buttonsElms = document.querySelectorAll('button.trending-coins__filter-item');
  var filteredButtons = Array.from(buttonsElms).filter(button => !button.classList.contains('trending-coins__filter-item_sub'));

  for (var button of filteredButtons) {
    button.addEventListener('click', (_event) => {
      var elmEvent = _event.target;
      var info = elmEvent.dataset.info;
      
      if (info === 'all_time_best') {
        document.querySelector('button.trending-coins__filter-item[data-info="today_hot"]').classList.remove('active');
        if (elmEvent.classList.contains('active')) return;
      }

      if (info === 'today_hot') {
        document.querySelector('button.trending-coins__filter-item[data-info="all_time_best"]').classList.remove('active');
        if (elmEvent.classList.contains('active')) return;
      };

      elmEvent.classList.toggle('active');

      var filter_item = [];
      filteredButtons.forEach( (elm) => {
        filter_item.push( {data_info: elm.dataset.info, active: elm.classList.contains('active')} )
      })

      loadCoins( {filter_item} );

    })
  }

}


export {
  setOpenAndCloseFilters,
  setEventTrendingCoins,
  setNextBackPages,
  setObserverTrendingCoins,
  setShowRowsNumber,

  setShowMore,

  setEventTrendingCoinsFilterItem,
  setEventTrendingCoinsFilterItemSublist,
  setEventResetFilters,

};
