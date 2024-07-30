// 


class TestClass {
  constructor() {
    this.testButton = this.getTestButton();
  }


  renameTextTestButton(text = 'Reset All Votes') {
    this.testButton.innerText = text;
  }

  getTestButton() {
    return document.querySelector('.header-middle__right .btn_light[data-action="btn-test"]');
  }


  setEventTestButton() {
    this.testButton.addEventListener('click', (_event) => {
      this.renameTextTestButton('Reset All Votes Down');
      setTimeout(() => {
        this.renameTextTestButton();
      }, 5000);

      this.fetchRequest('reset-all-votes/', 'GET')
        .then((data) => {
          if (!response.ok) throw new Error("Network response was not ok");
          data.json()
        })
        .then(data_json => console.log("Test Data: ", data_json))
        .catch(error => console.error("!!! There was a problem saving/retrieving the data:", error));
    });
  }


  fetchRequest(_url, _method, query_data = null) {
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
    return fetch(_url, requestOptions);
  }

}


export {
  TestClass,
};
