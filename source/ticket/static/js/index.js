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
    if (remaining_percentage > 100) {
        progress_bar_tag.style.background = 'red';
        progress_bar_tag.textContent = "-" + progress_bar_tag.textContent;
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


if (document.getElementsByClassName('progress-bar progress_list')) {
    window.addEventListener('load', ProgressBarList)
}

async function ProgressBarList() {
    let progress_list = document.getElementsByClassName('progress-bar progress_list')
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

        if(remaining_percentage > 90){
        progress_list[i].style.background = "red";
        progress_list[i].textContent = "-" + progress_list[i].textContent + "раб.час";
        }else if(remaining_percentage > 0.1){
                progress_list[i].style.background = "green"
                progress_list[i].textContent = progress_list[i].textContent + "раб.час"
            }

        }

}


let service_object = document.getElementById('id_service_object')
service_object.addEventListener("change", getTime)

async function getTime(){
    let url = `http://localhost:8000/service_object/${service_object.value}/detail/`
    console.log(url)
    let data = await make_request(url)
    console.log(data)
    let time_to_finish = document.getElementById('time-to-finish')
    console.log(time_to_finish)
    if (data.time_to_finish !== 'None'){
        time_to_finish.innerText = `Время за которое надо закончить работу по договору: ${data.time_to_finish} ч/м/с`}
}




