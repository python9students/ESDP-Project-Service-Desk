async function make_request(url, method = 'GET') {
    let response = await fetch(url, {method})
    if (response.ok) {
        console.log('OK')
        return await response.json();
    } else {
        console.log('Not Successful')
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }

}

window.addEventListener('load', ProgressBar)

async function ProgressBar() {
    let url = document.getElementById('progress_bar').dataset.timeUrl
    console.log(url)
    let data = await make_request(url)
    console.log(data)
    let readable_expected_finish_date = new Date(data.expected_time_to_finish_work);
    let expected_time = document.getElementById('expected_time')
    expected_time.innerText = `Дата окончания работы: ${readable_expected_finish_date}`


    let readable_date_time_now = new Date(data.date_time_now)
    let remaining_time = readable_expected_finish_date - readable_date_time_now

    let remain_time = document.getElementById("remaining_time")
    remain_time.innerText = `Оставшееся время оканчания работы: ${msToTime(remaining_time)}`
}


function msToTime(duration) {
  var milliseconds = parseInt((duration % 1000) / 100),
    seconds = Math.floor((duration / 1000) % 60),
    minutes = Math.floor((duration / (1000 * 60)) % 60),
    hours = Math.floor((duration / (1000 * 60 * 60)) % 24);

  hours = (hours < 10) ? "0" + hours : hours;
  minutes = (minutes < 10) ? "0" + minutes : minutes;
  seconds = (seconds < 10) ? "0" + seconds : seconds;

  return hours + ":" + minutes + ":" + seconds + "." + milliseconds;
}
