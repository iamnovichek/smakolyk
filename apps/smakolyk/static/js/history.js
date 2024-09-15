// IDK how to make it work with Django (I mean to import it from another file), so I just put it here
const DataMappingValues = Object.freeze({
    dish_quantity_field_names: [
        "first_course_quantity",
        "second_course_quantity",
        "dessert_quantity",
        "drink_quantity"
    ],
    dish_price_field_names: [
        "first_course_price",
        "second_course_price",
        "dessert_price",
        "drink_price"
    ],
    dish_field_names: [
        "first_course",
        "second_course",
        "dessert",
        "drink"
    ],
    week_day_names: [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday"
    ]
})

const cerrensy_symbol = " ₴";

function set_total_week_amount() {
    let total_amount = 0;
    for (let i = 0; i < 5; i++) {
        const day_total_amount = document.getElementById(`${DataMappingValues.week_day_names[i]}-total-amount`);
        total_amount += parseInt(day_total_amount.innerText);
    }

    document.getElementById('total').innerText = "Total : " + total_amount + cerrensy_symbol;
}

document.addEventListener("DOMContentLoaded", function (){
    set_total_week_amount();

    const date_input = document.getElementById("date");

    date_input.addEventListener("change", function (){
        const url = `/get-history-week/?date=${date_input.value}`;

        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        }).then(data => {
            if (data["date_exists"]){
                const history_data = data["history_data"];

                for (const weekday of DataMappingValues.week_day_names) {
                    for (const [index, item] of DataMappingValues.dish_field_names.map((value, index) => [index, value])) {
                        document.getElementById(`${weekday}-${item}`).innerText = history_data[weekday][item];
                        document.getElementById(`${weekday}-${DataMappingValues.dish_quantity_field_names[index]}`).innerText = history_data[weekday][DataMappingValues.dish_quantity_field_names[index]];
                        document.getElementById(`${weekday}-${DataMappingValues.dish_price_field_names[index]}`).innerText = history_data[weekday][DataMappingValues.dish_price_field_names[index]];
                    }

                    document.getElementById(`${weekday}-total-amount`).innerText = history_data[weekday]["total_amount"];
                }

                set_total_week_amount();
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    })
})
