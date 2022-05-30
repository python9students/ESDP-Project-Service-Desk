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


if (document.getElementById('progress_bar')) {
    window.addEventListener('load', ProgressBar)
}

async function ProgressBar() {
    let url = document.getElementById('progress_bar').dataset.timeUrl
    let data = await make_request(url)
    let converted_expected_finish_date = new Date(data.expected_time_to_finish_work);
    let converted_received_at_date = new Date(data.ticket_received_at)
    let converted_date_time_now = new Date(data.date_time_now)


    let remaining_time = converted_expected_finish_date - converted_date_time_now


    let received_and_end_date = converted_expected_finish_date - converted_received_at_date


    let percentage = (remaining_time / received_and_end_date) * 100
    let remaining_percentage = 100 - percentage
    let progress_bar_tag = document.getElementById("progress_bar")
    progress_bar_tag.style = `width: ${remaining_percentage}%`
    if (remaining_percentage > 80) {
        progress_bar_tag.style.background = 'red';
    }else{
        progress_bar_tag.style.background = 'green'
    }
}


function msToTime(duration) {
    let milliseconds = parseInt((duration % 1000) / 100),
        seconds = Math.floor((duration / 1000) % 60),
        minutes = Math.floor((duration / (1000 * 60)) % 60),
        hours = Math.floor((duration / (1000 * 60 * 60)) % 24);

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;

    return hours + ":" + minutes + ":" + seconds + "." + milliseconds;
}


if (document.getElementsByClassName('progress-bar')) {
    window.addEventListener('load', ProgressBarList)
}

async function ProgressBarList() {
    let progress_list = document.getElementsByClassName('progress-bar')
    for (i = 0; i < progress_list.length; i++) {
        let url = progress_list[i].dataset.timeUrl
        let data = await make_request(url)
        let converted_expected_finish_date = new Date(data.expected_time_to_finish_work);
        let converted_received_at_date = new Date(data.ticket_received_at)
        let converted_date_time_now = new Date(data.date_time_now)


        let remaining_time = converted_expected_finish_date - converted_date_time_now


        let received_and_end_date = converted_expected_finish_date - converted_received_at_date


        let percentage = (remaining_time / received_and_end_date) * 100
        let remaining_percentage = 100 - percentage
        progress_list[i].style = `width: ${remaining_percentage}%`

        if(remaining_percentage > 80){
        progress_list[i].style.background = "red"
        }else {
            progress_list[i].style.background = "green"
        }

    }
}




