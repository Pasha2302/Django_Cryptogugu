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
              console.log('Изменение в дочерних элементах:');
              console.log(mutation);
              setShowRowsNumber();
              setNextBackPages();
              document.querySelector('.trending-coins').scrollIntoView({ behavior: 'smooth', block: 'center' });
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
          console.log("\nElement Event Trending Coins: ", _event.target);
          console.log("\nComposed Path: ", composedPath);
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
        console.log("\ncontent-type", response.headers.get("content-type"));
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


function setShowRowsNumber() {
  var showRowsBlocks = document.querySelectorAll('.show-rows-filter__current');

  for (var elm of showRowsBlocks) {
    var parentBlock = elm.parentNode;
    console.log('\nParent Block:', parentBlock)

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
          var spanButton = this.closest('.show-rows-filter').querySelector('.show-rows-filter__current span');
          // Если первый дочерний узел текстовый, изменяем его значение
          if (spanButton.firstChild.nodeType === Node.TEXT_NODE) {
            spanButton.firstChild.nodeValue = `${rowsNumber} `;
          }
          // Закрываем выпадающее меню (если это требуется)
          this.closest('.show-rows-filter').classList.remove('open');
          
          var urlParams = new URLSearchParams(window.location.search);  // Получаем текущий номер страницы из URL
          var currentPage = parseInt(urlParams.get('page')) || 1;

          requestServer(
            "set-settings-user/",
            "POST",
            { per_page: rowsNumber, currentPage }
          ).then((data) => {
            var targetBlock = document.querySelector('.trending-coins');
            targetBlock.innerHTML = data.html;
          });
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


export {
  setOpenAndCloseFilters,
  setEventTrendingCoins,
  setNextBackPages,
  setObserverTrendingCoins,
  setShowRowsNumber
};
