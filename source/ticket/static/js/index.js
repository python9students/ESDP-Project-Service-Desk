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

if (document.getElementById('id_service_object')) {
    let service_object = document.getElementById('id_service_object')
    service_object.addEventListener("change", getTime)

    async function getTime() {
        let url = `http://188.166.9.203/service_object/${service_object.value}/detail/`;
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