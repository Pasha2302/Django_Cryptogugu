window.addEventListener("load", () => {
  var targetElementButton = document.querySelector(".open-filters");
  console.log("\nButton:", targetElementButton);

  // Добавляем обработчик клика на кнопку
  targetElementButton.addEventListener("click", function (event) {
    // Проверяем, не отключена ли кнопка
    if (!targetElementButton.classList.contains('disable-click')) {
      var filters = document.querySelector(".trending-coins__filters-items");
      // Вызываем функцию для переключения состояния фильтров
      slideToggle(filters);
    }
  });

  function slideToggle(element) {
    // Отключаем кнопку на время анимации
    targetElementButton.classList.add('disable-click');
    // Если элемент не виден, разворачиваем его, иначе сворачиваем
    if (!isElementVisible(element)) {
      slideDown(element);
    } else {
      slideUp(element);
    }
  }

  function slideDown(element) {
    // Делаем элемент видимым
    element.style.display = "flex";
    var height = element.offsetHeight;
    // Устанавливаем начальные стили для анимации
    element.style.height = 0;
    element.style.marginBottom = "0px"; // Начальное значение margin-bottom
    element.style.overflow = "hidden";
    element.style.transition = "height 0.5s ease-out";

    // Используем requestAnimationFrame для корректного запуска анимации
    requestAnimationFrame(() => {
      element.style.height = height + "px";
      element.style.marginBottom = "6px"; // Конечное значение margin-bottom
    });

    // Событие по окончании анимации
    element.addEventListener("transitionend", function handler() {
      setTimeout(() => {
        // Сбрасываем временные стили после анимации
        element.style.height = "";
        element.style.overflow = "";
        element.style.transition = "";
        // Удаляем обработчик события
        element.removeEventListener("transitionend", handler);
        // Включаем кнопку после завершения анимации
        targetElementButton.classList.remove('disable-click');
      }, 50); // Небольшая задержка для плавности
    });
  }

  function slideUp(element) {
    var height = element.offsetHeight;
    // Устанавливаем начальные стили для анимации
    element.style.height = height + "px";
    element.style.marginBottom = "6px";
    element.style.overflow = "hidden";
    element.style.transition = "height 0.5s ease-out";

    // Используем requestAnimationFrame для корректного запуска анимации
    requestAnimationFrame(() => {
      element.style.height = 0;
      element.style.marginBottom = "0px";
    });

    // Событие по окончании анимации
    element.addEventListener("transitionend", function handler() {
      setTimeout(() => {
        // Скрываем элемент и сбрасываем временные стили после анимации
        element.style.display = "none";
        element.style.height = "";
        element.style.overflow = "";
        element.style.transition = "";
        // Удаляем обработчик события
        element.removeEventListener("transitionend", handler);
        // Включаем кнопку после завершения анимации
        targetElementButton.classList.remove('disable-click');
      }, 50); // Небольшая задержка для плавности
    });
  }

  // Функция проверки видимости элемента
  function isElementVisible(element) {
    return element.offsetHeight > 0 && element.offsetWidth > 0;
  }
});
