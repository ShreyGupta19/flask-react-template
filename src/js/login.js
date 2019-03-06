import $ from "jquery";
import * as strings from './strings';
import styles from '../sass/login.scss';

$(document).ready(function (){
  $("#login-form").on("submit", function(event) {
    event.preventDefault();
    let data = $(this).serializeArray();

    fetch('/login', {
      method: 'POST',
      body: JSON.stringify({
        'email': data[0]['value'],
        'pass': data[1]['value'],
      }),
      headers:{
        'Content-Type': 'application/json',
      }
    }).then((res) => {
      if (!res.ok) throw Error(strings.LOGIN_FAILED);
      else res.json().then((body) => window.location = body.location)
    }).catch(error => {
      $('#login-error').css('display', 'block').html(error);
    });
  });
}) ;