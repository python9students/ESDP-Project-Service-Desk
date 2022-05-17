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


window.addEventListener('load', ProgressBar)

async function ProgressBar() {
    let url = document.getElementById('progress_bar').dataset.timeUrl
    console.log(url)
    let data = await make_request(url)
    console.log(data)
    let converted_expected_finish_date = new Date(data.expected_time_to_finish_work);
    let converted_received_at_date = new Date(data.ticket_received_at)
    let converted_date_time_now = new Date(data.date_time_now)



    let remaining_time = converted_expected_finish_date - converted_date_time_now


    let received_and_end_date = converted_expected_finish_date - converted_received_at_date


    let percentage = (remaining_time / received_and_end_date) * 100
    let remaining_percentage = 100 - percentage
    let progress_bar_tag = document.getElementById("progress_bar")
    progress_bar_tag.style = `width: ${remaining_percentage}%`
}




