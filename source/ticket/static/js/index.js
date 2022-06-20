async function make_request(url, method = 'GET') {
    let response = await fetch(url, {method})
    if (response.ok) {
        return await response.json();
    } else {
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

    if (data.ticket_status === "Завершенный") {
        let element = document.getElementById(data.ticket_id)
        element.remove()
    } else {

        let converted_expected_finish_date = new Date(data.expected_time_to_finish_work);
        let converted_received_at_date = new Date(data.ticket_received_at)
        let converted_date_time_now = new Date(data.date_time_now)


        let remaining_time = converted_expected_finish_date - converted_date_time_now


        let received_and_end_date = converted_expected_finish_date - converted_received_at_date


        let percentage = (remaining_time / received_and_end_date) * 100
        let progress_bar_tag = document.getElementById("progress_bar")
        progress_bar_tag.style = `width: ${percentage}%`
        if (percentage >= 100) {
            progress_bar_tag.style.background = 'white';
        } else if (percentage >= 40 | percentage === 100) {
            progress_bar_tag.style.background = 'green'
        } else if (percentage >= 15) {
            progress_bar_tag.style.background = 'yellow'
            progress_bar_tag.style.color = 'red'
        } else {
            progress_bar_tag.style.background = 'red'
            progress_bar_tag.style.color = "blue"
            progress_bar_tag.textContent = "-" + progress_bar_tag.textContent;
        }
    }
}


if (document.getElementsByClassName('progress-bar progress_list')) {
    window.addEventListener('load', ProgressBarList)
}

async function ProgressBarList() {
    let progress_list = document.getElementsByClassName('progress-bar progress_list')
    for (i = 0; i < progress_list.length; i++) {
        let url = progress_list[i].dataset.timeUrl
        let data = await make_request(url)
        if (data.ticket_status !== "Завершенный") {
            let converted_expected_finish_date = new Date(data.expected_time_to_finish_work);
            let converted_received_at_date = new Date(data.ticket_received_at)
            let converted_date_time_now = new Date(data.date_time_now)


            let remaining_time = converted_expected_finish_date - converted_date_time_now

            let received_and_end_date = converted_expected_finish_date - converted_received_at_date

            let percentage = (remaining_time / received_and_end_date) * 100
            progress_list[i].style = `width: ${percentage}%`

            if (percentage >= 100) {
                progress_list[i].style.background = 'white'
            } else if (percentage >= 40) {
                progress_list[i].style.background = "green"
                progress_list[i].textContent = progress_list[i].textContent + "раб.час"
            } else if (percentage >= 15) {
                progress_list[i].style.background = 'yellow'
                progress_list[i].style.color = 'red'
                progress_list[i].textContent = progress_list[i].textContent + "раб.час"
            } else if (percentage === 0) {
                progress_list[i].style.background = null
                progress_list[i].style.color = null
            } else if (percentage < 0) {
                progress_list[i].style.background = 'red'
                progress_list[i].style.color = "blue"
                progress_list[i].textContent = "-" + progress_list[i].textContent + "раб.час";
            }


        } else if (data.ticket_status === "Завершенный") {
            let element = document.getElementById(data.ticket_id)
            element.remove()

        }
    }
}


if (document.getElementById('id_service_object')) {
    let service_object = document.getElementById('id_service_object')
    service_object.addEventListener("change", getTime)

    async function getTime() {
        let url = `http://http://188.166.9.203/service_object/${service_object.value}/detail/`;
        let data = await make_request(url);
        if (data.time_to_finish !== 'None') {
            p_tag_time_to_finish = document.createElement('p')
            p_tag_time_to_finish.innerText = `Время за которое надо закончить работу по договору: ${data.time_to_finish} ч/м/с`
            p_tag_time_to_finish.style.background = "green"
            p_tag_time_to_finish.style.color = "white"
            p_tag_time_to_finish.style.padding = "10px"
            p_tag_time_to_finish.id = "p_tag_time_to_fix"
            if (document.getElementById('p_tag_time_to_fix')) {
                document.getElementById('p_tag_time_to_fix').remove()
                let time_to_finish = document.getElementById('time-to-finish')
                time_to_finish.appendChild(p_tag_time_to_finish)
            } else {
                let time_to_finish = document.getElementById('time-to-finish')
                time_to_finish.appendChild(p_tag_time_to_finish)
            }
        } else {
            document.getElementById('p_tag_time_to_fix').remove()
        }
    }
}