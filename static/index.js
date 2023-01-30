function add_event() {
  var givers = document.getElementsByName('giver');
  var n = givers.length;

  // check whether giver is checked
  var checked = false;
  for (let i = 0; i < n; i++) {
    if (givers[i].checked) {
      checked = true;
      break;
    }
  }
  if (!checked) {
    alert('check giver');
    return false;
  }

  // check whether receiver is checked
  checked = false;
  for (let i = 0; i < n; i++) {
    if (document.getElementById('receiver' + String(i)).checked) {
      checked = true;
      break;
    }
  }
  if (!checked) {
    alert('check at least one receiver');
    return false;
  }

  // check whether money is positive
  if (parseInt(document.getElementById('money').value) <= 0) {
    alert('money should be positive');
    return false;
  }

  return true;
}