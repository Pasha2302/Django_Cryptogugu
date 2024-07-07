"use strict"
var dropdownManagerInstance;


var createDropdownManager = () => {
  var closeOnClickOutsideElements = [];

  // Вспомогательная функция для переключения класса по щелчку
  var toggleClassOnClick = (triggerSelector, targetSelector, className) => {
    var trigger = document.querySelector(triggerSelector);
    
    if (trigger) {
      trigger.addEventListener('click', () => {
        document.querySelector(targetSelector).classList.toggle(className);
      });
    }
  };

  // Функция закрытия элементов при щелчке снаружи
  var closeOnClickOutside = (targetSelector, className) => {
    var targetElement = document.querySelector(targetSelector);
    if (targetElement) {
      var id_element = `id_${targetSelector}`
      closeOnClickOutsideElements = closeOnClickOutsideElements.filter( (obj) => obj.id_element !== id_element);
      closeOnClickOutsideElements.push({ id_element, targetElement, className });
      // console.log('\nClose On Click Outside Elements: ', closeOnClickOutsideElements)
    }
  };

  // Общий обработчик событий щелчка
  document.addEventListener('click', (e) => {
    closeOnClickOutsideElements.forEach(({ targetElement, className }) => {
      var withinBoundaries = e.composedPath().includes(targetElement);
      if (!withinBoundaries) {
        targetElement.classList.remove(className);
      }
    });
  });

  return { toggleClassOnClick, closeOnClickOutside };
};


var getDropdownManager = () => {
  if (!dropdownManagerInstance) {
    dropdownManagerInstance = createDropdownManager();
  }
  return dropdownManagerInstance;
};

export default getDropdownManager;
