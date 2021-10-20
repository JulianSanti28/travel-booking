
document.addEventListener('DOMContentLoaded', () => {

    validar_check();
    api_vuelos();


})


//No permite que los dos check tengan un valor verdadero al mismo tiempo
function validar_check() {
    //Checkbox
    let one_way = document.querySelector('#one_way');
    let round_trip_check = document.querySelector('#round_trip');
    one_way.addEventListener('change', function () {
        if (this.checked) {
            round_trip_check.checked = false;
        }
    });
    round_trip_check.addEventListener('change', function () {
        if (this.checked) {
            let e = document.querySelector('#round_trip');
            one_way.checked = false;
        }
    });
}

function api_vuelos() {
    document.querySelector('#btn_filtro_1').addEventListener('click', () => {

        // if (validar_campos()) {
        var select_origin = document.getElementById("origin"); /*Obtener el SELECT de Origen*/
        var id_option_origin = select_origin.options[select_origin.selectedIndex].id; /*Obtener id de la opción origen*/
        var select_destination = document.getElementById("destination"); /*Obtener el SELECT de Destino*/
        var id_option_destination = select_destination.options[select_destination.selectedIndex].id; /*Obtener id de la opción destino*/
        //       URL       METHOD HTTP              INFORMACIÓN A ENVIAR
        fetch('/vuelos', {
            method: 'POST', body: JSON.stringify({
                origin: id_option_origin,
                destination: id_option_destination,
                filter: document.querySelector('#one_way').checked
            })
        })
            .then(response => response.json())
            .then(result => {
                mostrar_vuelos(result)
            })
        //  }else{
        // alert("Revisa bien los campos")
        //}
    })

}

function mostrar_vuelos(result) {



    result.vuelos_ida.map(function (vuelo) {

        /*Elemento Padre*/
        var element_padre = document.createElement('tr');

        /*Elementos Hijos*/
        var code_vuelo = document.createElement('th');
        code_vuelo.scope = "row"
        code_vuelo.innerHTML = vuelo.origin.city_code
        element_padre.appendChild(code_vuelo);
       
        var origin = document.createElement('td');
        origin.innerHTML = vuelo.origin.city_name ;
        element_padre.appendChild(origin)

        var destination = document.createElement('td');
        destination.innerHTML = vuelo.destination.city_name ;
        element_padre.appendChild(destination)

        var duration = document.createElement('td');
        duration.innerHTML = vuelo.duration + " " + "Hours" ;
        element_padre.appendChild(duration)

        var capacity = document.createElement('td');
        capacity.innerHTML =  vuelo.capacity + "" + "People" ;
        element_padre.appendChild(capacity)

        var price = document.createElement('td');
        price.innerHTML =  vuelo.price + " " + "USD" ;
        element_padre.appendChild(price)

        document.getElementById('lst_vuelos').append(element_padre)



    });















    //if(result.vuelos_regreso.length){

    // }



}

function validar_campos() {

    /*Origen y Destino deben ser diferentes*/
    var select_origin = document.getElementById("origin"); /*Obtener el SELECT de Origen*/
    var id_option_origin = select_origin.options[select_origin.selectedIndex].id; /*Obtener id de la opción origen*/
    var select_destination = document.getElementById("destination"); /*Obtener el SELECT de Destino*/
    var id_option_destination = select_destination.options[select_destination.selectedIndex].id; /*Obtener id de la opción destino*/

    //Validaciones
    if (id_option_origin == id_option_destination) {
        return false
    } else if (!document.querySelector('#one_way').checked && !document.querySelector('#round_trip').checked) {
        return false
    } else if (document.getElementById('go').value.length == 0 || document.getElementById('return').value.length == 0) {
        return false
    }

    return true

}